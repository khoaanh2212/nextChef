from rest_framework import renderers
from rest_framework.negotiation import BaseContentNegotiation


class CookboothRenderer(renderers.JSONRenderer):
    media_type = 'text/json'
    format = 'json'


class IgnoreClientContentNegotiation(BaseContentNegotiation):
    """
    We are allowing any header passed by the app
    """
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)