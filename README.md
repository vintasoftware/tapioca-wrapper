# Tapioca-Wrapper

![Tapioca!!](tapioca.jpg "Tapioca")

Tapioca provides an easy way to make explorable python API wrappers.
APIs wrapped by Tapioca follow a simple interaction pattern that works uniformelly so developers don't need to learn how to use a new coding interface/style for each service API.

Supports Python 2.7, 3.2, 3.3 and 3.4.

## Concepts

Uniform and explorable wrappers means developers don't need to read full API and wrapper documentation before starting to play with it.

We will use ```tapioca-facebook``` as example to gide us through Tapioca.
We start by installing ```tapioca-facebook```:
```
pip install tapioca-facebook
```

To better experience Tapioca, we will also use iPython:
```
pip install ipython
```

Now, lets explore!!
Go to [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/), click "Get Access Token", select all "User Data Permissions" and "Extended Permissions" and click "Get Access Token". This will give you an teporary access token to play with Facebook API. In case it expires, just generate a new one.

``` python
from tapioca_facebook import Facebook

api = Facebook(access_token='{your_genereated_access_token}')

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

### Resources

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

### Exploring data

We can also expore the returned data using the iPython ```tab``` auto-complete

``` python
In [9]: likes.
likes.data    likes.paging
```

### Executor object

Whenever you use brackets, Tapioca will return to you an ```Executor``` object. You will use the executor every time you want to perform an action over data you possess. An example was when we filled url params for the ```user_likes``` resource, and then used the ```get``` method to fetch data.

Tapioca provides many methods, here are they:

#### get()/post()/put()/delete()/head()/options()

Tapioca uses ```requests``` library to make requests, so http methods will work just the same.
``` python
likes = api.user_likes(id='me').get()
```

#### data()
Use data to return data contained in the Tapioca object
``` python
likes = api.user_likes(id='me').get()

# this will print only the array contained in data field of the response
print(likes.data().data())
[...]
```

#### iterator

Many APIs use paging concept to provide large amounts of data. This way data is returned in multiple requests avoing a single long request.
Tapioca is buit to provide easy way to access paged data using iterators:

``` python
likes = api.user_likes(id='me').get()

for like in likes:
    print(like.id().data())
```
This will keep fetching user likes until there are none left.

#### open_docs()

If you are accessing a resource, you can call ```open_docs``` to open resource documentation in browser:

``` python
api.user_likes().open_docs()
```

#### open_in_browser()

Whenever the data contained in Tapioca object is a URL, you can open it in browser by using the ```open_in_browser``` method.


## Tapioca comes in many flavours

Facebook - [https://github.com/vintasoftware/tapioca-facebook](https://github.com/vintasoftware/tapioca-facebook)
Twitter - [https://github.com/vintasoftware/tapioca-twitter](https://github.com/vintasoftware/tapioca-twitter)
Mandrill - [https://github.com/vintasoftware/tapioca-mandrill](https://github.com/vintasoftware/tapioca-mandrill)
Parse - [https://github.com/vintasoftware/tapioca-parse](https://github.com/vintasoftware/tapioca-parse)

Send a pull request to add new ones to the list.

## Wrapping an API with Tapioca

This is all the code you need to build the Facebook Graph API wrapper you just played with:
``` python
# source here: https://github.com/vintasoftware/tapioca-facebook/blob/master/tapioca_facebook/tapioca_facebook.py

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter)
from requests_oauthlib import OAuth2

from resource_mapping import RESOURCE_MAPPING


class FacebookClientAdapter(TapiocaAdapter):
    api_root = 'https://graph.facebook.com'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params):
        client_id = api_params.get('client_id')
        return {
            'auth': OAuth2(client_id,
                token={
                    'access_token': api_params.get('access_token'),
                    'token_type': 'Bearer'})
        }

    def get_iterator_list(self, response_data):
        return response_data['data']

    def get_iterator_next_request_kwargs(self,
            iterator_request_kwargs, response_data):
        paging = response_data.get('paging')
        if not paging:
            return
        url = paging.get('next')

        if url:
            return {'url': url}


Facebook = generate_wrapper_from_adapter(FacebookClientAdapter)
```
Everything else is what we call ```resource_mapping``` and its merely documentation. You can take a look  [here](https://github.com/vintasoftware/tapioca-facebook/blob/master/tapioca_facebook/resource_mapping.py).

## Contributors

André Ericson de.ericson@gmail.com

Filipe Ximenes filipeximenes@gmail.com

