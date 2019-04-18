====================
TapiocaAdapter class
====================

.. class:: TapiocaAdapter

Attributes
----------

.. attribute:: api_root

This should contain the base URL that will be concatenated with the resource mapping itens and generate the final request URL. You can either set this attribute or use the ``get_api_root`` method.

.. attribute:: serializer_class

For more information about the ``serializer_class`` attribute, read the :doc:`serializers documentation <serializers>`.


Methods
-------

.. method:: get_api_root(self, api_params, \*\*kwargs)

This method can be used instead of the ``api_root`` attribute. You might also use it to decide which base URL to use according to a user input.

.. code-block:: python

	def get_api_root(self, api_params, **kwargs):
		if api_params.get('development'):
			return 'http://api.the-dev-url.com/'
		return 'http://api.the-production-url.com/'

You may also need to set different api_root to a specific resource. To do that you can access the ``resource_name`` inside ``kwargs``.

.. code-block:: python

    def get_api_root(self, api_params, **kwargs):
        if kwargs.get('resource_name') == 'some_resource_name':
            return 'http://api.another.com/'
        else:
            return self.api_root

.. method:: get_request_kwargs(self, api_params, \*args, \*\*kwargs)

This method is called just before any request is made. You should use it to set whatever credentials the request might need. The **api_params** argument is a dictionary and has the parameters passed during the initialization of the tapioca client:

.. code-block:: python
	
	cli = Facebook(access_token='blablabla', client_id='thisistheis')

For this example, api_params will be a dictionary with the keys ``access_token`` and ``client_id``.

Here is an example of how to implement Basic Auth:

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

.. method:: process_response(self, response)

This method is responsible for converting data returned in a response to a dictionary (which should be returned). It should also be used to raise exceptions when an error message or error response status is returned.

.. method:: format_data_to_request(self, data)

This converts data passed to the body of the request into text. For example, if you need to send JSON, you should use ``json.dumps(data)`` and return the response. **See the mixins section above.**

.. method:: response_to_native(self, response)

This method receives the response of a request and should return a dictionay with the data contained in the response. **see the mixins section above.**

.. method:: get_iterator_next_request_kwargs(self, iterator_request_kwargs, response_data, response)

Override this method if the service you are using supports pagination. It should return a dictionary that will be used to fetch the next batch of data, e.g.:

.. code-block:: python
	
	def get_iterator_next_request_kwargs(self,
			iterator_request_kwargs, response_data, response):
		paging = response_data.get('paging')
		if not paging:
			return
		url = paging.get('next')

		if url:
			iterator_request_kwargs['url'] = url
			return iterator_request_kwargs

In this example, we are updating the URL from the last call made. ``iterator_request_kwargs`` contains the paramenters from the last call made, ``response_data`` contains the response data after it was parsed by ``process_response`` method, and ``response`` is the full response object with all its attributes like headers and status code. 

.. method:: get_iterator_list(self, response_data)

Many APIs enclose the returned list of objects in one of the returned attributes. Use this method to extract and return only the list from the response.

.. code-block:: python

	def get_iterator_list(self, response_data):
		return response_data['data']

In this example, the object list is enclosed in the ``data`` attribute.

.. method:: is_authentication_expired(self, exception, \*args, \*\*kwargs)

Given an exception, checks if the authentication has expired or not. If so and ```refresh_token_by_default=True``` or
the HTTP method was called with ```refresh_token=True```, then it will automatically call ```refresh_authentication```
method and retry the original request.

If not implemented, ```is_authentication_expired``` will assume ```False```, ```refresh_token_by_default``` also
defaults to ```False``` in the client initialization.

.. method:: refresh_authentication(self, api_params, \*args, \*\*kwargs): 

Should do refresh authentication logic. Make sure you update `api_params` dictionary with the new token. If it successfully refreshs token it should return a truthy value that will be stored for later access in the executor class in the ``refresh_data`` attribute. If the refresh logic fails, return a falsy value. The original request will be retried only if a truthy is returned.
