# Using a tapioca package

**Yes, you are in the right place**

There is a good chance you found this page because you clicked a link from some python package called **tapioca-*SOMETHING* **. Well, welcome! You are in the right place, this page will teach you the basics of how to use the package that sent you here. If you didn't arive here from other package, please keep reading, the concepts learned here applies to any tapioca-***package*** available.

## What's tapioca?

**tapioca** is a *API wrapper maker*. It helps Python developers creating packages for APIs (like the [Facebook Graph API](flavours.html#facebook) or the [Twitter REST API](flavours.html#twitter)). You can find a full list of available API packages made with tapioca [here](flavours.md).  
All wrappers made with tapioca follow a simple interaction pattern that works uniformelly so once you learn how tapioca works you will be able to work with any tapioca package available.

## Getting started

We will use ```tapioca-facebook``` as example to gide us through tapioca concepts.
Lets install ```tapioca-facebook```:
```
pip install tapioca-facebook
```
To better experience tapioca, we will also use iPython:
```
pip install ipython
```
Lets explore!!
Go to [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/), click "Get Access Token", select all "User Data Permissions" and "Extended Permissions" and click "Get Access Token". This will give you an teporary access token to play with Facebook API. In case it expires, just generate a new one.

``` python
from tapioca_facebook import Facebook

api = Facebook(access_token='your_genereated_access_token')

```

If you are using iPython, you can now list available endpoints by typing ```api.``` and pressing ```tab```.

``` python
In [2]: api.
api.user_likes                  api.page_blocked                 api.page_locations
api.page_statuses                api.user_applications_developer  api.user_friends
api.user_invitable_friends       api.user_photos                  api.user_videos
api.object                       api.page_conversations           api.page_milestones
...
```

## Resources

Those are the available endpoints for the facebook API. As we can see there is one called: ```user_likes```, lets take a closer look.

Type ```api.user_likes?``` and press ```enter```

``` python
In [3]: api.user_likes?
...
Docstring:
Automatic generated __doc__ from resource_mapping.
Resource: {id}/likes
Docs: https://developers.facebook.com/docs/graph-api/reference/v2.2/user/likes
```

As we can see, ```user_likes``` resource requires an ```id``` to be passed to the url. Lets do it:

``` python
api.user_likes(id='me')

```

### Fetching data

To request current user likes, its easy:

``` python
likes = api.user_likes(id='me').get()
```

To print the returned data do:

``` python
In [9]: likes().data()
OUT [9]: {
    'data': [...],
    'paging': {...}
}
```

## Exploring data

We can also expore the returned data using the iPython ```tab``` auto-complete

``` python
In [9]: likes.
likes.data    likes.paging
```

## Executor object

Whenever you use brackets, Tapioca will return to you an ```Executor``` object. You will use the executor every time you want to perform an action over data you possess. 

An example was when we filled url params for the ```user_likes``` resource (calling it and passign the argument ``id='me'``). Whenever you make a ``call`` from a ``TapiocaClient`` it will return a ``TapiocaClientExecutor`` object. In this new object you will find many methods to help you play with the data available.

Here is the list of the methods available in a ``TapiocaClientExecutor``:

### get()/post()/put()/delete()/head()/options()

Tapioca uses [requests](http://docs.python-requests.org/en/latest/) library to make requests, so http methods will work just the same. 
``` python
likes = api.user_likes(id='me').get()
```
Please read [requests](http://docs.python-requests.org/en/latest/) for more detailed information about tho use HTTP methods. 

#### data()
Use data to return data contained in the Tapioca object
``` python
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
```

### iterator

Many APIs use paging concept to provide large amounts of data. This way data is returned in multiple requests avoing a single long request.
tapioca is buit to provide easy way to access paged data using iterators:

``` python
likes = api.user_likes(id='me').get()

for like in likes:
    print(like.id().data())
```
This will keep fetching user likes until there are none left.

### open_docs()

If you are accessing a resource, you can call ```open_docs``` to open resource documentation in browser:

``` python
api.user_likes().open_docs()
```

### open_in_browser()

Whenever the data contained in Tapioca object is a URL, you can open it in browser by using the ```open_in_browser``` method.
