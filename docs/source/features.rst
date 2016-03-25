========
Features
========

Here are some features tapioca supports. The wrapper you are using may support them or not, it will depend on the `tapioca-wrapper` version it is tied to and if the developer implemented the methods needed to support the feature. Either way, if you find yourself in a situation where you need one of these features, clone the wrapper, update the `tapioca-wrapper` version to the latest one, implement the features you need and submit a pull request to the developer. You will be helping a lot of people!


TapiocaClient
=============

The first object you get after you instanciate a tapioca wrapper is an instance of the ``TapiocaClient`` class. This class is capable of accessing the API endpoints of the wrapper and traversing respose objects. No other action besides those can be achieved from a ``TapiocaClient``. To retrieve the raw data returned from the API call you will need to transform it in a ``TapiocaClientExecutor``.

**TODO: add examples**

TapiocaClientExecutor
=====================

Everytive you ``call`` in ``TapiocaClient`` you will get a ``TapiocaClientExecutor``. Here are the features available in a ``TapiocaClientExecutor``:

Accessing raw response data
---------------------------

To access the raw data contained in the executor, use the ``data`` **attribute**. To access the raw response, use the ``response`` **attribute**. To access the status code of the response, use the ``status_code`` **attribute**.

**TODO: add examples**

HTTP calls
----------

Executors have access to make HTTP calls using the current data it possesses as the URL. `requests <http://docs.python-requests.org/en/latest/>`_ library, is used as the engine to perform API calls. Every key word parameter you pass to: ``get()``, ``post()``, ``put()``, ``patch()``, ``delete()`` methods will be directly passed to the request library call. This means you will be using ``params={'myparam': 'paramvalue'}`` to send querystring arguments in the url and ``data={'datakey': 'keyvalue'}`` to send data in the body of the request.

**TODO: add examples**

Auth refreshing (\*)
--------------------

Make any HTTP call passing ``refresh_auth=True`` and in case you have an expired API token, it will automatically be refreshed and the call retried.

**TODO: add examples**

*the wrapper you are current using may not support this feature

Pagination (\*)
---------------

Use ``pages()`` method to call an endpoint that returns a collection of objects in batches. This will make your client automatically fetch more data untill there is none more left. You may use ``max_pages`` and/or ``max_items`` to limit the number of items you want to iterate over.

**TODO: add examples**

*the wrapper you are current using may not support this feature

Open docs (\*)
--------------

When accessing an endpoint, you may want to read it's documentation in the internet. By calling ``open_docs()`` in a python interactive session, the doc page will be openned in a browser.

**TODO: add examples**

*the wrapper you are current using may not support this feature

Open in the browser (\*)
------------------------

Whenever the data contained in the executor is a URL, you can directly open it in the browser from an interactive session by calling ``open_in_browser()``

**TODO: add examples**

*the wrapper you are current using may not support this feature

Exceptions
==========

Tapioca built in exceptions will help you to beautifuly catch and handle whenever there is a client or server error. Make sure the wrapper you are using correctly raises exceptions, the developer might not have treated this. Please refer to the :doc:`exceptions <exceptions>` for more information about exceptions.

Serializers
===========

Serializers will help you processing data before it is sent to the endpoint and transforming data from responses into python objects. 

.. code-block:: python

	from tapioca import TapiocaAdapter
	from tapioca.serializers import SimpleSerializer

	class MyAPISerializer(SimpleSerializer):
		
		def serialize_datetime(self, data):
        	return data.isoformat()


    class MyAPIAdapter(TapiocaAdapter):
    	serializer_class = MyAPISerializer

    	...

In the example, everytime a ``datetime`` is passed to the parameters of a HTTP method, it will be converted to a iso formated ``string``.

Please refer to the :doc:`serializers <serializers>` for more information about serializers.
