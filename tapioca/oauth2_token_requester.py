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

    def request_token(self):
        '''
        Uses requests_oauthlib to request a token and response.
        Requires your app to have a redirect_uri set up.

        Prompts user through steps of obtaining a token.

        Usage:
        o = OauthRequester(**kwargs)  # '**kwargs' for brevity.
        token = o.request_token()
        '''
        oauth = OAuth2Session(self.client_id,
                              scope=self.scope_list,
                              redirect_uri=self.redirect_uri)
        authorization_url, state = oauth.authorization_url(self.authorization_base_url,
                                                           **self.auth_base_url_kwargs)

        print ('\n###### OauthRequester User Prompt ######\n'
               '1. Please go to the following URL to authorize access: \n\n%s' % authorization_url)

        redirect_response = raw_input('\n2. Enter the full callback URL that your request was '
                                      'redirected to:\n')

        oauth.fetch_token(self.obtain_token_url,
                          authorization_response=redirect_response,
                          client_secret=self.client_secret)

        return oauth.token
