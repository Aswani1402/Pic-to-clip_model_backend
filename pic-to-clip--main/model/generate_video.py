import os
import shutil
import requests
from gradio_client import Client, handle_file

def generate_video_from_input(image_path: str, prompt: str) -> str:
    """
    Generates a video from an image and prompt using the multimodalart API and saves it locally.
    Returns the local path to the downloaded video.
    """
    client = Client("THUDM/CogVideoX-5B-Space")

    # Call the model
    result = client.predict(
        input_image=handle_file(image_path),
        prompt=prompt,
        height=512,
        width=896,
        negative_prompt=(
            "Bright tones, overexposed, static, blurred details, subtitles, style, works, paintings, images, "
            "static, overall gray, worst quality, low quality, JPEG compression residue, ugly, incomplete, extra fingers, "
            "poorly drawn hands, poorly drawn faces, deformed, disfigured, misshapen limbs, fused fingers, still picture, "
            "messy background, three legs, many people in the background, walking backwards, watermark, text, signature"
        ),
        duration_seconds=2,
        guidance_scale=1,
        steps=4,
        seed=42,
        randomize_seed=True,
        api_name="/generate_video"
    )

    # Extract the video URL
    video_url = result[0]["video"]
    print(f"[INFO] Video URL from API: {video_url}")

    # Set up local path
    video_name = os.path.basename(video_url)
    local_video_dir = os.path.join("media", "videos")
    os.makedirs(local_video_dir, exist_ok=True)
    local_video_path = os.path.join(local_video_dir, video_name)

    # Download video from URL
    try:
        with requests.get(video_url, stream=True) as response:
            response.raise_for_status()
            with open(local_video_path, "wb") as f:
                shutil.copyfileobj(response.raw, f)
        print(f"[INFO] Video saved to: {local_video_path}")
    except Exception as e:
        print(f"[ERROR] Failed to download video: {e}")
        raise

    return local_video_path
