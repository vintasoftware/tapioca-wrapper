========================
Generating Access Tokens
========================

Overview
========

**This may not be implemented, or relevant, for your Tapioca wrapper**

Tapioca provides methods to assist with obtaining access tokens, such as for Oauth2. These are called directly on the wrapper class:

.. code-block:: python

    In [1]: MyWrapper.prompt_request_token()

.. method:: authorize_application()

Helps you authorize your application with a third party, may return a URL that has to be handled. See wrapper documentation for use.

.. method:: request_token()

Requests a new access token using your credentials. See wrapper documentation for use.

.. method:: prompt_request_token()

For shell use, takes you through the steps of obtaining an access token.

.. code-block:: python

	from tapioca_mywrapper import MyWrapper

	# call prompt_request_token on the uninstantiated wrapper
	MyWrapper.prompt_request_token()

	# follow the prompt to get the token <mytoken>

	# instantiate your api wrapper with <mytoken> and any other required parameters
	# see wrapper documentation for call signature
	api = MyWrapper(**kwargs)
