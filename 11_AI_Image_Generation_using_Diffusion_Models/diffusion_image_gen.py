#!/usr/innovation/env python3
"""
AI Image Generation — CLI Interface (v2)

Provides a command-line interface for the diffusion engine.
Users can generate images directly from terminal prompts.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Configure CLI logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] CLI: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Fast-path: handle --list-models before importing heavy deps
if "--list-models" in sys.argv:
    from engine import AVAILABLE_MODELS

    print("Available Stable Diffusion models:\n")
    for m in AVAILABLE_MODELS:
        default_tag = " (default)" if m.get("default") else ""
        print(f"  {m['id']}{default_tag}")
        print(f"      {m['name']} — VRAM: {m['vram']} — {m['notes']}")
    sys.exit(0)

from engine import (
    AVAILABLE_MODELS,
    PROJECT_ROOT,
    detect_device,
    generate_image,
    load_pipeline,
    make_filename,
    validate_params,
)


def main() -> None:
    """Parses command-line arguments and executes the image generation pipeline."""
    generated_dir: Path = PROJECT_ROOT / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(
        description="Generate images from text prompts using Stable Diffusion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "a cat wearing a wizard hat"
  %(prog)s "a sunset over mountains" --negative "blurry, cartoon"
  %(prog)s "a futuristic city" --steps 75 --guidance 8.5
  %(prog)s "abstract art" --output my_art.png --cpu
        """,
    )

    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("--negative", dest="negative_prompt", default="",
                        help="Negative prompt (what to avoid)")
    parser.add_argument("--steps", dest="num_inference_steps", type=int, default=50,
                        help="Number of inference steps (1-150, default: 50)")
    parser.add_argument("--guidance", dest="guidance_scale", type=float, default=7.5,
                        help="Guidance scale (1.0-20.0, default: 7.5)")
    parser.add_argument("--output", "-o", dest="output_file",
                        help="Output filename (default: auto-generated)")
    parser.add_argument("--model", dest="model_id",
                        default="runwayml/stable-diffusion-v1-5",
                        help="HuggingFace model ID")
    parser.add_argument("--cpu", action="store_true",
                        help="Force CPU usage even if GPU is available")
    parser.add_argument("--list-models", action="store_true",
                        help="List popular models and exit")

    args = parser.parse_args()

    # Validate parameters
    errors = validate_params(
        args.prompt, args.guidance_scale, args.num_inference_steps, args.negative_prompt
    )
    if errors:
        for e in errors:
            logger.error(f"Validation Error: {e}")
        sys.exit(1)

    # Device detection
    info = detect_device(force_cpu=args.cpu)
    device = info["device"]
    if device == "cuda":
        logger.info(f"✓ GPU detected: {info['name']} ({info['vram_gb']}GB)")
    else:
        logger.warning("⚠ No GPU detected. Using CPU (this will be slow).")

    # Load model
    logger.info(f"Loading model: {args.model_id}")
    try:
        pipe = load_pipeline(args.model_id, device)
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        sys.exit(1)

    # Generate
    logger.info("Generating image…")
    try:
        image, gen_time = generate_image(
            pipe,
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            guidance_scale=args.guidance_scale,
            num_inference_steps=args.num_inference_steps,
        )
        logger.info(f"Image generated in {gen_time:.2f}s")
    except Exception as e:
        logger.error(f"Failed to generate image: {e}")
        sys.exit(1)

    # Save
    if args.output_file:
        out_path = Path(args.output_file)
        if not out_path.is_absolute():
            out_path = PROJECT_ROOT / out_path
    else:
        out_path = generated_dir / make_filename(args.prompt)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        image.save(str(out_path))
        logger.info(f"✓ Image saved to: {out_path}")
        logger.info(f"✓ File size: {os.path.getsize(out_path) / 1024:.1f} KB")
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
