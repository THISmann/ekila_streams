from typing import Dict

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from ekilauth.user.models import EkilaUser


class TokenStrategy:
    @classmethod
    def obtain(cls, user):
        refresh_token = RefreshToken.for_user(user)
        return {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token),
            "user": user,
        }


class EkilaJWTAuthentication(JWTAuthentication):
    @classmethod
    def create_jwt(cls, user: EkilaUser) -> Dict[str, str]:
        jwt_token = TokenStrategy.obtain(user=user)
        return jwt_token
