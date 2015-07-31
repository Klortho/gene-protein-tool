from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic

from .models import ResultSet


def home(request):
    return render(request, 'gpt/home.html', using = 'jinja2')

def search(request):
    #return HttpResponse("Blech: '" + request.POST['term'] + "'")

    # Get Genes and Proteins, create a results set, and store it to
    # the database.  Result set will go into rs.



    # Redirect to the page that will show the result.
    #return HttpResponseRedirect(reverse('gpt:results', args=(rs.id,)))
    return HttpResponseRedirect(reverse('gpt:result', args=(1,)))

def result(request, result_set_id):
    return HttpResponse("GPT result")

class ResultView(generic.DetailView):
    model = ResultSet
    template_name = 'gpt/result.html'
