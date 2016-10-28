from django.core.cache import get_cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
import datetime

import facebook
from rest_framework.exceptions import ParseError

from rest_framework.mixins import ListModelMixin
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny

from api_utils.views import CookboothAPIView
from backend.cache_utils import CacheUtils
from books.models import Book
from books.serializers import ApiBookSpecialSerializer, ApiBookPaginatedSerializer
from notifications.models import Notification
from recipe.models import Recipes, Photos
from recipe.serializers import (ApiRecipeSerializer, ApiRecipePaginatedSerializer,
                                ApiPhotoSerializer, ApiPhotoPaginatedSerializer, WebRecipeSerializer)
from utils.email import send_reset_password_email

from .searchers import ChefMapping
from .serializers import (ApiChefsSerializer, ApiChefsViewSerializer, ChefsSerializer,
                          ApiChefsViewPaginatedSerializer)
from .models import Chefs, ChefFollows
from metrics.events import Events

from rest_framework.generics import GenericAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.http import HttpResponse
import json

from braces.views import CsrfExemptMixin
from infrastructure.chefs.stripe_payment.StripePaymentRepository import StripeException
from application.chefs.subscription.SubscriptionApplicationService import SubscriptionApplicationService
from application.chefs.plan.PlanApplicationService import PlanApplicationService
from django.conf import settings

class ChefsListView(generics.ListAPIView):
    model = Chefs
    queryset = Chefs.objects.chefs_all()
    serializer_class = ChefsSerializer


class ChefsProsListView(generics.ListAPIView):
    model = Chefs
    queryset = Chefs.objects.chefs_pros()
    serializer_class = ChefsSerializer


class ChefsFoodiesListView(generics.ListAPIView):
    model = Chefs
    queryset = Chefs.objects.chefs_foodies()
    serializer_class = ChefsSerializer

    def get_queryset(self):
        return Chefs.objects.chefs_foodies()


class FollowView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        try:
            if request.user.is_authenticated:
                chef_id = int(request.POST.get('chef_id', ''))
                chef = Chefs.objects.get(pk=chef_id)
                request.user.follow(chef)
                
                cache = get_cache('default')
                #chef looses or adds followers count
                key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWERS_COUNT, chef_id=chef_id)
                cache.set(key, None)
                #chef looses or adds followings in list
                key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWINGS_LIST_10, chef_id=chef_id)
                cache.set(key, None)
                #chef looses or adds followers in list
                key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWERS_LIST_10, chef_id=chef_id)
                cache.set(key, None)
        
                #user looses or adds to who is followings count
                key = CacheUtils.get_key(CacheUtils.CHEF_FOLLOWINGS_COUNT, chef_id=request.user.id)
                cache.set(key, None)
                #user looses or adds to who is following
                key = CacheUtils.get_key(CacheUtils.USER_FOLLOWINGS, user_id=request.user.id)
                cache.set(key, None)
        

                return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CookboothAPIView):
    def get_authenticators(self):
        # Deactivate all authentication for signup
        if self.request.method.lower() == 'post':
            return ()
        return super(LoginView, self).get_authenticators()

    def get_permissions(self):
        # Deactivate all authentication for login
        if self.request.method.lower() == 'post':
            return ()
        return super(LoginView, self).get_permissions()

    def post(self, request):
        """
        Login
        """
        email = request.DATA.get('email')
        password = request.DATA.get('password', '')
        fb_access_token = request.DATA.get('fb_access_token')

        try:
            user = Chefs.objects.get(email=email)
        except Chefs.DoesNotExist:
            return Response({'code': 404, 'message': 'chef do not exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        if fb_access_token:
            try:
                graph = facebook.GraphAPI(fb_access_token)
                profile = graph.get_object("me")
            except facebook.GraphAPIError:
                return Response('Not valid Facebook access token', status=status.HTTP_403_FORBIDDEN)

            if user.email != profile.get('email'):
                return Response('Not valid Facebook access token', status=status.HTTP_403_FORBIDDEN)

            if user.fb_user_id != profile['id']:
                user.fb_user_id = profile['id']
                user.save()
        else:
            if not password or not user.api_check_password(password):
                return Response({'code': 401, 'message': 'Bad credentials'},
                                status=status.HTTP_400_BAD_REQUEST)

        token = user.api_login(request)
        return Response({'auth': {'token': token}})

    def delete(self, request):
        """
        Logout
        """
        request.user.api_logout()
        return Response({'auth': {'token': ''}})


class ResetPasswordView(CookboothAPIView):
    authentication_classes = ()
    permission_classes = ()

    def put(self, request, *args, **kwargs):

        form = PasswordResetForm(request.DATA)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': None,
                'email_template_name': 'registration/password_reset_email.html',
                'subject_template_name': 'registration/password_reset_subject.txt',
                'request': request,
            }
            form.save(**opts)
            return Response({'response': {'return': True}})
        
        else:
            return Response({'code': 400, 'message': 'No chef found'}, status=status.HTTP_400_BAD_REQUEST)
        
        '''
        email = request.DATA.get('email')
        try:
            user = Chefs.objects.get(email=email)
        except Chefs.DoesNotExist:
            return Response({'code': 400, 'message': 'No chef found'},
                            status=status.HTTP_400_BAD_REQUEST)
        send_reset_password_email(user)
        return Response({'response': {'return': True}})
        '''

class ChefView(CookboothAPIView):
    def get_authenticators(self):
        # Deactivate all authentication for signup
        if self.request.method.lower() == 'post':
            return ()
        return super(ChefView, self).get_authenticators()

    def get_permissions(self):
        # Deactivate all authentication for signup
        if self.request.method.lower() == 'post':
            return ()
        return super(ChefView, self).get_permissions()

    def post(self, request, *args, **kwargs):
        """
        Sign up
        """
        # A little HACK: if the user is signing up with a facebook ID that is already
        # present in the database, instead of signing her up login her instead
        fb_access_token = request.DATA.get('fb_access_token')
        if fb_access_token:
            try:
                graph = facebook.GraphAPI(fb_access_token)
                profile = graph.get_object("me")
                user = Chefs.objects.get(email=profile['email'])
                user.fb_user_id = profile['id']
                user.fb_access_token = fb_access_token
                token = user.api_login(request)
                return Response({'auth': {'token': token}, 'is_new': False})
            except facebook.GraphAPIError:
                pass
            except Chefs.DoesNotExist:
                pass

        serializer = ApiChefsSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            user = serializer.save()
            token = user.api_login(request)
            return Response({'auth': {'token': token}, 'is_new': True})
        return self.invalid_serializer_response(serializer)

    def get(self, request, *args, **kwargs):
        """
        View self profile
        """
        serializer = ApiChefsViewSerializer(request.user)
        return Response({'chef': serializer.data})


class ChefDetailView(CookboothAPIView):
    def get(self, request, *args, **kwargs):
        """
        View chef profile
        """
        obj = get_object_or_404(Chefs, pk=kwargs['pk'])
        data = ApiChefsViewSerializer(obj, context={'most_popular_recipe_cover_image': True}).data
        data['followed'] = request.user.follows_to(obj)
        return Response({'chef': data})

    def put(self, request, *args, **kwargs):
        """
        Update profile
        """
        obj = get_object_or_404(Chefs, pk=kwargs['pk'])
        if obj != request.user:
            self.raise_invalid_credentials()
        serializer = ApiChefsSerializer(obj, data=request.DATA, files=request.FILES, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'chef': serializer.data})
        return self.invalid_serializer_response(serializer)

    def delete(self, request, *args, **kwargs):
        """
        Delete profile
        """
        obj = get_object_or_404(Chefs, pk=kwargs['pk'])
        if obj != request.user:
            self.raise_invalid_credentials()
        obj.delete()
        return Response({'response': {'return': True}})


class ChefFollowView(CookboothAPIView):
    def get(self, request, *args, **kwargs):
        """
        Does user follow chef?
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        if not request.user.follows_to(chef):
            raise Http404('Not following this chef')
        return Response({'response': {'return': True}})

    def post(self, request, *args, **kwargs):
        """
        Follow chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        if chef == request.user:
            return self.invalid_request('Users can not follow to himself')
        request.user.follow(chef)
        Notification.create_new_follow(chef, request.user)
        # JML Disabled due to high volume of notifications
        # Notification.send_new_friend_follow(chef, request.user)
        return Response({'response': {'return': True}})

    def delete(self, request, *args, **kwargs):
        """
        Unfollow chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        if not request.user.follows_to(chef):
            raise Http404('Not following this chef')
        request.user.unfollow(chef)
        return Response({'response': {'return': True}})


class ChefFollowersView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiChefsViewSerializer
    pagination_serializer_class = ApiChefsViewPaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        Get the followers or the followed chefs of a chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        current_results_field = ApiChefsViewPaginatedSerializer.results_field
        if kwargs['action'] == 'following':
            self.queryset = chef.following.all().prefetch_related('following').order_by('name')
            ApiChefsViewPaginatedSerializer.results_field = 'following'
        else:
            self.queryset = chef.followers.all().prefetch_related('followers')
            ApiChefsViewPaginatedSerializer.results_field = 'followers'
        ret = self.list(request, *args, **kwargs)
        ApiChefsViewPaginatedSerializer.results_field = current_results_field
        return ret

    def get_serializer_context(self):
        ret = super(ChefFollowersView, self).get_serializer_context()
        ret['most_popular_recipe_cover_image'] = True
        return ret


class ChefRecipesView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiRecipeSerializer
    pagination_serializer_class = ApiRecipePaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all the recipes of a chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        show_private = chef == request.user
        query = Recipes.objects.all_chef_recipes(chef, show_private=show_private)
        query = Recipes.objects.exclude_for_sale(query)
        self.queryset = query.order_by('-creation_date')
        return self.list(request, *args, **kwargs)


class ChefDraftsView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiRecipeSerializer
    pagination_serializer_class =  ApiRecipePaginatedSerializer

    def get_pagination_serializer(self, page):
        """
        Override results_field class var in pagination serializer but restore it after
        """
        results_field_default = ApiRecipePaginatedSerializer.results_field
        ApiRecipePaginatedSerializer.results_field = 'drafts'
        ret = super(ChefDraftsView, self).get_pagination_serializer(page)
        ApiRecipePaginatedSerializer.results_field = results_field_default
        return ret

    def get(self, request, *args, **kwargs):
        """
        Get all the drafts of a chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        # In the original API all the users are allowed to see this (!!)
        self.queryset = chef.recipes.filter(draft=True).order_by('creation_date')
        return self.list(request, *args, **kwargs)


class ChefBooksView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiBookSpecialSerializer
    pagination_serializer_class = ApiBookPaginatedSerializer

    def get_serializer_context(self):
        ret = super(ChefBooksView, self).get_serializer_context()
        ret['most_popular_recipe_cover_image'] = True
        return ret

    def get(self, request, *args, **kwargs):
        """
        Get all the books of a chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        show_private = chef == request.user
        query = Book.objects.all_books(chef, show_private=show_private, show_for_sale=False)
        self.queryset = query.order_by('creation_date')
        ApiBookSpecialSerializer.user = request.user
        return self.list(request, *args, **kwargs)


class ChefPhotosView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiPhotoSerializer
    pagination_serializer_class =  ApiPhotoPaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all the photos of a chef
        """
        chef = get_object_or_404(Chefs, pk=kwargs['pk'])
        show_private = chef == request.user
        recipes = Recipes.objects.all_chef_recipes(chef, show_private=show_private)
        self.queryset = Photos.objects.filter(recipe__in=recipes)
        return self.list(request, *args, **kwargs)


class ChefSearchView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiChefsViewSerializer
    pagination_serializer_class = ApiChefsViewPaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        Search chefs
        """
        chef = request.user
        action = kwargs['action']

        if action == 'suggested':
            self.queryset = Chefs.objects.exclude(pk=chef.pk)\
                                         .exclude(pk__in=chef.following.all())\
                                         .order_by('-final_score')
        elif action == 'search':
            query = request.GET.get('search')
            if not query:
                return self.invalid_request('Not search query string')
            self.queryset = ChefMapping.cookbooth_search(query)
        else:
            raise Http404()

        return self.list(request, *args, **kwargs)

    def get_serializer_context(self):
        ret = super(ChefSearchView, self).get_serializer_context()
        ret['most_popular_recipe_cover_image'] = True
        return ret


class FacebookView(ListModelMixin, CookboothAPIView):
    serializer_class = ApiChefsViewSerializer
    pagination_serializer_class = ApiChefsViewPaginatedSerializer

    def get(self, request, *args, **kwargs):
        """
        Get chef's facebook id
        """
        if 'action' in kwargs:
            if kwargs['action'] == 'friends':
                return self.friends(request, *args, **kwargs)
            else:
                raise Http404()

        chef = request.user
        if not chef.fb_access_token:
            raise Http404('The chef has no Facebook connection')

        return Response({'response': {'fb_user_id': chef.fb_user_id}})

    def post(self, request, *args, **kwargs):
        """
        Set chef's facebook connection
        """
        chef = request.user

        if 'action' in kwargs:
            raise Http404()

        if chef.fb_access_token:
            return self.invalid_request('User has already FB connection')

        fb_user_id = request.POST.get('fb_user_id')
        fb_access_token = request.POST.get('fb_access_token')

        if not fb_user_id or not fb_access_token:
            return self.invalid_request('There is no fb_user_id or fb_access_token')

        chef.fb_user_id = fb_user_id
        chef.fb_access_token = fb_access_token
        chef.save()

        return Response({'response': {'return': True}})

    def delete(self, request, *args, **kwargs):
        """
        Delete chef's facebook connection
        """
        chef = request.user

        if 'action' in kwargs:
            raise Http404()

        if not chef.fb_access_token:
            raise Http404('The chef has no Facebook connection')

        chef.fb_user_id = None
        chef.fb_access_token = None
        chef.save()

        return Response({'response': {'return': True}})

    def friends(self, request, *args, **kwargs):
        """
        Search chefs that are facebook friends of chef
        """
        chef = request.user

        fb_access_token = request.GET.get('fb_access_token', '').strip()
        if fb_access_token:
            dirty_fb_access_token = True
        else:
            dirty_fb_access_token = False
            if not chef.fb_access_token:
                raise Http404('The chef has no Facebook connection')
            fb_access_token = chef.fb_access_token

        try:
            graph = facebook.GraphAPI(fb_access_token)
            friends = graph.get_connections("me", "friends")
        except facebook.GraphAPIError:
            return self.invalid_request('Not valid Facebook access token')

        if not friends or not friends.get('data'):
            raise Http404('The chef has no friends to follow')

        facebook_friends_ids = [f['id'] for f in friends['data']]

        queryset = Chefs.objects.filter(fb_user_id__in=facebook_friends_ids)\
                                .exclude(pk__in=chef.following.all())

        if queryset.count() == 0:
            raise Http404('The chef has no friends to follow')

        self.queryset = queryset

        current_results_field = ApiChefsViewPaginatedSerializer.results_field
        ApiChefsViewPaginatedSerializer.results_field = 'friends'
        ret = self.list(request, *args, **kwargs)
        ApiChefsViewPaginatedSerializer.results_field = current_results_field
        return ret


class PaymentWebhookView(CookboothAPIView):

    permission_classes = (AllowAny, )
    authentication_classes = ()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentWebhookView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        event_json = json.loads(request.body)
        type = event_json['type']

        if type == settings.STRIPE_SUBSCRIPTION_UPDATE :
            subscription_details = dict(
                customer = event_json['data']['object']['customer'],
                plan = event_json['data']['object']['plan']['id'],
                ended_at = event_json['data']['object']['ended_at'],
                current_period_end = event_json['data']['object']['current_period_end'],
                current_period_start = event_json['data']['object']['current_period_start'],
                canceled_at = event_json['data']['object']['canceled_at'],
                cancel_at_period_end = event_json['data']['object']['cancel_at_period_end']
            )

            applicationService = SubscriptionApplicationService.new()
            try:
                applicationService.updateSubscription(subscription_details)
            except StripeException:
                return HttpResponse(status=400)

            return HttpResponse(status=200)

class PlanView(CookboothAPIView):

    def get(self, request, *args, **kwargs):
        plan_type = request.GET.get('type')
        plan_interval = request.GET.get('interval')

        planApplicationService = PlanApplicationService.new()
        plan = planApplicationService.getPlanByTypeAndInterval(plan_type, plan_interval)

        return Response({
            'amount': plan['amount'],
            'due_date': plan['due_date'],
            'type': plan['plan'].type,
            'interval': plan['plan'].interval
        })
