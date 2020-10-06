

class UserData(object):

    def __init__(self, data):
        self._data = data

    def get_iss(self):
        return self._data["iss"]

    def get_audience(self):
        return self._data["aud"]

    def get_expiration(self):
        return self._data["exp"]

    def get_iat(self):
        return self._data["iat"]

    def get_sub(self):
        return self._data["sub"]

    def get_hash(self):
        return self._data["at_hash"]

    def get_email(self):
        return self._data["email"]

    def get_is_email_verified(self):
        return self._data["email_verified"]

    def get_auth_time(self):
        return self._data["auth_time"]
