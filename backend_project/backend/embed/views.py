import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

from recipe.models import Recipes

@xframe_options_exempt
def recipe(request, slug, id):
    # Sanitize input, if we don't get id redirect permanent to home page
    try:
        recipe_id = int(id)
    except ValueError:
        return redirect('home', permanent=True)

    try:
        r = Recipes.objects.select_related('chef').get(id=recipe_id)
        response = dict(recipe=r)
        return render_to_response('embed/recipe.html', response, context_instance=RequestContext(request))
    except Recipes.DoesNotExist:
        raise Http404

