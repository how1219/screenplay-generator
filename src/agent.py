"""
LangGraph agent entry point for deployment.
This file exports the compiled graph for the LangGraph server.
"""
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from src.state import ScreenplayState
from src.agents.logline_agent import create_logline_agent
from src.agents.outline_agent import create_outline_agent
from src.agents.character_agent import create_character_agent
from src.agents.scene_agent import create_scene_agent
from src.agents.dialogue_agent import create_dialogue_agent
from src.utils.formatter import ScreenplayFormatter
from src.utils.image_generator import ImageGenerator
from src.utils.pdf_exporter import ScreenplayPDFExporter

# Load environment variables
load_dotenv()

# Initialize utilities
formatter = ScreenplayFormatter()
image_generator = ImageGenerator()
pdf_exporter = ScreenplayPDFExporter()


def format_screenplay(state: dict) -> dict:
    """Format the screenplay text."""
    scenes = state.get('scenes', [])
    title = state.get('title', 'UNTITLED')
    author = "AI Generated"

    formatted_text = formatter.format_screenplay(title, author, scenes)

    return {
        "formatted_screenplay": formatted_text,
        "author": author
    }


def generate_character_images(state: dict) -> dict:
    """Generate images for main characters."""
    characters = state.get('characters', [])
    updated_characters = []

    for character in characters:
        if character.image_prompt:
            print(f"\n🎨 Generating image for {character.name}...")
            image_path = image_generator.generate_character_image(
                character.name,
                character.image_prompt,
                style="cinematic photorealistic"
            )
            character.image_path = image_path

        updated_characters.append(character)

    return {"characters": updated_characters}


def export_to_pdf(state: dict) -> dict:
    """Export screenplay to PDF."""
    title = state.get('title', 'UNTITLED')
    author = state.get('author', 'AI Generated')
    characters = state.get('characters', [])
    scenes = state.get('scenes', [])

    print(f"\n📄 Exporting to PDF...")

    pdf_path = pdf_exporter.export_pdf(
        title=title,
        author=author,
        characters=characters,
        scenes=scenes
    )

    # Calculate total pages
    total_pages = len(characters) + 2 + len(scenes)

    return {
        "pdf_path": pdf_path,
        "total_pages": total_pages
    }


# Build the workflow
workflow = StateGraph(ScreenplayState)

# Add nodes
workflow.add_node("logline_agent", create_logline_agent)
workflow.add_node("outline_agent", create_outline_agent)
workflow.add_node("character_agent", create_character_agent)
workflow.add_node("scene_agent", create_scene_agent)
workflow.add_node("dialogue_agent", create_dialogue_agent)
workflow.add_node("formatter", format_screenplay)
workflow.add_node("image_generator", generate_character_images)
workflow.add_node("pdf_exporter", export_to_pdf)

# Define flow
workflow.set_entry_point("logline_agent")
workflow.add_edge("logline_agent", "outline_agent")
workflow.add_edge("outline_agent", "character_agent")
workflow.add_edge("character_agent", "scene_agent")
workflow.add_edge("scene_agent", "dialogue_agent")
workflow.add_edge("dialogue_agent", "formatter")
workflow.add_edge("formatter", "image_generator")
workflow.add_edge("image_generator", "pdf_exporter")
workflow.add_edge("pdf_exporter", END)

# Export the compiled graph for LangGraph server
graph = workflow.compile()


def main():
    """CLI entry point for running the screenplay generator."""
    import sys
    import time

    if len(sys.argv) < 2:
        print("Usage: python -m src.agent 'Your story idea here'")
        print("\nExample:")
        print("  python -m src.agent 'A retired detective returns for one last cold case'")
        sys.exit(1)

    idea = " ".join(sys.argv[1:])
    start_time = time.time()

    print(f"\n{'='*60}")
    print(f"🎬 AI SCREENPLAY GENERATOR")
    print(f"{'='*60}\n")
    print(f"📝 Story Idea: {idea}\n")
    print("🤖 Starting screenplay generation workflow...\n")

    # Run workflow
    initial_state = {"idea": idea}
    final_state = graph.invoke(initial_state)

    # Calculate generation time
    generation_time = time.time() - start_time

    print(f"\n{'='*60}")
    print(f"✅ SCREENPLAY GENERATION COMPLETE!")
    print(f"{'='*60}\n")
    print(f"📊 Summary:")
    print(f"  Title: {final_state.get('title', 'N/A')}")
    print(f"  Genre: {final_state.get('genre', 'N/A')}")
    print(f"  Logline: {final_state.get('logline', 'N/A')}")
    print(f"  Characters: {len(final_state.get('characters', []))}")
    print(f"  Scenes: {len(final_state.get('scenes', []))}")
    print(f"  PDF: {final_state.get('pdf_path', 'N/A')}")
    print(f"  Generation Time: {generation_time:.1f}s\n")
    print(f"✨ Open your screenplay: {final_state['pdf_path']}\n")


if __name__ == "__main__":
    main()
