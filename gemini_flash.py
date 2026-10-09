from app.config import settings
from app.models import ComicOutline


def _client():
    from google import genai
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_outline(story_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> ComicOutline:
    prompt = f"""
Create a cohesive five-panel comic outline.

User story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Requirements:
- Exactly 5 panels, numbered 1 through 5.
- Maintain the same main character, setting, and visual identity across all panels.
- Each panel needs a short title, a scene description, and a detailed image-generation prompt.
- The final panel should provide a satisfying ending or cliffhanger.
- Do not put dialogue in image prompts; the application adds dialogue separately.
"""
    response = _client().models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ComicOutline,
            "temperature": 0.9,
        },
    )
    if getattr(response, "parsed", None):
        return response.parsed
    return ComicOutline.model_validate_json(response.text)
