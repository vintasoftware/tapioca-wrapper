============
New Flavours
============


Wrapping an API with Tapioca
============================

The easiest way to wrap an API using tapioca is starting from the `cookiecuter template <https://github.com/vintasoftware/cookiecutter-tapioca>`_. 

To use it, install cookiecutter in your machine:

.. code-block:: bash

	pip install cookiecutter

and then use it to download the template and run the config steps

.. code-block:: bash

	cookiecutter gh:vintasoftware/cookiecutter-tapioca

After this process it's possible that you have a ready to go wrapper. But in most cases you will need to customize stuff. Read through this document to understand what methods are available and how your wrapper can take the most of tapioca. Also, you might want to take a look in the source code of :doc:`other wrappers <flavours>` to get more ideas. 

In case you are having any difficulties, seek help on `Gitter <https://gitter.im/vintasoftware/tapioca-wrapper>`_ or send an email to contact@vinta.com.br .

The Adapter
===========

Tapioca features are mainly implemente in the ``TapiocaClient`` and ``TapiocaClientExecutor`` classes. Those are generic, common to all wrappers and cannot be customized to specific services. All the code specific to the API wrapper you are creating goes in your adapter class which should inherit from ``TapiocaAdapter`` and implement specific behaviours to the service you are working with. 

Take a look in the generated code from the cookiecutter or in the `tapioca-facebook adapter <https://github.com/vintasoftware/tapioca-facebook/blob/master/tapioca_facebook/tapioca_facebook.py>`_ to get a little familiar with it before you contiue. Note that in the end of the file you will need to perform the transformation of your adapter into a client:

.. code-block:: python

	Facebook = generate_wrapper_from_adapter(FacebookClientAdapter)


The Resouce Mapping
===================

The resource mapping is a very simple dictionary which will tell your tapioca client what are the available endpoints and how to call them. There's an exemplo in your cookiecutter generated project. You can also take a look into `tapioca-facebook's resouce mapping <https://github.com/vintasoftware/tapioca-facebook/blob/master/tapioca_facebook/resource_mapping.py>`_.

Tapioca uses `requests <http://docs.python-requests.org/en/latest/>`_ to perform HTTP requests. This is important to know because you will be using the method ``get_request_kwargs`` to set authentication details and return a dictionary that will be passed directly to ther request method. 


Data formating Mixins
=====================

You might want to use one of the following mixins to help you with data format handling in you wrapper: 

- ``FormAdapterMixin`` 
- ``JSONAdapterMixin``


.. class:: TapiocaAdapter

Attributes
----------

.. attribute:: api_root

This should contain the base url that will be concatenated with the resource mapping itens and generate the final request url. You can either set this attribute or use the ``get_api_root`` method.

.. attribute:: serializer_class

For more information about ``serializer_class`` attribute read the :doc:`serializers documentation <serializers>`.

Methods
-------

.. method:: get_api_root(self, api_params)

Can be used instead of the ``api_root`` attribute. You might also use it the decide which base url to use according to a user input.

.. code-block:: python

	def get_api_root(self, api_params):
		if api_params.get('development'):
			return 'http://api.the-dev-url.com/'
		return 'http://api.the-production-url.com/'

.. method:: get_request_kwargs(self, api_params, *args, **kwargs)

This method is called just before any request is made, you should use it to set whatever credetials the request migh need. The **api_params** argument is a dictionary and has the parameters passed during the initialization of the tapioca client:

.. code-block:: python
	
	cli = Facebook(access_token='blablabla', client_id='thisistheis')

for this example, api_params will be a dictionary with the keys ``access_token`` and ``client_id``.

Here is an example on how to implement Basic Auth:

.. code-block:: python

	from requests.auth import HTTPBasicAuth

	class MyServiceClientAdapter(TapiocaAdapter):
		...
		def get_request_kwargs(self, api_params, *args, **kwargs):
			params = super(MyServiceClientAdapter, self).get_request_kwargs(
				api_params, *args, **kwargs)

			params['auth'] = HTTPBasicAuth(
				api_params.get('user'), api_params.get('password'))

			return params


