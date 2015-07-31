
class ResponseProcessException(Exception):

    def __init__(self, tapioca_exception, data, *args, **kwargs):
        self.tapioca_exception = tapioca_exception
        self.data = data
        super(ResponseProcessException, self).__init__(*args, **kwargs)


class TapiocaException(Exception):

    def __init__(self, client=None, *args, **kwargs):
        self.client = client
        if client:
            self.status = client().response().status_code
        super(TapiocaException, self).__init__(*args, **kwargs)


class ClientError(TapiocaException):
    pass


class ServerError(TapiocaException):
    pass
