from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.


def index(request):
    latest_quesgtion_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_quesgtion_list])
    return HttpResponse(output)

def detail(request, question_id):
    return HttpResponse('Your are looking for question %s' % question_id)

def results(request, question_id):
    response = 'You are looking for results of question %s.'
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = 'You are voting on  question %s.'
    return HttpResponse(response % question_id)
