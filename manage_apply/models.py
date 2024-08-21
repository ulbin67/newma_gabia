from django.db import models
from django.core.validators import RegexValidator
from single_page.models import User

#박스 요청 및 수거 date 틀
class Apply(models.Model):
    #모델 생성 시 오류를 없애기 위해 null=True로 지정 (값이 null이어도 됨, 추후 추가된 칼럼의 경우 자동으로 null값이 생겨서 오류 발생..)

    #신청 시간
    apply_at = models.DateTimeField(auto_now_add=True,null=True)

    #회사 정보
    company = models.CharField(max_length=10,null=True,blank=False)
    com_num = models.CharField(max_length=14,null=True,blank=True)

    #주소
    address_num = models.CharField(max_length=5,null=True,blank=True)
    address_info = models.TextField(null=True,blank=True)
    address_detail = models.TextField(null=True,blank=True)
    deli_request = models.TextField(null=True,blank=True)
    
    #신청자 정보(unique=True로 해서 이미 신청한 사람은 다시 신청 불가하도록 지정, 모든 거래 완료시 제거하여 충돌 제거할 필요가 있음)
    applicant = models.CharField(max_length=10, null=True, blank=False)
    apcan_phone = models.CharField(max_length=14,null=True,blank=False)
   
    #진행상황을 딕셔너리 형태로 저장
    PROGRESS_RATE = (
    	(0, '박스 요청중'),
        (1, '박스 전송중'),
        (2, '박스 수거 요청중'),
        (3, '수거진행중'),
        (4, '송장 입력 전'),
    )

    #진행상황
    progress = models.IntegerField(choices=PROGRESS_RATE, default=0, null=True)

    #박스 수(보내야할 박스수 혹은 받을 박스 수)
    box_num = models.IntegerField(null=True,blank=False)

    sent_box_num = models.IntegerField(null=True,blank=False)

    #송장 번호
    invoice_num = models.TextField(null=True,blank=False)

    ##박스 요청 없이 오는 경우의 연결
    #지르코니아 블록
    zir_block_count = models.IntegerField(null=True, blank=True)

    #지르코니아 분말
    zir_powder_count = models.IntegerField(null=True, blank=True)

    #환봉
    round_bar_count = models.IntegerField(null=True, blank=True)

    #밀링툴
    tool_count = models.IntegerField(null=True, blank=True)

    #개인 요청에 따른 주소를 만드는 함수(관리 페이지를 위해 사용)
    def get_absolute_url(self):
        return f'applymain/{self.pk}/progress_check/'
    
    #삭제 메소드
    def delete(self, *args, **kwargs):
        # 삭제 전 수행할 작업
        print(f"Deleting Apply object: {self.pk}")
        
        # 슈퍼클래스의 delete 메소드를 호출하여 실제 삭제를 수행
        super(Apply, self).delete(*args, **kwargs)

#회사 정보를 저장하기 위한 쿼리! 
class CompanyInfo(models.Model):
    #회사 정보(회사명은 하나만 저장되도록 함.)
    count = models.PositiveIntegerField(default=1,null=True,blank=False)
    company = models.CharField(max_length=10,null=True,blank=False,unique=True)
    com_num = models.CharField(max_length=14,null=True,blank=True)

    #주소
    address_num = models.CharField(max_length=5,null=True,blank=True)
    address_info = models.TextField(null=True,blank=True)
    address_detail = models.TextField(null=True,blank=True)

    #회사 최근 거래자 & 거래 시각 파악
    recent_apply = models.DateTimeField(auto_now = True,null=True)
    recent_employee = models.CharField(max_length=10, null=True, blank=False)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.company

class DoneApply(models.Model):
    #모델 생성 시 오류를 없애기 위해 null=True로 지정 (값이 null이어도 됨, 추후 추가된 칼럼의 경우 자동으로 null값이 생겨서 오류 발생..)

    #회사 정보
    company = models.CharField(max_length=10,null=True,blank=False)
    
    #신청자 정보(unique=True로 해서 이미 신청한 사람은 다시 신청 불가하도록 지정, 모든 거래 완료시 제거하여 충돌 제거할 필요가 있음)
    applicant = models.CharField(max_length=10, null=True, blank=False)
    apcan_phone = models.CharField(max_length=14,null=True,blank=False)

    done_at = models.DateTimeField(auto_now_add=True,null=True)

    box_num = models.IntegerField(null=True,blank=False)


