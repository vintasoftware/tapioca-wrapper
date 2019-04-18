=========
Changelog
=========

1.5.1
=====
- Adds a ``resource_name`` kwarg to the ``get_api_root`` method

1.5
===
- Removes support for Python 3.3


1.4
===
- Adds support to Session requests

1.3
===
- ``refresh_authentication`` should return data about the refresh token process
- If a falsy value is returned by ``refresh_authentication`` the request wont be retried automatically
- Data returned by ``refresh_authentication`` is stored in the tapioca class and can be accessed in the executor via the attribute ``refresh_data``

1.2.3
======
- ``refresh_token_by_default`` introduced to prevent passing ``refresh_token`` on every request.

1.1.10
======
- Fixed bugs regarding ``request_kwargs`` passing over calls
- Fixed bugs regarding external ``serializer`` passing over calls
- Wrapper instatiation now accepts ``default_url_params``

1.1
===
- Automatic refresh token support
- Added Python 3.5 support
- Added support for ``OrderedDict``
- Documentation cleanup

1.0
===
- Data serialization and deserialization
- Access CamelCase attributes using snake_case
- Dependencies are now tied to specific versions of libraries
- ``data`` and ``response`` are now attributes instead of methods in the executor
- Added ``status_code`` attribute to tapioca executor
- Renamed ``status`` exception attribute to ``status_code``
- Fixed return for ``dir`` call on executor, so it's lot easier to explore it
- Multiple improvments to documentation

0.6.0
=====
- Giving access to request_method in ``get_request_kwargs``
- Verifying response content before trying to convert it to json on ``JSONAdapterMixin``
- Support for ``in`` operator
- pep8 improvments

0.5.3
=====
- Adding ``max_pages`` and ``max_items`` to ``pages`` method

0.5.1
=====
- Verifying if there's data before json dumping it on ``JSONAdapterMixin``

0.5.0
=====
- Automatic pagination now requires an explicit ``pages()`` call
- Support for ``len()``
- Attributes of wrapped data can now be accessed via executor
- It's now possible to iterate over wrapped lists

0.4.1
=====
- changed parameters for Adapter's ``get_request_kwargs``. Also, subclasses are expected to call ``super``.
- added mixins to allow adapters to easily choose witch data format they will be dealing with.
- ``ServerError`` and ``ClientError`` are now raised on 4xx and 5xx response status. This behaviour can be customized for each service by overwriting adapter's ``process_response`` method.