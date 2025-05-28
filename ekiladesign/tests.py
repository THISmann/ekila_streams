import faker
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestPublicite:
    api_client = APIClient()

    def test_publicite_creation(self, build_user, generate_fake_image):
        url = reverse("publicities-list")
        user = build_user(is_confirmed=True)
        data = {
            "description": "This is a test for an ad creation",
            "pub_image": generate_fake_image,
        }
        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == data["description"]
        assert response.data["is_enable"] == True

    def test_publicite_update(self, build_publicite, generate_fake_image):
        publicite = build_publicite(pub_image=generate_fake_image)
        url = reverse("publicities-detail", kwargs={"pk": publicite.id})
        data = {
            "description": "This is a test for an ad update",
            "pub_image": publicite.pub_image,
            "is_enable": True,
        }
        user_token = RefreshToken.for_user(publicite.user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.put(url, data, format="multipart")
        assert response.status_code == status.HTTP_200_OK

    def test_publicite_delete(self, build_publicite, generate_fake_image):
        publicite = build_publicite(pub_image=generate_fake_image)
        url = reverse("publicities-detail", kwargs={"pk": publicite.id})
        user_token = RefreshToken.for_user(publicite.user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data == None

    def test_publicite_list(self, build_publicite, generate_fake_image):
        publicite = build_publicite(pub_image=generate_fake_image)
        url = reverse("publicities-list")
        user_token = RefreshToken.for_user(publicite.user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_publicite_detail(self, build_publicite, generate_fake_image):
        publicite = build_publicite(pub_image=generate_fake_image)
        url = reverse("publicities-detail", kwargs={"pk": publicite.id})
        user_token = RefreshToken.for_user(publicite.user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == publicite.id
        assert response.data["is_created_at"] == publicite.is_created_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        assert response.data["is_updated_at"] == publicite.is_updated_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        assert response.data["description"] == publicite.description
