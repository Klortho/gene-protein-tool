from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView

import pprint
import logging
from .models import *


logger = logging.getLogger(__name__)


# This code is executed only once, and makes sure we initialize anon_user,
# which is a dummy user that is used whenever the person is not logged in.

anon_username = '8wKKUs32hp43ZvU5'
anon_ = User.objects.filter(username=anon_username)
if (len(anon_) == 0):
    anon_user = User.objects.create_user(anon_username, '', 'fleegle')
else:
    anon_user = anon_[0]


# If the user is logged in, this returns that user object, otherwise, returns
# the anonymous user object
def _get_user(request):
    req_user = request.user
    return (
        req_user if req_user.is_authenticated() 
        else anon_user
    )

def home(request):
    user = _get_user(request)
    result_sets = ResultSet.objects.filter(user=user)
    context = {
        'result_sets': result_sets,
        'request': request,
    }
    return render(request, 'gpt/home.html', context, using = 'jinja2')

def search(request):
    user = _get_user(request)

    # Get Genes and Proteins, create a results set, and store it to
    # the database.  Result set will go into rs.
    rs = ResultSet.create_from_query(request.POST['term'], user)

    # Redirect to the page that will show the result.
    return HttpResponseRedirect(reverse('gpt:result', args=(rs.id,)))

class ResultView(DetailView):
    model = ResultSet
    template_name = 'gpt/result.html'

    # Pass the value of is_authenticated into the template, since the 
    # anonymous user can't save searches.
    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['is_anon'] = not self.request.user.is_authenticated()
        return context

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




