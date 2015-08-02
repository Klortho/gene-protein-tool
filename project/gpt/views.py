from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
import pprint

from .models import ResultSet
from gpt.eutils import *



def home(request):
    return render(request, 'gpt/home.html', using = 'jinja2')

def search(request):
    # Get Genes and Proteins, create a results set, and store it to
    # the database.  Result set will go into rs.

    esearch_result = esearch(request.POST['term'], db='gene')
    idlist = esearch_result['idlist']
    idlist_str = ",".join(idlist)

    esummary_genes = esummary(idlist_str, db='gene')




    # FIXME - for now, we're not redirecting
    # Redirect to the page that will show the result.
    #return HttpResponseRedirect(reverse('gpt:result', args=(rs_id,)))

    return HttpResponse(pprint.pformat(esummary_genes),
                        content_type="text/plain");


class ResultView(generic.DetailView):
    model = ResultSet
    template_name = 'gpt/result.html'
