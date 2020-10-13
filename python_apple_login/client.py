# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import jwt
from python_apple_login.apple_auth import AppleAuthService
from python_apple_login.client_secret import ClientSecret
from python_apple_login.configuration import Config
from python_apple_login.rsa_key_service import RSAKeyService


class UserData(object):

    def __init__(self, data: dict):
        self._data = data

    @property
    def data(self) -> dict:
        return self._data

    @property
    def email(self) -> str:
        #TODO
        return "TODo"


class Client(object):

    def __init__(self, team_id, client_id, identity_token, store_directory):
        self.team_id = team_id
        self.client_id = client_id
        self.identity_token = identity_token
        self.store_directory = store_directory

    def verify(self, key_id, authorization_code) -> UserData:
        # Create client secret
        #TODO work with private key more safely
        with open(self.store_directory + '/' + Config.PRIVATE_KEY_FILENAME, "r") as file:
            private_key = file.read()
        client_secret_filename = self.store_directory + '/' + Config.CLIENT_SECRET_FILENAME
        client_secret = ClientSecret(private_key, key_id, self.team_id, self.client_id, client_secret_filename)\
            .get_valid_client_secret()

        # Create apple authorization service
        auth_service = AppleAuthService(self.client_id, client_secret)
        auth_response = auth_service.auth(authorization_code)

        # Get public keys
        identity_token_key_id = get_identity_token_key_id(self.identity_token)
        apple_public_keys = auth_service.get_public_keys()
        public_key = RSAKeyService().get_public_key(apple_public_keys, identity_token_key_id)

        id_token = auth_response.id_token
        print(id_token)
        data = jwt.decode(id_token, public_key, algorithm='RS256',
                               options={'verify_signature': True,'verify_exp': True, 'verify_aud': True}, audience=self.client_id)
        print(data)
        user_data = UserData(data)
        return user_data


def get_identity_token_key_id(identity_token):
    identity_token_headers = jwt.get_unverified_header(identity_token)
    return identity_token_headers["kid"]
