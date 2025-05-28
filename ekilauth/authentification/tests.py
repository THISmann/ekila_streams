import json
from random import randint

import pytest
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from .views import EkilAuthViewSet


@pytest.mark.django_db
class TestAuthentication:
    api_client = APIClient()

    def test_login(self, build_user):
        user = build_user(is_confirmed=True)
        url = reverse("token")
        data = {
            "email": user.email,
            "password": "testpassword",
        }

        response = self.api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in json.loads(response.content)

    def test_user_registration(self, build_user):
        url = reverse("users-register")
        user_data = {
            "email": "abcdeff@example.com",
            "username": "abcdeff",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword",
            "password2": "testpassword",
        }
        request = APIRequestFactory().post(url, user_data, format="json")
        response = EkilAuthViewSet.as_view({"post": "register"})(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == user_data["email"]
        assert response.data["username"] == user_data["username"]

    def test_resend_code_activation(self, build_user):
        url = reverse("users-resend-code-activation")
        user = build_user(is_confirmed=False)
        data = {"email": user.email}
        response = self.api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_user_change_password(self, build_user):
        url = reverse("users-change-password")

        user_old_password = "mypassword"
        user_new_password = "mynew_password"

        user = build_user(
            password=user_old_password,
            is_confirmed=True,
        )

        passwords = {
            "old_password": user_old_password,
            "new_password": user_new_password,
            "confirm_password": user_new_password,
        }

        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.post(url, passwords, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_user_profile(self, build_user):
        url = reverse("users-me")

        user = build_user(is_confirmed=True)

        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        self.api_client.force_authenticate(user=user)
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["username"] == user.username
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name

    def test_user_verify_email(self, build_user):
        url = reverse("users-verify-email")
        confirm_number = randint(settings.MIN_VALUE, settings.MAX_VALUE)
        user = build_user(confirm_number=confirm_number)
        data = {"email": user.email, "confirm_number": user.confirm_number}

        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_user_reset_password(self, build_user):
        url = reverse("users-reset-password")

        user = build_user()

        data = {
            "email": user.email,
        }

        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_user_reset_password_confirm(self, build_user):
        url = reverse("users-reset-password-confirm")
        user_new_password = "mynew_password"
        user = build_user()
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        data = {
            "uid": uid,
            "token": token,
            "new_password1": user_new_password,
            "new_password2": user_new_password,
        }

        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_user_logout(self, build_user):
        url = reverse("users-logout")
        user = build_user(is_confirmed=True)
        refresh = RefreshToken.for_user(user)
        data = {"refresh": str(refresh)}
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Ekila {refresh.access_token}")
        response = self.api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
