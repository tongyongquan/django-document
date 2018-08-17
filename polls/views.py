from django.shortcuts import get_object_or_404,render
# render 的本质是HttpResponse(template.render(context, request))
from django.http import HttpResponse, Http404
from .models import Question


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    try:
        question = Question.objects.get(pk=question_id)
    # 当模型对象查询结果为空时会发出Question.DoesNotExist异常,可以设置返回Http404
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    # 或者使用更便捷的 get_object_or_404 ,拿到对象或返回404
    # 在Class.objexts.filter()时则使用  get_list_or_404()
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
