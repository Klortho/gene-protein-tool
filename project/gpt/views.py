from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
import pprint
import logging
from .models import *

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'gpt/home.html', using = 'jinja2')

def search(request):
    # Get Genes and Proteins, create a results set, and store it to
    # the database.  Result set will go into rs.
    #rs = ResultSet.create_from_query(request.POST['term'])

    # FIXME - for now, we're not redirecting
    # Redirect to the page that will show the result.
    return HttpResponseRedirect(reverse('gpt:result', args=(25,)))

    #return HttpResponse(
    #    "esearch_result\n==============\n" +
    #    pprint.pformat(rs.esearch_result) + "\n\n" +
    #    "esummary_genes\n==============\n" +
    #    pprint.pformat(rs.esummary_genes) + "\n\n" +
    #    "elink_result\n============\n" +
    #    pprint.pformat(rs.elink_result) + "\n\n" +
    #    "esummary_proteins\n=================\n" +
    #    pprint.pformat(rs.esummary_proteins) + "\n\n",
    #    content_type="text/plain"
    #);


class ResultView(generic.DetailView):
    model = ResultSet
    template_name = 'gpt/result.html'



