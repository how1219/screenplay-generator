"""
Test script for Gemini 2.5 Flash image generation.
"""
from src.utils.image_generator import ImageGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_image_generation():
    """Test image generation with mock character descriptions."""

    generator = ImageGenerator()

    # Mock character descriptions
    test_characters = [
        {
            "name": "DETECTIVE SARAH CHEN",
            "image_prompt": "Asian woman, age 35, sharp features, intense dark eyes, shoulder-length black hair tied back, wearing a gray trench coat over a white button-up shirt, professional and determined expression, strong jawline, neutral background"
        },
        {
            "name": "DR. MARCUS WEBB",
            "image_prompt": "African American man, age 45, kind face with reading glasses, short graying hair, wearing a white lab coat over blue scrubs, warm smile, professional headshot, medical office background"
        }
    ]

    print("=" * 60)
    print("TESTING GEMINI 2.5 FLASH IMAGE GENERATION")
    print("=" * 60)
    print()

    for char in test_characters:
        print(f"\n📋 Testing character: {char['name']}")
        print(f"   Description: {char['image_prompt'][:80]}...")
        print()

        result = generator.generate_character_image(
            character_name=char['name'],
            image_prompt=char['image_prompt'],
            style="cinematic photorealistic"
        )

        if result:
            print(f"✅ SUCCESS: Image generated at {result}")
        else:
            print(f"❌ FAILED: Could not generate image for {char['name']}")

        print("-" * 60)

    print("\n" + "=" * 60)
    print("IMAGE GENERATION TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_image_generation()
