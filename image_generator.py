import re
import uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from app.config import settings, PANELS_DIR


def _safe_name(prompt: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", prompt.lower()).strip("-")[:45]
    return f"{slug or 'panel'}-{uuid.uuid4().hex[:8]}.png"


def _demo_image(prompt: str, output: Path) -> None:
    image = Image.new("RGB", (settings.image_width, settings.image_height), (244, 238, 220))
    draw = ImageDraw.Draw(image)
    draw.rectangle((12, 12, image.width - 12, image.height - 12), outline=(30, 30, 30), width=5)
    draw.text((30, 30), "COMICCRAFT DEMO PANEL", fill=(20, 20, 20))
    wrapped = " ".join(prompt.split())
    draw.text((30, 100), wrapped[:350], fill=(50, 50, 50), spacing=8)
    image.save(output, format="PNG")


def _hf_image(prompt: str) -> Image.Image:
    if not settings.hf_api_key:
        raise RuntimeError("HF_API_KEY is not configured for IMAGE_BACKEND=hf.")
    from huggingface_hub import InferenceClient
    client = InferenceClient(api_key=settings.hf_api_key, provider="auto")
    return client.text_to_image(
        prompt=prompt,
        model=settings.hf_image_model,
    )


def _local_diffusers_image(prompt: str) -> Image.Image:
    try:
        import torch
        from diffusers import DiffusionPipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local Diffusers backend requires the optional packages in requirements-local-diffusers.txt."
        ) from exc

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    kwargs = {"torch_dtype": dtype}
    if torch.cuda.is_available():
        kwargs["variant"] = "fp16"
    pipe = DiffusionPipeline.from_pretrained(settings.local_image_model, **kwargs)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    result = pipe(
        prompt,
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=settings.image_steps,
    )
    return result.images[0]


def generate_image(prompt: str) -> str:
    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    filename = _safe_name(prompt)
    output = PANELS_DIR / filename

    backend = settings.image_backend.lower()
    if backend == "demo":
        _demo_image(prompt, output)
    elif backend == "hf":
        _hf_image(prompt).save(output)
    elif backend == "local_diffusers":
        _local_diffusers_image(prompt).save(output)
    else:
        raise RuntimeError(f"Unsupported IMAGE_BACKEND: {settings.image_backend}")

    return f"/static/panels/{filename}"
