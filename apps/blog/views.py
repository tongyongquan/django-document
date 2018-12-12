from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Article, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings

try:
    categories = Category.objects.all()  # 获取全部的分类对象
    tags = Tag.objects.all()  # 获取全部的标签对象
    pub_dates = Article.objects.datetimes('pub_time', 'month', order='DESC')
    months = {}
    for pub_date in pub_dates:
        count = Article.objects.filter(pub_time__year=pub_date.year, pub_time__month=pub_date.month).count()
        months.update({pub_date: count})
except Exception as e:
    print(e)


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
    return render(request, 'home.html',
                  {'post_list': post_list, 'category_list': categories, 'months': months, 'tag_list': tags})


def detail(request, id):  # 查看文章详情
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
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
        'year_month': year + '年' + month + '月'
    }
                  )


def manager_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        try:
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        except Exception as e:
            print(e)
            message = "用户名或密码错误!"
            args = {
                'username': username,
                'raw_password': raw_password,
                'message': message
            }
            return render(request, 'login.html', args)

    return render(request, 'login.html')


def manager_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).count() != 0:
                raise KeyError
            u = User(username=username)
            u.set_password(raw_password)
            u.save()
            return redirect('/blog_login')
        except:
            message = "用户名已被使用或不合法,请重新输入!"
            args = {
                'username': username,
                'raw_password': raw_password,
                'message': message
            }
            return render(request, 'register.html', args)

    return render(request, 'register.html')

@login_required()
def manager_logout(request):
    logout(request)
    return redirect('/')