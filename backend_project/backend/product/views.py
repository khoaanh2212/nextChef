
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

def product(request):
    if request.user.is_authenticated():
        response = {}
        return render_to_response('product/product.html', response, context_instance=RequestContext(request))
    else:
        response = {}
        return render_to_response('product/product.html', response, context_instance = RequestContext(request))