"""
Character image generation using Gemini 2.5 Flash.
"""
import os
from pathlib import Path
import urllib.request
import urllib.error
import json
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
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.google_api_key}"

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

            # Use urllib instead of requests to avoid LangSmith tracing recursion issues
            req = urllib.request.Request(
                gemini_url,
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"}
            )

            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    if response.status != 200:
                        print(f"❌ Error from Gemini API: {response.status}")
                        return None

                    data = json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                print(f"❌ HTTP Error from Gemini API: {e.code}")
                return None
            except urllib.error.URLError as e:
                print(f"❌ Connection Error: {e.reason}")
                return None

            # Process response immediately
            try:
                candidates = data.get("candidates", [])

                if not candidates:
                    print(f"⚠️  No candidates in response")
                    return None

                parts = candidates[0].get("content", {}).get("parts", [])

                # Find the image data in parts
                for part in parts:
                    inline_data = part.get("inlineData")
                    if inline_data:
                        # Extract and process image immediately
                        image_b64 = inline_data.get("data")
                        mime = inline_data.get("mimeType", "image/png")

                        # Decode and save
                        img_bytes = base64.b64decode(image_b64)

                        safe_name = character_name.replace(" ", "_").replace(".", "").lower()
                        ext = "png" if "png" in mime else "jpg"
                        image_path = self.output_dir / f"{safe_name}.{ext}"

                        with open(image_path, 'wb') as f:
                            f.write(img_bytes)

                        print(f"✓ Generated image: {image_path}")
                        return str(image_path)

                print(f"⚠️  No image data in response")
                return None

            except Exception as parse_error:
                print(f"❌ Error parsing response")
                return None

        except Exception as e:
            print(f"❌ Error generating image: {str(e)[:100]}")
            return None
