import jwt
from python_apple_login.user_data import UserData
from python_apple_login.client_secret import ClientSecret
from python_apple_login.apple_auth_service import AppleAuthService
from python_apple_login.rsa_key_service import RSAKeyService


class AppleLoginService(object):

    def __init__(self, key_file_name, auth_key_id, team_id, client_id):
        self.client_id = client_id
        client_secret = ClientSecret(key_file_name, auth_key_id, team_id, self.client_id).get()
        self._auth_service = AppleAuthService(client_id, client_secret)

    def auth(self, authorization_code, key_id, validate_identity=False):
        auth_response = self._auth_service.auth(authorization_code)

        public_key = None
        if validate_identity:
            apple_public_keys = self._auth_service.get_public_keys()
            public_key = RSAKeyService().get_public_key(apple_public_keys, key_id)

        id_token = auth_response.get_id_token()
        user_data = self._get_user_data(public_key, id_token, validate_identity=validate_identity)
        return user_data

    def refresh(self, refresh_token):
        refresh_response = refresh_response = self._auth_service.refresh(refresh_token)
        return refresh_response

    def _get_user_data(self, public_key, id_token, validate_identity=False):
        options = {'verify_signature': validate_identity, 'verify_exp': True, 'verify_aud': True}
        decoded = jwt.decode(id_token, public_key, algorithm='RS256', options=options, audience=self.client_id)
        return UserData(decoded)
