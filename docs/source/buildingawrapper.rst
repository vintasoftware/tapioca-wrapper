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

Requesting Authentication (optional)
------------------------------------

.. method:: authorize_application()

Implement this method to authorize an application with a third party and document its call signature with examples. Some values should be hard-coded with the wrapper, for example, an authorization URL or the scope list might make sense to include hard-coded with your wrapper.

The return value should be the authorization parameters returned from a 3rd party app (e.g. a redirect URI that includes authentication data).

.. code-block:: python

    class MyClientAdapter(TapiocaAdapter):

        # other methods

        @classmethod
        def authorize_application(cls):
            # your implementation here

.. method:: request_token()

Implement this method to request an access token (such as an Oauth2 token) and document its call signature with examples.

The method should return a dictionary of at least an access token, along with metadata (e.g. expiry times, token type) and a refresh token if applicable.

.. code-block:: python

    class MyClientAdapter(TapiocaAdapter):

        # other methods

        @classmethod
        def request_token(cls):
            # your implementation here

.. method:: prompt_request_token()

Implement this method to walk the user through the steps of authorizing their application, and then obtaining a token. Some values may be hard-coded with the wrapper, for example, an authorization URL, the URL to obtain a token from, or the scope list.

.. code-block:: python

    class MyClientAdapter(TapiocaAdapter):

        # other methods

        @classmethod
        def prompt_request_token(cls):
            # your implementation here

An example prompt may be:

.. code-block:: python

    In [1]: MyWrapper.prompt_request_token()

    Enter your app's client id:
    <waits for user to enter client id>

    Enter your app's client secret:
    <waits for user to enter client secret>

    Enter your app's redirect URI:
    <waits for user to enter redirect URI>

    1. Please go to the following URL to authorize access:

    <prints url returned by the application authorization AND uses webbrowser.open()>

    2. Enter the full callback URL that your request was redirected to:
    <waits for user to enter callback URL>

    Out[1]:
    {'access_token': '<access token>',
     'expires_at': 1452733703.134222,
     'expires_in': 3600,
     'refresh_token': '<refresh token>',
     'token_type': 'Bearer'}

``requests-oauthlib`` has great examples of requesting tokens:
`https://requests-oauthlib.readthedocs.org/en/latest/examples/github.html`_