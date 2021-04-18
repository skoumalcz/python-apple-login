# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import re

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
    def iss(self):
        return self._data["iss"]

    @property
    def audience(self):
        return self._data["aud"]

    @property
    def expiration(self):
        return self._data["exp"]

    @property
    def iat(self):
        return self._data["iat"]

    @property
    def sub(self):
        return self._data["sub"]

    @property
    def hash(self):
        return self._data["at_hash"]

    @property
    def email(self):
        return self._data["email"]

    @property
    def is_email_verified(self):
        return self._data["email_verified"]

    @property
    def auth_time(self):
        return self._data["auth_time"]


class Client(object):

    def __init__(self, team_id, client_id, key_id, store_directory, client_private_key=None):
        self.team_id = team_id
        self.client_id = client_id
        self.key_id = key_id
        self.store_directory = store_directory
        self.__client_private_key = client_private_key

    def verify(self, identity_token_key_id, authorization_code, validate_identity=False) -> UserData:
        # Create client secret
        if not self.__client_private_key:
            with open(self.store_directory + '/' + Config.PRIVATE_KEY_FILENAME, "r") as file:
                self.__client_private_key = file.read()
        client_secret_filename = self.store_directory + '/client_secret_' + re.sub(r'[^\w\d-]','_',self.client_id)
        client_secret = ClientSecret(self.__client_private_key, self.key_id, self.team_id, self.client_id, client_secret_filename) \
            .get_valid_client_secret()

        # Create apple authorization service
        auth_service = AppleAuthService(self.client_id, client_secret)
        auth_response = auth_service.auth(authorization_code)

        # Get public keys
        public_key = None
        options = {'verify_signature': validate_identity, 'verify_exp': True, 'verify_aud': True}
        if validate_identity:
            apple_public_keys = auth_service.get_public_keys()
            public_key = RSAKeyService().get_public_key(apple_public_keys, identity_token_key_id)

        id_token = auth_response.id_token
        data = jwt.decode(id_token, public_key, algorithm='RS256',options=options, audience=self.client_id)
        user_data = UserData(data)
        return user_data
