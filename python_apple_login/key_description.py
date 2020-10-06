import base64
import re


class KeyDescription(object):

    def __init__(self, data):
        self._data = data

    def get_kty(self):
        return self._data["kty"]

    def get_kid(self):
        return self._data["kid"]

    def get_e(self):
        return self._data["e"]

    def get_n(self):
        return self._data["n"]

    def get_decoded_e(self):
        return int(self._decode(self.get_e()))

    def get_decoded_n(self):
        return int(self._decode(self.get_n()))

    def _decode(self, data, altchars=b'+/'):
        decoded_bytes = base64.urlsafe_b64decode(data + "===")
        decoded = int.from_bytes(decoded_bytes, "big")
        return decoded
