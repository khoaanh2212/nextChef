from django.shortcuts import render
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from chefs.models import Chefs
from emailing.models import EmailingList

def unsubscribe(request, user_hash):
    
    chef = Chefs.objects.filter(email_unsubscribe_hash=user_hash)
    if chef.exists():
        EmailingList.objects.unsubscribe_chef(chef[0])
        response = dict()
        return render_to_response('emailing/unsubscribe.html', response, context_instance=RequestContext(request))
    else:
        raise Http404()
        