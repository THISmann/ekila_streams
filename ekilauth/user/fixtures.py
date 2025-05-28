from typing import Callable

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from ekilauth.user.factories import UserModelFactory


@pytest.fixture()
def build_user() -> Callable:
    def _build_user(**kwargs):
        return UserModelFactory(**kwargs)

    return _build_user


@pytest.fixture()
def create_admin_user(build_user) -> Callable:
    def _setup_user(role) -> tuple:
        user = build_user(is_confirmed=True, roles=role)
        user_token = RefreshToken.for_user(user)
        return user, user_token

    return _setup_user
