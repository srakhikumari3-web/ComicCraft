from typing import List
from pydantic import BaseModel, Field, field_validator

class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=5, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: str = Field(min_length=1, max_length=80)
    art_style: str = Field(min_length=1, max_length=120)

    @field_validator("story_prompt", "character_name", "setting", "tone", "art_style")
    @classmethod
    def strip_values(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value

class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    image_prompt: str

class ComicOutline(BaseModel):
    panels: List[PanelOutline] = Field(min_length=5, max_length=5)

class StoryPanel(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    narration: str
    caption: str
    dialogue: List[str] = Field(default_factory=list)

class ComicStory(BaseModel):
    panels: List[StoryPanel] = Field(min_length=5, max_length=5)

class ComicPanel(BaseModel):
    panel_number: int
    title: str
    image_path: str
    scene_description: str
    image_prompt: str
    narration: str
    caption: str
    dialogue: List[str]

class ComicResponse(BaseModel):
    success: bool
    title: str
    layout: List[ComicPanel]
    pdf_url: str
