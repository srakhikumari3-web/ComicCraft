from pathlib import Path
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth import require_non_empty
from app.config import EXPORTS_DIR, TEMPLATES_DIR, settings
from app.models import PromptRequest
from app.services.comic_service import generate_comic

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _form_request(story_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> PromptRequest:
    return PromptRequest(
        story_prompt=require_non_empty(story_prompt, "Story prompt"),
        character_name=require_non_empty(character_name, "Character name"),
        setting=require_non_empty(setting, "Setting"),
        tone=require_non_empty(tone, "Tone"),
        art_style=require_non_empty(art_style, "Art style"),
    )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"settings": settings})


@router.post("/generate", response_class=HTMLResponse)
async def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = _form_request(story_prompt, character_name, setting, tone, art_style)
        title, layout, pdf_url = generate_comic(data)
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={"title": title, "layout": layout, "pdf_url": pdf_url},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc), "settings": settings},
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):
    try:
        title, layout, pdf_url = generate_comic(payload)
        return {"success": True, "title": title, "layout": [p.model_dump() for p in layout], "pdf_url": pdf_url}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    from app.services.image_generator import generate_image
    try:
        image_path = generate_image(require_non_empty(prompt, "Prompt"))
        return {"success": True, "image_path": image_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/export/{filename}")
async def export_pdf(filename: str):
    safe_name = Path(filename).name
    if safe_name != filename or not safe_name.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid PDF filename.")
    path = EXPORTS_DIR / safe_name
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(path, media_type="application/pdf", filename=safe_name)


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(request=request, name="export_success.html", context={})


@router.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}
