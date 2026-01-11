"""
Dialogue Agent: Enhances scenes with natural, character-specific dialogue.
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
import os
import json
from typing import List, Optional
from ..state import Scene


class DialogueItem(BaseModel):
    """A single line of dialogue."""
    character: str = Field(description="Character name in CAPS")
    parenthetical: Optional[str] = Field(default=None, description="Optional acting direction like (whispers)")
    line: str = Field(description="The dialogue line")


class DialogueList(BaseModel):
    """List of dialogue lines for a scene."""
    dialogue: List[DialogueItem] = Field(description="List of dialogue exchanges")


def create_dialogue_agent(state: dict) -> dict:
    """
    Write or enhance dialogue for each scene.
    """
    llm = ChatAnthropic(
        model=os.getenv("SCREENPLAY_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.8,  # Higher temperature for more creative dialogue
        max_tokens=4096
    )

    # Use structured output for dialogue
    structured_llm = llm.with_structured_output(DialogueList)

    # Process each scene
    enhanced_scenes = []

    for scene in state.get('scenes', []):
        # Get character info for this scene
        characters_in_scene = set()
        for dialogue in scene.dialogue:
            characters_in_scene.add(dialogue.get('character', ''))

        character_info = "\n".join([
            f"- {char.name}: {char.description}"
            for char in state.get('characters', [])
            if char.name in characters_in_scene
        ])

        system_prompt = """You are an award-winning screenplay dialogue writer.

Your task is to write natural, compelling dialogue that:
- Reveals character personality
- Advances the plot
- Sounds like real people talking
- Includes subtext and conflict
- Uses parentheticals sparingly (only for important acting notes)
- Varies in rhythm and pacing

Keep dialogue concise - film is a visual medium. Show, don't tell."""

        user_prompt = f"""Scene #{scene.scene_number}
Heading: {scene.heading}
Action: {scene.action}

Characters in this scene:
{character_info}

Genre: {state['genre']}
Tone: {state['tone']}

Current dialogue (enhance or replace):
{json.dumps(scene.dialogue, indent=2)}

Write compelling, natural dialogue for this scene."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            response = structured_llm.invoke(messages)
            print(response)
            # Convert DialogueItem objects to dicts
            scene.dialogue = [item.dict() for item in response.dialogue]
        except Exception as e:
            print(f"Error generating dialogue for scene {scene.scene_number}: {e}")
            # Keep original dialogue if parsing fails
            pass

        enhanced_scenes.append(scene)

    return {"scenes": enhanced_scenes}
