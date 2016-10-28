# -*- coding: utf-8 -*-
from django.conf import settings

import geoip2.webservice
from geoip2.errors import GeoIP2Error, HTTPError
import redis


def get_ip(request):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = request.META.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


def get_country_from_ip(ip):
    """
    Use GeoIP Service for country lookup from user IP address
    :param ip:
    :return: string Country ISO Code
    """
    # If we are in development environments don't call GEOIP Service
    if not settings.GEOIP_KEY:
        return None

    try:
        client = geoip2.webservice.Client(settings.GEOIP_USER, settings.GEOIP_KEY)
        response = client.country(ip)
        return response.country.iso_code
    except HTTPError:
        return None
    except GeoIP2Error:
        # If we have an error calling GEOIP, we need to flag the user so not calling again and
        # consume API calls
        return 'ERR'


def get_redis():
    return redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                             db=settings.REDIS_DB)
