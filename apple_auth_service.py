import requests
from key_description import KeyDescription
from authorization_response import AuthorizationResponse


class AppleAuthService(object):

    BASE_URL = 'https://appleid.apple.com'
    ACCESS_TOKEN_URL = BASE_URL + '/auth/token'
    PUBLIC_TOKENS_URL = BASE_URL + '/auth/keys'
    REFRESH_TOKEN_URL = ACCESS_TOKEN_URL

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def auth(self, authorization_code):
        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = self._get_base_auth_data()
        data["code"] = authorization_code
        data["grant_type"] = "authorization_code"

        res = requests.post(self.ACCESS_TOKEN_URL, data=data, headers=headers)
        response_dict = res.json()
        return AuthorizationResponse(response_dict)

    def refresh(self, refresh_token):
        headers = {'content-type': "application/x-www-form-urlencoded"}
        data = self._get_base_auth_data()
        data["refresh_token"] = refresh_token
        data["grant_type"] = "refresh_token"

        res = requests.post(self.REFRESH_TOKEN_URL, data=data, headers=headers)
        response_dict = res.json()
        return AuthorizationResponse(response_dict)

    def get_public_keys(self):
        res = requests.get(self.PUBLIC_TOKENS_URL)
        response_dict = res.json()
        keys = [KeyDescription(key_dic) for key_dic in response_dict["keys"]]
        return keys

    def _get_base_auth_data(self):
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
