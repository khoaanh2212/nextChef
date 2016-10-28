
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.clickjacking import xframe_options_exempt

from products.models import Product
from recipe.models import Recipes

@xframe_options_exempt
def related_recipes_embed(request, barcode):
    product = Product.objects.filter(barcode=barcode)
    recipes = Recipes.objects.filter(products__in=product).order_by("?")[:3]
    response = dict(recipes=recipes)
    return render_to_response('products/related_recipes_embed.html', response, context_instance=RequestContext(request))

