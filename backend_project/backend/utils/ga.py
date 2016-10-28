
from UniversalAnalytics import Tracker
from django.conf import settings

def sendGoogleAnalyticsPageview(path, title):
    #tracker = Tracker.create('UA-45832883-9', client_id=CUSTOMER_UNIQUE_ID)
    tracker = Tracker.create('UA-45832883-9')
    tracker.send('pageview', {
        'path': path,
        'title': title
    })