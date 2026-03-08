"""
Example usage of Veo 3.1 Video Generator
Demonstrates various ways to generate videos
"""

import os
from veo3_video_generator import Veo3VideoGenerator

# Set your API key (or use environment variable GOOGLE_API_KEY)
API_KEY = os.getenv('GOOGLE_API_KEY', 'your_api_key_here')


def example_text_to_video_basic():
    """Basic text-to-video generation"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Text-to-Video")
    print("="*60)

    generator = Veo3VideoGenerator(api_key=API_KEY)

    prompt = "A golden retriever puppy playing with a red ball in a sunny park, slow motion"

    generator.generate_text_to_video(
        prompt=prompt,
        output_path="puppy_playing.mp4"
    )


def example_text_to_video_advanced():
    """Advanced text-to-video with custom parameters"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Advanced Text-to-Video (Portrait, 1080p, 8s)")
    print("="*60)

    generator = Veo3VideoGenerator(api_key=API_KEY)

    prompt = "A professional chef preparing sushi in a modern kitchen, cinematic lighting, close-up shots"

    generator.generate_text_to_video(
        prompt=prompt,
        output_path="chef_cooking.mp4",
        aspect_ratio="9:16",  # Portrait for social media
        resolution="1080p",    # High quality
        duration="8",          # 8 seconds
        negative_prompt="blurry, low quality, distorted hands"
    )


def example_image_to_video():
    """Convert a static image to video with motion"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Image-to-Video")
    print("="*60)

    generator = Veo3VideoGenerator(api_key=API_KEY)

    # You'll need an actual image file for this
    image_path = "input_photo.jpg"

    if os.path.exists(image_path):
        prompt = "Camera slowly zooms in while the subject looks at camera and smiles"

        generator.generate_image_to_video(
            prompt=prompt,
            image_path=image_path,
            output_path="animated_photo.mp4",
            duration="6"
        )
    else:
        print(f"⚠️  Image not found: {image_path}")
        print("Please provide an image file to test image-to-video generation")


def example_video_extension():
    """Extend an existing Veo-generated video"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Video Extension")
    print("="*60)

    generator = Veo3VideoGenerator(api_key=API_KEY)

    # You'll need a previously generated Veo video
    video_path = "output.mp4"

    if os.path.exists(video_path):
        generator.extend_video(
            video_path=video_path,
            output_path="extended_output.mp4"
        )
    else:
        print(f"⚠️  Video not found: {video_path}")
        print("Please generate a video first to test extension feature")


def example_creative_prompts():
    """Examples of creative video prompts"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Creative Prompt Ideas")
    print("="*60)

    generator = Veo3VideoGenerator(api_key=API_KEY)

    creative_prompts = [
        {
            "name": "Cinematic Drone Shot",
            "prompt": "Aerial drone shot flying over a misty mountain range at sunrise, cinematic colors, sweeping camera movement",
            "output": "drone_mountains.mp4",
            "aspect_ratio": "16:9",
            "resolution": "1080p",
            "duration": "8"
        },
        {
            "name": "Product Showcase",
            "prompt": "Luxury watch rotating on a black velvet surface, studio lighting, reflections, elegant presentation",
            "output": "product_watch.mp4",
            "aspect_ratio": "9:16",
            "resolution": "1080p",
            "duration": "6"
        },
        {
            "name": "Nature Scene",
            "prompt": "Underwater footage of colorful tropical fish swimming through coral reef, clear blue water, natural lighting",
            "output": "underwater_reef.mp4",
            "aspect_ratio": "16:9",
            "resolution": "720p",
            "duration": "6"
        },
        {
            "name": "Abstract Art",
            "prompt": "Colorful paint mixing in water, abstract patterns forming, macro photography, vibrant colors",
            "output": "abstract_paint.mp4",
            "aspect_ratio": "9:16",
            "resolution": "720p",
            "duration": "4"
        }
    ]

    print("\nHere are some creative prompt ideas you can try:\n")
    for i, example in enumerate(creative_prompts, 1):
        print(f"{i}. {example['name']}")
        print(f"   Prompt: {example['prompt']}")
        print(f"   Settings: {example['aspect_ratio']} | {example['resolution']} | {example['duration']}s")
        print(f"   Output: {example['output']}\n")

    # Uncomment to generate one of them:
    # choice = creative_prompts[0]  # Generate the first example
    # generator.generate_text_to_video(
    #     prompt=choice['prompt'],
    #     output_path=choice['output'],
    #     aspect_ratio=choice['aspect_ratio'],
    #     resolution=choice['resolution'],
    #     duration=choice['duration']
    # )


def main():
    """
    Run examples (uncomment the ones you want to try)
    """
    print("\n" + "="*70)
    print(" Veo 3.1 Video Generator - Usage Examples")
    print("="*70)

    # Check API key
    if API_KEY == 'your_api_key_here':
        print("\n⚠️  WARNING: Please set your GOOGLE_API_KEY")
        print("Get your API key at: https://aistudio.google.com/apikey")
        print("\nSet it in one of these ways:")
        print("1. Environment variable: export GOOGLE_API_KEY=your_key")
        print("2. Edit this file and replace 'your_api_key_here' with your key")
        print("3. Pass it directly: Veo3VideoGenerator(api_key='your_key')\n")
        return

    # Uncomment the examples you want to run:

    # example_text_to_video_basic()
    # example_text_to_video_advanced()
    # example_image_to_video()
    # example_video_extension()
    example_creative_prompts()  # This just displays ideas, doesn't generate

    print("\n" + "="*70)
    print(" 💡 Tip: Uncomment the examples in main() to generate videos")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
