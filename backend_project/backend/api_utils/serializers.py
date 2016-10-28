from rest_framework import serializers


def datetime_to_timestamp(dt):
        return dt.strftime("%s")


class CookboothModelSerializer(serializers.ModelSerializer):
    def datetime_to_timestamp(self, dt):
        return datetime_to_timestamp(dt)

    def transform_creation_date(self, obj, value):
        return self.datetime_to_timestamp(obj.creation_date)

    def transform_edit_date(self, obj, value):
        return self.datetime_to_timestamp(obj.edit_date)
