# -*- coding: utf-8 -*-

# 生产环境／测试环境
PRODUCTION = True
if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'blog',
            'USER': 'root',
            'PASSWORD': 'funny123',
            'HOST': '127.0.0.1',  # ip
            'PORT': '3306',
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'blog',
            'USER': 'root',
            'PASSWORD': 'funny123',
            'HOST': '127.0.0.1',  # ip
            'PORT': '3306',
            'OPTIONS': {'charset': 'utf8mb4'},
        },
    }
