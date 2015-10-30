==========
Quickstart
==========

Using a tapioca package
=======================

**Yes, you are in the right place**

There is a good chance you found this page because you clicked a link from some python package called **tapioca-*SOMETHING* **. Well, welcome! You are in the right place, this page will teach you the basics of how to use the package that sent you here. If you didn't arrive here from other package, please keep reading, the concepts learned here applies to any tapioca-***package*** available.

What's tapioca?
===============

**tapioca** is a *API wrapper maker*. It helps Python developers creating packages for APIs (like the :ref:`Facebook Graph API <flavour-facebook>` or the :ref:`Twitter REST API <flavour-twitter>`. You can find a full list of available API packages made with tapioca :doc:`here <flavours>`.  

All wrappers made with tapioca follow a simple interaction pattern that works uniformly so once you learn how tapioca works you will be able to work with any tapioca package available.

Getting started
===============

We will use ``tapioca-facebook`` as example to guide us through tapioca concepts.
Lets install ``tapioca-facebook``:

.. code-block:: bash

	$ pip install tapioca-facebook

To better experience tapioca, we will also use iPython:

.. code-block:: bash

	$ pip install ipython

Lets explore!  

Go to  `https://developers.facebook.com/tools/explorer/ <https://developers.facebook.com/tools/explorer/>`_, click "Get Access Token", select all "User Data Permissions" and "Extended Permissions" and click "Get Access Token". This will give you a temporary access token to play with Facebook API. In case it expires, just generate a new one.

TapiocaClient object
====================

This is how you initialize your tapioca client:

.. code-block:: python

	from tapioca_facebook import Facebook

	api = Facebook(access_token='{your_genereated_access_token}')


If you are using iPython, you can now list available endpoints by typing ``api.`` and pressing ``tab``.

.. code-block:: python

	In [2]: api.
	api.user_likes                  api.page_blocked                 api.page_locations
	api.page_statuses                api.user_applications_developer  api.user_friends
	api.user_invitable_friends       api.user_photos                  api.user_videos
	api.object                       api.page_conversations           api.page_milestones
	...


Resources
---------

Those are the available endpoints for the facebook API. As we can see there is one called: ``user_likes``, lets take a closer look.

Type ``api.user_likes?`` and press ``enter``

.. code-block:: python

	In [3]: api.user_likes?
	...
	Docstring:
	Automatic generated __doc__ from resource_mapping.
	Resource: {id}/likes
	Docs: https://developers.facebook.com/docs/graph-api/reference/v2.2/user/likes


As we can see, ``user_likes`` resource requires an ``id`` to be passed to the url. Lets do it:

.. code-block:: python

	api.user_likes(id='me')


Fetching data
-------------

To request current user likes, its easy:

.. code-block:: python

	likes = api.user_likes(id='me').get()


To print the returned data do:

.. code-block:: python

	In [9]: likes().data()
	OUT [9]: {
		'data': [...],
		'paging': {...}
	}


Exploring data
--------------

We can also explore the returned data using the iPython ``tab`` auto-complete

.. code-block:: python

	In [9]: likes.
	likes.data    likes.paging


Iterating over data
-------------------

You can iterate over returned data:

.. code-block:: python

	likes = api.user_likes(id='me').get()

	for like in likes.data:
		print(like.id().data())

Items passed to the ``for`` loop will be wrapped in tapioca so you still have access to all features.

TapiocaClientExecutor object
============================

Whenever you make a "call" on a ``TapiocaClient`` it will return to you an ``TapiocaClientExecutor`` object. You will use the executor every time you want to perform an action over data you possess. 

An example was when we filled url params for the ``user_like`` resource (calling it and passing the argument ``id='me'``). In this new object you will find many methods to help you play with the data available.

Here is the list of the methods available in a ``TapiocaClientExecutor``:

get()/post()/put()/delete()/head()/options()
--------------------------------------------

Tapioca uses `requests <http://docs.python-requests.org/en/latest/>`_ library to make requests, so http methods will work just the same. The only difference is that we don't need to pass a url since tapioca will take care of this.

.. code-block:: python

	likes = api.user_likes(id='me').get()


**URL params**

To pass querystring parameters in the url, your can use the ```params``` parameter:

.. code-block:: python

	likes = api.user_likes(id='me').get(
		params={'limit': 5})

This will return only 5 results.

**Body data**

If you need to pass data in the body of your request, you can use the ```data``` parameter. For example, lets post a message to a facebook wall:

.. code-block:: python

	# this will only work if you have a post to wall permission
	api.user_feed(id='me').post(
		data={'message': 'I love tapiocas!! S2'})

Please read `requests <http://docs.python-requests.org/en/latest/>`_ for more detailed information about how to use HTTP methods. 

data()
------

Use data to return data contained in the Tapioca object
.. code-block:: python

	IN [8]: likes = api.user_likes(id='me').get()
	IN [9]: likes().data()
	OUT [10]: {
		'data': [...],
		'paging': {...}
	}
	# this will print only the array contained 
	# in the 'data' field of the response
	IN [11]: likes.data().data()
	OUT [12]: [...]

pages()
-------

Many APIs use paging concept to provide large amounts of data. This way data is returned in multiple requests avoiding a single long request.
Tapioca is built to provide an easy way to access paged data using ``pages()`` method:

.. code-block:: python

	likes = api.user_likes(id='me').get()

	for like in likes().pages():
		print(like.name().data())

This will keep fetching user likes until there are none left. Items passed to the ``for`` loop will be wrapped in tapioca so you still have access to all features.

This method also accepts ``max_pages`` and ``max_items`` parameters. If both parameters are used, the for loop will stop after ``max_pages`` are fetched or ``max_items`` are yielded, witch ever comes first:

.. code-block:: python

	for item in resp().pages(max_pages=2, max_items=40):
		print(item)
	# in this example, the for loop will stop after two pages are fetched or 40 items are yielded, 
	# witch ever comes first.

Accessing wrapped data attributes
---------------------------------

It's possible to access wrapped data attributes on executor. For example it's possible to reverse a wrapped list:

.. code-block:: python

	likes = api.user_likes(id='me').get()

	likes_list = likes.data
	likes_list().reverse() 
	# items in the likes_list are now in reverse order
	# but still wrapped in a tapioca object

open_docs()
-----------

If you are accessing a resource, you can call ``open_docs`` to open resource documentation in browser:

.. code-block:: python

	api.user_likes().open_docs()

open_in_browser()
-----------------

Whenever the data contained in Tapioca object is a URL, you can open it in browser by using the ``open_in_browser`` method.
