from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import ArticleComment, ArticleCommentReply
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.blog.models import Article


# Create your views here.


def write_comment(request):
    if request.is_ajax():
        story_comment = ArticleComment()
        story_comment.content = request.POST.get('comment_text')
        story_comment.user = request.user
        story_id = request.POST.get('story_id')
        story_comment.story_id = story_id
        story_comment.score = request.POST.get('score')
        story_comment.save()
        score = ArticleComment.objects.filter(story_id=story_id).aggregate(Avg('score'))['score__avg']
        story = Article.objects.only('score').get(id=story_id)
        story.score = round(score, 1)
        story.save()
        return HttpResponse('success')


def comment_replies(request, comment_id):
    reply_comment = ArticleComment.objects.get(id=comment_id)
    # 默认图片路径
    return render(request, 'novel/replyDetail.html', locals())


def reply(request):
    if request.is_ajax():
        comment_reply = ArticleCommentReply()
        comment_reply.content = request.POST.get('comment_text')
        comment_reply.user = request.user
        comment_id = request.POST.get('comment_id')
        comment_reply.comment = ArticleComment.objects.get(id=comment_id)
        comment_reply.save()
        return HttpResponse('success')


def reply_reply(request):
    if request.is_ajax():
        reply_reply = ArticleCommentReply()
        reply_reply.content = request.POST.get('comment_text')
        reply_reply.user = request.user
        reply_id = request.POST.get('reply_id')
        reply_reply.reply = ArticleCommentReply.objects.get(id=reply_id)
        reply_reply.comment_id = request.POST.get('comment_id')
        reply_reply.save()
        return HttpResponse('success')


def read_comment(request, story_id):

    story = Article.objects.get(id=story_id)
    comment_posts = ArticleComment.objects.filter(story_id=story_id)
    # 默认图片路径
    paginator = Paginator(comment_posts, 20)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request,'novel/readComment.html',locals())


def comment_good(request):
    if request.method == 'POST':
        comment_id = request.POST.get('id')
        comment = get_object_or_404(ArticleComment, id=comment_id)
        comment.good += 1
        comment.save()
        return JsonResponse({"comment_good": comment.good})


def reply_good(request):
    if request.method == 'POST':
        comment_id = request.POST.get('id')
        comment = get_object_or_404(ArticleCommentReply, id=comment_id)
        comment.good += 1
        comment.save()
        return JsonResponse({"comment_good": comment.good})