import requests
import base64


class KeyDescription(object):

    def __init__(self, data):
        self._data = data

    @property
    def kty(self):
        return self._data["kty"]

    @property
    def kid(self):
        return self._data["kid"]

    @property
    def e(self):
        return self._data["e"]

    @property
    def n(self):
        return self._data["n"]

    def get_decoded_e(self):
        return int(self._decode(self.e))

    def get_decoded_n(self):
        return int(self._decode(self.n))

    def _decode(self, data):
        decoded_bytes = base64.urlsafe_b64decode(data + "===")
        decoded = int.from_bytes(decoded_bytes, "big")
        return decoded


class AuthorizationResponse(object):

    def __init__(self, data):
        self._data = data

    @property
    def id_token(self):
        return self._data["id_token"]

    @property
    def access_token(self):
        return self._data["access_token"]

    @property
    def refresh_token(self):
        return self._data["refresh_token"]

    @property
    def expiration(self):
        return int(self._data["expires_in"])


class AppleAuthService(object):

    BASE_URL = 'https://appleid.apple.com'
    ACCESS_TOKEN_URL = BASE_URL + '/auth/token'
    PUBLIC_TOKENS_URL = BASE_URL + '/auth/keys'
    REFRESH_TOKEN_URL = ACCESS_TOKEN_URL

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def auth(self, authorization_code):
        data = {}
        data["code"] = authorization_code
        data["grant_type"] = "authorization_code"
        response_dict = self._process_post_json_request(self.ACCESS_TOKEN_URL, data)
        return AuthorizationResponse(response_dict)

    def refresh(self, refresh_token):
        data = {}
        data["refresh_token"] = refresh_token
        data["grant_type"] = "refresh_token"
        response_dict = self._process_post_json_request(self.REFRESH_TOKEN_URL, data)
        return AuthorizationResponse(response_dict)

    def get_public_keys(self):
        res = requests.get(self.PUBLIC_TOKENS_URL)
        if res.status_code != 200:
            raise Exception("Invalid apple service ({}) response".format(self.PUBLIC_TOKENS_URL))
        # TODo check response json
        response_dict = res.json()
        keys = [KeyDescription(key_dic) for key_dic in response_dict["keys"]]
        return keys

    def _process_post_json_request(self, url, data):
        headers = {'content-type': "application/x-www-form-urlencoded"}
        request_data = self._get_base_auth_data()
        request_data.update(data)
        res = requests.post(url, data=data, headers=headers)
        if res.status_code != 200:
            raise Exception("Invalid apple service ({}) response".format(url))
        #TODo check response json
        return res.json()

    def _get_base_auth_data(self):
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
