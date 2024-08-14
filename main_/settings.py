import os, json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

#디렉토리 경로 설정
#서버 열 때 static 폴더를 잘 불러오기 위해 이 경로가 필요
BASE_DIR = Path(__file__).resolve().parent.parent

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

#디버그 비허용시 static 자동 연결 해제됨
#서버 설정으로 다시 연결 필요
DEBUG = True

ALLOWED_HOSTS = [
    # 사용 DNS 설정
    ".ap-northeast-2.compute.amazonaws.com",
    ".newmatestul.store",
    ".newmakorea.com",
    'localhost',
    '127.0.0.1',
]


# 사용 앱, 위 django.~은 기본 앱으로 삭제 X
# 앱 추가할 때마다 아래에 추가 필요

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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'newmadb.sqlite3',
    }
}

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

#시간존 사용을 허용할 것인지 설정 SQL과 장고 시간존이 일치 하지 않아 생긴 오류의 경우
#아래 코드를 False로 바꿔보면 잘 돌아감
#배포시 False 하지 않도록 주의!

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

##static 파일들의 경로 설정
#static을 읽어들일 경우, URL -> static 파일에 접근 시, 자동으로 붙는 URL
#ex: http://example/static/이미지.jpg
#root는 읽어들일 때의 경로... (중요함..)

##media 파일들의 경로 설정

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'



LOGIN_REDIRECT_URL = '/'

#로그아웃 성공시 리다이랙트 주소
LOGOUT_REDIRECT_URL = '/'

# 비밀번호 찾기(초기화)에 사용
# 메일을 호스트하는 서버
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'                                      # gmail과의 통신하는 포트
EMAIL_HOST_USER = 'lka111617@gmail.com'                 # 발신할 이메일
EMAIL_HOST_PASSWORD = 'zruk ydku fdsy fsrs'                       # 발신할 메일의 비밀번호
EMAIL_USE_TLS = True                                    # TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER                    # 사이트와 관련한 자동응답을 받을 이메일 주소