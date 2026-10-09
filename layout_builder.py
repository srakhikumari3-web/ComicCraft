from typing import List
from app.models import ComicOutline, ComicStory, ComicPanel


def build_comic_layout(outline: ComicOutline, story: ComicStory, image_paths: List[str]) -> List[ComicPanel]:
    story_by_number = {p.panel_number: p for p in story.panels}
    layout: List[ComicPanel] = []
    for outline_panel, image_path in zip(sorted(outline.panels, key=lambda p: p.panel_number), image_paths):
        story_panel = story_by_number.get(outline_panel.panel_number)
        if not story_panel:
            raise ValueError(f"Missing story data for panel {outline_panel.panel_number}.")
        layout.append(
            ComicPanel(
                panel_number=outline_panel.panel_number,
                title=outline_panel.title,
                image_path=image_path,
                scene_description=outline_panel.scene_description,
                image_prompt=outline_panel.image_prompt,
                narration=story_panel.narration,
                caption=story_panel.caption,
                dialogue=story_panel.dialogue,
            )
        )
    return layout
