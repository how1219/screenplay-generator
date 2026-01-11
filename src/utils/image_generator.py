"""
Character image generation using Gemini 2.5 Flash.
"""
import os
from pathlib import Path
import requests
from typing import Optional
import base64


class ImageGenerator:
    """Generate character reference images using Gemini 2.5 Flash."""

    def __init__(self):
        self.output_dir = Path(os.getenv("IMAGES_DIR", "generated_images"))
        self.output_dir.mkdir(exist_ok=True)
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.model = "gemini-2.5-flash-image"  

    def generate_character_image(
        self,
        character_name: str,
        image_prompt: str,
        style: str = "cinematic photorealistic"
    ) -> Optional[str]:
        """
        Generate a character reference image using Gemini 2.5 Flash.

        Args:
            character_name: Name of the character (for filename)
            image_prompt: Detailed visual description
            style: Image style modifier

        Returns:
            Path to generated image, or None if failed
        """
        try:
            # Enhance prompt with style
            full_prompt = f"{style} portrait of {image_prompt}. Professional headshot style, neutral background, high detail, 4K quality, photorealistic."

            print(f"🎨 Generating image for {character_name} using Gemini 2.5 Flash...")

            # Use Gemini API endpoint for image generation
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

            headers = {
                "Content-Type": "application/json",
            }

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Generate an image: {full_prompt}"
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                }
            }

            # Make API request
            response = requests.post(
                f"{gemini_url}?key={self.google_api_key}",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                result = response.json()

                # Debug: Print full response structure
                print(f"   DEBUG: Response keys: {result.keys()}")

                # Extract image data from Gemini response
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]
                    print(f"   DEBUG: Candidate keys: {candidate.keys()}")

                    if "content" in candidate:
                        content = candidate["content"]
                        print(f"   DEBUG: Content keys: {content.keys()}")
                        parts = content.get("parts", [])
                        print(f"   DEBUG: Number of parts: {len(parts)}")

                        for i, part in enumerate(parts):
                            print(f"   DEBUG: Part {i} keys: {part.keys()}")

                            if "inlineData" in part:
                                # Image is returned as inline data
                                image_data_b64 = part["inlineData"]["data"]
                                mime_type = part["inlineData"]["mimeType"]

                                # Decode base64 image
                                image_data = base64.b64decode(image_data_b64)

                                # Save image with appropriate extension
                                safe_name = character_name.replace(" ", "_").replace(".", "").lower()
                                ext = "png" if "png" in mime_type else "jpg"
                                image_path = self.output_dir / f"{safe_name}.{ext}"

                                with open(image_path, 'wb') as f:
                                    f.write(image_data)

                                print(f"✓ Generated image: {image_path}")
                                return str(image_path)

                    print(f"⚠️  No image data in response for {character_name}")
                    print(f"   Full response: {result}")
                    return None
                else:
                    print(f"⚠️  No candidates in response for {character_name}")
                    print(f"   Response: {result}")
                    return None
            else:
                print(f"❌ Error from Gemini API: {response.status_code}")
                print(f"   Response: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Error generating image for {character_name}: {e}")
            print("   Tip: Make sure your Google API key has access to Gemini API with image generation")
            return None
