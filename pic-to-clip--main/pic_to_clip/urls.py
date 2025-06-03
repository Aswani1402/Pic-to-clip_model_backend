from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic import RedirectView
from image_app.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image_app/', include('image_app.urls')),
    path('home/', home, name='home'),
    
    # Serve media files in development (DO NOT use in production)
    path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),

    # Redirect root URL to the image gallery
    path('', RedirectView.as_view(url='/image_app/gallery/', permanent=False)),
]

# Add static and media URL configurations in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
