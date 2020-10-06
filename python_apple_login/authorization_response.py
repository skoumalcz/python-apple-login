

class AuthorizationResponse(object):

    def __init__(self, data):
        self._data = data

    def get_id_token(self):
        return self._data["id_token"]

    def get_access_token(self):
        return self._data["access_token"]

    def get_refresh_token(self):
        return self._data["refresh_token"]

    def get_expiration(self):
        return int(self._data["expires_in"])
