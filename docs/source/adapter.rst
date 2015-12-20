==========
Adapter
==========

Authentication helpers
---------------------

You can implement the ```refresh_authentication``` and ```is_authentication_expired``` methods in your Tapioca Client to refresh your authentication token every time that it expires.
```is_authentication_expired``` receives an error object from the request method (it contains the server response and HTTP Status code). You can use it to decide if a request failed because of the token. This method should return true if the authentication is expired or false otherwise.

If the authentication is expired, ```refresh_authentication``` is called. This method does not receive any parameter.

.. code-block:: python
    def is_authentication_expired(self,error)
        ....
    def refresh_authentication(self):
        ...


