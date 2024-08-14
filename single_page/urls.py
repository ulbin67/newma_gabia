from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.maincall, name='home'),
    path("introduce_newma/", views.introcall),
    path("information_newma/",views.infocall),

    path("accounts/", include('django.contrib.auth.urls')),

    # localhost/accounts/register : 회원가입
    path("accounts/register/",views.UserCreateView.as_view(), name="register"),

    # localhost/accounts/register/checkid : 회원가입 >> 아이디 중복 검사
    path("accounts/register/checkid/", views.UserIdCheckView.as_view(), name="check_id"),

    # localhost/acounts/register/done : 회원가입 성공시 사용
    path("accounts/register/success",views.UserCreateDoneTV.as_view(), name="register_done"),

    # localhost/accounts/search_id/   : 아이디 찾기
    path("accounts/search_id/", views.SearchIdView.as_view(), name='search_id'),

    # localhost/accounts/search_id/success/  : 아이디 찾기 성공
    path("accounts/search_id/success/", views.SearchIdDoneTV.as_view(), name='search_id_done'),

    # 이메일 입력
    path("accounts/reset_password/", views.UserPasswordResetView.as_view(), name="reset_password"),

    # 이메일 발송 완료
    path("accounts/password_reset_done/", views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),

    # 비밀번호 초기화(메일에서)
    path("accounts/password_reset_confirm/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # 비밀번호 초기화 성공
    path("accounts/password_reset_complete/", views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # localhost/accounts/my_page/   : 마이페이지
    path("accounts/my_page/", views.MyPageView.as_view(), name='my_page'),

    # localhost/accounts/my_page/info/   : 내 정보 수정
    path("accounts/my_page/info/<int:pk>/", views.UpdateMyInfoView.as_view(), name='update_info'),

    # localhost/accounts/my_page/change_psw/   : 비밀번호 변경
    path("accounts/my_page/change_psw/", views.ChangePswView.as_view(), name='change_psw'),

    # localhost/accounts/delete_before/    : 삭제전 인증
    path("accounts/delete_before/", views.DeleteBefore.as_view(), name='delete_before'),

    # localhost/accounts/my_page/info/delete   : 회원 탈퇴 기능
    path("accounts/delete_info/<int:pk>", views.DeleteMyInfoView.as_view(), name='delete_info'),
]