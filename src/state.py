"""
State management for the screenplay generation workflow.
"""
from typing import TypedDict, List, Optional
from pydantic import BaseModel


class Character(BaseModel):
    """Character information."""
    name: str
    age: Optional[int] = None
    description: str  # Physical appearance and personality
    role: str  # protagonist, antagonist, supporting
    arc: Optional[str] = None  # Character arc description
    image_prompt: Optional[str] = None  # Detailed prompt for image generation
    image_path: Optional[str] = None  # Path to generated character image


class Scene(BaseModel):
    """Individual screenplay scene."""
    scene_number: int
    episode_number: Optional[int] = 1  # Episode this scene belongs to
    heading: str  # e.g., "INT. DETECTIVE'S OFFICE - NIGHT"
    action: str  # Scene description/action
    dialogue: List[dict]  # [{"character": "JOHN", "line": "...", "parenthetical": "(optional)"}]
    transition: Optional[str] = None  # e.g., "CUT TO:", "FADE OUT."


class ScreenplayState(TypedDict):
    """State for the screenplay generation workflow."""
    # Input
    idea: str

    # Agent outputs
    logline: Optional[str]
    genre: Optional[str]
    tone: Optional[str]

    outline: Optional[str]  # 3-act structure
    beat_sheet: Optional[str]  # Detailed scene breakdown

    characters: Optional[List[Character]]

    scenes: Optional[List[Scene]]
    episode_number: Optional[int]  # Episode number for this screenplay

    # Formatting
    title: Optional[str]
    author: Optional[str]
    formatted_screenplay: Optional[str]  # Properly formatted text

    # Output
    pdf_path: Optional[str]

    # Metadata
    total_pages: Optional[int]
    generation_time: Optional[float]
