from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader



def home(request):
    template = loader.get_template('gpt/home.html', using = 'jinja2')
    return HttpResponse(template.render())

def results(request, result_set_id):
    return HttpResponse("GPT results")

