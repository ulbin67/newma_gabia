from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    ".ap-northeast-2.compute.amazonaws.com",
    ".newmatestul.store",
    ".newmakorea.com",
    '117.52.84.176',
    '.youngwon.site'
]

# PostgreSQL이나 MySQL을 배포 환경에서 사용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newmadb',
        'USER': 'main',
        'PASSWORD': 'qpqp1234',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# HTTPS 설정
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# 세션의 기본 만료 시간 (초 단위)
SESSION_COOKIE_AGE = 7200  # 2시간

# 브라우저를 닫을 때 세션 만료 설정
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
