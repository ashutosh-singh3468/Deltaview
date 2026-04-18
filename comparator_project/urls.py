from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from comparator_app.views import compare_documents

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', compare_documents, name='compare_documents'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
