from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, get_authorization_header


class CustomTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        try:
            token = get_authorization_header(request).decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return
