from requests_oauthlib import OAuth2Session


class Oauth2TokenRequester(object):

    def __init__(self,
                 client_id,
                 client_secret,
                 redirect_uri,
                 authorization_base_url,
                 obtain_token_url,
                 scope_list,
                 **auth_base_url_kwargs):

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_base_url = authorization_base_url
        self.obtain_token_url = obtain_token_url
        self.scope_list = scope_list
        self.auth_base_url_kwargs = auth_base_url_kwargs

    def authorize_app(self):
        '''
        Uses requests_oauthlib to request a token and response.
        Requires your app to have a redirect_uri set up.

        Usage:
        o = Oauth2TokenRequester(**kwargs)  # '**kwargs' for brevity.
        authorization_url = o.authorize_app()
        # go to authorization_url to perform authorization with third party
        # record redirect_response
        token = o.get_token(redirect_response)
        '''
        self.oauth = OAuth2Session(self.client_id,
                                   scope=self.scope_list,
                                   redirect_uri=self.redirect_uri)
        authorization_url, state = self.oauth.authorization_url(self.authorization_base_url,
                                                                **self.auth_base_url_kwargs)

        return authorization_url

    def get_token(self, redirect_response):

        self.oauth.fetch_token(self.obtain_token_url,
                               authorization_response=redirect_response,
                               client_secret=self.client_secret)

        return self.oauth.token
