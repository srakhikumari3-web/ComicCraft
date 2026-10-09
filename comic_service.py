from app.config import settings
from app.models import PromptRequest, ComicPanel
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf


def _demo_pipeline(request: PromptRequest):
    from app.models import ComicOutline, PanelOutline, ComicStory, StoryPanel
    panels = []
    story = []
    for i in range(1, 6):
        panels.append(PanelOutline(
            panel_number=i,
            title=f"Adventure Panel {i}",
            scene_description=f"{request.character_name} continues the adventure in {request.setting}.",
            image_prompt=f"{request.art_style} comic panel, {request.character_name} in {request.setting}, panel {i}, {request.tone} mood, expressive character, cinematic composition"
        ))
        story.append(StoryPanel(
            panel_number=i,
            narration=f"{request.character_name} moves the story forward in panel {i}.",
            caption=f"A {request.tone} moment in {request.setting}.",
            dialogue=[f"{request.character_name}: Let's keep going!"]
        ))
    return ComicOutline(panels=panels), ComicStory(panels=story)


def generate_comic(request: PromptRequest):
    if settings.demo_mode:
        outline, story = _demo_pipeline(request)
    else:
        outline = generate_outline(
            request.story_prompt, request.character_name, request.setting, request.tone, request.art_style
        )
        story = generate_story(outline, request.character_name, request.tone)

    image_paths = []
    for panel in outline.panels:
        image_prompt = (
            f"{panel.image_prompt}. Consistent character design: {request.character_name}. "
            f"Visual style: {request.art_style}. Clean comic illustration, no text, no speech bubbles."
        )
        image_paths.append(generate_image(image_prompt))

    layout = build_comic_layout(outline, story, image_paths)
    title = outline.panels[0].title if outline.panels else "My Comic"
    pdf_url = save_pdf(layout, title)
    return title, layout, pdf_url
