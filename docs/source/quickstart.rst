==========
Quickstart
==========

Using a tapioca package
=======================

**Yes, you are in the right place**

There is a good chance you found this page because you clicked a link from some python package called **tapioca-SOMETHING**. Well, welcome! You are in the right place. This page will teach you the basics of how to use the package that sent you here. If you didn't arrive here from another package, then please keep reading. The concepts learned here apply to any tapioca-**package** available.

What's tapioca?
===============

**tapioca** is an *API wrapper maker*. It helps Python developers creating packages for APIs (like the :ref:`Facebook Graph API <flavour-facebook>` or the :ref:`Twitter REST API <flavour-twitter>`. You can find a full list of available API packages made with tapioca :doc:`here <flavours>`.  

All wrappers made with tapioca follow a simple interaction pattern that works uniformly, so once you learn how tapioca works, you will be able to work with any tapioca package available.

Getting started
===============

We will use ``tapioca-facebook`` as example to guide us through tapioca concepts. Let's install ``tapioca-facebook``:

.. code-block:: bash

	$ pip install tapioca-facebook

To better experience tapioca, we will also use IPython:

.. code-block:: bash

	$ pip install ipython

Let's explore!  

Go to  `https://developers.facebook.com/tools/explorer/ <https://developers.facebook.com/tools/explorer/>`_, click "Get Access Token", select all "User Data Permissions" and "Extended Permissions", and click "Get Access Token". This will give you a temporary access token to play with Facebook API. In case it expires, just generate a new one.

TapiocaClient object
====================

This is how you initialize your tapioca client:

.. code-block:: python

	from tapioca_facebook import Facebook

	api = Facebook(access_token='{your_genereated_access_token}')


If you are using IPython, you can now list available endpoints by typing ``api.`` and pressing ``tab``.

.. code-block:: python

	>>> api.
	api.user_likes                  api.page_blocked                 api.page_locations
	api.page_statuses                api.user_applications_developer  api.user_friends
	api.user_invitable_friends       api.user_photos                  api.user_videos
	api.object                       api.page_conversations           api.page_milestones
	...


Resources
---------

Those are the available endpoints for the Facebook API. As we can see, there is one called ``user_likes``. Let's take a closer look.

Type ``api.user_likes?`` and press ``enter``.

.. code-block:: python

	In [3]: api.user_likes?
	...
	Docstring:
	Automatic generated __doc__ from resource_mapping.
	Resource: {id}/likes
	Docs: https://developers.facebook.com/docs/graph-api/reference/v2.2/user/likes


As we can see, the ``user_likes`` resource requires an ``id`` to be passed to the URL. Let's do it:

.. code-block:: python

	api.user_likes(id='me')


Fetching data
-------------

To request the current user likes, its easy:

.. code-block:: python

	likes = api.user_likes(id='me').get()


To print the returned data:

.. code-block:: python

	In [9]: likes().data
	OUT [9]: {
		'data': [...],
		'paging': {...}
	}


Exploring data
--------------

We can also explore the returned data using the IPython ``tab`` auto-complete:

.. code-block:: python

	In [9]: likes.
	likes.data    likes.paging


Iterating over data
-------------------

You can iterate over returned data:

.. code-block:: python

	likes = api.user_likes(id='me').get()

	for like in likes.data:
		print(like.id().data)

Items passed to the ``for`` loop will be wrapped in tapioca so you still have access to all features.

TapiocaClientExecutor object
============================

Whenever you make a "call" on a ``TapiocaClient``, it will return an ``TapiocaClientExecutor`` object. You will use the executor every time you want to perform an action over data you possess. 

We did this already when we filled the URL parameters for the ``user_like`` resource (calling it and passing the argument ``id='me'``). In this new object, you will find many methods to help you play with the data available.

Here is the list of the methods available in a ``TapiocaClientExecutor``:

Making requests
---------------

Tapioca uses the `requests <http://docs.python-requests.org/en/latest/>`_ library to make requests so HTTP methods will work just the same (get()/post()/put()/delete()/head()/options()). The only difference is that we don't need to pass a URL since tapioca will take care of this.

.. code-block:: python

	likes = api.user_likes(id='me').get()


**URL params**

To pass query string parameters in the URL, you can use the ```params``` parameter:

.. code-block:: python

	likes = api.user_likes(id='me').get(
		params={'limit': 5})

This will return only 5 results.

**Body data**

If you need to pass data in the body of your request, you can use the ```data``` parameter. For example, let's post a message to a Facebook wall:

.. code-block:: python

	# this will only work if you have a post to wall permission
	api.user_feed(id='me').post(
		data={'message': 'I love tapiocas!! S2'})

Please read `requests <http://docs.python-requests.org/en/latest/>`_ for more detailed information about how to use HTTP methods. 

Accessing raw data
------------------

Use ``data`` to return data contained in the Tapioca object.

.. code-block:: python

	>>> likes = api.user_likes(id='me').get()
	>>> likes().data
	{
		'data': [...],
		'paging': {...}
	}
	>>> this will print only the array contained 
	>>> # in the 'data' field of the response
	>>> likes.data().data
	>>> [...]

Dynamically fetching pages
-------------------------

Many APIs use a paging concept to provide large amounts of data. This way, data is returned in multiple requests to avoid a single long request. Tapioca is built to provide an easy way to access paged data using the ``pages()`` method:

.. code-block:: python

	likes = api.user_likes(id='me').get()

	for like in likes().pages():
		print(like.name().data

This will keep fetching user likes until there are none left. Items passed to the ``for`` loop will be wrapped in tapioca so you still have access to all features.

This method also accepts ``max_pages`` and ``max_items`` parameters. If both parameters are used, the ``for`` loop will stop after ``max_pages`` are fetched or ``max_items`` are yielded, whichever comes first:

.. code-block:: python

	for item in resp().pages(max_pages=2, max_items=40):
		print(item)
	# in this example, the for loop will stop after two pages are fetched or 40 items are yielded, 
	# whichever comes first.

Accessing wrapped data attributes
---------------------------------

It's possible to access wrapped data attributes on executor. For example, it's possible to reverse a wrapped list:

.. code-block:: python

	likes = api.user_likes(id='me').get()

	likes_list = likes.data
	likes_list().reverse() 
	# items in the likes_list are now in reverse order
	# but still wrapped in a tapioca object

Opening documentation in the browser
------------------------------------

If you are accessing a resource, you can call ``open_docs`` to open the resource documentation in a browser:

.. code-block:: python

	api.user_likes().open_docs()

Opening any link in the browser
-------------------------------

Whenever the data contained in a tapioca object is a URL, you can open it in a browser by using the ``open_in_browser()`` method.


For more information on what wrappers are capable of, please refer to the :doc:`features <features>` section.
