"""
Veo 3.1 AI Video Generation Script
Integrates with Google's Gemini API to generate videos using Veo 3.1

Setup:
1. Install: pip install google-genai
2. Get API key: https://aistudio.google.com/apikey
3. Set environment variable: GOOGLE_API_KEY=your_key_here
"""

import os
import time
import argparse
from pathlib import Path
from google import genai
from google.genai import types


class Veo3VideoGenerator:
    """
    Wrapper class for Google's Veo 3.1 video generation API
    """

    def __init__(self, api_key=None):
        """
        Initialize the Veo3 client

        Args:
            api_key (str, optional): Google API key. If not provided, reads from GOOGLE_API_KEY env variable
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')

        if not self.api_key:
            raise ValueError(
                "API key required. Either pass it as argument or set GOOGLE_API_KEY environment variable.\n"
                "Get your API key at: https://aistudio.google.com/apikey"
            )

        # Initialize the client with API key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "veo-3.1-generate-preview"

    def generate_text_to_video(
        self,
        prompt: str,
        output_path: str = "output.mp4",
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        duration: str = "6",
        negative_prompt: str = None,
        poll_interval: int = 10
    ):
        """
        Generate video from text prompt

        Args:
            prompt (str): Description of the video to generate
            output_path (str): Path where to save the generated video
            aspect_ratio (str): "16:9" (landscape) or "9:16" (portrait)
            resolution (str): "720p", "1080p", or "4k"
            duration (str): "4", "6", or "8" seconds
            negative_prompt (str): Elements to avoid in the video
            poll_interval (int): Seconds between status checks

        Returns:
            str: Path to the generated video file
        """
        print(f"\n{'='*60}")
        print("Veo 3.1 Video Generation - Text to Video")
        print(f"{'='*60}")
        print(f"Prompt: {prompt}")
        print(f"Configuration:")
        print(f"  - Aspect Ratio: {aspect_ratio}")
        print(f"  - Resolution: {resolution}")
        print(f"  - Duration: {duration}s")
        if negative_prompt:
            print(f"  - Negative Prompt: {negative_prompt}")
        print(f"{'='*60}\n")

        # Build configuration
        config = types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration=duration
        )

        if negative_prompt:
            config.negative_prompt = negative_prompt

        # Start video generation
        print("Starting video generation...")
        operation = self.client.models.generate_videos(
            model=self.model,
            prompt=prompt,
            config=config
        )

        # Poll for completion
        start_time = time.time()
        while not operation.done:
            elapsed = int(time.time() - start_time)
            print(f"⏳ Generation in progress... ({elapsed}s elapsed)")
            time.sleep(poll_interval)
            operation = self.client.operations.get(operation)

        elapsed_total = int(time.time() - start_time)
        print(f"\n✅ Video generation completed in {elapsed_total}s!")

        # Download the video
        print(f"Downloading video to: {output_path}")
        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video, path=output_path)

        print(f"✅ Video saved successfully: {output_path}")
        return output_path

    def generate_image_to_video(
        self,
        prompt: str,
        image_path: str,
        output_path: str = "output.mp4",
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        duration: str = "6",
        negative_prompt: str = None,
        poll_interval: int = 10
    ):
        """
        Generate video from image with text prompt

        Args:
            prompt (str): Description of the video motion/action
            image_path (str): Path to the input image
            output_path (str): Path where to save the generated video
            aspect_ratio (str): "16:9" (landscape) or "9:16" (portrait)
            resolution (str): "720p", "1080p", or "4k"
            duration (str): "4", "6", or "8" seconds
            negative_prompt (str): Elements to avoid in the video
            poll_interval (int): Seconds between status checks

        Returns:
            str: Path to the generated video file
        """
        print(f"\n{'='*60}")
        print("Veo 3.1 Video Generation - Image to Video")
        print(f"{'='*60}")
        print(f"Input Image: {image_path}")
        print(f"Prompt: {prompt}")
        print(f"Configuration:")
        print(f"  - Aspect Ratio: {aspect_ratio}")
        print(f"  - Resolution: {resolution}")
        print(f"  - Duration: {duration}s")
        if negative_prompt:
            print(f"  - Negative Prompt: {negative_prompt}")
        print(f"{'='*60}\n")

        # Upload the image
        print("Uploading image...")
        uploaded_image = self.client.files.upload(path=image_path)

        # Build configuration
        config = types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration=duration
        )

        if negative_prompt:
            config.negative_prompt = negative_prompt

        # Start video generation with image
        print("Starting video generation...")
        operation = self.client.models.generate_videos(
            model=self.model,
            prompt=prompt,
            image=uploaded_image,
            config=config
        )

        # Poll for completion
        start_time = time.time()
        while not operation.done:
            elapsed = int(time.time() - start_time)
            print(f"⏳ Generation in progress... ({elapsed}s elapsed)")
            time.sleep(poll_interval)
            operation = self.client.operations.get(operation)

        elapsed_total = int(time.time() - start_time)
        print(f"\n✅ Video generation completed in {elapsed_total}s!")

        # Download the video
        print(f"Downloading video to: {output_path}")
        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video, path=output_path)

        print(f"✅ Video saved successfully: {output_path}")
        return output_path

    def extend_video(
        self,
        video_path: str,
        output_path: str = "extended_output.mp4",
        poll_interval: int = 10
    ):
        """
        Extend a Veo-generated video by 7 seconds

        Args:
            video_path (str): Path to the existing Veo-generated video
            output_path (str): Path where to save the extended video
            poll_interval (int): Seconds between status checks

        Returns:
            str: Path to the extended video file
        """
        print(f"\n{'='*60}")
        print("Veo 3.1 Video Extension")
        print(f"{'='*60}")
        print(f"Input Video: {video_path}")
        print(f"Extension: +7 seconds")
        print(f"{'='*60}\n")

        # Upload the video
        print("Uploading video...")
        uploaded_video = self.client.files.upload(path=video_path)

        # Start video extension
        print("Starting video extension...")
        operation = self.client.models.generate_videos(
            model=self.model,
            video=uploaded_video
        )

        # Poll for completion
        start_time = time.time()
        while not operation.done:
            elapsed = int(time.time() - start_time)
            print(f"⏳ Extension in progress... ({elapsed}s elapsed)")
            time.sleep(poll_interval)
            operation = self.client.operations.get(operation)

        elapsed_total = int(time.time() - start_time)
        print(f"\n✅ Video extension completed in {elapsed_total}s!")

        # Download the extended video
        print(f"Downloading extended video to: {output_path}")
        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video, path=output_path)

        print(f"✅ Extended video saved successfully: {output_path}")
        return output_path


def main():
    """
    Command-line interface for Veo3 video generation
    """
    parser = argparse.ArgumentParser(
        description="Generate videos using Google's Veo 3.1 AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to video (basic)
  python veo3_video_generator.py --prompt "A dog playing in a park"

  # Text to video (advanced)
  python veo3_video_generator.py --prompt "A sunset over mountains" --resolution 1080p --aspect-ratio 16:9 --duration 8

  # Image to video
  python veo3_video_generator.py --mode image-to-video --prompt "Camera pans across the scene" --image input.jpg

  # Extend video
  python veo3_video_generator.py --mode extend --video previous_output.mp4
        """
    )

    parser.add_argument(
        '--mode',
        choices=['text-to-video', 'image-to-video', 'extend'],
        default='text-to-video',
        help='Generation mode (default: text-to-video)'
    )

    parser.add_argument(
        '--prompt',
        type=str,
        help='Text description of the video to generate'
    )

    parser.add_argument(
        '--image',
        type=str,
        help='Path to input image (for image-to-video mode)'
    )

    parser.add_argument(
        '--video',
        type=str,
        help='Path to input video (for extend mode)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='output.mp4',
        help='Output video file path (default: output.mp4)'
    )

    parser.add_argument(
        '--aspect-ratio',
        choices=['16:9', '9:16'],
        default='16:9',
        help='Video aspect ratio (default: 16:9)'
    )

    parser.add_argument(
        '--resolution',
        choices=['720p', '1080p', '4k'],
        default='720p',
        help='Video resolution (default: 720p)'
    )

    parser.add_argument(
        '--duration',
        choices=['4', '6', '8'],
        default='6',
        help='Video duration in seconds (default: 6)'
    )

    parser.add_argument(
        '--negative-prompt',
        type=str,
        help='Elements to avoid in the video'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Google API key (or set GOOGLE_API_KEY env variable)'
    )

    args = parser.parse_args()

    try:
        # Initialize generator
        generator = Veo3VideoGenerator(api_key=args.api_key)

        # Execute based on mode
        if args.mode == 'text-to-video':
            if not args.prompt:
                parser.error("--prompt is required for text-to-video mode")

            generator.generate_text_to_video(
                prompt=args.prompt,
                output_path=args.output,
                aspect_ratio=args.aspect_ratio,
                resolution=args.resolution,
                duration=args.duration,
                negative_prompt=args.negative_prompt
            )

        elif args.mode == 'image-to-video':
            if not args.prompt:
                parser.error("--prompt is required for image-to-video mode")
            if not args.image:
                parser.error("--image is required for image-to-video mode")

            generator.generate_image_to_video(
                prompt=args.prompt,
                image_path=args.image,
                output_path=args.output,
                aspect_ratio=args.aspect_ratio,
                resolution=args.resolution,
                duration=args.duration,
                negative_prompt=args.negative_prompt
            )

        elif args.mode == 'extend':
            if not args.video:
                parser.error("--video is required for extend mode")

            generator.extend_video(
                video_path=args.video,
                output_path=args.output
            )

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
