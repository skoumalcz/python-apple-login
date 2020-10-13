from Cryptodome.PublicKey import RSA


class RSAKeyService(object):

    def get_public_key(self, apple_public_keys, key_id):
        key = self._find_apple_key(apple_public_keys, key_id)
        if key is None:
            raise Exception("No public key have been found with id: " + key_id)

        exponent = key.get_decoded_e()
        modulus = key.get_decoded_n()
        rsa_key = RSA.construct((modulus, exponent))
        public_key = rsa_key.publickey()
        pem_format = public_key.export_key("PEM")
        pem_string = pem_format.decode("utf-8")
        # TODO save public key and re-used it
        # self._file_manager.save(pem_string)
        return pem_string

    def _find_apple_key(self, apple_keys, key_id):
        for apple_key in apple_keys:
            if apple_key.kid == key_id:
                return apple_key
        return None
