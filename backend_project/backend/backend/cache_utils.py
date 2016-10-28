from django.core.cache import get_cache
import logging


class CacheUtils:
    #Context processors
    USER_LOVES = 'user_loves_%(USER_ID)s'
    USER_AVATAR = 'user_avatar_%(USER_ID)s'
    USER_FOLLOWINGS = 'user_followings_%(USER_ID)s'
    COLLECTIONS = 'collections/nav_bar/list'

    EXPLORE_RECOMMENDED_PAGE1 = 'explore/recommended/page1'
    EXPLORE_RECOMMENDED_CHEF_PAGE1 = 'explore/recommended/%(USER_ID)s/page1'
    
    #Explore
    EXPLORE_RECIPES_ALL_PAGE1 = 'explore/recipes/all/page1'
    EXPLORE_RECIPES_ALL_CHEF_PAGE1 = 'explore/recipes/all/%(USER_ID)s/page1'

    EXPLORE_RECIPES_PRO_PAGE1 = 'explore/recipes/pro/page1'
    EXPLORE_RECIPES_PRO_CHEF_PAGE1 = 'explore/recipes/pro/%(USER_ID)s/page1'

    EXPLORE_RECIPES_FOODIE_PAGE1 = 'explore/recipes/foodies/page1'
    EXPLORE_RECIPES_FOODIE_CHEF_PAGE1 = 'explore/recipes/foodies/%(USER_ID)s/page1'

    EXPLORE_CHEFS_ALL_PAGE1 = 'explore/chefs/all/page1'
    EXPLORE_CHEFS_PRO_PAGE1 = 'explore/chefs/pro/page1'
    EXPLORE_CHEFS_FOODIE_PAGE1 = 'explore/chefs/foodie/page1'
    EXPLORE_BANNERS_PAGE1 = 'explore/banners/page1'
    EXPLORE_BANNERS_COUNT = 'explore/banners_count'
    EXPLORE_BOOKS_PAGE1 = 'explore/books/page1'

    #Recipe
    BOOK = 'book/%(BOOK_ID)s'
    BOOK_COVER = 'book/%(BOOK_ID)s/cover'
    BOOK_RECIPES = 'book/%(BOOK_ID)s/recipes'
    
    #Recipe
    RECIPE = 'recipe/%(RECIPE_ID)s'
    RECIPE_COVER = 'recipe/%(RECIPE_ID)s/cover'
    RECIPE_STEPS = 'recipe/%(RECIPE_ID)s/steps'
    RECIPE_INGREDIENTS = 'recipe/%(RECIPE_ID)s/ingredients'
    RECIPE_TAGS = 'recipe/%(RECIPE_ID)s/tags'
    RECIPE_COMMENTS = 'recipe/%(RECIPE_ID)s/comments'
    RECIPE_PRODUCTS = 'recipe/%(RECIPE_ID)s/products'
    RECIPE_OTHER_RECIPES = 'recipe/%(RECIPE_ID)s/other_recipes'

    #Chef
    CHEF = 'chef/%(CHEF_ID)s'

    CHEF_FOLLOWINGS_COUNT = 'chef/%(CHEF_ID)s/followings_count'
    CHEF_FOLLOWERS_COUNT = 'chef/%(CHEF_ID)s/followers_count'
    CHEF_FOLLOWERS_LIST_10 = 'chef/%(CHEF_ID)s/followers/list_10'
    CHEF_FOLLOWINGS_LIST_10 = 'chef/%(CHEF_ID)s/followings/list_10'

    CHEF_AVATAR = 'chef/%(CHEF_ID)s/avatar'
    CHEF_BASE_NAV_AVATAR = 'chef/%(CHEF_ID)s/base_nav_avatar'
    CHEF_COVER = 'chef/%(CHEF_ID)s/cover'
    CHEF_EDIT_COVER = 'chef/%(CHEF_ID)s/edit_cover'

    CHEF_RESTAURANT = 'chef/%(CHEF_ID)s/restaurant'
    CHEF_RESTAURANT_IMAGE = 'chef/%(CHEF_ID)s/restaurant/image'

    CHEF_BOOKS = 'chef/%(CHEF_ID)s/books'
    CHEF_PUBLIC_BOOKS = 'chef/%(CHEF_ID)s/public/books'
    CHEF_ALL_BOOKS = 'chef/%(CHEF_ID)s/all/books'
    CHEF_DRAFTS = 'chef/%(CHEF_ID)s/drafts'

    CHEF_PRIVATE_RECIPES_COUNT = 'chef/%(CHEF_ID)s/recipes/private/count'
    CHEF_PUBLIC_RECIPES_COUNT = 'chef/%(CHEF_ID)s/recipes/public/count'
    CHEF_PRIVATE_RECIPES_12_PAGE1 = 'chef/%(CHEF_ID)s/recipes/private/list_12'
    CHEF_PUBLIC_RECIPES_12_PAGE1 = 'chef/%(CHEF_ID)s/recipes/public/list_12'
    CHEF_RELATED_RECIPES_5 = 'chef/%(CHEF_ID)s/related_recipes/list_5'

    #Collection
    COLL = 'coll/%(SLUG)s'
    COLL_RECIPES = 'coll/%(SLUG)s/recipes'
    COLL_COVER = 'coll/%(SLUG)s/cover'

    @staticmethod
    def get_key(value, chef_id=None, user_id=None, recipe_id=None, book_id=None, page=None, slug=None):
        value = str(value)
        return value % {'USER_ID': user_id, 'CHEF_ID': chef_id, 'RECIPE_ID': recipe_id, 'BOOK_ID': book_id, 'PAGE': page, 'SLUG': slug}

    def refresh_recipe(self, recipe_id=None, chef_id=None, book_id=None):
        keys = []
        if recipe_id is not None:
            keys.append(self.RECIPE)
            keys.append(self.RECIPE_COVER)
            keys.append(self.RECIPE_STEPS)
            keys.append(self.RECIPE_INGREDIENTS)
            keys.append(self.RECIPE_TAGS)
            keys.append(self.RECIPE_COMMENTS)
            keys.append(self.RECIPE_PRODUCTS)
            keys.append(self.RECIPE_OTHER_RECIPES)

        if chef_id is not None:
            keys.append(self.CHEF_BOOKS)
            keys.append(self.CHEF_DRAFTS)
            keys.append(self.CHEF_PRIVATE_RECIPES_COUNT)
            keys.append(self.CHEF_PUBLIC_RECIPES_COUNT)
            keys.append(self.CHEF_PRIVATE_RECIPES_12_PAGE1)
            keys.append(self.CHEF_PUBLIC_RECIPES_12_PAGE1)
            keys.append(self.CHEF_RELATED_RECIPES_5)

        if book_id is not None:
            keys.append(self.BOOK)
            keys.append(self.BOOK_COVER)
            keys.append(self.BOOK_RECIPES)
            
        res = []
        for key in keys:
            tmp = self.get_key(value=key, chef_id=chef_id, recipe_id=recipe_id, book_id=book_id)
            res.append(tmp)

        return res
    
    def get(self, key, chef_id=None, user_id=None, recipe_id=None, book_id=None, page=None):
        logger = logging.getLogger('CacheUtil')
        cache = get_cache('default')
        key = self.get_key(key, chef_id=chef_id, user_id=user_id, recipe_id=recipe_id, book_id=book_id, page=page)
        try:
            value = cache.get(key, None)
            logger.info('Get cache %s', key)
            logger.debug(key)
            logger.debug(value)
            return value
        except:
            return None

    def set(self, key, value):
        logger = logging.getLogger('CacheUtil')
        cache = get_cache('default')
        try:
            cache.set(key, value)
            logger.info('Set cache %s', key)
            logger.debug(key)
            logger.debug(value)
            return True
        except:
            return False
        
    def reset_chef_cache(self, chef_id):
        
        cache = get_cache('default')
        recipes_count_key = CacheUtils.get_key(CacheUtils.CHEF_PRIVATE_RECIPES_COUNT, chef_id=chef_id)
        cache.set(recipes_count_key, None)
        recipes_count_key = CacheUtils.get_key(CacheUtils.CHEF_PUBLIC_RECIPES_COUNT, chef_id=chef_id)
        cache.set(recipes_count_key, None)
        drafts_key = CacheUtils.get_key(CacheUtils.CHEF_DRAFTS, chef_id=chef_id)
        cache.set(drafts_key, None)
        private_recipes_key = CacheUtils.get_key(CacheUtils.CHEF_PRIVATE_RECIPES_12_PAGE1, chef_id=chef_id)
        cache.set(private_recipes_key, None)
        public_recipes_key = CacheUtils.get_key(CacheUtils.CHEF_PUBLIC_RECIPES_12_PAGE1, chef_id=chef_id)
        cache.set(public_recipes_key, None)