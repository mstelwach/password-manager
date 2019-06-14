from base64 import encodebytes, decodebytes
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from django.conf import settings
from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.encoding import force_text
from django.utils.http import base36_to_int, int_to_base36


class LinkTokenGeneration(object):
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """
    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
    secret = settings.SECRET_KEY

    def make_token(self, password):
        """
        Return a token that can be used once to do a password reset
        for the given user.
        """
        return self._make_token_with_timestamp(password, self._num_seconds(self._today()))

    def check_token(self, password, token):
        """
        Check that a password reset token is correct for a given user.
        """

        PASSWORD_RESET_TIMEOUT_SECONDS = 300

        if not (password and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(password, ts), token):
            return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._today()) - ts) > PASSWORD_RESET_TIMEOUT_SECONDS:
            return False

        return True

    def _make_token_with_timestamp(self, password, timestamp):
        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            self.key_salt,
            self._make_hash_value(password, timestamp),
            secret=self.secret,
        ).hexdigest()[::2]  # Limit to 20 characters to shorten the URL.
        return "%s-%s" % (ts_b36, hash_string)

    def _make_hash_value(self, password, timestamp):
        return (
            six.text_type(password.pk) + six.text_type(timestamp)
        )

    def _num_seconds(self, dt):
        return (dt - datetime(2001, 1, 1)).seconds

    def _today(self):
        return datetime.today()


class PasswordCrypto(object):

    def __init__(self, secret_key):

        self.secret_key = secret_key
        self.secret = self._get_secret(secret_key)
        self.cipher = AES.new(self.secret)
        self.decipher = AES.new(self.secret)

    def _pad(self, msg):
        return msg + ((32 - len(msg) % 32) * '{')

    def _depad(self, msg):
        msg = force_text(msg)
        return msg.rstrip('{')

    def _get_secret(self, key):
        return MD5.new(key).hexdigest()[:32]

    def encrypt(self, password):
        return encodebytes(self.cipher.encrypt(self._pad(password)))

    def decrypt(self, enc_password):
        return self._depad((self.decipher.decrypt(decodebytes(enc_password))))


password_activation_token = LinkTokenGeneration()
