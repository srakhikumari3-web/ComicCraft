from app.config import settings
from app.models import ComicOutline, ComicStory


def _client():
    from google import genai
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(outline: ComicOutline, character_name: str, tone: str) -> ComicStory:
    outline_text = outline.model_dump_json(indent=2)
    prompt = f"""
Expand this five-panel comic outline into polished comic narration.
Main character: {character_name}
Tone: {tone}

Outline:
{outline_text}

Requirements:
- Return exactly five story panels matching panel numbers 1-5.
- Each panel must have concise narration, one atmospheric caption, and natural character dialogue.
- Keep continuity of character, location, events, and emotions.
- Dialogue should be suitable for a comic speech bubble and should not contain screenplay directions.
"""
    response = _client().models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ComicStory,
            "temperature": 0.95,
        },
    )
    if getattr(response, "parsed", None):
        return response.parsed
    return ComicStory.model_validate_json(response.text)
