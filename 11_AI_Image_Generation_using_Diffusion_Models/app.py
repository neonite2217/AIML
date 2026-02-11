"""
AI Image Generation — Flask Web Server (v2)

Wraps the diffusion engine with a REST API and serves the frontend.
"""

import os
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context

from engine import (
    AVAILABLE_MODELS,
    DOWNLOADING_DIR,
    HF_HUB_CACHE_DIR,
    PROJECT_TMP_DIR,
    TORCH_HOME_DIR,
    TRANSFORMERS_CACHE_DIR,
    detect_device,
    download_model_stream,
    generate_image,
    get_downloaded_images,
    is_model_downloaded,
    load_pipeline,
    make_filename,
    mark_image_downloaded,
    validate_params,
    GenerationCancelledException,
    cancel_generation,
)

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent
GENERATED_DIR: Path = BASE_DIR / "generated"
GENERATED_DIR.mkdir(exist_ok=True)

def _reset_directory_contents(directory: Path) -> None:
    """Removes all files/subdirectories from the specified directory and recreates it.
    
    Args:
        directory (Path): The directory to wipe clean.
    """
    directory.mkdir(parents=True, exist_ok=True)
    for entry in directory.iterdir():
        try:
            if entry.is_dir():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                entry.unlink(missing_ok=True)
        except OSError as e:
            logger.debug(f"Failed to remove {entry}: {e}")


def _cleanup_runtime_artifacts() -> None:
    """Selectively cleans up runtime artifacts on startup.

    - Generated images NOT explicitly saved are wiped.
    - Temporary cache spaces (transformers, torch) are wiped.
    - Partial model downloads are wiped.
    - Completed model downloads remain untouched.
    """
    logger.info("Cleaning up old runtime artifacts...")
    # ── 1. Generated images: always wipe ───────────────────────────────────
    _reset_directory_contents(GENERATED_DIR)

    # ── 2. Temp / transformers / torch scratch space: always wipe ────────
    for directory in (PROJECT_TMP_DIR, TRANSFORMERS_CACHE_DIR, TORCH_HOME_DIR):
        _reset_directory_contents(directory)

    # ── 3. Wipe partial downloads (DOWNLOADING_DIR) ─────────────────────
    _reset_directory_contents(DOWNLOADING_DIR)

    # ── 4. Wipe old HF hub cache (models now live in MODELS_DIR) ────────
    _reset_directory_contents(HF_HUB_CACHE_DIR)
    logger.info("Runtime artifact cleanup completed.")


# Clear all runtime artifacts on server startup so no stale files remain.
_cleanup_runtime_artifacts()

app = Flask(__name__, static_folder="static", static_url_path="/static")

# ---------------------------------------------------------------------------
# Startup: detect device
# ---------------------------------------------------------------------------

device_info: Dict[str, Any] = detect_device()
logger.info(f"Device initialized: {device_info['name']} ({device_info['device']})")

# We encapsulate the global lazy-loaded state into a dictionary so 
# it can be explicitly modified without scattered globals.
class AppState:
    pipeline: Any = None
    current_model_id: Optional[str] = None

app_state = AppState()


def _get_pipeline(model_id: str) -> Any:
    """Returns the cached pipeline, initializing it if necessary.
    
    Args:
        model_id (str): The model ID to load.
        
    Returns:
        Any: The Stable Diffusion pipeline.
    """
    if app_state.pipeline is None or app_state.current_model_id != model_id:
        logger.info(f"Initializing pipeline lazily for {model_id} on {device_info['device']}")
        app_state.pipeline = load_pipeline(model_id, device_info["device"])
        app_state.current_model_id = model_id
    return app_state.pipeline


# ---------------------------------------------------------------------------
# Routes — Frontend
# ---------------------------------------------------------------------------

@app.route("/")
def index() -> Response:
    """Serves the primary frontend HTML."""
    return send_from_directory(app.static_folder, "index.html")


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------

@app.route("/api/device", methods=["GET"])
def api_device() -> Response:
    """Returns information about the available computation device."""
    return jsonify(device_info)


@app.route("/api/models", methods=["GET"])
def api_models() -> Response:
    """Returns a list of all available models."""
    return jsonify(AVAILABLE_MODELS)


@app.route("/api/model-status", methods=["GET"])
def api_model_status() -> Response:
    """Returns the download status for each known model."""
    statuses: Dict[str, bool] = {}
    for m in AVAILABLE_MODELS:
        statuses[m["id"]] = is_model_downloaded(m["id"])
    return jsonify(statuses)


@app.route("/api/download-model", methods=["POST"])
def api_download_model() -> Union[Response, Tuple[Response, int]]:
    """Initiates a model download and streams progress via Server-Sent Events (SSE)."""
    data = request.get_json(force=True, silent=True) or {}
    model_id = data.get("model_id", "").strip()

    known_ids = [m["id"] for m in AVAILABLE_MODELS]
    if model_id not in known_ids:
        logger.warning(f"Download requested for unknown model: {model_id}")
        return jsonify({"ok": False, "errors": [f"Unknown model: {model_id}"]}), 400

    logger.info(f"Starting API streaming download for model: {model_id}")
    return Response(
        stream_with_context(download_model_stream(model_id)),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/api/generated", methods=["GET"])
def api_generated() -> Response:
    """Lists the 50 most recently generated images."""
    images = sorted(GENERATED_DIR.glob("*.png"), key=os.path.getmtime, reverse=True)
    gallery: List[Dict[str, Any]] = []
    
    for img in images[:50]:
        gallery.append({
            "filename": img.name,
            "url": f"/generated/{img.name}",
            "size_kb": round(img.stat().st_size / 1024, 1),
        })
    return jsonify(gallery)


@app.route("/api/cancel", methods=["POST"])
def api_cancel() -> Response:
    """Cancels an ongoing image generation."""
    logger.info("API cancellation requested.")
    cancel_generation()
    return jsonify({"ok": True, "message": "Cancellation requested."})


@app.route("/api/generate", methods=["POST"])
def api_generate() -> Union[Response, Tuple[Response, int]]:
    """Generates an image from a JSON payload matching the Diffusion Engine API."""
    data = request.get_json(force=True, silent=True) or {}

    prompt: str = data.get("prompt", "").strip()
    negative_prompt: str = data.get("negative_prompt", "").strip()
    guidance_scale: float = float(data.get("guidance_scale", 7.5))
    steps: int = int(data.get("steps", 50))
    model_id: str = data.get("model_id", "runwayml/stable-diffusion-v1-5")

    # Validate inputs
    errors = validate_params(prompt, guidance_scale, steps, negative_prompt)
    if errors:
        logger.warning(f"Validation failed for generate API: {errors}")
        return jsonify({"ok": False, "errors": errors}), 400

    # Validate model
    known_ids = [m["id"] for m in AVAILABLE_MODELS]
    if model_id not in known_ids:
        logger.warning(f"API generate requested for unknown model: {model_id}")
        return jsonify({"ok": False, "errors": [f"Unknown model: {model_id}"]}), 400

    try:
        pipe = _get_pipeline(model_id)
        image, gen_time = generate_image(
            pipe,
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=steps,
        )

        filename = make_filename(prompt)
        save_path = GENERATED_DIR / filename
        image.save(str(save_path))

        logger.info(f"Successfully generated API image: {filename} in {gen_time}s")
        return jsonify({
            "ok": True,
            "image_url": f"/generated/{filename}",
            "filename": filename,
            "generation_time": gen_time,
            "prompt": prompt,
        })

    except GenerationCancelledException as exc:
        logger.warning("Agent generation cancelled mid-process.")
        return jsonify({"ok": False, "cancelled": True, "errors": [str(exc)]}), 499
    except Exception as exc:
        logger.error(f"Image generation failed: {exc}", exc_info=True)
        return jsonify({"ok": False, "errors": [str(exc)]}), 500


@app.route("/generated/<path:filename>")
def serve_generated(filename: str) -> Response:
    """Serves a specific generated image file."""
    return send_from_directory(str(GENERATED_DIR), filename)


@app.route("/api/download-image/<path:filename>")
def api_download_image(filename: str) -> Response:
    """Serves a generated image with specific Content-Disposition headers to prompt browser download."""
    # Record that the user saved this image so it survives server restarts.
    mark_image_downloaded(filename)
    logger.info(f"User requested download of image: {filename}")
    return send_from_directory(
        str(GENERATED_DIR),
        filename,
        as_attachment=True,
        download_name=filename,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Diffusion Image Generator on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
