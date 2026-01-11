"""
Logline Agent: Creates compelling one-sentence logline from story idea.
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
import os


class LoglineSchema(BaseModel):
    """Screenplay logline with genre and tone."""
    logline: str = Field(description="One-sentence logline (max 40 words)")
    genre: str = Field(description="Genre (e.g., Drama, Thriller, Comedy, Horror, Sci-Fi)")
    tone: str = Field(description="Tone (e.g., Dark, Humorous, Suspenseful, Heartwarming)")


def create_logline_agent(state: dict) -> dict:
    """
    Generate a compelling logline from the story idea.

    A logline should be one sentence that includes:
    - Protagonist
    - Inciting incident
    - Goal/Stakes
    """
    llm = ChatAnthropic(
        model=os.getenv("SCREENPLAY_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=0.7,
        max_tokens=1024
    )

    # Use structured output
    structured_llm = llm.with_structured_output(LoglineSchema)

    system_prompt = """You are an expert screenplay consultant specializing in loglines.

Your task is to create a compelling, professional logline from a story idea.

A great logline should:
- Be ONE sentence (max 40 words)
- Include the protagonist
- State the inciting incident
- Reveal the goal or stakes
- Hint at the genre/tone
- Be intriguing and marketable"""

    user_prompt = f"""Story Idea:
{state['idea']}

Create a professional logline with genre and tone."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        response = structured_llm.invoke(messages)
        print(response)
        print(f"Logline generated: {response.logline[:100]}...")

        return {
            "logline": response.logline,
            "genre": response.genre,
            "tone": response.tone
        }
    except Exception as e:
        print(f"Error in logline generation: {e}")
        return {
            "logline": "A compelling story unfolds.",
            "genre": "Drama",
            "tone": "Dramatic"
        }
