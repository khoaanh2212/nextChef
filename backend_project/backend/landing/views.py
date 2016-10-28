from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


def landing(request):
    if request.user.is_authenticated():
        response = dict()
        return render_to_response('landing/landing.html', response, context_instance=RequestContext(request))
    else:
        response = dict()
        return render_to_response('landing/landing.html', response, context_instance=RequestContext(request))


def bii_landing(request):
    if request.user.is_authenticated():
        response = dict()
        return render_to_response('landing/bii_landing.html', response, context_instance=RequestContext(request))
    else:
        response = dict()
        return render_to_response('landing/bii_landing.html', response, context_instance=RequestContext(request))


def taste_of_london(request):
    response = dict()
    return render_to_response('landing/taste_of_london.html', response, context_instance=RequestContext(request))
