from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint
from model_utils.models import TimeStampedModel
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
import datetime
from django.utils import timezone
from django.conf import settings

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
    phone_num = models.CharField(max_length=14, verbose_name='휴대폰 번호')

class Authsms(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(null=True, verbose_name='인증 번호')
    is_phone_verified = models.BooleanField(default=False)
    class Meta:
        db_table = 'auth_sms'

    def save(self, *args, **kwargs):
        send_sms = kwargs.pop('send_sms', True)
        if not self.auth_number:  # 인증번호가 없을 경우 새로 발급
            self.auth_number = randint(100000, 999999)

        super().save(*args, **kwargs)

        if send_sms and self.auth_number:
            self.send_sms()

    def send_sms(self):

        api_key = settings.COOL_SMS_API
        api_secret = settings.COOL_SMS_SECRET

        print(f"Sending SMS with auth_number: {self.auth_number}")

        data = {
            'to': self.phone_number,
            'from': '01098012501',
            'text': '[뉴마] 인증 번호 [{}]를 입력해주세요.'.format(self.auth_number)
        }
        cool = Message(api_key, api_secret)

        try:
            response = cool.send(data)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

    @classmethod
    def request_auth_number(cls, p_num):
        # 기존 인증 번호가 있으면 무효화
        authsms, created = cls.objects.get_or_create(phone_number=p_num)
        if not created:  # 이미 객체가 존재하는 경우
            authsms.auth_number = randint(100000, 999999)
            authsms.save(send_sms=True)  # 인증번호 갱신 후 SMS 전송
        return authsms

    @classmethod
    def check_auth_number(cls, p_num, c_num):
        time_limit = timezone.now() - datetime.timedelta(minutes=5)
        result = cls.objects.filter(
            phone_number=p_num,
            auth_number=c_num,
            modified__gte=time_limit
        ).first()
        if result:
            result.is_phone_verified = True
            result.save(send_sms=False)
            return True
        return False