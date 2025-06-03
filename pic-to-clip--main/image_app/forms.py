from django import forms
from .models import ImagePrompt

class ImagePromptForm(forms.ModelForm):
    class Meta:
        model = ImagePrompt
        fields = ['image', 'prompt']
