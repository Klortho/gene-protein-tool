from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader



def home(request):
    return render(request, 'gpt/home.html', using = 'jinja2')

def results(request, result_set_id):
    return HttpResponse("GPT results")

