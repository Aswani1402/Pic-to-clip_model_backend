from django.db import models

class ImagePrompt(models.Model):
    image = models.ImageField(upload_to='images/')
    prompt = models.TextField()
    video_path = models.FileField(upload_to='videos/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt: {self.prompt[:30]}..."
