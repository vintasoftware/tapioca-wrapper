
import arrow
from decimal import Decimal


class BaseSerializer(object):

    def deserialize(self, method_name, value, **kwargs):
        if hasattr(self, method_name):
            return getattr(self, method_name)(value, **kwargs)
        raise NotImplementedError("Desserialization method not found")

    def serialize_dict(self, data):
        serialized = {}

        for key, value in data.items():
            serialized[key] = self.serialize(value)

        return serialized

    def serialize_list(self, data):
        serialized = []
        for item in data:
            serialized.append(self.serialize(item))

        return serialized

    def serialize(self, data):
        data_type = type(data).__name__

        serialize_method = ('serialize_' + data_type).lower()
        if hasattr(self, serialize_method):
            return getattr(self, serialize_method)(data)

        return data


class SimpleSerializer(BaseSerializer):

    def to_datetime(self, value):
        return arrow.get(value).datetime

    def to_decimal(self, value):
        return Decimal(value)

    def serialize_decimal(self, data):
        return str(data)

    def serialize_datetime(self, data):
        return arrow.get(data).isoformat()
