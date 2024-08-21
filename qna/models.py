from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.



class Post(models.Model):
    postname = models.CharField(max_length=50)
    # 게시글 Post에 이미지 추가
    mainphoto = models.ImageField(blank=True, null=True)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(null=True,blank=True)
    password = models.PositiveBigIntegerField()
    is_faq = models.BooleanField(default=False) #자주 묻는 질문 여부



    # 게시글의 제목
    def __str__(self):
        return self.postname
    
