from django.contrib import admin
from.models import Post
# Register your models here.

# 관리자가 게시글 접근 가능
admin.site.register(Post)