from django.contrib.auth.decorators import login_required
from django.core.cache import get_cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string

from application.chefs.plan.PlanApplicationService import PlanApplicationService
from application.chefs.subscription.SubscriptionApplicationService import SubscriptionApplicationService
from books.models import BookHasRecipes
from chefs.models import Chefs
from recipe.models import Recipes

from django.conf import settings

import json
from django.views.decorators.csrf import csrf_exempt
from infrastructure.chefs.stripe_payment.StripePaymentRepository import StripeException

class InvalidArgumentException(Exception):
    pass


def activation(request):
    from django.contrib.sites.models import RequestSite

    site = RequestSite(request)

    recipe = Recipes.objects.get(pk=4948)
    books = BookHasRecipes.objects.filter(book__chef=recipe.chef, recipe=recipe)
    response = dict(user=request.user, recipe=recipe, books=books, site=site, activation_key='asdf')
    # mail = render_to_string('recipe/publish_email.html', response)
    # mail = render_to_string('registration/activation_email_es.html', response)
    # mail = render_to_string('registration/welcome_email_es.html', response)
    # mail = render_to_string('emails/activation_email_A.html', response)
    mail = render_to_string('emails/activation_email_B.html', response)

    from premailer import transform
    inlined_mail = transform(mail)

    '''
    from django.core.mail.message import  EmailMultiAlternatives
    mail = EmailMultiAlternatives('MY PERFECT STEAK, la fotoreceta ','', 
                                  settings.SERVER_EMAIL, [request.user.email,],)
    mail.attach_alternative(inlined_mail, 'text/html')
    mail.send(fail_silently=True)
    '''

    # send_mail('WelcomeTest', '', 'hello@nextchef.co', [request.user.email, ], html_message=inlined_mail)
    return HttpResponse(inlined_mail)


def chefs(request, chefs, MORE_CHEFS_URL):
    user_follows_list = None
    if request.user.is_authenticated():
        user_follows_list = request.user.follows_list
    response = dict(chefs=chefs, MORE_CHEFS_URL=MORE_CHEFS_URL, USER_FOLLOWS_LIST=user_follows_list)
    return render_to_response('chefs/chefs.html', response, context_instance=RequestContext(request))


def chefs_all(request):
    chefs_list = Chefs.objects.chefs_all()[:12]
    MORE_CHEFS_URL = reverse('chefs-json')
    return chefs(request, chefs_list, MORE_CHEFS_URL)


def chefs_pro(request):
    chefs_list = Chefs.objects.chefs_pros()[:12]
    MORE_CHEFS_URL = reverse('chefs-pros-json')
    return chefs(request, chefs_list, MORE_CHEFS_URL)


def chefs_foodies(request):
    chefs_list = Chefs.objects.chefs_foodies()[:12]
    MORE_CHEFS_URL = reverse('chefs-foodies-json')
    return chefs(request, chefs_list, MORE_CHEFS_URL)


@login_required
def delete_chef(request, id):
    try:
        chef_id = int(id)
    except ValueError:
        return redirect('home', permanent=True)

    chef = get_object_or_404(Chefs, pk=chef_id)

    if request.user == chef:
        chef.delete()
        cache = get_cache('default')
        cache.set('library/%d/chef' % chef_id, None)
        return redirect('home', permanent=True)


@login_required
def select_payment(request):
    applicationService = PlanApplicationService.new()

    if (request.method == 'GET'):
        selected_plan = request.GET.get('plan')

        response = dict(
            plan=applicationService.getPlanType(),
            interval=applicationService.getPlanInterval(),
            selected_plan=selected_plan
        )
        return render_to_response('chefs/select-payment.html', response, context_instance=RequestContext(request))

    if (request.method == 'POST'):
        selected_plan = request.POST.get('payment-plan', 'pro')
        selected_interval = request.POST.get('payment-interval', 'monthly')

        response = applicationService.getPlanByTypeAndInterval(selected_plan, selected_interval)
        return render_to_response('chefs/confirm-payment.html', response, context_instance=RequestContext(request))


@login_required
def submit_payment(request):
    if request.method == 'POST':
        costing_page = request.POST.get('costingPage')
        current_user = request.user
        plan_type = request.POST.get('plan_type')
        plan_interval = request.POST.get('plan_interval')
        token = request.POST.get('token')
        card_last4 = request.POST.get('last4')
        card_expMonth = request.POST.get('expMonth')
        card_expYear = request.POST.get('expYear')

        try:
            planApplicationService = PlanApplicationService.new()
            _plan = planApplicationService.getPlanByTypeAndInterval(plan_type, plan_interval)

            previous_plan = 'free' if current_user.membership == 'default' else current_user.membership
            applicationService = SubscriptionApplicationService.new()
            applicationService.startSubscription(current_user, _plan['plan'].id, token, card_last4, card_expMonth, card_expYear)

            response = dict(
                name = current_user.name.capitalize() + " " + current_user.surname.capitalize(),
                previous_plan = previous_plan,
                plan = _plan['plan'].type
            )

            return redirect('costing' if costing_page else 'explore')

        except Exception, e:
            print(e)
            planApplicationService = PlanApplicationService.new()
            _plan = planApplicationService.getPlanByTypeAndInterval(plan_type, plan_interval)

            response = _plan
            response['error'] = 'SOMETHING WENT WRONG'

            return render_to_response('chefs/confirm-payment.html', response, context_instance=RequestContext(request))

    else:
        raise Http404()


def get_chef_by_name_limit(request):
    from infrastructure.chefs.chef.ChefRepository import ChefRepository
    from domain.chefs.chef.ChefService import ChefService
    from django.http import HttpResponse
    import json

    chef_repository = ChefRepository.new()
    chef_service = ChefService.new()

    try:
        if request.method == 'GET':
            chef_name = str(request.GET.get('chef_name'))
            page_limit = int(request.GET.get('page_limit'))

            chefs_list = chef_repository.get_chef_by_name(chef_name, page_limit)
            result = chef_service.collaborator_list(chefs_list)

            response = {
                'success': True,
                'chefs': result['chefs'],
                'readmore': result['readmore']
            }

            return HttpResponse(json.dumps(response), content_type="application/json")

    except Exception, e:
        response = {'success': False, 'error': e}
        return HttpResponse(json.dumps(response), content_type="application/json")


def get_chef_by_list_id(request):
    from infrastructure.chefs.chef.ChefRepository import ChefRepository
    from domain.chefs.chef.ChefService import ChefService
    from django.http import HttpResponse
    import json
    chef_repository = ChefRepository.new()
    chef_service = ChefService.new()
    try:
        if request.method == 'POST':
            event_json = json.loads(request.body)
            arrId = event_json['arrId']
            chef_list = chef_repository.get_chef_by_list_id(arrId)
            result = chef_service.collaborator_list(chef_list)
            response = {'success': True, 'chefs': result['chefs']}
            return HttpResponse(json.dumps(response), content_type="application/json")
    except Exception, e:
        response = {'success': False, 'error': e}
        return HttpResponse(json.dumps(response), content_type='application/json')
