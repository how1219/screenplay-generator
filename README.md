# 🎬 AI Screenplay Generator

A professional AI-powered screenplay generator using **LangGraph** and **Python**. Transforms story ideas into complete, industry-formatted screenplays with character reference images.

## ✨ Features

- 🤖 **Multi-Agent Pipeline**: 8-step workflow with 5 AI agents 
- 📝 **Industry-Standard Format**: Proper screenplay formatting (Courier 12pt equivalent)
- 🎨 **Character Images**: AI-generated character reference images using Gemini 2.5 Flash
- 📄 **Professional PDF**: Export to PDF with episode markers, scene numbers, and character pages
- ⚡ **LangGraph Workflow**: State-of-the-art orchestration with LangChain
- 🎯 **Claude 3.5 Sonnet**: Best-in-class creative writing AI
- 📺 **Episode Structure**: Intelligent scene division into episodes with natural story breaks
- 🔒 **Structured Output**: Pydantic v2 with LangChain's with_structured_output()

## 🏗️ Architecture

### Multi-Agent Workflow

```
Story Idea
    ↓
1. Logline Agent → Creates title, logline, genre, and tone
    ↓
2. Outline Agent → 3-act structure + beat sheet (3-5 key scenes)
    ↓
3. Character Agent → Detailed character profiles + visual descriptions
    ↓
4. Scene Agent → Breaks outline into 3-5 scenes with episode numbering
    ↓
5. Dialogue Agent → Writes natural, character-specific dialogue
    ↓
6. Formatter → Applies industry-standard screenplay formatting
    ↓
7. Image Generator → Generates character reference images (Gemini 2.5 Flash)
    ↓
8. PDF Exporter → Creates professional PDF with episodes and scene numbers
    ↓
Complete Screenplay PDF ✨
```

### Technology Stack

- **Framework**: LangGraph (LangChain)
- **Language**: Python 3.11+
- **AI Model**: Claude 3.5 Sonnet (Anthropic)
- **Image Generation**: Gemini 2.5 Flash (Google)
- **PDF Generation**: ReportLab
- **Structured Output**: LangChain's with_structured_output() + Pydantic v2 models

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Anthropic API key (for Claude 3.5 Sonnet)
- Google API key (for Gemini 2.5 Flash image generation)
- LangSmith API key (optional - only for LangGraph Studio/Cloud deployment)

### Installation

```bash
# Clone or navigate to project directory
cd screenplay-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Configuration

Edit `.env` file:

```bash
# Required API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Optional - LangSmith (only for LangGraph Studio/Cloud)
LANGSMITH_API_KEY=your_langsmith_key_here

# Optional - customize models
SCREENPLAY_MODEL=claude-3-5-sonnet-20241022

# Optional - customize output
OUTPUT_DIR=generated_screenplays
IMAGES_DIR=generated_images
```

## 📖 Usage

### Method 1: LangGraph Studio (Recommended)

Use [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) for visual workflow debugging:

```bash
# Start the LangGraph development server
langgraph dev

# This will:
# - Start a local server
# - Open LangGraph Studio in your browser
# - Auto-detect langgraph.json configuration
```

Then in the Studio UI:
1. Enter your story idea in the input
2. Run the workflow and watch each agent execute
3. View the generated screenplay PDF

**Note**: Requires `LANGSMITH_API_KEY` in `.env`

### Method 2: Direct Python Execution

Run the screenplay generator directly from the command line:

```bash
# Direct execution
python -m src.agent "Your story idea here"

# Example
python -m src.agent "A retired detective returns to solve one last cold case"
```

**Note**: Only requires `ANTHROPIC_API_KEY` and `GOOGLE_API_KEY`

### Testing

Test the image generation:

```bash
# Test Gemini image generation
python test_image_gen.py
```

## 📂 Project Structure

```
screenplay-generator/
├── src/
│   ├── agents/              # AI agents
│   │   ├── logline_agent.py
│   │   ├── outline_agent.py
│   │   ├── character_agent.py
│   │   ├── scene_agent.py
│   │   └── dialogue_agent.py
│   ├── utils/               # Utilities
│   │   ├── formatter.py     # Screenplay formatting
│   │   ├── image_generator.py  # Gemini image generation
│   │   └── pdf_exporter.py  # PDF export with episodes
│   ├── state.py             # Pydantic state models
│   └── agent.py             # LangGraph workflow (entry point)
├── langgraph.json           # LangGraph Studio configuration
├── test_image_gen.py        # Test image generation
├── generated_screenplays/   # Output PDFs
├── generated_images/        # Character images
├── requirements.txt
├── .env.example
└── README.md
```

## 📝 Output Format

### Generated Files

1. **Character Reference Images** (`.png`)
   - AI-generated character portraits
   - Saved to `generated_images/`

2. **Screenplay PDF** (`.pdf`)
   - Title page
   - Character pages with images and descriptions
   - Industry-formatted screenplay
   - Saved to `generated_screenplays/`

### PDF Structure

```
1. Title Page
   - Screenplay title
   - "Written by AI Generated"

2. Character Reference Section
   - One page per main character
   - Character image (AI-generated with Gemini)
   - Age, role, description
   - Character arc

3. Screenplay with Episodes
   - FADE IN:
   - Episode markers (when episode changes)
   - Properly formatted scenes:
     * Scene numbers (left margin)
     * Scene headings (INT/EXT)
     * Action description
     * Character names
     * Dialogue
     * Transitions
   - FADE OUT.
   - THE END
```

## 🎯 Screenplay Format

Follows industry-standard screenplay format:

- **Courier 12pt** equivalent
- **Scene Headings**: ALL CAPS, bold
- **Action**: Left-aligned, present tense
- **Character Names**: Centered above dialogue
- **Dialogue**: Indented, natural
- **Parentheticals**: Actor directions in (parentheses)
- **Transitions**: Right-aligned (CUT TO:, FADE OUT.)

Example:

```
EPISODE 1

1    INT. DETECTIVE'S OFFICE - NIGHT

JOHN REYNOLDS (55, weathered) sits at his desk, surrounded
by cold case files. Rain hammers against the window.

                    JOHN
            (muttering)
    Twenty years. Twenty goddamn years.

He picks up a yellowed photograph, studies it.

                                        CUT TO:
```

## ⚙️ Customization

### Modify Agents

Edit agent files in `src/agents/` to customize:
- Writing style
- Scene structure
- Dialogue approach
- Character development

### Change Models

Update `.env`:

```bash
# Use different Claude model
SCREENPLAY_MODEL=claude-3-opus-20240229

# Change output directories
OUTPUT_DIR=my_screenplays
IMAGES_DIR=my_images
```

### Adjust Output

Modify `src/utils/pdf_exporter.py`:
- PDF styling
- Page layout
- Font sizes
- Margins
- Episode formatting

### Control Screenplay Length

Edit agent prompts to change scene count:
- `src/agents/outline_agent.py` - Change "3-5 key scenes" to your desired count
- `src/agents/scene_agent.py` - Change "3-5 scenes" to match

## 🐛 Troubleshooting

### Common Issues

**"API key not found"**
- Ensure `.env` file exists with `ANTHROPIC_API_KEY` and `GOOGLE_API_KEY`
- Load environment: `source venv/bin/activate`

**"Image generation failed"**
- Check Google API key
- Verify Gemini API access
- Check quota/billing
- Note: Image generation is still being tested

**"PDF has formatting issues"**
- Ensure ReportLab installed: `pip install reportlab`
- Check font availability (Courier should be built-in)

**"Agents not responding"**
- Check Anthropic API key
- Verify model name: `claude-3-5-sonnet-20241022`
- Check API quota

**"Structured output errors"**
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Project uses LangChain's `.with_structured_output()` method
- This wraps Claude with Pydantic v2 models for type-safe responses

---

**Built with LangGraph, Claude 3.5 Sonnet, and Gemini 2.5 Flash**