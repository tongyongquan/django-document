from django.shortcuts import render
from apps.blog.models import Article, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings

categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
months = Article.objects.datetimes('pub_time', 'month', order='DESC')


def home(request):  # 主页
    posts = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list,'category_list': categories, 'months': months})


def detail(request, id):  # 查看文章详情
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()   # 更新浏览次数
        tags = post.tags.all()  # 获取文章对应所有标签
        next_post = post.next_article()  # 上一篇文章对象
        prev_post = post.prev_article()  # 下一篇文章对象
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html',
                  {
                      'post': post,
                      'tags': tags,
                      'category_list': categories,
                      'next_post': next_post,
                      'prev_post': prev_post
                  })


def search_category(request, id):  # 分类搜索
    posts = Article.objects.filter(category_id=str(id))
    category = categories.get(id=str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'post_list': post_list, 'category_list': categories, 'category': category})


def search_tag(request, tag):  # 标签搜索
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tag.html', {'post_list': post_list, 'category_list': categories, 'tag': tag})


def archives(request, year, month):
    posts = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'archive.html', {
        'post_list': post_list,
        'category_list': categories,
        'months': months,
        'year_month': year+'年'+month+'月'
        }
    )