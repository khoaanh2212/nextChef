import datetime
from django.shortcuts import render
from .models import Subscriber, SubscriptionRecipe
from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.renderers import  XMLRenderer, JSONRenderer
from .serializers import SubscriptionRecipeSerializer
from django.shortcuts import render_to_response
from django.template import RequestContext
from chefs.models import Chefs

def first_day_of_month(any_day):
    return any_day.replace(day=1)

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

def recipes(request, token):
    subscribers = Subscriber.objects.filter(token=token, is_active=True)
    if subscribers.exists():
        subscriber = subscribers[0]
        today = datetime.datetime.now()
        first_day = first_day_of_month(today)
        last_day = last_day_of_month(today)
        subscription_recipes = SubscriptionRecipe.objects.filter(date__gte=first_day, date__lte=last_day, subscriber=subscriber)
        response = dict(subscription_recipes=subscription_recipes)
        return render_to_response('subscribers/wordpress_export_recipes.xml', response, context_instance=RequestContext(request), content_type='text/xml')

    else:
        return HttpResponseNotFound()
    
    
def chefs(request, token):
    subscribers = Subscriber.objects.filter(token=token, is_active=True)
    if subscribers.exists():
        subscriber = subscribers[0]
        today = datetime.datetime.now()
        first_day = first_day_of_month(today)
        last_day = last_day_of_month(today)
        subscription_chefs_ids = SubscriptionRecipe.objects.select_related('recipe').filter(date__gte=first_day, date__lte=last_day, subscriber=subscriber).values_list('recipe__chef__id', flat=True)
        chefs = Chefs.objects.filter(id__in=subscription_chefs_ids)
        response = dict(chefs=chefs)
        return render_to_response('subscribers/wordpress_export_chefs.xml', response, context_instance=RequestContext(request), content_type='text/xml')

    else:
        return HttpResponseNotFound()