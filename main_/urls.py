from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("single_page.urls")),
    path("applymain/", include("manage_apply.urls")),
    path('qna/', include('qna.urls')),
    path('dashboard/', include('dashboard.urls')), #20240805
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

