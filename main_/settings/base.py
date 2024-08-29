import os, json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

#디렉토리 경로 설정
#서버 열 때 static 폴더를 잘 불러오기 위해 이 경로가 필요
BASE_DIR = Path(__file__).resolve().parent.parent.parent

#보안 키를 숨기기 위해 json에 저장
#깃허브에 업로드 시, 깃 이그노어에 secrets.json 추가 후 푸쉬
#배포할 때, project_ 폴더 안에 secrets.json 을 만들어야 접근 가능
secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# Secret key
SECRET_KEY = get_secret("SECRET_KEY")

# OpenAI API Key
# OPENAI_API_KEY = get_secret("OPENAI_API_KEY")

# NAVER API Credentials
NAVER_CLIENT_ID = get_secret('NAVER_CLIENT_ID')  # 네이버 클라이언트 ID
NAVER_CLIENT_SECRET = get_secret('NAVER_CLIENT_SECRET')

# COOLSMS
COOL_SMS_API = get_secret('COOL_SMS_API')
COOL_SMS_SECRET = get_secret('COOL_SMS_SECRET')

# SLACK
SLACK_API_TOKEN = get_secret('SLACK_API_TOKEN')
SLACK_CHANNEL = get_secret('SLACK_CHANNEL')

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",  # 회원가입 form에서 사용
    "single_page",
    "manage_apply",
    "qna",
    "crispy_forms",
    "crispy_bootstrap4",
    "dashboard", #정보요약추가 -240805
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'single_page.User'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main_.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main_.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = 'ko-KR'
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


LOGIN_REDIRECT_URL = '/'
#로그아웃 성공시 리다이랙트 주소
LOGOUT_REDIRECT_URL = '/'

# 비밀번호 찾기(초기화)에 사용
# 메일을 호스트하는 서버
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_PORT = '587'                                      # gmail과의 통신하는 포트
EMAIL_HOST_USER = 'lka1116@naver.com'                 # 발신할 이메일
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')                       # 발신할 메일의 비밀번호
EMAIL_USE_TLS = True                                    # TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER                    # 사이트와 관련한 자동응답을 받을 이메일 주소

