from base64 import b64decode
from imghdr import what

from django.db.models.fields.files import ImageFieldFile
from django.core.files.base import ContentFile

from rest_framework.fields import BooleanField, WritableField


class IntegerBooleanField(BooleanField):
    def to_native(self, value):
        ret = super(IntegerBooleanField, self).to_native(value)
        return 1 if ret else 0


class Base64ImageField(WritableField):
    ACCEPTED_FORMATS = ('gif', 'jpeg', 'png')

    def __init__(self, accepted_formats=None, *args, **kwargs):
        if accepted_formats is None:
            self.accepted_formats = self.ACCEPTED_FORMATS
        else:
            self.accepted_formats = accepted_formats
        super(Base64ImageField, self).__init__(*args, **kwargs)

    def from_native(self, value):
        if not value:
            return None

        value = b64decode(value)
        ext = what(None, value)
        if not ext in self.accepted_formats:
            return None

        data = ContentFile(value, name='temp.' + ext)
        return super(Base64ImageField, self).from_native(data)

    def field_to_native(self, obj, field_name):
        if self.write_only:
            return None
        field = getattr(obj,field_name)
        if isinstance(field, ImageFieldFile):
            return field.url if field else None
        return super(WritableField, self).field_to_native(obj, field_name)
