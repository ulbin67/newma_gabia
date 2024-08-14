from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.\

#기본 유저 정의
class User(AbstractUser):
    id = models.AutoField(primary_key=True, db_column='user_id')
    username = models.CharField(max_length=30, unique=True, verbose_name='아이디')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    name = models.CharField(max_length=50, verbose_name='이름')
    email = models.EmailField(null=False, blank=False, verbose_name='이메일 주소')
    company_name = models.CharField(max_length=50, verbose_name='회사명')
    address_num = models.CharField(max_length=5, verbose_name='우편번호')
    address_info = models.TextField(verbose_name='도로명 주소')
    address_detail = models.TextField(verbose_name='상세주소')
    deli_request = models.TextField(null=True,blank=True, verbose_name='세부사항')
    phone_telecom = models.CharField(max_length=10, verbose_name='통신사')
    phone_num = models.CharField(max_length=14, verbose_name='휴대폰 번호')


