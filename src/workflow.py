"""
Main LangGraph workflow for screenplay generation.
"""
from langgraph.graph import StateGraph, END
from typing import Dict
import time
from dotenv import load_dotenv

from .state import ScreenplayState
from .agents.logline_agent import create_logline_agent
from .agents.outline_agent import create_outline_agent
from .agents.character_agent import create_character_agent
from .agents.scene_agent import create_scene_agent
from .agents.dialogue_agent import create_dialogue_agent
from .utils.formatter import ScreenplayFormatter
from .utils.image_generator import ImageGenerator
from .utils.pdf_exporter import ScreenplayPDFExporter

# Load environment variables
load_dotenv()


class ScreenplayWorkflow:
    """LangGraph workflow for generating complete screenplays."""

    def __init__(self):
        self.formatter = ScreenplayFormatter()
        self.image_generator = ImageGenerator()
        self.pdf_exporter = ScreenplayPDFExporter()

    def generate_title(self, state: Dict) -> Dict:
        """Extract title from logline."""
        # Simple title generation - extract from logline
        logline = state.get('logline', '')
        # Take first few words as title
        words = logline.split()[:4]
        title = " ".join(words).replace(",", "").replace(".", "")
        return {"title": title.upper(), "author": "AI Generated"}

    def format_screenplay(self, state: Dict) -> Dict:
        """Format the screenplay text."""
        scenes = state.get('scenes', [])
        title = state.get('title', 'UNTITLED')
        author = state.get('author', 'AI Generated')

        formatted_text = self.formatter.format_screenplay(title, author, scenes)

        return {"formatted_screenplay": formatted_text}

    def generate_character_images(self, state: Dict) -> Dict:
        """Generate images for main characters."""
        characters = state.get('characters', [])
        updated_characters = []

        for character in characters:
            if character.image_prompt:
                print(f"\n🎨 Generating image for {character.name}...")
                image_path = self.image_generator.generate_character_image(
                    character.name,
                    character.image_prompt,
                    style="cinematic photorealistic"
                )
                character.image_path = image_path

            updated_characters.append(character)

        return {"characters": updated_characters}

    def export_to_pdf(self, state: Dict) -> Dict:
        """Export screenplay to PDF."""
        title = state.get('title', 'UNTITLED')
        author = state.get('author', 'AI Generated')
        characters = state.get('characters', [])
        scenes = state.get('scenes', [])

        print(f"\n📄 Exporting to PDF...")

        pdf_path = self.pdf_exporter.export_pdf(
            title=title,
            author=author,
            characters=characters,
            scenes=scenes
        )

        # Calculate total pages (rough estimate)
        total_pages = len(characters) + 2 + len(scenes)  # Character pages + title + scenes

        return {
            "pdf_path": pdf_path,
            "total_pages": total_pages
        }

    def build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""

        # Create workflow
        workflow = StateGraph(ScreenplayState)

        # Add nodes (use different names than state keys to avoid conflicts)
        workflow.add_node("logline_agent", create_logline_agent)
        workflow.add_node("outline_agent", create_outline_agent)
        workflow.add_node("character_agent", create_character_agent)
        workflow.add_node("scene_agent", create_scene_agent)
        workflow.add_node("dialogue_agent", create_dialogue_agent)
        workflow.add_node("title_generator", self.generate_title)
        workflow.add_node("formatter", self.format_screenplay)
        workflow.add_node("image_generator", self.generate_character_images)
        workflow.add_node("pdf_exporter", self.export_to_pdf)

        # Define flow
        workflow.set_entry_point("logline_agent")
        workflow.add_edge("logline_agent", "outline_agent")
        workflow.add_edge("outline_agent", "character_agent")
        workflow.add_edge("character_agent", "scene_agent")
        workflow.add_edge("scene_agent", "dialogue_agent")
        workflow.add_edge("dialogue_agent", "title_generator")
        workflow.add_edge("title_generator", "formatter")
        workflow.add_edge("formatter", "image_generator")
        workflow.add_edge("image_generator", "pdf_exporter")
        workflow.add_edge("pdf_exporter", END)

        return workflow.compile()

    def generate_screenplay(self, idea: str) -> Dict:
        """
        Generate a complete screenplay from an idea.

        Args:
            idea: The story idea/concept

        Returns:
            Final state with PDF path and metadata
        """
        start_time = time.time()

        print(f"\n{'='*60}")
        print(f"🎬 AI SCREENPLAY GENERATOR")
        print(f"{'='*60}\n")
        print(f"📝 Story Idea: {idea}\n")

        # Build and run workflow
        app = self.build_workflow()

        # Initial state
        initial_state = {"idea": idea}

        # Run workflow
        print("🤖 Starting screenplay generation workflow...\n")

        final_state = app.invoke(initial_state)

        # Calculate generation time
        generation_time = time.time() - start_time
        final_state['generation_time'] = generation_time

        print(f"\n{'='*60}")
        print(f"✅ SCREENPLAY GENERATION COMPLETE!")
        print(f"{'='*60}\n")
        print(f"📊 Summary:")
        print(f"  Title: {final_state.get('title', 'N/A')}")
        print(f"  Episode: {final_state.get('episode_number', 'N/A')}")
        print(f"  Genre: {final_state.get('genre', 'N/A')}")
        print(f"  Logline: {final_state.get('logline', 'N/A')}")
        print(f"  Characters: {len(final_state.get('characters', []))}")
        print(f"  Scenes: {len(final_state.get('scenes', []))}")
        print(f"  PDF: {final_state.get('pdf_path', 'N/A')}")
        print(f"  Generation Time: {generation_time:.1f}s\n")

        return final_state


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.workflow 'Your story idea here'")
        print("\nExample:")
        print("  python -m src.workflow 'A retired detective returns for one last cold case'")
        sys.exit(1)

    idea = " ".join(sys.argv[1:])

    workflow = ScreenplayWorkflow()
    result = workflow.generate_screenplay(idea)

    print(f"\n✨ Open your screenplay: {result['pdf_path']}")


if __name__ == "__main__":
    main()
