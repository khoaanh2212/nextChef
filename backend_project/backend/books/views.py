import json
import datetime
from django.core.cache import get_cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from backend.cache_utils import CacheUtils
from django.core.exceptions import PermissionDenied
from django.conf import settings
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from django.contrib.sites.models import RequestSite
from registration.models import RegistrationProfile
from django.contrib.auth import login

from .models import Recipes
from .models import Book,ChefsHasBooks
from books.models import BookHasRecipes, BookSale
from chefs.models import Chefs
from library.serializers import LibraryChefSerializer
from recipe.serializers_v1 import APIV1RecipesSerializer

from xhtml2pdf import pisa
import cStringIO as StringIO
from django.template.loader import render_to_string


def book(request, id, need_login=False, need_change_password=False):
    
    try:
        book_id = int(id)
    except ValueError:
        raise Http404

    need_login = False
    if request.session.has_key('need_login'):
        need_login = request.session['need_login']
        if need_login == None:
            need_login = False
        request.session['need_login'] = None
    
    need_change_password = False
    if request.session.has_key('need_change_password'):
        need_change_password = request.session['need_change_password']
        if need_change_password == None:
            need_change_password = False
        request.session['need_change_password'] = None
        
    buy_callback = False
    if request.session.has_key('buy_callback'):
        buy_callback = request.session['buy_callback']
        if buy_callback == None:
            buy_callback = False
        request.session['buy_callback'] = None
        
    already_bought = False
    if request.session.has_key('already_bought'):
        already_bought = request.session['already_bought']
        if already_bought == None:
            already_bought = False
        request.session['already_bought'] = None
            
    cache = get_cache('default')
    
    book_key = CacheUtils.get_key(CacheUtils.BOOK, book_id=book_id)
    book = cache.get(book_key, None)
    if settings.DEBUG or book is None:
        try:
            book = Book.objects.select_related('chef').get(id=book_id)
            cache.set(book_key, book)
        except Exception:
            raise Http404

    if(book.chef != request.user):
        if (book.book_type != Book.TO_SELL and book.status != Book.AVAILABLE):
            raise PermissionDenied()

    book_cover_key = CacheUtils.get_key(CacheUtils.BOOK_COVER, book_id=book_id)
    book_cover = cache.get(book_cover_key, None)
    if settings.DEBUG or book_cover is None:
        if book.image:
            book_cover = book.image.url 
        else:
            book_cover = thumbnail_url(book.cover, 'explore_cover')
        cache.set(book_cover_key, book_cover)

    book_recipes_key = CacheUtils.get_key(CacheUtils.BOOK_RECIPES, book_id=book_id)
    book_recipes = cache.get(book_recipes_key, None)
    if book_recipes is None:
        book_recipes = []
        
        serializer = APIV1RecipesSerializer(book.recipes.all())
        if request.user.is_authenticated():
            serializer.user = request.user
        else:
            serializer.user = None
        
        book_recipes = json.dumps(serializer.data)
        cache.set(book_recipes_key, book_recipes)

    book_bought = ChefsHasBooks.objects.filter(chef__id=request.user.id, book__id=book.id).count() > 0
    
    chef = book.chef
    chef_avatar_key = CacheUtils.get_key(CacheUtils.CHEF_AVATAR, chef_id=chef.id)
    chef_avatar = cache.get(chef_avatar_key, None)
    if chef_avatar is None:
        if chef.avatar:
            chef_avatar = thumbnail_url(chef.avatar, 'chef_avatar')
            cache.set(chef_avatar_key, chef_avatar)

    site = Site.objects.get_current()
    
    response = dict(
        book=book,
        book_price=book.price * 100 if book.price else 0,
        book_cover=book_cover,
        book_recipes=book_recipes,
        book_nb_recipes=book.recipes.count(),
        chef=chef,
        chef_avatar=chef_avatar,
        book_bought=book_bought,
        already_bought=already_bought,
        site=site,
        need_login=need_login,
        need_change_password=need_change_password,
        buy_callback=buy_callback,
        stripe_key=settings.STRIPE_KEY_PUBLIC
    )
    
    return render_to_response('books/book.html', response, context_instance=RequestContext(request))

def checkout(request, id):
    if request.method == 'POST':
        import stripe
        
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://dashboard.stripe.com/account/apikeys
        stripe.api_key = settings.STRIPE_KEY_SECRET
        
        # Get the credit card details submitted by the form
        token = request.POST['stripe_token']
        stripe_response = json.loads(request.POST['stripe_response'])
        
        book = Book.objects.get(pk=id)
        
        #if(book.chef == request.user):
        #    raise PermissionDenied()
        
        if (book.book_type != Book.TO_SELL or book.status != Book.AVAILABLE):
            raise PermissionDenied()
        
        email = stripe_response['email']
        user = None
        success = False
        need_change_password = False
        need_login = False
        
        if request.user.is_authenticated():
            user = request.user
            
        else:
            users = Chefs.objects.filter(email=email)
            if users.exists():
                user = users[0]
                need_login = True
                
            else:
                site = RequestSite(request)
                name = email.split('@')[0] 
                surname = ''
                password = ''
                type = 0
            
                language = request.LANGUAGE_CODE[0:2]
                site = RequestSite(request)
                user = RegistrationProfile.objects.create_active_user(name, surname, email, password, language, type, site)
                user.backend = 'chefs.backends.auth.EmailAuthBackend'
                login(request, user)
                need_change_password = True
        
        current_books = ChefsHasBooks.objects.filter(chef=user, book=book)
        if current_books.exists():
            request.session['already_bought'] = True
            return HttpResponseRedirect(reverse('book', kwargs={'id':id}))
        
        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
                                          amount=int(book.price * 100), # amount in cents, again
                                          currency="eur",
                                          source=token,
                                          description=user.email
                                        )
            
            if charge.paid:
                book.buy(
                     user, 
                     BookSale.STRIPE, 
                     charge.id)
                success = True
            
        except stripe.CardError, e:
            # The card has been declined
            pass
          
        if success:
            request.session['need_login'] = need_login
            request.session['need_change_password'] = need_change_password
            request.session['buy_callback'] = True
            
            return HttpResponseRedirect(reverse('book', kwargs={'id':id}))
        else:
            return HttpResponseRedirect(reverse('book', kwargs={'id':id}))
    else:
            return HttpResponseRedirect(reverse('book', kwargs={'id':id}))
        
        
        
def checkout_change_password(request, id):
    if request.method == 'POST':
        from django.contrib.auth.forms import SetPasswordForm
        form = SetPasswordForm(user=request.user, data=request.POST)
        need_change_password = True
        if form.is_valid():
            form.save()
            need_change_password = False
        
        book = Book.objects.get(pk=id)
        request.session['need_change_password'] = need_change_password
        return HttpResponseRedirect(reverse('book', kwargs={'id':id}))
        
    else:
        return HttpResponseRedirect(reverse('book', kwargs={'id':id}))
        
        
        
        