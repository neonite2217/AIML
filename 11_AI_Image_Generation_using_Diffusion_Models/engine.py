"""
Diffusion Image Generation Engine — Core Module

Provides shared logic and a foundational API for generating images using 
Hugging Face diffusers. Shared between the CLI tool and Flask web server.
"""

import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Dict, Set, Tuple, List, Optional

# Configure module logger
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Project-local storage configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parent
PROJECT_DATA_DIR: Path = PROJECT_ROOT / ".project_data"
PROJECT_TMP_DIR: Path = PROJECT_DATA_DIR / "tmp"
PROJECT_CACHE_DIR: Path = PROJECT_DATA_DIR / "cache"
HF_HOME_DIR: Path = PROJECT_CACHE_DIR / "huggingface"
HF_HUB_CACHE_DIR: Path = HF_HOME_DIR / "hub"
TRANSFORMERS_CACHE_DIR: Path = HF_HOME_DIR / "transformers"
TORCH_HOME_DIR: Path = PROJECT_CACHE_DIR / "torch"
MODEL_FLAGS_FILE: Path = PROJECT_DATA_DIR / "model_flags.json"
MODELS_DIR: Path = PROJECT_DATA_DIR / "models"          # permanent home for completed downloads
DOWNLOADING_DIR: Path = PROJECT_DATA_DIR / "_downloading"  # scratch space for in-progress downloads
DOWNLOADED_IMAGES_FILE: Path = PROJECT_DATA_DIR / "downloaded_images.json"

for _dir in (
    PROJECT_DATA_DIR,
    PROJECT_TMP_DIR,
    PROJECT_CACHE_DIR,
    HF_HOME_DIR,
    HF_HUB_CACHE_DIR,
    TRANSFORMERS_CACHE_DIR,
    TORCH_HOME_DIR,
    MODELS_DIR,
    DOWNLOADING_DIR,
):
    _dir.mkdir(parents=True, exist_ok=True)

# Keep all runtime/cache/tmp artifacts inside the project for all users.
os.environ.setdefault("TMPDIR", str(PROJECT_TMP_DIR))
os.environ.setdefault("TEMP", str(PROJECT_TMP_DIR))
os.environ.setdefault("TMP", str(PROJECT_TMP_DIR))
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_CACHE_DIR))
os.environ.setdefault("HF_HOME", str(HF_HOME_DIR))
os.environ.setdefault("HUGGINGFACE_HUB_CACHE", str(HF_HUB_CACHE_DIR))
os.environ.setdefault("TRANSFORMERS_CACHE", str(TRANSFORMERS_CACHE_DIR))
os.environ.setdefault("TORCH_HOME", str(TORCH_HOME_DIR))

try:
    from diffusers import StableDiffusionPipeline
    import torch
except ImportError as e:
    raise ImportError(
        f"Required packages not installed. Run: pip install -r requirements.txt\nMissing: {e}"
    )


# ---------------------------------------------------------------------------
# Available models
# ---------------------------------------------------------------------------

AVAILABLE_MODELS: List[Dict[str, Any]] = [
    {
        "id": "runwayml/stable-diffusion-v1-5",
        "name": "Stable Diffusion v1.5",
        "vram": "~4 GB",
        "notes": "Best balance of speed and quality",
        "default": True,
    },
    {
        "id": "CompVis/stable-diffusion-v1-4",
        "name": "Stable Diffusion v1.4",
        "vram": "~4 GB",
        "notes": "Classic, slightly lower quality",
    },
    {
        "id": "stabilityai/stable-diffusion-2-1",
        "name": "Stable Diffusion v2.1",
        "vram": "~5 GB",
        "notes": "Higher resolution (768px)",
    },
    {
        "id": "stabilityai/stable-diffusion-xl-base-1.0",
        "name": "Stable Diffusion XL",
        "vram": "~8 GB",
        "notes": "Highest quality, most VRAM",
    },
]


# ---------------------------------------------------------------------------
# Download flags (persist completed model downloads)
# ---------------------------------------------------------------------------

def _read_model_flags() -> Dict[str, Any]:
    """Reads persisted model flags from disk.
    
    Returns:
        Dict[str, Any]: A dictionary containing model flags, with at least 
        the key 'completed_models' pointing to a list of strings.
    """
    if not MODEL_FLAGS_FILE.exists():
        return {"completed_models": []}
    try:
        with MODEL_FLAGS_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            return {"completed_models": []}
        models = data.get("completed_models", [])
        if not isinstance(models, list):
            models = []
        return {"completed_models": [m for m in models if isinstance(m, str)]}
    except Exception as e:
        logger.warning(f"Failed to read model flags: {e}. Defaulting to empty.")
        return {"completed_models": []}


def _write_model_flags(data: Dict[str, Any]) -> None:
    """Writes model flags to disk.
    
    Args:
        data (Dict[str, Any]): The model flags data to persist.
    """
    MODEL_FLAGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_FLAGS_FILE.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)


def get_completed_model_ids() -> Set[str]:
    """Returns the set of model IDs flagged as fully downloaded.
    
    Returns:
        Set[str]: A set of completed model IDs.
    """
    return set(_read_model_flags().get("completed_models", []))


def mark_model_completed(model_id: str) -> None:
    """Persists a specific model ID as fully downloaded.
    
    Args:
        model_id (str): The Hugging Face model ID to mark as completed.
    """
    data = _read_model_flags()
    completed = set(data.get("completed_models", []))
    completed.add(model_id)
    data["completed_models"] = sorted(completed)
    _write_model_flags(data)


# ---------------------------------------------------------------------------
# Downloaded-image tracking (persist which generated images the user saved)
# ---------------------------------------------------------------------------

def _read_downloaded_images() -> Set[str]:
    """Reads the set of filenames the user has explicitly downloaded.
    
    Returns:
        Set[str]: A set of filenames.
    """
    if not DOWNLOADED_IMAGES_FILE.exists():
        return set()
    try:
        with DOWNLOADED_IMAGES_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            return {f for f in data if isinstance(f, str)}
        return set()
    except Exception as e:
        logger.warning(f"Failed to read downloaded images list: {e}")
        return set()


def _write_downloaded_images(filenames: Set[str]) -> None:
    """Writes the set of downloaded filenames to disk.
    
    Args:
        filenames (Set[str]): The set of filenames to persist.
    """
    DOWNLOADED_IMAGES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DOWNLOADED_IMAGES_FILE.open("w", encoding="utf-8") as fh:
        json.dump(sorted(filenames), fh, indent=2)


def get_downloaded_images() -> Set[str]:
    """Returns the set of generated-image filenames the user explicitly saved.
    
    Returns:
        Set[str]: The set of saved filenames.
    """
    return _read_downloaded_images()


def mark_image_downloaded(filename: str) -> None:
    """Records that the user specifically downloaded a generated image.
    
    Args:
        filename (str): The filename of the downloaded image.
    """
    current = _read_downloaded_images()
    current.add(filename)
    _write_downloaded_images(current)


# ---------------------------------------------------------------------------
# Device detection
# ---------------------------------------------------------------------------

def detect_device(force_cpu: bool = False) -> Dict[str, Any]:
    """Detects and returns information about the best available compute device.
    
    Args:
        force_cpu (bool, optional): If True, skips GPU detection and forces CPU usage. 
                                    Defaults to False.
    
    Returns:
        Dict[str, Any]: A dictionary containing device information:
                        - 'device' (str): e.g., 'cuda' or 'cpu'.
                        - 'name' (str): The human-readable device name.
                        - 'vram_gb' (Optional[float]): Available VRAM in GB if GPU, else None.
    """
    if force_cpu:
        return {"device": "cpu", "name": "CPU", "vram_gb": None}

    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
        return {"device": "cuda", "name": gpu_name, "vram_gb": vram_gb}

    return {"device": "cpu", "name": "CPU (no GPU detected)", "vram_gb": None}


# ---------------------------------------------------------------------------
# Pipeline management
# ---------------------------------------------------------------------------

_loaded_pipelines: Dict[str, StableDiffusionPipeline] = {}  # cache: model_id -> pipeline


def load_pipeline(model_id: str, device: str = "cuda") -> StableDiffusionPipeline:
    """Loads (or returns cached) Stable Diffusion pipeline for the given model ID.
    
    Args:
        model_id (str): The Hugging Face model repository ID.
        device (str, optional): The compute device to load onto. Defaults to "cuda".
        
    Returns:
        StableDiffusionPipeline: The initialized Hugging Face diffusers pipeline.
    """
    cache_key = f"{model_id}@{device}"

    if cache_key in _loaded_pipelines:
        logger.debug(f"Returning cached pipeline for {cache_key}")
        return _loaded_pipelines[cache_key]

    logger.info(f"Loading pipeline for {model_id} on {device}")
    torch_dtype = torch.float16 if device == "cuda" else torch.float32

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        safety_checker=None,
        requires_safety_checker=False,
        cache_dir=str(MODELS_DIR),
    )
    pipe = pipe.to(device)

    # Memory‑efficient attention when available
    if hasattr(pipe, "enable_xformers_memory_efficient_attention"):
        try:
            pipe.enable_xformers_memory_efficient_attention()
            logger.debug("Enabled xformers memory efficient attention.")
        except Exception as e:
            logger.debug(f"Could not enable xformers attention: {e}")

    _loaded_pipelines[cache_key] = pipe
    return pipe


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

class GenerationCancelledException(Exception):
    """Raised when the user cancels an ongoing image generation process."""
    pass


_cancel_requested: bool = False


def cancel_generation() -> None:
    """Sets a global flag to cancel an ongoing generation operation."""
    global _cancel_requested
    logger.info("Cancelling generation requested by user.")
    _cancel_requested = True


def generate_image(
    pipe: StableDiffusionPipeline,
    prompt: str,
    negative_prompt: str = "",
    guidance_scale: float = 7.5,
    num_inference_steps: int = 50,
    width: int = 512,
    height: int = 512,
) -> Tuple[Any, float]:
    """Generates an image from a text prompt using the provided pipeline.
    
    Args:
        pipe (StableDiffusionPipeline): The diffusion pipeline to use.
        prompt (str): The text prompt describing the desired image.
        negative_prompt (str, optional): Prompt detailing what to avoid. Defaults to "".
        guidance_scale (float, optional): Classifier-free guidance scale. Defaults to 7.5.
        num_inference_steps (int, optional): Number of denoising steps. Defaults to 50.
        width (int, optional): Output image width in pixels. Defaults to 512.
        height (int, optional): Output image height in pixels. Defaults to 512.
        
    Raises:
        GenerationCancelledException: If generation is cancelled mid-process.
        
    Returns:
        Tuple[Any, float]: A tuple containing the Pillow Image object and the elapsed time in seconds.
    """
    global _cancel_requested
    _cancel_requested = False

    start = time.time()

    def _callback_on_step_end(pipe_ref: Any, step_index: int, timestep: int, callback_kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Callback invoked by the diffusers pipeline after every generation step."""
        if _cancel_requested:
            raise GenerationCancelledException("Generation cancelled by user.")
        return callback_kwargs

    logger.info(f"Generating image. Prompt: '{prompt}', Steps: {num_inference_steps}, Scale: {guidance_scale}")
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt or None,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        width=width,
        height=height,
        callback_on_step_end=_callback_on_step_end,
    )

    elapsed = round(time.time() - start, 2)
    logger.info(f"Image generation completed in {elapsed}s.")
    return result.images[0], elapsed


# ---------------------------------------------------------------------------
# Filename helper
# ---------------------------------------------------------------------------

def make_filename(prompt: str, extension: str = "png") -> str:
    """Generates a unique, filesystem‑safe filename based on the prompt.
    
    Args:
        prompt (str): The prompt used for generation.
        extension (str, optional): The file extension. Defaults to "png".
        
    Returns:
        str: A safe, timestamped filename.
    """
    safe = "".join(c for c in prompt[:50] if c.isalnum() or c in (" ", "-", "_")).rstrip()
    safe = safe.replace(" ", "_") or "image"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{safe}_{ts}.{extension}"


# ---------------------------------------------------------------------------
# Model download helpers
# ---------------------------------------------------------------------------

def is_model_downloaded(model_id: str) -> bool:
    """Checks whether a specific model has been fully downloaded.

    Uses the persistent flags file (`model_flags.json`) as the single source of
    truth so the cached status survives server restarts.
    
    Args:
        model_id (str): The Hugging Face model repository ID.
        
    Returns:
        bool: True if fully downloaded, False otherwise.
    """
    return model_id in get_completed_model_ids()


def download_model_stream(model_id: str) -> Generator[str, None, None]:
    """Downloads a model and yields Server-Sent Events (SSE) progress updates.

    Downloads into `DOWNLOADING_DIR` (used as the HF cache directory). On success,
    the cached sub-folders are moved into the permanent `MODELS_DIR` to ensure 
    partial downloads never pollute the primary model directory.
    
    Args:
        model_id (str): The Hugging Face model repository ID to download.
        
    Yields:
        str: SSE-formatted JSON strings indicating download progress and status.
    """
    import json as _json
    import gc
    import shutil

    yield f"data: {_json.dumps({'progress': 0, 'status': 'Starting download…'})}\n\n"

    try:
        yield f"data: {_json.dumps({'progress': 10, 'status': 'Downloading model & components…'})}\n\n"
        logger.info(f"Starting background download for model: {model_id}")

        # HF creates `models--org--name/` folders inside the cache_dir.
        # We point it at DOWNLOADING_DIR so nothing lands in MODELS_DIR until
        # the download is fully successful.
        _pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,   # CPU-safe dtype for download-only
            safety_checker=None,
            requires_safety_checker=False,
            cache_dir=str(DOWNLOADING_DIR),
        )
        # Free memory immediately — we only needed the download side-effect.
        del _pipe
        gc.collect()

        # Move completed artifacts from _downloading -> models dir
        for entry in DOWNLOADING_DIR.iterdir():
            dest = MODELS_DIR / entry.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.move(str(entry), str(dest))

        mark_model_completed(model_id)
        logger.info(f"Successfully downloaded and cached model: {model_id}")

        yield f"data: {_json.dumps({'progress': 100, 'status': 'Download complete!'})}\n\n"
    except Exception as exc:
        logger.error(f"Error downloading model {model_id}: {exc}", exc_info=True)
        # Clean up partial artifacts in _downloading
        for entry in DOWNLOADING_DIR.iterdir():
            try:
                if entry.is_dir():
                    shutil.rmtree(entry, ignore_errors=True)
                else:
                    entry.unlink(missing_ok=True)
            except OSError as cleanup_exc:
                logger.warning(f"Failed to clean up incomplete download artifact {entry}: {cleanup_exc}")
        yield f"data: {_json.dumps({'progress': -1, 'status': f'Error: {exc}'})}\n\n"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_params(
    prompt: str,
    guidance_scale: float = 7.5,
    num_inference_steps: int = 50,
    negative_prompt: str = "",
) -> List[str]:
    """Validates generation parameters returning a list of error messages.
    
    Args:
        prompt (str): Primary image generation prompt.
        guidance_scale (float, optional): Classifier-free guidance. Defaults to 7.5.
        num_inference_steps (int, optional): Denoising steps. Defaults to 50.
        negative_prompt (str, optional): Prompt details to avoid. Defaults to "".
        
    Returns:
        List[str]: A list of error strings. Empty if all parameters are valid.
    """
    errors: List[str] = []
    if not prompt or not prompt.strip():
        errors.append("Prompt cannot be empty.")
    if len(prompt) > 500:
        errors.append("Prompt too long (max 500 characters).")
    if negative_prompt and len(negative_prompt) > 500:
        errors.append("Negative prompt too long (max 500 characters).")
    if not (1.0 <= guidance_scale <= 20.0):
        errors.append("Guidance scale must be between 1.0 and 20.0.")
    if not (1 <= num_inference_steps <= 150):
        errors.append("Inference steps must be between 1 and 150.")
    return errors
