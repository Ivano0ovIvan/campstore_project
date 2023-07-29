from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('campstore.user_profile.urls')),
    path('', include('campstore.store.urls')),
    path('', include('campstore.core.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'campstore.core.views.page_not_found'
