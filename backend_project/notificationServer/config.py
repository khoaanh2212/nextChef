#!/usr/bin/env python

from os.path import abspath, dirname, join, normpath

SERVER_ROOT = dirname(abspath(__file__))
SERVER_LOG_PATH = normpath(join(SERVER_ROOT, 'log'))

REDIS_HOST = 'nextchef.redis'
REDIS_PORT = 6379
REDIS_DB = 5
REDIS_QUEUE_KEY = 'cookbooth'

PUSH_DEV_CERT_FILE = normpath(join(SERVER_ROOT, 'PUSH_Pro_Debug.pem'))
PUSH_RELEASE_CERT_FILE = normpath(join(SERVER_ROOT, 'PUSH_Pro_Release.pem'))

ANDROID_API_KEY = 'AIzaSyDRIgNmGrg0t6RVJfqf1i5lF9LpFj3QWcA'
ANDROID_GCM_URL = 'https://android.googleapis.com/gcm/send'

ERROR_LOG_FILE = normpath(join(SERVER_LOG_PATH, 'notification-server-error.log'))
CRASH_LOG_FILE = normpath(join(SERVER_LOG_PATH, 'notification-server-crash.log'))
PID_FILE = normpath(join(SERVER_ROOT, 'server.pid'))
