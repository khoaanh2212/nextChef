import json

from django.http import HttpResponse
from rest_framework.response import Response

from api_utils.views import CookboothAPIView
from application.costing.CostingApplicationService import CostingApplicationService
from domain.costing.custom_changes_ingredient.CustomChangesIngredientService import \
    InvalidCustomChangesIngredientArgumentException
from domain.costing.generic_ingredient.GenericIngredientService import InvalidGenericIngredientArgumentException
from domain.costing.CostingIngredient import InvalidCostingIngredientArgumentException


class CostingListView(CookboothAPIView):
    # get list of costing row for user
    def get(self, request, *args, **kwargs):
        filter = request.GET.get('filter', '')
        page = request.GET.get('page', 1)

        costing_application_service = CostingApplicationService.new()
        result = costing_application_service.get_costing_table(request.user, filter, page)

        return Response(result)


class CostingView(CookboothAPIView):
    # create custom row
    def post(self, request):

        if not request.user.membership == 'business' and not request.user.membership == 'enterprise':
            return HttpResponse('You don\' have permission to do this', status=401)

        arr_event_json = json.loads(request.body)
        response = {}
        try:
            for event_json in arr_event_json:
                ingredient = event_json['ingredient']
                family = event_json['family']
                quantity = event_json['quantity']
                unit = event_json['unit']
                gross_price = event_json['grossPrice']
                waste = event_json['waste']
                net_price = event_json['netPrice']
                supplier = event_json['supplier']
                comment = event_json['comment']

                chef = request.user

                costing_application_service = CostingApplicationService.new()
                response = costing_application_service.add_custom_ingredient_row(chef, ingredient, family,
                                                                                 supplier, quantity, unit,
                                                                                 gross_price, net_price, waste, comment)

        except InvalidCostingIngredientArgumentException:
            return HttpResponse(status=400)

        except KeyError, e:
            return HttpResponse('Key error: %s' % e.message, status=400)

        return Response(response)

    # delete custom row
    def delete(self, request):

        if not request.user.membership == 'business' and not request.user.membership == 'enterprise':
            return HttpResponse('You don\' have permission to do this', status=401)

        try:
            id = request.GET.get('id')
            costing_application_service = CostingApplicationService.new()
            costing_application_service.remove_custom_ingredient_row(id)
            return HttpResponse(status=200)
        except InvalidCustomChangesIngredientArgumentException:
            return HttpResponse(status=400)

    # edit custom row
    def put(self, request):

        if not request.user.membership == 'business' and not request.user.membership == 'enterprise':
            return HttpResponse('You don\' have permission to do this', status=401)

        event_json = json.loads(request.body)
        response = {}
        try:
            custom_ingredient_id = event_json['custom_ingredient_id']
            ingredient = event_json['ingredient']
            family = event_json['family']
            quantity = event_json['quantity']
            unit = event_json['unit']
            gross_price = event_json['grossPrice']
            waste = event_json['waste']
            net_price = event_json['netPrice']
            supplier = event_json['supplier']
            comment = event_json['comment']

            chef = request.user

            costing_application_service = CostingApplicationService.new()
            response = costing_application_service.edit_custom_ingredient_row(custom_ingredient_id, chef,
                                                                              ingredient, family,
                                                                              supplier, quantity, unit,
                                                                              gross_price, net_price, waste,
                                                                              comment)

        except InvalidCostingIngredientArgumentException:
            return HttpResponse(status=400)

        except KeyError, e:
            return HttpResponse('Key error: %s' % e.message, status=400)

        return HttpResponse(status=200)


class CostingGenericView(CookboothAPIView):
    # edit generic row
    def post(self, request):

        if not request.user.membership == 'business' and not request.user.membership == 'enterprise':
            return HttpResponse('You don\' have permission to do this', status=401)

        event_json = json.loads(request.body)
        response = {}
        try:
            chef = request.user
            edit_ingredient = {'generic_table_row_id': event_json['generic_table_row_id'],
                               'ingredient': event_json['ingredient'],
                               'family': event_json['family'],
                               'quantity': event_json['quantity'],
                               'unit': event_json['unit'],
                               'gross_price': event_json['gross_price'],
                               'waste': event_json['waste'],
                               'net_price': event_json['net_price'],
                               'supplier': event_json['supplier'],
                               'comment': ''}
            costing_application_service = CostingApplicationService.new()
            if event_json['custom_id']:
                edit_ingredient['id'] = event_json['custom_id']
                response = costing_application_service.edit_custom_ingredient_row(chef, edit_ingredient)
            else:
                response = costing_application_service.edit_generic_custom_ingredient_row(chef, edit_ingredient)



        except InvalidCostingIngredientArgumentException:
            return HttpResponse(status=400)

        except KeyError, e:
            return HttpResponse('Key error: %s' % e.message, status=400)

        return Response(response)

    # delete generic row
    def delete(self, request):

        if not request.user.membership == 'business' and not request.user.membership == 'enterprise':
            return HttpResponse('You don\' have permission to do this', status=401)

        try:
            id = request.GET.get('id')
            chef = request.user
            costing_application_service = CostingApplicationService.new()
            costing_application_service.remove_custom_generic_ingredient_row(chef, id)
            return HttpResponse(status=200)
        except InvalidGenericIngredientArgumentException:
            return HttpResponse(status=400)


class CostingIngredientDuplicateView(CookboothAPIView):
    # duplicate generic row
    def put(self, request):

        if not request.user.membership == 'business' and not request.user.membership == 'enterprise':
            return HttpResponse('You don\' have permission to do this', status=401)

        try:
            id = request.GET.get('id')
            chef = request.user
            costing_application_service = CostingApplicationService.new()
            costing_application_service.duplicate_custom_generic_ingredient_row(chef, id)
            return HttpResponse(status=200)
        except InvalidGenericIngredientArgumentException:
            return HttpResponse(status=400)

    # duplicate custom row
    def post(self, request):

        if not request.user.membership == 'business' and not request.user.membership == 'enterprise':
            return HttpResponse('You don\' have permission to do this', status=401)

        try:
            id = request.GET.get('id')
            chef = request.user
            costing_application_service = CostingApplicationService.new()
            costing_application_service.duplicate_custom_ingredient_row(chef, id)
            return HttpResponse(status=200)
        except InvalidGenericIngredientArgumentException:
            return HttpResponse(status=400)


class GenericIngredientView(CookboothAPIView):
    # create generic row
    def post(self, request):

        event_json = json.loads(request.body)
        response = {}
        try:
            ingredient = event_json['ingredient']
            family = event_json['family']
            quantity = event_json['quantity']
            unit = event_json['unit']
            gross_price = event_json['grossPrice']
            waste = event_json['waste']
            net_price = event_json['netPrice']
            supplier = event_json['supplier']
            comment = event_json['comment']

            costing_application_service = CostingApplicationService.new()
            response = costing_application_service.add_ingredient_row(ingredient, family,
                                                                      supplier, quantity, unit,
                                                                      gross_price, net_price, waste, comment)

        except InvalidCostingIngredientArgumentException:
            return HttpResponse(status=400)

        except KeyError, e:
            return HttpResponse('Key error: %s' % e.message, status=400)

        return Response(response)
