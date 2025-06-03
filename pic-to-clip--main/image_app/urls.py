from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Assuming urls.py is inside your app folder

urlpatterns = [
    path('', views.home, name='home'),                 # Home page
    path('upload/', views.upload_image, name='upload_image'), # Image upload + video generation
    path('gallery/', views.gallery, name='gallery'),    # Gallery to view images/videos
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
