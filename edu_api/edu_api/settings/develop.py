# 开发配置
"""
Django settings for edu_api project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 修改apps为默认的子应用目录
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jnxsz$q^n&)2-vufl&bm5x6l)_)=!q$#fj@h6eiiv7jgl1+o=o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',

    'xadmin',
    'crispy_forms',
    'reversion',
    'django_filters',

    'home',
    'user',
    'course',
    'detail',
    'cart',
    'order',
    'payments',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'edu_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'edu_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'edu_zgz',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# 修改语言配置  中文
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# 静态资源
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

MEDIA_URL = "/media/"


# drf配置
# 指定REST_FRAMEWORK的配置   全局配置
REST_FRAMEWORK = {
    # 使用自定义的处理异常的方法
    'EXCEPTION_HANDLER': 'edu_api.utils.exceptions.custom_exception_handler',
    # 配置JWT token的认证方式
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    )
}

# 允许跨域请求访问
CORS_ORIGIN_ALLOW_ALL = True

# 指定自定义用户模型为django默认user表
AUTH_USER_MODEL = 'user.UserInfo'

# jwt相关配置
JWT_AUTH = {
    # jwt 登录视图返回的数据的格式
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'user.utils.jwt_response_payload_handler',
    # token 有效期 50min
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),

}

# redis相关配置
CACHES = {
    # 默认库
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # redis服务器所在的ip:port  redis所在的linux系统的ip
        "LOCATION": "redis://192.168.181.128:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 验证码库
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.181.128:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 购物车库
    "cart": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.181.128:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "order_site": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.181.128:6379/6",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}


# 自定义django的登录方式
AUTHENTICATION_BACKENDS = [
    'user.utils.UserModelBackend',
]

# 支付宝配置信息
ALIAPY_CONFIG = {
    # 网关地址
    # "gateway_url": "https://openapi.alipay.com/gateway.do?",
    "gateway_url": "https://openapi.alipaydev.com/gateway.do?",
    "appid": "2016102200738366",
    "app_notify_url": None,
    "app_private_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read(),
    "alipay_public_key_path": open(os.path.join(BASE_DIR, "apps/payments/keys/alipay_public_key.pem")).read(),
    "sign_type": "RSA2",
    "debug": False,
    # 支付成功后跳转的地址
    "return_url": "http://localhost:8080/result",
    # 同步回调地址
    "notify_url": "http://127.0.0.1:8000/payments/result",  # 异步结果通知
}

# 日志配置
LOGGING = {
    'version': 1,
    # 是否禁用项目中其它存在日志
    'disable_existing_loggers': False,
    # 格式化记录 - 输出格式
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理方法
    'handlers': {
        # 输出至控制台信息配置
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            # 打印格式
            'formatter': 'simple'
        },
        # 记录至文件日志信息
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs/edu_api.log"),
            # 单文件大小
            'maxBytes': 100 * 1024 * 1024,
            # 文件最大数量
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    # 日志对象 - 记录django项目日志
    'loggers': {
        # 将日志配置到django中
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}