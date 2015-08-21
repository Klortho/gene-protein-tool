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
    result_sets = ResultSet.objects.all()
    context = {'result_sets': result_sets}
    return render(request, 'gpt/home.html', context, using = 'jinja2')

def search(request):
    # Get Genes and Proteins, create a results set, and store it to
    # the database.  Result set will go into rs.
    rs = ResultSet.create_from_query(request.POST['term'])

    # Redirect to the page that will show the result.
    return HttpResponseRedirect(reverse('gpt:result', args=(rs.id,)))

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


def save(request):
    if (request.method != "POST"):
        return HttpResponse("HTTP method other than post", 
                            status=400, 
                            content_type="text/plain")

    post = request.POST
    if ('resultset_id' not in post):
        return HttpResponse("No resultset_id", 
                            status = 400, 
                            content_type="text/plain")

    resultset_id = post['resultset_id']
    #print('resultset_id is ' + resultset_id)

    try:
        ResultSet.archive_it(resultset_id)
    except:
        return HttpResponse("Error saving to the database",
                            status=500,
                            content_type="text/plain")

    # Success
    return HttpResponse("resultset_id = " + resultset_id, 
                        content_type="text/plain")

