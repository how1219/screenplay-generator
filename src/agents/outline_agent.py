"""
Outline Agent: Creates 3-act structure and beat sheet using structured output.
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
import os


class ScreenplayStructure(BaseModel):
    """Screenplay structure with 3-act outline and beat sheet."""
    outline: str = Field(description="The detailed 3-act structure outline (Save the Cat style)")
    beat_sheet: str = Field(description="Scene-by-scene beat breakdown (3-5 key scenes)")
    estimated_page_count: int = Field(description="Estimated number of pages for the script")


def create_outline_agent(state: dict) -> dict:
    """
    Generate a 3-act structure outline and detailed beat sheet.

    Uses LangChain's structured output to ensure reliable JSON parsing.
    """
    # Setup LLM with increased max_tokens for longer screenplay content
    llm = ChatAnthropic(
        model=os.getenv("SCREENPLAY_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.7,
        max_tokens=8192
    )

    # Apply structured output - returns Pydantic object instead of raw string
    structured_llm = llm.with_structured_output(ScreenplayStructure)

    system_prompt = """You are an expert screenplay story structure consultant.
Your task is to create a detailed 3-act structure outline with beat sheet.

Structure your outline using Save the Cat! or traditional 3-act format:

ACT 1 (Setup - 25%)
- Opening Image
- Setup/Status Quo
- Inciting Incident
- Debate/Resistance
- Break into Act 2

ACT 2 (Confrontation - 50%)
- B Story/Subplot
- Fun and Games/Rising Action
- Midpoint (false victory or defeat)
- Bad Guys Close In
- All is Lost
- Dark Night of the Soul
- Break into Act 3

ACT 3 (Resolution - 25%)
- Finale/Climax
- Resolution
- Closing Image

Then create a BEAT SHEET with 3-5 key scenes/beats."""

    user_prompt = f"""Logline: {state['logline']}
Genre: {state['genre']}
Tone: {state['tone']}

Create a detailed 3-act outline and beat sheet for this screenplay."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        # Invoke the structured model - returns a ScreenplayStructure object
        response = structured_llm.invoke(messages)

        print(response)

        print(f"Outline generated. Est pages: {response.estimated_page_count}")

        # Access data directly from the Pydantic object
        return {
            "outline": response.outline,
            "beat_sheet": response.beat_sheet
        }

    except Exception as e:
        print(f"Error in outline generation: {e}")
        # Fallback handling
        return {
            "outline": "Error generating outline.",
            "beat_sheet": "Error generating beat sheet."
        }
