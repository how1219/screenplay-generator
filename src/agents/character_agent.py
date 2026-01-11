"""
Character Agent: Develops detailed character profiles with visual descriptions.
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
import os
from typing import List
from ..state import Character


class CharacterSchema(BaseModel):
    """Character profile with visual description."""
    name: str = Field(description="Character name in CAPS (e.g., DR. ELENA REEVES)")
    age: int = Field(description="Character age")
    role: str = Field(description="Role: protagonist, antagonist, or supporting")
    description: str = Field(description="Comprehensive personality and background")
    arc: str = Field(description="How the character changes throughout the story")
    image_prompt: str = Field(description="DETAILED physical appearance for AI image generation")


class CharacterList(BaseModel):
    """List of characters for the screenplay."""
    characters: List[CharacterSchema] = Field(description="List of 3-5 main characters")


def create_character_agent(state: dict) -> dict:
    """
    Generate detailed character profiles with visual descriptions for image generation.
    """
    llm = ChatAnthropic(
        model=os.getenv("SCREENPLAY_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.7,
        max_tokens=4096
    )

    # Use structured output with a wrapper class
    structured_llm = llm.with_structured_output(CharacterList)

    system_prompt = """You are an expert character development consultant for screenplays.

Your task is to create detailed character profiles for the screenplay.

For each main character, provide:
1. Name (in CAPS for screenplay format)
2. Age
3. Role (protagonist, antagonist, supporting)
4. Description: Comprehensive personality and background
5. Character Arc: How they change throughout the story
6. Visual Description: DETAILED physical appearance for AI image generation

CRITICAL for Visual Description:
- Be extremely specific about physical features
- Include: age, gender, ethnicity, build, height
- Facial features: face shape, eyes, nose, hair (color, style, length)
- Clothing style and specific outfit details
- Distinguishing features (scars, tattoos, glasses, etc.)
- Overall demeanor and posture
- Use photorealistic, cinematic style language

Focus on 1-3 main characters (protagonist, antagonist, 1-3 supporting)."""

    user_prompt = f"""Logline: {state['logline']}
Genre: {state['genre']}
Tone: {state['tone']}

Outline:
{state['outline']}

Create detailed character profiles with visual descriptions for AI image generation."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        response = structured_llm.invoke(messages)
        print(response)
        print(f"Generated {len(response.characters)} characters")

        # Convert CharacterSchema objects to Character objects
        characters = [Character(**char.dict()) for char in response.characters]
        return {"characters": characters}
    except Exception as e:
        print(f"Error in character generation: {e}")
        # Return empty list as fallback
        return {"characters": []}
