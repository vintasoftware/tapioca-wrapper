
import arrow
from decimal import Decimal


class BaseSerializer(object):

    def deserialize(self, method_name, value):
        if hasattr(self, method_name):
            return getattr(self, method_name)(value)
        raise NotImplementedError("Desserialization method not found")


class SimpleSerializerMixin(object):

    def to_datetime(self, value):
        return arrow.get(value).datetime

    def to_decimal(self, value):
        return Decimal(value)


class SimpleSerializer(SimpleSerializerMixin, BaseSerializer):
    pass
