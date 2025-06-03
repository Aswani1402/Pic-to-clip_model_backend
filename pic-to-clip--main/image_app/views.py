import os
import shutil
import requests
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from .models import ImagePrompt
from .forms import ImagePromptForm
from model.generate_video import generate_video_from_input  # Your model function

# Optional helper for long filenames
def handle_uploaded_file(f):
    max_length = 100
    filename = f.name
    if len(filename) > max_length:
        base, ext = os.path.splitext(filename)
        base = base[:max_length - len(ext)]
        filename = base + ext
    f.name = filename
    return f


def upload_image(request):
    """
    Handles image upload, runs video generation using a prompt,
    and saves both the image and generated video.
    """
    if request.method == 'POST':
        form = ImagePromptForm(request.POST, request.FILES)
        if form.is_valid():
            image_prompt = form.save(commit=False)

            # Handle long file names
            image_prompt.image = handle_uploaded_file(request.FILES['image'])
            image_prompt.save()

            image_path = image_prompt.image.path
            prompt = image_prompt.prompt

            try:
                # Generate video using external model
                video_path = generate_video_from_input(image_path, prompt)

                # Ensure video was downloaded and exists locally
                if os.path.exists(video_path):
                    image_prompt.video_path = video_path
                    image_prompt.save()
                    messages.success(request, "✅ Image uploaded and video generated successfully!")
                else:
                    messages.error(request, "❌ Video generation failed. File not found.")
            except Exception as e:
                messages.error(request, f"❌ Error during video generation: {str(e)}")

            return redirect(reverse_lazy('gallery'))
        else:
            messages.error(request, "❌ Failed to upload image. Please check the form.")
    else:
        form = ImagePromptForm()

    return render(request, 'image_app/upload.html', {'form': form})


def gallery(request):
    """
    Shows uploaded images and their corresponding generated videos.
    """
    images = ImagePrompt.objects.all().order_by('-created_at')
    return render(request, 'image_app/gallery.html', {'images': images})


def home(request):
    """
    Displays the home page.
    """
    return render(request, 'home.html')
