# -*- coding: utf-8 -*-
import os
from documentdjango.settings import BASE_DIR

# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# 生产环境／测试环境
PRODUCTION = True
if PRODUCTION:
    # 生产环境使用mysql
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
    # 测试环境使用sqlite3
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


