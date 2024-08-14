from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, FormView, UpdateView, DeleteView             # 제너릭 뷰 상속(장고 기본 제공)
from django.contrib.auth.views import (PasswordChangeView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)  # 패스워드 변경 뷰(장고 기본 제공)
from .forms import (CustomUserCreationForm, CheckForm, SearchIdForm,
                    PasswordResetForm, Confirm_infoForm, UpdateMyInfoForm, CustomPasswordChangeForm, UserSetPasswordForm)     # 작성한 폼 가져오기
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin   # 로그인된 사용자만 접근 가능
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout

# 메인 화면 및 로그인을 수행하는 View
def maincall(request):
    return render(request, 'single_page/main.html')

def introcall(request):
    return render(
        request,
        'single_page/introduce.html'
    )

def infocall(request):
    return render(
        request,
        'single_page/information.html'
    )

# 회원가입
class UserCreateView(CreateView):                   # 새로운 레코드 생성을 위해 CreateView 상속
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')     # 폼에 에러가 없고 테이블 생성이 완료된 경우 회원가입 성공 페이지로 이동

    # 폼에서 유효성 검사를 만족하지 못한 경우
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.context_data['errors'] = form.custom_error()
        return response

# 회원가입 성공시 사용
class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

# 아이디 중복체크
class UserIdCheckView(FormView):
    form_class = CheckForm
    template_name = 'registration/check_id.html'

    # 아이디 중복 체크 진행 함수
    def get(self, request, *args, **kwargs):
        context = {
            'username': '',
            'is_taken': -1,
        }
        return render(self.request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            check_id = form.cleaned_data['check_id']
            is_taken = User.objects.filter(username=check_id).exists()
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

class SearchIdView(FormView):
    template_name = 'registration/search_id.html'
    form_class = SearchIdForm

    def form_valid(self, form):
        user_name = form.cleaned_data.get('search_name')
        user_email = form.cleaned_data.get('email_address')

        user_info = User.objects.filter(name=user_name, email=user_email)

        if user_info.exists():
            return render(self.request, 'registration/search_id_done.html', {'user_info': user_info})
        else:
            form.add_error(None, '일치하는 정보가 없습니다. 입력을 다시 확인해 주세요.')
            return self.form_invalid(form)

    # form의 입력 값을 유지시키는 함수
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class SearchIdDoneTV(TemplateView):
    template_name = 'registration/search_id_done.html'

class UserPasswordResetView(FormView):
    template_name = 'registration/reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        user_name = form.cleaned_data['user_name']
        user_username = form.cleaned_data['user_username']
        user_email = form.cleaned_data['user_email']

        user_info = User.objects.filter(name=user_name, username=user_username, email=user_email)

        if user_info.exists():
            for user in user_info:
                # Create email subject and body
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
                    'link' : link,
                }

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

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/email_send_done.html'

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = UserSetPasswordForm
    invalid_template_name = 'registration/password_reset_invalid.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/reset_success.html'

class MyPageView(LoginRequiredMixin, FormView):
    template_name = 'my_page/my_page.html'
    form_class = Confirm_infoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form_name = self.request.POST.get('form_name', '')
        if form_name == 'info':
            return redirect(reverse_lazy('update_info', kwargs={'pk': self.request.user.pk}))
        elif form_name == 'psw':
            return redirect(reverse_lazy('change_psw'))
        return super().form_valid(form)


class UpdateMyInfoView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'my_page/update_info.html'
    form_class = UpdateMyInfoForm
    def get_success_url(self):
        return reverse_lazy('my_page')

class ChangePswView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'my_page/change_psw.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('my_page')


class DeleteBefore(LoginRequiredMixin, FormView):
    template_name = 'my_page/delete_before.html'
    form_class = Confirm_infoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return redirect(reverse_lazy('delete_info', kwargs={'pk': self.request.user.pk}))


class DeleteMyInfoView(LoginRequiredMixin, DeleteView):
    template_name = 'my_page/delete_info.html'
    model = User
    success_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if request.user.is_authenticated:
            logout(request)
        return response




