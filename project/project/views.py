from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import pprint
import logging

logger = logging.getLogger(__name__)


def register(request):
    context = {'next': 5}
    return render(request, 'registration/register.html', context)

def do_register(request):
    try:
        if (request.user.is_authenticated()):
            raise Exception("You are already logged in!")

        # Fixme: change this to POST
        if (request.method != "POST"):
            raise Exception("This page should only be accessible by POST")

        req_data = request.POST
        for f in ('username', 'password1', 'password2'):
            if (f not in req_data):
                raise Exception("'" + f + "' missing from form data")

        uname = req_data['username']
        pwd1 = req_data['password1']
        pwd2 = req_data['password2']

        if (pwd1 != pwd2):
            raise Exception("Passwords don't match")

        if (len(User.objects.filter(username=uname)) > 0):
            raise Exception("That username is taken!")

        User.objects.create_user(uname, '', pwd1)
        user = authenticate(username=uname, password=pwd1)
        login(request, user)

    except Exception as err:
        return HttpResponse(
            "Error: {0}.\n\nHit the 'back' button and try again.".format(err),
            status=500,
            content_type="text/plain"
        )

    #return HttpResponse("Cool!", content_type="text/plain")
    return HttpResponseRedirect(reverse('gpt:home'))
