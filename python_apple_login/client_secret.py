import jwt
from datetime import timedelta, datetime


class ClientSecret(object):

    def __init__(self, private_key, key_id, team_id, client_id, secret_filepath):
        self.key_id = key_id
        self.team_id = team_id
        self.client_id = client_id
        self._private_key = private_key
        self.__secret_filepath = secret_filepath
        self.__client_secret = None

    @property
    def client_secret(self) -> str:
        if not self.__client_secret:
            self._load_secret()
        return self.__client_secret

    def _load_secret(self):
        try:
            with open(self.__secret_filepath,"r") as file:
                self.__client_secret = file.read()
        except FileNotFoundError:
            self.__client_secret = None

    def _store_secret(self, client_secret):
        with open(self.__secret_filepath,"w") as file:
            file.write(client_secret)
        self.__client_secret = client_secret

    def get_valid_client_secret(self):
        if self.client_secret is None or self.is_expired():
            self._generate_client_secret_and_save()
        return self.client_secret

    def is_expired(self):
        options = {'verify_signature': False, 'verify_exp': False, 'verify_aud': False}
        decoded = jwt.decode(self.client_secret, None, algorithm='RS256', options=options)
        expiration = datetime.fromtimestamp(decoded["exp"])
        return datetime.now() > expiration

    def _generate_client_secret_and_save(self):
        client_secret = self._generate_client_secret()
        self._store_secret(client_secret)
        return client_secret

    def _generate_client_secret(self):
        headers = {
            'kid': self.key_id
        }

        payload = {
            'iss': self.team_id,
            'iat': datetime.now(),
            'exp': datetime.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': self.client_id,
        }

        client_secret = jwt.encode(payload, self._private_key, algorithm='ES256', headers=headers)
        return client_secret.decode("utf-8")

