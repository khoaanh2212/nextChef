from rest_framework.pagination import PaginationSerializer


class CookboothPaginationSerializer(PaginationSerializer):
    def to_native(self, obj):
        ret = super(CookboothPaginationSerializer, self).to_native(obj)
        del ret['count']
        if not ret['previous']:
            del ret['previous']
        if not ret['next']:
            del ret['next']
        return ret
