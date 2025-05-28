from random import choice

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from ekilauth.user.views import AdminObtainTokenView
from ekilauth.user.views import AdminUserViewSetViewSet


@pytest.mark.django_db
class TestUser:
    def test_user_existing(self):
        pass


@pytest.mark.django_db
class TestAdministration:
    api_request = APIRequestFactory()

    def test_admin_or_vendor_can_login(self, build_user):
        role = choice(["admin", "revendeur"])
        user = build_user(is_confirmed=True, roles=role)
        url = reverse("administration:token")
        data = {
            "email": user.email,
            "password": "testpassword",
        }
        request = self.api_request.post(url, data, format="json")
        response = AdminObtainTokenView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_client_can_not_login(self, build_user):
        user = build_user(is_confirmed=True, roles="client")
        url = reverse("administration:token")
        data = {
            "email": user.email,
            "password": "testpassword",
        }
        request = self.api_request.post(url, data, format="json")
        response = AdminObtainTokenView.as_view()(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_dealer_can_add_user_with_client_roles(self, create_admin_user, build_user):
        dealer, dealer_token = create_admin_user("revendeur")
        user_to_add = build_user(is_confirmed=True, roles="client", confirm_number=1234)
        url = reverse("administration:users-list")
        data = {
            "email": "user1@gmail.com",
            "username": user_to_add.username,
            "first_name": user_to_add.first_name,
            "last_name": user_to_add.last_name,
            "is_confirmed": user_to_add.is_confirmed,
            "roles": user_to_add.roles,
            "password": "testpassword",
            "confirm_password": "testpassword",
        }
        request = self.api_request.post(url, data, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"post": "create"})(request)
        assert response.status_code == status.HTTP_201_CREATED

    def test_dealer_can_not_add_user_with_admin_or_dealer_roles(
        self, build_user, create_admin_user
    ):
        dealer, dealer_token = create_admin_user("revendeur")
        roles_choices = ["admin", "revendeur"]
        user_to_add = build_user(
            is_confirmed=True, roles=choice(roles_choices), confirm_number=1234
        )
        data = {
            "email": "user1@gmail.com",
            "username": user_to_add.username,
            "first_name": user_to_add.first_name,
            "last_name": user_to_add.last_name,
            "is_confirmed": user_to_add.is_confirmed,
            "roles": user_to_add.roles,
            "password": "testpassword",
            "confirm_password": "testpassword",
        }
        url = reverse("administration:users-list")
        request = self.api_request.post(url, data, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"post": "create"})(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_get_all_users(self, create_admin_user):
        admin_token = create_admin_user("admin")[1]
        url = reverse("administration:users-list")
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {admin_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "list"})(request)
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_retrieve_user(self, build_user, create_admin_user):
        user = build_user(is_confirmed=True, roles="client")
        admin_token = create_admin_user("admin")[1]
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {admin_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "retrieve"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_update_user(self, build_user, create_admin_user):
        admin_token = create_admin_user("admin")[1]
        user = build_user(is_confirmed=True, roles="client")
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {admin_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "retrieve"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_user(self, build_user, create_admin_user):
        admin_token = create_admin_user("admin")[1]
        user = build_user(email="test@gmail.com", is_confirmed=True, roles="client")
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.delete(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {admin_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"delete": "destroy"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_admin_can_not_delete_other_admin(self, build_user, create_admin_user):
        admin_token = create_admin_user("admin")[1]
        user = build_user(is_confirmed=True, roles="admin")
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.delete(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {admin_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"delete": "destroy"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_activate_user(self, build_user, create_admin_user):
        admin_token = create_admin_user("admin")[1]
        user = build_user(email="user@example.com", is_confirmed=False, roles="client")
        url = reverse("administration:users-activate", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {admin_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "activate"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_deactivate_user(self, build_user, create_admin_user):
        admin_token = create_admin_user("admin")[1]
        user = build_user(is_confirmed=True, roles="client")
        url = reverse("administration:users-deactivate", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {admin_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "deactivate"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dealer_can_get_only_his_users(self, create_admin_user):
        dealer, dealer_token = create_admin_user("revendeur")
        url = reverse("administration:users-list")
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "list"})(request)
        assert response.status_code == status.HTTP_200_OK

    def test_dealer_can_retrieve_only_his_user(self, build_user, create_admin_user):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client", created_by=dealer)
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "retrieve"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dealer_can_not_retrieve_other_user_it_did_not_create(
        self, build_user, create_admin_user
    ):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client")
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "retrieve"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_dealer_can_update_only_his_user(self, build_user, create_admin_user):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client", created_by=dealer)
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "retrieve"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dealer_can_not_update_other_user_it_did_not_create(
        self, build_user, create_admin_user
    ):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client")
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "retrieve"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_dealer_can_delete_only_his_user(self, build_user, create_admin_user):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client", created_by=dealer)
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.delete(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"delete": "destroy"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_dealer_can_not_delete_other_user_it_did_not_create(
        self, build_user, create_admin_user
    ):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client")
        url = reverse("administration:users-detail", kwargs={"pk": user.id})
        request = self.api_request.delete(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"delete": "destroy"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_dealer_can_activate_only_his_user(self, build_user, create_admin_user):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=False, roles="client", created_by=dealer)
        url = reverse("administration:users-activate", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "activate"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dealer_can_not_activate_other_user_it_did_not_create(
        self, build_user, create_admin_user
    ):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=False, roles="client")
        url = reverse("administration:users-activate", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "activate"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_dealer_can_deactivate_only_his_user(self, build_user, create_admin_user):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client", created_by=dealer)
        url = reverse("administration:users-deactivate", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "deactivate"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dealer_can_not_deactivate_other_user_it_did_not_create(
        self, build_user, create_admin_user
    ):
        dealer, dealer_token = create_admin_user("revendeur")
        user = build_user(is_confirmed=True, roles="client")
        url = reverse("administration:users-deactivate", kwargs={"pk": user.id})
        request = self.api_request.get(url, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {dealer_token.access_token}"
        response = AdminUserViewSetViewSet.as_view({"get": "deactivate"})(
            request, pk=user.id
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
