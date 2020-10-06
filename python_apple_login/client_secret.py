import jwt
from datetime import timedelta, datetime
from python_apple_login.file_text_manager import FileTextManager


class ClientSecret(object):

    def __init__(self, private_key_file_name, key_id, team_id, client_id):
        self.key_id = key_id
        self.team_id = team_id
        self.client_id = client_id
        self._private_key = self._load_private_key(private_key_file_name)
        self._file_manager = FileTextManager("client_secret.txt")

    def get(self):
        client_secret = self._file_manager.load()
        if client_secret is None or self._is_expired(client_secret):
            client_secret = self._generate_client_secret_and_save()
        return client_secret

    def _load_private_key(self, private_key_file_name):
        private_key_file = open(private_key_file_name)
        private_key = private_key_file.read()
        private_key_file.close()
        return private_key

    def _is_expired(self, client_secret):
        options = {'verify_signature': False, 'verify_exp': False, 'verify_aud': False}
        decoded = jwt.decode(client_secret, None, algorithm='RS256', options=options)
        expiration = datetime.fromtimestamp(decoded["exp"])
        return datetime.now() > expiration

    def _generate_client_secret_and_save(self):
        client_secret = self._generate_client_secret()
        self._file_manager.save(client_secret)
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
