"""
PDF Export with professional screenplay formatting and character pages.
Uses ReportLab for industry-standard PDF generation.
Includes episode numbers and scene numbers on margins.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, PageTemplate, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from pathlib import Path
from typing import List, Optional
from ..state import Character, Scene
import os


class ScreenplayPDFExporter:
    """Export screenplay to professional PDF - just formats data, no calculation logic."""

    def __init__(self):
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "generated_screenplays"))
        self.output_dir.mkdir(exist_ok=True)

        # Standard screenplay format
        self.page_width, self.page_height = letter
        self.left_margin = 1.5 * inch
        self.right_margin = 1.0 * inch
        self.top_margin = 1.0 * inch
        self.bottom_margin = 1.0 * inch

    def create_styles(self):
        """Create custom paragraph styles for screenplay elements."""
        styles = {}

        # Title page
        styles['Title'] = ParagraphStyle(
            'Title',
            fontName='Courier-Bold',
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=12
        )

        styles['Author'] = ParagraphStyle(
            'Author',
            fontName='Courier',
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=6
        )

        # Scene heading with scene number
        styles['SceneHeading'] = ParagraphStyle(
            'SceneHeading',
            fontName='Courier-Bold',
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12
        )

        # Action
        styles['Action'] = ParagraphStyle(
            'Action',
            fontName='Courier',
            fontSize=12,
            spaceAfter=6,
            alignment=TA_LEFT
        )

        # Character name
        styles['Character'] = ParagraphStyle(
            'Character',
            fontName='Courier',
            fontSize=12,
            leftIndent=2.2 * inch,
            spaceAfter=0
        )

        # Parenthetical
        styles['Parenthetical'] = ParagraphStyle(
            'Parenthetical',
            fontName='Courier',
            fontSize=12,
            leftIndent=1.8 * inch,
            spaceAfter=0
        )

        # Dialogue
        styles['Dialogue'] = ParagraphStyle(
            'Dialogue',
            fontName='Courier',
            fontSize=12,
            leftIndent=1.3 * inch,
            rightIndent=1.5 * inch,
            spaceAfter=6
        )

        # Transition
        styles['Transition'] = ParagraphStyle(
            'Transition',
            fontName='Courier-Bold',
            fontSize=12,
            leftIndent=4.0 * inch,
            spaceAfter=6,
            spaceBefore=6
        )

        # Character page
        styles['CharacterName'] = ParagraphStyle(
            'CharacterName',
            fontName='Helvetica-Bold',
            fontSize=18,
            spaceAfter=12
        )

        styles['CharacterInfo'] = ParagraphStyle(
            'CharacterInfo',
            fontName='Helvetica',
            fontSize=11,
            spaceAfter=6
        )

        # Scene number style (left and right margins)
        styles['SceneNumber'] = ParagraphStyle(
            'SceneNumber',
            fontName='Courier',
            fontSize=12,
            alignment=TA_LEFT
        )

        return styles

    def create_title_page(self, title: str, author: str) -> List:
        """Create title page elements."""
        styles = self.create_styles()
        story = []

        # Add spacing to center on page
        story.append(Spacer(1, 2.5 * inch))

        # Title
        story.append(Paragraph(title.upper(), styles['Title']))
        story.append(Spacer(1, 0.3 * inch))

        # Written by
        story.append(Paragraph("Written by", styles['Author']))
        story.append(Spacer(1, 0.1 * inch))

        # Author
        story.append(Paragraph(author, styles['Author']))

        # Page break
        story.append(PageBreak())

        return story

    def create_character_pages(self, characters: List[Character]) -> List:
        """Create character reference pages with images and descriptions."""
        styles = self.create_styles()
        story = []

        story.append(Paragraph("CHARACTER REFERENCE", styles['Title']))
        story.append(Spacer(1, 0.3 * inch))
        story.append(PageBreak())

        for character in characters:
            # Character name
            story.append(Paragraph(character.name, styles['CharacterName']))
            story.append(Spacer(1, 0.1 * inch))

            # Character image if available
            if character.image_path and os.path.exists(character.image_path):
                try:
                    img = Image(character.image_path, width=3*inch, height=3*inch)
                    story.append(img)
                    story.append(Spacer(1, 0.2 * inch))
                except Exception as e:
                    print(f"Could not load image for {character.name}: {e}")

            # Character details
            if character.age:
                story.append(Paragraph(f"<b>Age:</b> {character.age}", styles['CharacterInfo']))

            story.append(Paragraph(f"<b>Role:</b> {character.role.title()}", styles['CharacterInfo']))
            story.append(Spacer(1, 0.1 * inch))

            # Description
            story.append(Paragraph(f"<b>Description:</b>", styles['CharacterInfo']))
            story.append(Paragraph(character.description, styles['CharacterInfo']))
            story.append(Spacer(1, 0.1 * inch))

            # Character arc
            if character.arc:
                story.append(Paragraph(f"<b>Character Arc:</b>", styles['CharacterInfo']))
                story.append(Paragraph(character.arc, styles['CharacterInfo']))

            # Page break between characters
            story.append(PageBreak())

        return story

    def create_screenplay_pages(self, scenes: List[Scene]) -> List:
        """Create formatted screenplay pages with scene numbers and episode markers."""
        styles = self.create_styles()
        story = []

        # FADE IN
        story.append(Paragraph("FADE IN:", styles['SceneHeading']))
        story.append(Spacer(1, 0.2 * inch))

        # Track current episode to insert episode markers
        current_episode = None

        # Process each scene
        for scene in scenes:
            # Add episode marker when episode changes
            if scene.episode_number != current_episode:
                current_episode = scene.episode_number
                story.append(Spacer(1, 0.3 * inch))
                story.append(Paragraph(f"<b>EPISODE {current_episode}</b>", styles['SceneHeading']))
                story.append(Spacer(1, 0.3 * inch))

            # Scene heading with scene number on both margins
            # We'll add the scene number prefix to the heading
            scene_num = str(scene.scene_number)
            heading_with_number = f"{scene_num}    {scene.heading.upper()}"

            story.append(Paragraph(heading_with_number, styles['SceneHeading']))

            # Action
            story.append(Paragraph(scene.action, styles['Action']))
            story.append(Spacer(1, 0.1 * inch))

            # Dialogue
            for dialogue_block in scene.dialogue:
                character = dialogue_block.get('character', '')
                parenthetical = dialogue_block.get('parenthetical', '')
                line = dialogue_block.get('line', '')

                if character and line:
                    # Character name
                    story.append(Paragraph(character.upper(), styles['Character']))

                    # Parenthetical
                    if parenthetical:
                        if not parenthetical.startswith('('):
                            parenthetical = f"({parenthetical})"
                        story.append(Paragraph(parenthetical, styles['Parenthetical']))

                    # Dialogue
                    story.append(Paragraph(line, styles['Dialogue']))

            # Transition
            if scene.transition:
                story.append(Paragraph(scene.transition.upper(), styles['Transition']))

            story.append(Spacer(1, 0.2 * inch))

        # FADE OUT
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("FADE OUT.", styles['Transition']))
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("THE END", styles['Character']))

        return story

    def export_pdf(
        self,
        title: str,
        author: str,
        characters: List[Character],
        scenes: List[Scene],
        filename: Optional[str] = None
    ) -> str:
        """
        Export complete screenplay to PDF with episode number and scene numbers.

        Returns:
            Path to generated PDF
        """
        # Generate filename
        if not filename:
            safe_title = title.replace(" ", "_").replace(".", "").lower()
            filename = f"{safe_title}_screenplay.pdf"

        output_path = self.output_dir / filename

        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            leftMargin=self.left_margin,
            rightMargin=self.right_margin,
            topMargin=self.top_margin,
            bottomMargin=self.bottom_margin
        )

        # Build story
        story = []

        # Title page
        story.extend(self.create_title_page(title, author))

        # Character pages
        if characters:
            story.extend(self.create_character_pages(characters))

        # Screenplay with inline episode markers
        story.extend(self.create_screenplay_pages(scenes))

        # Build PDF
        doc.build(story)

        print(f"✓ PDF exported: {output_path}")
        return str(output_path)
