==================
Building a wrapper
==================


Wrapping an API with Tapioca
============================

The easiest way to wrap an API using tapioca is starting from the `cookiecutter template <https://github.com/vintasoftware/cookiecutter-tapioca>`_. 

To use it, install cookiecutter in your machine:

.. code-block:: bash

	pip install cookiecutter

and then use it to download the template and run the config steps:

.. code-block:: bash

	cookiecutter gh:vintasoftware/cookiecutter-tapioca

After this process, it's possible that you have a ready to go wrapper. But in most cases you will need to customize stuff. Read through this document to understand what methods are available and how your wrapper can make the most of tapioca. Also, you might want to take a look in the source code of :doc:`other wrappers <flavours>` to get more ideas. 

In case you are having any difficulties, seek help on `Gitter <https://gitter.im/vintasoftware/tapioca-wrapper>`_ or send an email to contact@vinta.com.br .

Adapter
=======

Tapioca features are mainly implemented in the ``TapiocaClient`` and ``TapiocaClientExecutor`` classes. Those are generic classes common to all wrappers and cannot be customized to specific services. All the code specific to the API wrapper you are creating goes in your adapter class, which should inherit from ``TapiocaAdapter`` and implement specific behaviours to the service you are working with. 

Take a look in the generated code from the cookiecutter or in the `tapioca-facebook adapter <https://github.com/vintasoftware/tapioca-facebook/blob/master/tapioca_facebook/tapioca_facebook.py>`_ to get a little familiar with it before you contiue. Note that at the end of the module you will need to perform the transformation of your adapter into a client:

.. code-block:: python

	Facebook = generate_wrapper_from_adapter(FacebookClientAdapter)

Plase refer to the :doc:`TapiocaAdapter class <adapter_class>` document for more information on the available methods.

Features
========

Here is some information you should know when building your wrapper. You may chose to or not to support features marked with `(optional)`.

Resource Mapping
----------------

The resource mapping is a very simple dictionary which will tell your tapioca client about the available endpoints and how to call them. There's an example in your cookiecutter generated project. You can also take a look at `tapioca-facebook's resouce mapping <https://github.com/vintasoftware/tapioca-facebook/blob/master/tapioca_facebook/resource_mapping.py>`_.

Tapioca uses `requests <http://docs.python-requests.org/en/latest/>`_ to perform HTTP requests. This is important to know because you will be using the method ``get_request_kwargs`` to set authentication details and return a dictionary that will be passed directly to ther request method. 


Formating data
--------------

Use the methods ``format_data_to_request`` and ``response_to_native`` to correctly treat data leaving and being received in your wrapper.

**TODO: add examples**

You might want to use one of the following mixins to help you with data format handling in your wrapper: 

- ``FormAdapterMixin`` 
- ``JSONAdapterMixin``
- ``XMLAdapterMixin``


Exceptions
----------

Overwrite the ``process_response`` method to identify API server and client errors raising the correct exception accordingly. Please refer to the :doc:`exceptions <exceptions>` for more information about exceptions.

**TODO: add examples**

Pagination (optional)
---------------------

``get_iterator_list`` and ``get_iterator_next_request_kwargs`` are the two methods you will need to implement for the executor ``pages()`` method to work.

**TODO: add examples**

Serializers (optional)
----------------------

Set a ``serializer_class`` attribute or overwrite the ``get_serializer()`` method in your wrapper for it to have a default serializer. Please refer to the :doc:`serializers <serializers>` for more information about serializers.

**TODO: add examples**


Refreshing Authentication (optional)
------------------------------------

You can implement the ```refresh_authentication``` and ```is_authentication_expired``` methods in your Tapioca Client to refresh your authentication token every time that it expires.
```is_authentication_expired``` receives an error object from the request method (it contains the server response and HTTP Status code). You can use it to decide if a request failed because of the token. This method should return true if the authentication is expired or false otherwise. If the authentication is expired, ```refresh_authentication``` is called automatically.

.. code-block:: python

    def is_authentication_expired(self, exception, *args, **kwargs):
        ....
    

    def refresh_authentication(self, api_params, *args, **kwargs):
        ...


XMLAdapterMixin Configuration (only if required)
------------------------------------------------

Additionally, the XMLAdapterMixin accepts configuration keyword arguments to be passed to the xmltodict library during parsing and unparsing by prefixing the xmltodict keyword with ``xmltodict_parse__`` or ``xmltodict_unparse`` respectively. These parameters should be configured so that the end-user has a consistent experience across multiple Tapioca wrappers irrespective of various API requirements from wrapper to wrapper.

Note that the end-user should **not** need to modify these keyword arguments themselves. See xmltodict `docs <http://xmltodict.readthedocs.org/en/latest/>`_ and `source <https://github.com/martinblech/xmltodict>`_ for valid parameters.

Users should be able to construct dictionaries as defined by the xmltodict library, and responses should be returned in the canonical format.

Example XMLAdapterMixin configuration keywords:

.. code-block:: python

    class MyXMLClientAdapter(XMLAdapterMixin, TapiocaAdapter):
        ...
        def get_request_kwargs(self, api_params, *args, **kwargs):
            ...
            # omits XML declaration when constructing requests from dictionary
            kwargs['xmltodict_unparse__full_document'] = False
            ...
