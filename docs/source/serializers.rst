===========
Serializers
===========


Serializer classes are capable of performing serialization and deserialization of data.

**Serialization** is the transformation of data in a native format (in our case Python data types) into a serialized format (e.g. text). For example, this could be transforming a native Python ``Datetime`` instance containing a date into a string.

**Deserialization** is the transformation of data in a serialized format (e.g. text) into a native format. For example, this could be transforming a string containing a date into a native Python ``Datetime`` instance.


Usage
=====

Serialization
-------------

Data serialization is done in the background when tapioca is executing the request. It will traverse any data structure passed to the ``data`` param of the request and convert Python data types into serialized types.

.. code-block:: python

	>>> reponse = cli.the_resource().post(data={'date': datetime.today()})

In this example, ``datetime.today()`` will be converted into a string formatted date just before the request is executed.

Deserialization
---------------

To deserialize data, you need to transform your client into an executor and then call a deserialization method from it:

.. code-block:: python

	>>> reponse = cli.the_resource().get()
	>>> print(response.created_at())
	<TapiocaClientExecutor object
	2015-10-25T22:34:51+00:00>
	>>> print(respose.created_at().to_datetime())
	2015-10-25 22:34:51+00:00
	>>> print(type(respose.created_at().to_datetime()))
	datetime.datetime


Swapping the default serializer
-------------------------------

Clients might have the default ``SimpleSerializer``, some custom serializer designed by the wrapper creator, or even no serializer. Either way, you can swap it for one of your own even if you were not the developer of the library. For this, you only need to pass the desired serializer class during the client initialization:

.. code-block:: python
	
	from my_serializers import MyCustomSerializer

	cli = MyServiceClient(
		access_token='blablabla',
		serializer_class=MyCustomSerializer)


Built-ins
=========

.. class:: SimpleSerializer

``SimpleSerializer`` is a very basic and generic serializer. It is included by default in adapters unless explicitly removed. These are the deserialization methods it provides:

.. method:: to_datetime()

Uses `Arrow <http://crsmithdev.com/arrow/>`_ to parse the data to a Python ``datetime``.

.. method:: to_decimal()

Converts data to ``Decimal``


Writing a custom serializer
===========================

To write a custom serializer, you just need to extend the ``BaseSerializer`` class and add the methods you want. But you can also extend from ``SimpleSerializer`` to inherit its functionalities.

Serializing
-----------
To allow serialization of any desired data type, add a method to your serializer named using the following pattern: ``serialize_ + name_of_your_data_type_in_lower_case``. For example:

.. code-block:: python

	class MyCustomDataType(object):
		message = ''

	class MyCustomSerializer(SimpleSerializer):

		def serialize_mycustomdatatype(self, data):
			return data.message


Deserializing
-------------
Any method starting with ``to_`` in your custom serializer class will be available for data deserialization.

.. code-block:: python
	
	from tapioca.serializers import BaseSerializer

	class MyCustomSerializer(BaseSerializer):

		def to_striped(self, value):
			return value.strip()

Here's a usage example for it:

.. code-block:: python
	
	from my_serializers import MyCustomSerializer

	cli = MyServiceClient(
		access_token='blablabla',
		serializer_class=MyCustomSerializer)

	response = cli.the_resource().get()

	striped_data = response.the_data().to_striped()
