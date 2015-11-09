==========
Exceptions
==========

Catching API errors
===================

Tapioca supports 2 main types of exceptions: ``ClientError`` and ``ServerError``. The default implementation raises ``ClientError`` for HTTP response 4xx status codes, and ``ServerError`` for 5xx status codes. Since each API has it own ways of reporting errors and not all of them follow HTTP recommendations to status codes, this can be overriden by each implemented client to reflect it's behaviour. 
Both of this exceptions extend from ``TapiocaException`` which can be used to catch errors in a more generic way.


.. class:: TapiocaException

Base class for tapioca exceptions. Example usage:

.. code-block:: python

	from tapioca.exceptions import TapiocaException

	try:
		cli.fetch_something().get()
	except TapiocaException, e:
		print("API call failed with error %s", e.status)

You can also access a tapioca client that contains response data from the exception:

.. code-block:: python

	from tapioca.exceptions import TapiocaException

	try:
		cli.fetch_something().get()
	except TapiocaException, e:
		print(e.client.error_message().data)

.. class:: ClientError

Default exception for client errors. Extends from ``TapiocaException``.

.. class:: ServerError

Default exception for server errors. Extends from ``TapiocaException``.
