# coding=utf-8
from django.contrib import admin
from .models import Question

# Register your models here.
# 注册模型到管理系统

admin.site.register(Question)


# 需要注册一个超级用户: python manage.py createsuperuser
