from gradio_client import Client, handle_file

def generate_video_from_input(image_path: str, prompt: str) -> str:
    client = Client("multimodalart/wan2-1-fast")
    
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

    video_output_path = result[0]["video"]
    return video_output_path
