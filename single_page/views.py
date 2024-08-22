from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, FormView, UpdateView, DeleteView  # 제너릭 뷰 상속(장고 기본 제공)
from django.views import View
from django.contrib.auth.views import (PasswordChangeView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)  # 패스워드 변경 및 재설정 뷰(장고 기본 제공)
from .forms import (CustomUserCreationForm, CheckForm, SearchIdForm,
                    PasswordResetForm, Confirm_infoForm, UpdateMyInfoForm, CustomPasswordChangeForm, UserSetPasswordForm)  # 작성한 폼 가져오기
from django.urls import reverse_lazy
from .models import User, Authsms
from django.contrib.auth.mixins import LoginRequiredMixin  # 로그인된 사용자만 접근 가능
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from django.db.models import Value
from django.db.models.functions import Replace
import re

# 메인 화면 및 로그인을 수행하는 View
def maincall(request):
    return render(request, 'single_page/main.html')

# 사이트 소개 페이지 호출
def introcall(request):
    return render(
        request,
        'single_page/introduce.html'
    )

# 정보 페이지 호출
def infocall(request):
    return render(
        request,
        'single_page/information.html'
    )

# 서비스 약관 페이지를 표시하는 뷰
class rule(TemplateView):
    template_name = 'single_page/rule.html'

# 회원가입 기능을 담당하는 View
class UserCreateView(CreateView):  # 새로운 레코드 생성을 위해 CreateView 상속
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')  # 회원가입 성공 시 이동할 페이지 설정

    # 폼에서 유효성 검사를 만족하지 못한 경우 처리
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.context_data['errors'] = form.custom_error()  # 커스텀 에러 메시지를 전달
        return response

# 회원가입 성공 후 보여줄 페이지 View
class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

# 아이디 중복체크를 위한 View
class UserIdCheckView(FormView):
    form_class = CheckForm
    template_name = 'registration/check_id.html'

    # GET 요청 시 기본 컨텍스트 설정
    def get(self, request, *args, **kwargs):
        context = {
            'username': '',
            'is_taken': -1,  # 초기 상태: 아이디 사용 여부 미확인
        }
        return render(self.request, self.template_name, context=context)

    # POST 요청 시 아이디 중복 체크 수행
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            check_id = form.cleaned_data['check_id']
            is_taken = User.objects.filter(username=check_id).exists()  # 아이디 중복 여부 확인
            context = {
                'username': check_id,
                'is_taken': is_taken,
            }
        else:
            context = {
                'form': form,
                'is_taken': -1,
            }
        return render(self.request, self.template_name, context=context)

# 첫 번째 인증 단계 View
class VerifyFirstView(View):
    template_name = 'registration/verify_first.html'

    # GET 요청 시 휴대폰 번호 입력 양식 표시
    def get(self, request):
        phone_number = request.GET.get('phone_number')
        return render(request, self.template_name, {'phone_number': phone_number})

    # POST 요청 시 입력된 휴대폰 번호 유효성 검사 및 인증 번호 요청
    def post(self, request):
        p_num = request.POST.get('phone_number')
        phone_regex = re.compile(r'^010\d{8}$')  # 한국 휴대폰 번호 정규식

        if not phone_regex.match(p_num):  # 휴대폰 번호 유효성 검사
            return render(request, self.template_name, {'message': '휴대폰 번호를 확인해 주세요', 'phone_number': p_num})

        normalized_p_num = p_num.replace("-", "")  # 번호 형식을 표준화
        if User.objects.annotate(
            normalized_phone_num=Replace('phone_num', Value('-'), Value(''))
        ).filter(normalized_phone_num=normalized_p_num).exists():  # 이미 존재하는 번호인지 확인
            return render(request, self.template_name, {'message': '이미 존재하는 번호 입니다', 'phone_number': p_num})

        authsms = Authsms.request_auth_number(p_num)  # 인증 번호 요청
        return render(request, 'registration/verify_phone.html', {'phone_number': p_num})

# 인증 번호 입력 View
class VerifyPhoneView(View):
    template_name = 'registration/verify_phone.html'

    # POST 요청 시 인증 번호 확인 또는 재전송 처리
    def post(self, request):
        action = request.POST.get('action')
        p_num = request.POST.get('phone_number')
        phone_regex = re.compile(r'^010\d{8}$')

        if action == 'resend':  # 인증 번호 재전송 처리
            if phone_regex.match(p_num):
                Authsms.request_auth_number(p_num)  # 인증 번호 재발급 및 SMS 전송
                message = '인증 번호가 재발송되었습니다.'
            else:
                message = '올바른 전화번호를 입력해 주세요.'

        elif action == 'confirm':  # 인증 번호 확인 처리
            a_num = request.POST.get('auth_number')
            if not phone_regex.match(p_num):
                message = '올바른 전화번호를 입력해 주세요.'

            elif not a_num:
                message = '인증문자를 입력해 주세요.'

            else:
                result = Authsms.check_auth_number(p_num, a_num)  # 인증 번호 확인
                if result:
                    message = 'success'
                else:
                    message = '인증 번호가 유효하지 않습니다.'
        else:
            message = '폼 제출 오류가 발생했습니다.'

        return render(request, self.template_name, {'phone_number': p_num, 'message': message})

# 아이디 찾기 기능을 제공하는 View
class SearchIdView(FormView):
    template_name = 'registration/search_id.html'
    form_class = SearchIdForm

    # 유효한 폼 처리 시 사용자 정보 검색
    def form_valid(self, form):
        user_name = form.cleaned_data.get('search_name')
        user_email = form.cleaned_data.get('email_address')

        user_info = User.objects.filter(name=user_name, email=user_email)

        if user_info.exists():
            return render(self.request, 'registration/search_id_done.html', {'user_info': user_info})
        else:
            form.add_error(None, '일치하는 정보가 없습니다. 입력을 다시 확인해 주세요.')
            return self.form_invalid(form)

    # 폼 입력 값이 유효하지 않은 경우 처리
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# 아이디 찾기 완료 페이지 View
class SearchIdDoneTV(TemplateView):
    template_name = 'registration/search_id_done.html'

# 비밀번호 재설정 요청 View
class UserPasswordResetView(FormView):
    template_name = 'registration/reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    # 유효한 폼 처리 시 비밀번호 재설정 이메일 전송
    def form_valid(self, form):
        user_name = form.cleaned_data['user_name']
        user_username = form.cleaned_data['user_username']
        user_email = form.cleaned_data['user_email']

        user_info = User.objects.filter(name=user_name, username=user_username, email=user_email)

        if user_info.exists():
            for user in user_info:
                # 이메일 제목 및 본문 생성
                subject = '[주식회사 뉴마] 비밀번호 재설정 요청'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                link = self.request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )

                context = {
                    'user': user,
                    'uid': uid,
                    'token': token,
                    'link': link,
                }

                # 이메일 전송
                html_message = render_to_string('registration/password_email.html', context)
                plain_message = strip_tags(html_message)

                email = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    'lka111617@gmail.com',
                    [user.email],
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)

            return super().form_valid(form)
        else:
            form.add_error(None, '일치하는 정보가 없습니다. 입력을 다시 확인해 주세요.')
            return self.render_to_response(self.get_context_data(form=form))

# 비밀번호 재설정 요청 완료 페이지 View
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/email_send_done.html'

# 비밀번호 재설정 확인 페이지 View
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = UserSetPasswordForm
    invalid_template_name = 'registration/password_reset_invalid.html'

    # 유효한 폼 처리
    def form_valid(self, form):
        return super().form_valid(form)

    # 폼 입력 값이 유효하지 않은 경우 처리
    def form_invalid(self, form):
        return super().form_invalid(form)

# 비밀번호 재설정 완료 페이지 View
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/reset_success.html'

# 마이페이지 접근을 위한 View
class MyPageView(LoginRequiredMixin, FormView):
    template_name = 'my_page/my_page.html'
    form_class = Confirm_infoForm

    # 폼에 현재 로그인된 사용자 정보를 전달
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # 유효한 폼 처리 시 마이페이지로 리다이렉트
    def form_valid(self, form):
        form_name = self.request.POST.get('form_name', '')
        if form_name == 'info':
            return redirect(reverse_lazy('update_info', kwargs={'pk': self.request.user.pk}))
        elif form_name == 'psw':
            return redirect(reverse_lazy('change_psw'))
        return super().form_valid(form)

# 사용자 정보 수정 View
class UpdateMyInfoView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'my_page/update_info.html'
    form_class = UpdateMyInfoForm

    # 정보 수정 후 성공 페이지 URL 설정
    def get_success_url(self):
        return reverse_lazy('my_page')

# 비밀번호 변경 View
class ChangePswView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'my_page/change_psw.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('my_page')

# 회원 탈퇴 전 확인 페이지 View
class DeleteBefore(LoginRequiredMixin, FormView):
    template_name = 'my_page/delete_before.html'
    form_class = Confirm_infoForm

    # 폼에 현재 로그인된 사용자 정보를 전달
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # 유효한 폼 처리 시 탈퇴 페이지로 리다이렉트
    def form_valid(self, form):
        return redirect(reverse_lazy('delete_info', kwargs={'pk': self.request.user.pk}))

# 회원 탈퇴 View
class DeleteMyInfoView(LoginRequiredMixin, DeleteView):
    template_name = 'my_page/delete_info.html'
    model = User
    success_url = reverse_lazy('login')

    # 회원 탈퇴 처리 및 로그아웃
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.user.is_authenticated:
            logout(request)
        return response
