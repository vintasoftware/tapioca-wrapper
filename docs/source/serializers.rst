===========
Serializers
===========


Currently, serializers are only capable of deserilizing data but in future releases they will also be capable of serializing.

**Deserialization**: is the transformation of a data which is in a serialized format (eg.: text) into a native format. For example, this could be transforming a string containing a date into a native python ``Datetime`` instance.


Usage
=====
To deserialize data, you need to transform you client into a executor and then call a deserialization method from it. Eg.:

.. code-block:: python

	>>> reponse = cli().get()
	>>> print(response.created_at())
	<TapiocaClientExecutor object
	2015-10-25T22:34:51+00:00>
	>>> print(respose.created_at().to_datetime())
	2015-10-25 22:34:51+00:00
	>>> print(type(respose.created_at().to_datetime()))
	datetime.datetime

Clients might have the default ``SimpleSerializer``, some custom serializer designed by the wrapper creator, or even no serializer. Either way you can swap it for one of your own. For this, you only need to pass the desired serializer class during the client initialization.

.. code-block:: python
	
	from my_serializers import MyCustomSerializer

	cli = MyServiceClient(
		access_token='blablabla',
		serializer_class=MyCustomSerializer)


SimpleSerializer
================

``SimpleSerialzer`` is a very basic and generic serializer. It is included by default in adapters unless explicitly removed. These are the deserialization methods it provides:

.. method:: to_datetime()

Uses `Arrow <http://crsmithdev.com/arrow/>`_ to parse the data to a Python ``datetime``.

.. method:: to_decimal()

Converts data to ``Decimal``


Writing a custom serializer
===========================

To write a custom serializer, you just need to extend the ``BaseSerializer`` class and add the methods you want.

Deserializing
-------------
Any method starting with ``to_`` in your custom serializer class will be available for data deserialization.

.. code-block:: python
	
	from tapioca.serializers import BaseSerializer

	class MyCustomSerializer(BaseSerializer):

		to_striped(self, value):
			return value.strip()

Here a usage example for it:

.. code-block:: python
	
	from my_serializers import MyCustomSerializer

	cli = MyServiceClient(
		access_token='blablabla',
		serializer_class=MyCustomSerializer)

	response = cli.the_resource().get()

	striped_data = response.the_data().to_striped()
