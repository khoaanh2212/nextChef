# -*- coding: utf-8 -*-
import string

class PricingService:
    '''Pricing Service'''

    def getFakeData(self):
        return [
        	{
                'price': {'type': 'Free', 'amount': '0', 'currency': '£', 'desc': 'share for free', 'unit': 'month'},
                'info': {
                    'desc_html': '<b>Free</b> includes all of these great features:',
                    'user_limit': '1 user',
                    'features': ['Personal library', 'Step by step photo recipes', 'Ingredients, method, books', 'Public recipes']
                },
                'upgrade_path': '#'
            },
            {
                'price': {'type': 'Pro', 'amount': '19.90', 'currency': '£', 'desc': 'private recipe cloud', 'unit': 'month'},
                'info': {
                    'desc_html': '<b>Pro</b> includes everything in Free, plus:',
                    'user_limit': '1 user',
                    'features': ['Private recipes', 'Allergens', 'Sub-recipes', 'Print PDF']
                },
                'upgrade_path': '#'
            },
            {
                'price': {'type': 'Business', 'amount': '59', 'currency': '£', 'desc': 'Increase your Profit', 'unit': 'month'},
                'info': {
                    'desc_html': '<b>Business</b> includes everything in Pro, plus:',
                    'user_limit': '5 users',
                    'features': ['Private groups', 'Automatic recipe costing *']
                },
                'upgrade_path': '#'
            },
            {
                'price': {'type': 'Enterprise', 'amount': 'Contact us', 'desc': 'Manage multiple teams'},
                'info': {
                    'desc_html': '<b>Enterprise</b> includes everything in Business, plus:',
                    'user_limit': 'unlimited users',
                    'features': ['License package', 'Account Set-Up', 'Account manager', 'Recipes Photo Shooting', 'App customisation']
                },
                'upgrade_path': 'enterprise/upgrade/'
            }
        ]

    def splitStringIntoTwoParts(self,object):
        strObj = str(object)
        return strObj.split('.')


