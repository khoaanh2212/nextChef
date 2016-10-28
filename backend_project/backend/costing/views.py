from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseForbidden
from django.template import RequestContext


def index(request):
    if request.user.is_authenticated():
        user_type = request.user.membership
        response = {'user_type': user_type}
        if (user_type == 'pro' or user_type == 'default'):
            return redirect('/pricing/')

        return render_to_response('costing/costing.html', response, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden()
