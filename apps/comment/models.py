from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from apps.blog.models import Article


class BaseComment(models.Model):
    """基础评论模型"""
    content = models.TextField('评论内容', max_length=500)
    time = models.DateTimeField('评论时间', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
    good = models.IntegerField('点赞',default=0)

    class Meta:
        # 抽象类不生成表
        abstract = True


class ArticleComment(BaseComment):
    """文章评论模型"""
    story = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='评论')

    class Meta:
        ordering = ['-time']


class ArticleCommentReply(BaseComment):
    """小说评论回复(二级评论)"""
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='replies', verbose_name='一级评论')
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='回复对象')

    class Meta:
        ordering = ['time']
