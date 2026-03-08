# Veo 3.1 AI Video Generator

Generate high-quality AI videos using Google's Veo 3.1 model through the Gemini API.

## Features

- **Text-to-Video**: Generate videos from text descriptions
- **Image-to-Video**: Animate static images with motion prompts
- **Video Extension**: Extend existing Veo videos by 7 seconds
- **Customizable Parameters**: Control resolution, aspect ratio, duration
- **Progress Tracking**: Real-time status updates during generation
- **Command-line Interface**: Easy-to-use CLI with multiple options

## Quick Start

### 1. Install Dependencies

```bash
pip install google-genai
```

### 2. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key for the next step

### 3. Set Up Your API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows (Command Prompt)
set GOOGLE_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:GOOGLE_API_KEY="your_api_key_here"

# Linux/Mac
export GOOGLE_API_KEY=your_api_key_here
```

**Option B: Create .env file**
```bash
# Copy the example file
copy .env.veo3.example .env.veo3

# Edit .env.veo3 and add your API key
GOOGLE_API_KEY=your_actual_api_key
```

**Option C: Pass directly in code**
```python
generator = Veo3VideoGenerator(api_key="your_api_key_here")
```

### 4. Generate Your First Video

**Command Line:**
```bash
python veo3_video_generator.py --prompt "A cat playing piano in a jazz club"
```

**Python Code:**
```python
from veo3_video_generator import Veo3VideoGenerator

generator = Veo3VideoGenerator()
generator.generate_text_to_video(
    prompt="A cat playing piano in a jazz club",
    output_path="cat_piano.mp4"
)
```

## Usage Examples

### Text-to-Video (Basic)

```bash
python veo3_video_generator.py --prompt "A sunset over the ocean with waves crashing"
```

### Text-to-Video (Advanced)

```bash
python veo3_video_generator.py \
  --prompt "Professional chef preparing sushi, cinematic lighting" \
  --resolution 1080p \
  --aspect-ratio 9:16 \
  --duration 8 \
  --negative-prompt "blurry, low quality" \
  --output chef_cooking.mp4
```

### Image-to-Video

```bash
python veo3_video_generator.py \
  --mode image-to-video \
  --prompt "Camera zooms in slowly while subject smiles" \
  --image photo.jpg \
  --output animated_photo.mp4
```

### Video Extension

```bash
python veo3_video_generator.py \
  --mode extend \
  --video original_video.mp4 \
  --output extended_video.mp4
```

## Python API

### Initialize Generator

```python
from veo3_video_generator import Veo3VideoGenerator

# Using environment variable
generator = Veo3VideoGenerator()

# Or pass API key directly
generator = Veo3VideoGenerator(api_key="your_key")
```

### Generate Text-to-Video

```python
generator.generate_text_to_video(
    prompt="Your video description here",
    output_path="output.mp4",
    aspect_ratio="16:9",      # "16:9" or "9:16"
    resolution="720p",        # "720p", "1080p", or "4k"
    duration="6",             # "4", "6", or "8" seconds
    negative_prompt="blurry, distorted"
)
```

### Generate Image-to-Video

```python
generator.generate_image_to_video(
    prompt="Camera pans across the scene",
    image_path="input.jpg",
    output_path="output.mp4",
    aspect_ratio="16:9",
    resolution="1080p",
    duration="6"
)
```

### Extend Video

```python
generator.extend_video(
    video_path="previous_output.mp4",
    output_path="extended.mp4"
)
```

## Parameters Reference

### Aspect Ratio
- `16:9` - Landscape (default) - Best for YouTube, websites
- `9:16` - Portrait - Best for TikTok, Instagram Stories, Reels

### Resolution
- `720p` - 1280x720 (default) - Faster, lower cost
- `1080p` - 1920x1080 - High quality, balanced
- `4k` - 3840x2160 - Maximum quality, slower, higher cost

### Duration
- `4` - 4 seconds - Quick clips
- `6` - 6 seconds (default) - Standard length
- `8` - 8 seconds - Longer scenes

### Negative Prompt
Describe what you DON'T want in the video:
- Use descriptive terms: "blurry", "low quality", "distorted"
- Avoid instructional language: Don't say "don't show X", just say "X"
- Examples: "cartoon style, watermark, text overlay"

## Prompt Writing Tips

### Good Prompts
✅ **Be Specific**: "A golden retriever puppy playing with a red ball in a sunny park, slow motion"

✅ **Include Camera Movement**: "Aerial drone shot flying over mountains at sunrise"

✅ **Describe Lighting**: "Studio lighting with dramatic shadows"

✅ **Set the Scene**: "In a modern minimalist kitchen with white marble countertops"

### Avoid
❌ Too vague: "A dog"
❌ Multiple scenes: "A dog playing, then eating, then sleeping"
❌ Impossible physics: "Dog flying through space without a spacesuit"

### Example Prompts

**Cinematic**
```
"Aerial drone shot flying over a misty mountain range at golden hour, cinematic colors, sweeping camera movement"
```

**Product Showcase**
```
"Luxury watch rotating on a black velvet surface, studio lighting, reflections visible on glass, elegant presentation"
```

**Nature**
```
"Close-up of a hummingbird hovering near a red flower, wings moving in slow motion, shallow depth of field"
```

**Abstract**
```
"Colorful acrylic paint mixing in water, abstract patterns forming, macro photography, vibrant colors"
```

## Cost & Limits

- **Generation Time**: 2-10 minutes depending on resolution and duration
- **API Costs**: Varies by resolution and duration (check Google's pricing)
- **Rate Limits**: Check your Google Cloud project quotas
- **File Size**: Videos range from 5-50MB depending on settings

## Troubleshooting

### "API key required" Error
Make sure you've set your GOOGLE_API_KEY environment variable or passed it directly:
```python
generator = Veo3VideoGenerator(api_key="your_key")
```

### Generation Taking Too Long
- Lower resolution (use 720p instead of 1080p/4k)
- Shorter duration (use 4s instead of 6s/8s)
- Check Google Cloud status page for API issues

### Poor Quality Output
- Use more descriptive prompts
- Specify camera angles and lighting
- Add negative prompts to avoid unwanted elements
- Try higher resolution (1080p or 4k)

### File Not Found Errors
- Use absolute paths for input files
- Check file paths use correct slashes for your OS
- Ensure input files exist before running

## Advanced Features

### Batch Generation

```python
prompts = [
    "A sunset over mountains",
    "A cat playing with yarn",
    "Rain falling on city streets"
]

generator = Veo3VideoGenerator()

for i, prompt in enumerate(prompts):
    print(f"\nGenerating video {i+1}/{len(prompts)}")
    generator.generate_text_to_video(
        prompt=prompt,
        output_path=f"video_{i+1}.mp4"
    )
```

### Custom Poll Interval

```python
# Check status every 5 seconds instead of 10
generator.generate_text_to_video(
    prompt="Your prompt here",
    poll_interval=5  # Faster updates, more API calls
)
```

### Error Handling

```python
try:
    generator.generate_text_to_video(
        prompt="Your prompt here",
        output_path="output.mp4"
    )
except Exception as e:
    print(f"Error generating video: {e}")
```

## Files Included

- `veo3_video_generator.py` - Main script with Veo3VideoGenerator class
- `veo3_example.py` - Example usage demonstrations
- `.env.veo3.example` - Example environment configuration
- `VEO3_README.md` - This documentation file

## Resources

- [Google AI Studio](https://aistudio.google.com/apikey) - Get API key
- [Veo 3.1 Documentation](https://ai.google.dev/gemini-api/docs/video) - Official docs
- [Google Cloud Console](https://console.cloud.google.com/) - Manage quotas & billing

## Support

For issues with:
- **This script**: Check the troubleshooting section above
- **Veo 3.1 API**: Visit Google's official documentation
- **API access/billing**: Contact Google Cloud support

## License

This script is provided as-is for use with Google's Veo 3.1 API. Please comply with Google's terms of service and usage policies.

---

**Happy video creating! 🎬✨**
