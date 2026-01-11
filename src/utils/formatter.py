"""
Screenplay formatter - converts structured data to properly formatted screenplay text.
Follows industry-standard formatting (Courier 12pt equivalent spacing).
"""
from typing import List
from ..state import Scene, Character


class ScreenplayFormatter:
    """Format screenplay according to industry standards."""

    def __init__(self):
        # Standard screenplay margins and spacing
        self.page_width = 60  # Characters per line
        self.left_margin = 0
        self.dialogue_margin = 10
        self.character_margin = 20
        self.parenthetical_margin = 15
        self.transition_margin = 45

    def format_title_page(self, title: str, author: str = "AI Generated") -> str:
        """
        Format the title page.

        Example:
            TITLE

            Written by

            Author Name
        """
        title_page = "\n" * 20  # Start lower on page
        title_page += f"{title.upper()}\n\n\n"
        title_page += "Written by\n\n"
        title_page += f"{author}\n"
        title_page += "\n" * 20
        return title_page

    def format_scene_heading(self, heading: str) -> str:
        """
        Format scene heading (slug line).
        Example: INT. DETECTIVE'S OFFICE - NIGHT
        """
        return f"\n\n{heading.upper()}\n\n"

    def format_action(self, action: str) -> str:
        """
        Format action/description.
        Wraps text to proper width.
        """
        # Simple word wrap
        words = action.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= self.page_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return "\n".join(lines) + "\n"

    def format_character_name(self, character: str) -> str:
        """
        Format character name (centered above dialogue).
        """
        spaces = " " * self.character_margin
        return f"\n{spaces}{character.upper()}\n"

    def format_parenthetical(self, parenthetical: str) -> str:
        """
        Format parenthetical (actor direction).
        Example: (whispers)
        """
        spaces = " " * self.parenthetical_margin
        if not parenthetical.startswith("("):
            parenthetical = f"({parenthetical})"
        return f"{spaces}{parenthetical}\n"

    def format_dialogue_line(self, line: str) -> str:
        """
        Format dialogue (indented from character name).
        """
        # Simple word wrap for dialogue
        words = line.split()
        lines = []
        current_line = ""
        max_dialogue_width = 35  # Dialogue is narrower

        for word in words:
            if len(current_line) + len(word) + 1 <= max_dialogue_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        spaces = " " * self.dialogue_margin
        return "\n".join([f"{spaces}{line}" for line in lines]) + "\n"

    def format_transition(self, transition: str) -> str:
        """
        Format transition (right-aligned).
        Example: CUT TO:
        """
        if not transition:
            return ""

        spaces = " " * self.transition_margin
        return f"\n{spaces}{transition.upper()}\n"

    def format_scene(self, scene: Scene) -> str:
        """Format a complete scene."""
        formatted = ""

        # Scene heading
        formatted += self.format_scene_heading(scene.heading)

        # Action
        formatted += self.format_action(scene.action)

        # Dialogue
        for dialogue_block in scene.dialogue:
            character = dialogue_block.get('character', '')
            parenthetical = dialogue_block.get('parenthetical', '')
            line = dialogue_block.get('line', '')

            if character and line:
                formatted += self.format_character_name(character)

                if parenthetical:
                    formatted += self.format_parenthetical(parenthetical)

                formatted += self.format_dialogue_line(line)

        # Transition
        if scene.transition:
            formatted += self.format_transition(scene.transition)

        return formatted

    def format_screenplay(
        self,
        title: str,
        author: str,
        scenes: List[Scene]
    ) -> str:
        """
        Format complete screenplay.
        """
        screenplay = ""

        # Title page
        screenplay += self.format_title_page(title, author)

        # Page break
        screenplay += "\n" + "=" * 60 + "\n\n"

        # Screenplay content
        screenplay += "FADE IN:\n"

        # All scenes
        for scene in scenes:
            screenplay += self.format_scene(scene)

        # End
        screenplay += "\n\nFADE OUT.\n\nTHE END"

        return screenplay
