#!/usr/bin/env python

import sys
import time
import redis
import json
import urllib3
import config
from time import gmtime, strftime
from daemon import Daemon
from apnsclient import *


class NotificationServer(Daemon):

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = config.CRASH_LOG_FILE
        self.pidfile = pidfile

    def log(self, message):
        with open(config.ERROR_LOG_FILE, 'a') as f:
            f.write(message + '\n')

    def send_push_to_ios(self, environment, devices, alert, payload):
        if environment == 'dev':
            session = Session()
            con = session.get_connection('push_sandbox', cert_file=config.PUSH_DEV_CERT_FILE)
        elif environment == 'release':
            session = Session()
            con = session.get_connection('push_production', cert_file=config.PUSH_RELEASE_CERT_FILE)

        message = Message(devices, alert=alert, payLoad=payload, badge=1)

        # Send the message.
        srv = APNs(con)
        res = srv.send(message)

        # Check failures. Check codes in APNs reference docs.
        for token, reason in res.failed.items():
            code, errmsg = reason
            self.log(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ': ' + "Device failed: {0}, reason: {1}".format(token, errmsg))
        
        # Check failures not related to devices.
        for code, errmsg in res.errors:
            self.log(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ': ' + "Error: " + errmsg)            

    def send_push_to_android(self, environment, devices, alert, payload):
        apiKey = config.ANDROID_API_KEY    
        data = {
            'registration_ids': devices,
            'alert': alert,
            'data': {
                'alert': alert,
                'payload': payload
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + apiKey
        }

        http = urllib3.PoolManager()
        url = config.ANDROID_GCM_URL

        # Send the message
        r = http.urlopen('POST', url, headers=headers, body=json.dumps(data))

        # Check failures
        response = json.loads(r.data)
        if response['failure'] == 1:
            self.log(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ': ' + r.data)

    def send_push_message(self, message):
        jsonMessage = json.loads(message)
        osType = jsonMessage['os_type']
        environment = jsonMessage['environment']
        devices = jsonMessage['devices']
        alert = jsonMessage['alert']
        payload = jsonMessage['payload']

        if osType == 'ios':
            self.send_push_to_ios(environment=environment, devices=devices, alert=alert, payload=payload)
        elif osType == 'android':
            self.send_push_to_android(environment=environment, devices=devices, alert=alert, payload=payload)

    def run(self):
        r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
        while True:
            time.sleep(3)
            message = r.lpop(config.REDIS_QUEUE_KEY)
            if message:
                self.send_push_message(message)


if __name__ == "__main__":
    daemon = NotificationServer(config.PID_FILE)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
