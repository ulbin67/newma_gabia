from django.urls import path
from django.contrib import admin
from . import views
# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings

app_name='qna'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.blog, name='blog'),
    #path('password/<int:pk>/', views.posting, name="posting"),
    path('password/<int:pk>/', views.password, name="password"),
    path('new_post/', views.new_post),
    path('<int:pk>/remove/', views.remove_post, name='remove'),
    # path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
