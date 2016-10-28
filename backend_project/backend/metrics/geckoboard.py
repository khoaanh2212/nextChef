# -*- coding: utf-8 -*-
import json
import requests

from django.conf import settings
from .models import Metric


class GeckoBoard(object):
    API_URL = 'https://push.geckoboard.com/v1/send/'

    # Geckoboard widget IDs
    WIDGET_WEEKLY_USERS = "107628-cf872a38-9803-43f7-a2fe-17195aec9979"
    WIDGET_WEEKLY_FOLLOWS = "107628-25b26238-cbb2-4165-8f62-f5361c34599a"
    WIDGET_WEEKLY_LIKES = "107628-c755857d-c157-4b57-93f2-113c4569802f"
    WIDGET_WEEKLY_COMMENTS = "107628-175d8dc5-1e40-45a2-b831-abf429fc6564"
    WIDGET_RECIPES_CREATED = "107628-a52fb33d-21f8-419b-a791-e7976a763acf"

    @staticmethod
    def push_weekly_metric(kpi, segment=Metric.SEG_ALL):
        """
        Send weekly series of specified metric to Widget
        """
        if settings.GB_DISABLED:
            return None

        if kpi == Metric.KPI_REGISTERED_USERS:
            widget_id = GeckoBoard.WIDGET_WEEKLY_USERS
        elif kpi == Metric.KPI_TOTAL_FOLLOWS:
            widget_id = GeckoBoard.WIDGET_WEEKLY_FOLLOWS
        elif kpi == Metric.KPI_TOTAL_LIKES:
            widget_id = GeckoBoard.WIDGET_WEEKLY_LIKES
        elif kpi == Metric.KPI_TOTAL_COMMENTS:
            widget_id = GeckoBoard.WIDGET_WEEKLY_COMMENTS
        elif kpi == Metric.KPI_TOTAL_RECIPES:
            widget_id = GeckoBoard.WIDGET_RECIPES_CREATED
        else:
            return None

        push_url = GeckoBoard.API_URL + widget_id

        points = Metric.objects.filter(kpi=kpi, segment=segment).values_list('value_num', flat=True)\
            .order_by("created")[:7]

        last_point = Metric.objects.filter(kpi=kpi, segment=segment).values_list('value_num', flat=True)\
            .order_by("-created")[:1]

        if last_point:
            last_value = last_point[0]
        else:
            last_value = 0

        item = [dict(value=last_value), list(points)]
        data = dict(item=item)
        payload = dict(api_key=settings.GB_API_KEY, data=data)
        headers = {'content-type': 'application/json'}

        r = requests.post(push_url, data=json.dumps(payload), headers=headers)
        return r.status_code

    @staticmethod
    def push_recipes_created(total, pros, foodies):
        """
        Send number of recipes created to a RAG widget

        :param total: Total recipes created with more than 3 photos
        :param pros: Number of recipes created by Pro users
        :param foodies: Number of recipes created by foodies
        :return: None of HTTP status code
        """
        if settings.GB_DISABLED:
            return None

        widget_id = GeckoBoard.WIDGET_RECIPES_CREATED
        push_url = GeckoBoard.API_URL + widget_id

        item = [dict(value=total, text="Total"),
                dict(value=foodies, text="Foodies"),
                dict(value=pros, text="Chefs")]

        data = dict(item=item)
        payload = dict(api_key=settings.GB_API_KEY, data=data)
        headers = {'content-type': 'application/json'}

        r = requests.post(push_url, data=json.dumps(payload), headers=headers)
        return r.status_code
