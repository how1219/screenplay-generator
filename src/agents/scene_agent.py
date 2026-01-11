"""
Scene Agent: Breaks outline into individual screenplay scenes.
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
import os
from typing import List, Optional
from ..state import Scene


class DialogueItem(BaseModel):
    """A single line of dialogue."""
    character: str = Field(description="Character name in CAPS")
    parenthetical: Optional[str] = Field(default=None, description="Optional acting direction")
    line: str = Field(description="The dialogue line")


class SceneSchema(BaseModel):
    """A single screenplay scene."""
    scene_number: int = Field(description="Scene number (sequential)")
    episode_number: int = Field(description="Episode number this scene belongs to")
    heading: str = Field(description="Scene heading: INT./EXT. LOCATION - TIME")
    action: str = Field(description="Scene description in present tense (3-5 sentences)")
    dialogue: List[DialogueItem] = Field(default_factory=list, description="Dialogue exchanges")
    transition: Optional[str] = Field(default=None, description="Optional transition (e.g., CUT TO:)")


class SceneList(BaseModel):
    """List of scenes for the screenplay."""
    scenes: List[SceneSchema] = Field(description="List of 3-5 scenes")


def create_scene_agent(state: dict) -> dict:
    """
    Break the outline into individual scenes with proper screenplay formatting.
    """
    llm = ChatAnthropic(
        model=os.getenv("SCREENPLAY_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.7,
        max_tokens=8192
    )

    # Use structured output with a wrapper class
    structured_llm = llm.with_structured_output(SceneList)

    # Create character list for reference
    character_names = [char.name for char in state.get('characters', [])]
    character_info = "\n".join([
        f"- {char.name}: {char.description}" for char in state.get('characters', [])
    ])

    system_prompt = """You are an expert screenplay writer specializing in scene construction.

Your task is to break the outline into individual scenes with proper screenplay format.

SCENE AND EPISODE NUMBERING:
- Assign sequential scene_number starting from 1 (continues across all episodes)
- Divide scenes into episodes based on story structure and natural narrative breaks
- YOU decide how many episodes are needed based on the story:
  * Simple stories may need 1-2 episodes
  * Complex stories may need 3-5 episodes
  * Each episode should represent a major story arc or act
- Episode breaks should occur at natural story beats (act breaks, major turning points, cliffhangers)
- Each scene must have both scene_number and episode_number

EXAMPLE EPISODE STRUCTURES:
- For 10 scenes in 2 episodes: Scenes 1-5 (ep 1: setup), Scenes 6-10 (ep 2: resolution)
- For 12 scenes in 3 `episodes: Scenes 1-4 (ep 1), Scenes 5-8 (ep 2), Scenes 9-12 (ep 3)
- For 15 scenes in 4 episodes: Scenes 1-4 (ep 1), Scenes 5-8 (ep 2), Scenes 9-12 (ep 3), Scenes 13-15 (ep 4)

SCENE HEADING FORMAT:
- INT. or EXT.
- LOCATION
- TIME OF DAY (DAY, NIGHT, MORNING, EVENING, etc.)
Example: "INT. DETECTIVE'S OFFICE - NIGHT"

ACTION (Scene Description):
- Present tense
- Visual and cinematic
- Character introductions in CAPS first time
- Specific and engaging
- Usually 3-5 sentences per scene

DIALOGUE:
- Character name in CAPS
- Optional parenthetical for delivery/action
- Natural, character-specific dialogue
- Keep it tight and purposeful

TRANSITIONS (optional):
- CUT TO:
- FADE OUT.
- DISSOLVE TO:

Create 3-5 scenes total divided intelligently into episodes based on the story's natural structure."""

    user_prompt = f"""Logline: {state['logline']}
Genre: {state['genre']}
Tone: {state['tone']}

Beat Sheet:
{state['beat_sheet']}

Characters:
{character_info}

Create 3-5 scenes with proper screenplay formatting.

IMPORTANT:
- Assign scene_number sequentially (1, 2, 3, 4, 5...)
- Decide how many episodes this story needs (1-5 episodes)
- Assign episode_number to each scene based on natural story structure and turning points
- Episode breaks should happen at dramatic moments that would make good episode endings

Include scene headings, action, and placeholder for dialogue (dialogue will be written in next step)."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        response = structured_llm.invoke(messages)
        print(response)
        print(f"Generated {len(response.scenes)} scenes")

        # Convert SceneSchema objects to Scene objects
        # LLM assigns both scene_number and episode_number
        scenes = []
        for scene_schema in response.scenes:
            # Convert DialogueItem objects to dicts
            dialogue_list = [item.dict() for item in scene_schema.dialogue]

            # Use episode_number from LLM response
            scene_dict = {
                "scene_number": scene_schema.scene_number,
                "episode_number": scene_schema.episode_number,  # From LLM
                "heading": scene_schema.heading,
                "action": scene_schema.action,
                "dialogue": dialogue_list,
                "transition": scene_schema.transition
            }
            scenes.append(Scene(**scene_dict))

        # Show episode breakdown
        if scenes:
            episodes = {}
            for scene in scenes:
                ep = scene.episode_number
                if ep not in episodes:
                    episodes[ep] = []
                episodes[ep].append(scene.scene_number)

            print(f"✓ Generated {len(scenes)} scenes across {len(episodes)} episodes")
            for ep_num in sorted(episodes.keys()):
                scene_nums = episodes[ep_num]
                print(f"  Episode {ep_num}: Scenes {scene_nums[0]}-{scene_nums[-1]} ({len(scene_nums)} scenes)")

            # Return max episode number (total episodes)
            max_episode = max(episodes.keys())
        else:
            max_episode = 1

        return {
            "scenes": scenes,
            "episode_number": max_episode  # Total number of episodes
        }
    except Exception as e:
        print(f"Error in scene generation: {e}")
        return {"scenes": [], "episode_number": 1}
