from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from .models import User, Authsms
from django.core.exceptions import ValidationError
import re

# 기본 사용자 생성 폼을 확장한 커스텀 사용자 생성 폼
class CustomUserCreationForm(UserCreationForm):
    phone_part1 = forms.CharField(max_length=3, required=True, label='휴대폰 번호')
    phone_part2 = forms.CharField(max_length=4, required=False)
    phone_part3 = forms.CharField(max_length=4, required=False)

    class Meta(UserCreationForm.Meta):
        # 커스텀 User 모델 사용
        model = User
        # 폼에 포함할 필드들
        fields = ('username', 'password1', 'password2', 'name', 'address_num',
                  'address_info', 'address_detail', 'deli_request', 'company_name', 'email')

        # 특정 필드의 외관을 커스터마이징하기 위해 위젯 정의
        widgets = {
            'address_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'address_detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'deli_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }

    # 저장 메서드를 재정의하여 전화번호 부분을 하나의 필드로 결합
    def save(self, commit=True):
        user = super().save(commit=False)
        # 전화번호 부분을 하나의 문자열로 결합
        phone_num = f"{self.cleaned_data['phone_part1']}-{self.cleaned_data['phone_part2']}-{self.cleaned_data['phone_part3']}"
        # 결합된 전화번호를 사용자 인스턴스에 할당
        user.phone_num = phone_num
        if commit:
            # 사용자 인스턴스를 데이터베이스에 저장
            user.save()
        return user

    # 오류 메세지 출력을 개선하기 위한 함수
    def get_error_messages(self):
        error_messages = []
        for field, errors in self.errors.items():
            field_verbose_name = self.fields[field].label or field
            for error in errors:
                error_messages.append(f"[{field_verbose_name}]\n{error}")
        return error_messages

    def custom_error(self):
        return '\n'.join(self.get_error_messages())

#  아이디 중복여부 확인 유효성검사 폼
class CheckForm(forms.Form):
    check_id = forms.CharField(label='아이디 확인', max_length=20, required=True)

    def clean(self):
        cleaned_data = super().clean()
        check_id = cleaned_data.get('check_id')
        if check_id is None:
            self.add_error('check_id', '아이디를 입력해주세요')
        else:
            check_id = check_id.strip()
            if not check_id:
                self.add_error('check_id', '아이디를 입력해주세요')
            else:
                p = re.compile("^[a-zA-Z][a-zA-Z0-9]{5,19}$")                  # 아이디 유효성 검사
                if not p.match(check_id):
                    self.add_error('check_id', '6~20자 이내 영문자와 숫자로 작성해 주세요(첫 글자는 영문자)')


class SearchIdForm(forms.Form):
    search_name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)

class PasswordResetForm(forms.Form):
    user_name = forms.CharField(required=True, label='이름')
    user_username = forms.CharField(required=True, label='아이디')
    user_email = forms.CharField(required=True, label='이메일 주소')

# 마이페이지 비밀번호 변경 폼
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        label='기존 비밀번호'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput,
        label='비밀번호'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='비밀번호 확인'
    )

    def clean(self):
        cleaned_data = super().clean()
        old_psw = cleaned_data.get('old_password')
        new_psw1 = cleaned_data.get('new_password1')

        if old_psw == new_psw1:
            self.add_error('old_password', '기존 비밀번호와 같습니다.')

        if new_psw1 and re.search('\s', new_psw1):
            self.add_error('new_password1', '비밀번호에 공백이 포함되어 있습니다.')

        return cleaned_data


class Confirm_infoForm(forms.Form):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("confirm_password")

        if not self.user.check_password(current_password):
            raise ValidationError("비밀번호 불일치")

        return cleaned_data


class UpdateMyInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'company_name', 'name', 'email', 'address_num', 'address_info', 'address_detail',
                  'deli_request', 'phone_num']

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='새 비밀번호')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='비밀번호 확인')
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")

        if new_password1 and re.search('\s', new_password1):
            self.add_error('new_password1', '비밀번호에 공백이 포함되어 있습니다.')

        return cleaned_data

