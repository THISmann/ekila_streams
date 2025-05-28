# Create your tests here.
from random import choice

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from radio.models import Radio
from radio.models import RadioMenuModel
from radio.radio_menu.views import RadioMenuViewSet
from radio.utils import extract_domain


@pytest.mark.django_db
class TestRadio:
    client = APIRequestFactory()
    api_client = APIClient()

    def test_radio_stream_metadata(self, build_radio):
        shoutcast_radio = build_radio(
            server_type="shoutcast",
            url_flux_radio="https://radio.pro-fhi.net:19000/stream",
            url_server_radio="https://radio.pro-fhi.net:19000",
            url_api_radio_current_song="https://radio.pro-fhi.net:19000/currentsong?sid=1",
            url_api_radio_history="https://radio.pro-fhi.net:19000/played.html?sid=1",
            sid=1,
        )
        url = reverse(
            "radio:radio-get-stream-result", kwargs={"name": shoutcast_radio.name}
        )
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Radio.objects.get(name=shoutcast_radio.name) is not None
        assert response.data["id"] == shoutcast_radio.pk
        assert response.data["radio_flux"] == shoutcast_radio.url_flux_radio
        keys = (
            "id",
            "title",
            "radio_flux",
            "album_title",
            "cover",
            "artist_name",
            "song_history",
            "menu",
        )
        for k in keys:
            assert k in response.data

    def test_radio_stream_not_send_metadata(self, build_radio):
        any_radio = build_radio(url_server_radio="http://radio4.pro-fhi.net:9017/")
        url = reverse("radio:radio-get-stream-result", kwargs={"name": any_radio.name})
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Radio.objects.get(name=any_radio.name) is not None
        assert (
            response.data["detail"]
            == f"{any_radio.url_api_radio_current_song} or {any_radio.url_api_radio_history} is not available, check your api before"
        )

    def test_create_radio_ice_or_shoutcast(
        self, build_radio, build_user, generate_fake_image
    ):
        server_type = choice(
            (
                "shoutcast",
                "icecast",
            )
        )

        url = reverse("radio:radio-list")
        radio = build_radio(url_server_radio="http://radio4.pro-fhi.net:9017/")
        data = {
            "name": radio.name,
            "url_server_radio": radio.url_server_radio,
            "url_cover_default": radio.url_cover_default,
            "url_site": radio.url_site,
            "radio_image_icon": generate_fake_image,
            "sid": radio.sid,
            "server_type": server_type,
            "user": radio.user,
        }
        user = build_user(is_confirmed=True)

        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["url_server_radio"] == "http://radio4.pro-fhi.net:9017"
        if server_type == "icecast":
            assert (
                response.data["url_api_radio_current_song"]
                == response.data["url_server_radio"] + "/" + "status-json.xsl"
            )
            assert (
                response.data["url_api_radio_history"]
                == response.data["url_server_radio"] + "/" + "status-json.xsl"
            )
        else:
            assert (
                response.data["url_api_radio_current_song"]
                == response.data["url_server_radio"]
                + "/"
                + f"currentsong?sid={radio.sid}"
            )
            assert (
                response.data["url_api_radio_history"]
                == response.data["url_server_radio"]
                + "/"
                + f"played.html?sid={radio.sid}"
            )

    def test_creation_of_other_radio(
        self, build_radio, build_user, generate_fake_image
    ):
        url = reverse("radio:radio-list")
        server_type = choice(
            (
                "everestcast",
                "everestpanel",
                "rcast",
                "centovacast",
                "azuracast",
                "radioking",
            )
        )
        radio = build_radio(url_server_radio="http://radio4.pro-fhi.net:9017/")
        data = {
            "name": radio.name,
            "url_flux_radio": radio.url_flux_radio,
            "url_pannel_connexion": radio.url_pannel_connexion,
            "username_radio_account": radio.username_radio_account,
            "radio_account_port": radio.radio_account_port,
            "url_server_radio": radio.url_server_radio,
            "url_cover_default": radio.url_cover_default,
            "url_site": radio.url_site,
            "radio_image_icon": generate_fake_image,
            "sid": radio.sid,
            "station_id": radio.station_id,
            "server_type": server_type,
            "user": radio.user,
        }
        if server_type == "rcast" or server_type == "azuracast":
            data["name"] = "Ekila api"
        if server_type == "radioking":
            data["name"] = "Web Latinos zouk"
        user = build_user(is_confirmed=True)
        user_token = RefreshToken.for_user(user)
        self.api_client.credentials(
            HTTP_AUTHORIZATION=f"Ekila {user_token.access_token}"
        )
        response = self.api_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        if server_type == "everestcast":
            domain = extract_domain(data["url_flux_radio"])
            assert (
                response.data["url_api_radio_current_song"]
                == domain
                + ":"
                + str(data["radio_account_port"])
                + "/api/v2/history/?limit=1&offset=0"
            )
            assert (
                response.data["url_api_radio_history"]
                == domain
                + ":"
                + str(data["radio_account_port"])
                + "/api/v2/history/?limit=5&offset=1"
            )
        elif server_type == "everestpanel":
            domain = extract_domain(data["url_flux_radio"])
            assert (
                response.data["url_api_radio_current_song"]
                == domain
                + f"/widget/get-current-track-api?station={data['station_id']}"
            )
            assert (
                response.data["url_api_radio_history"]
                == domain + f"/widget/get-current-track-api/{data['station_id']}"
            )
        elif server_type == "rcast":
            assert (
                response.data["url_api_radio_current_song"]
                == response.data["url_api_radio_history"]
                == response.data["url_pannel_connexion"] + f"/json/stream/ekilaapi"
            )
        elif server_type == "centovacast":
            assert (
                response.data["url_api_radio_current_song"]
                == response.data["url_pannel_connexion"]
                + f"/rpc/{data['username_radio_account']}/streaminfo.get"
            )
            assert (
                response.data["url_api_radio_history"]
                == response.data["url_pannel_connexion"]
                + f"/recentfeed/{data['username_radio_account']}/json/"
            )
        elif server_type == "azuracast":
            assert (
                response.data["url_api_radio_current_song"]
                == response.data["url_pannel_connexion"]
                + "/api/nowplaying_static/ekilaapi.json"
                == response.data["url_api_radio_history"]
            )
        elif server_type == "radioking":
            assert (
                response.data["url_api_radio_current_song"]
                == "https://api.radioking.io/widget/radio/web-latinos-zouk/track/current"
            )
            assert (
                response.data["url_api_radio_history"]
                == "https://api.radioking.io/widget/radio/web-latinos-zouk/track/ckoi?limit=5"
            )


@pytest.mark.django_db
class TestRadioMenu:
    client = APIRequestFactory()

    def test_user_can_create_radio_menu_with_existing_radio(
        self, build_user, build_radio, build_radio_menu
    ):
        url = reverse("radio-menu:radio-list")
        role = choice(["client", "admin", "revendeur"])
        user = build_user(is_confirmed=True, roles=role)
        if role == "revendeur":
            user.created_by = user
            user.save()
        radio = build_radio(
            url_server_radio="http://radio4.pro-fhi.net:9017/", user=user
        )  # radio du user
        menu = build_radio_menu(radio=radio)
        data = {"title": menu.title, "link": menu.link, "radio": menu.radio.pk}
        user_token = RefreshToken.for_user(user)
        request = self.client.post(url, data, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {user_token.access_token}"
        response = RadioMenuViewSet.as_view({"post": "create"})(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert RadioMenuModel.objects.filter(
            title=menu.title, radio=menu.radio.pk
        ).exists()

    def test_user_cannot_create_menu_without_radio(
        self, build_user, build_radio, build_radio_menu
    ):
        url = reverse("radio-menu:radio-list")
        role = choice(["client", "admin", "revendeur"])
        user1 = build_user(is_confirmed=True, roles=role)
        data = {"title": "ekila", "link": "http://radio4.pro-fhi.net:9017/", "radio": 1}
        user_token = RefreshToken.for_user(user1)
        request = self.client.post(url, data, format="json")
        request.META["HTTP_AUTHORIZATION"] = f"Ekila {user_token.access_token}"
        response = RadioMenuViewSet.as_view({"post": "create"})(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            RadioMenuModel.objects.filter(
                title="ekila", radio__user_id=user1.pk
            ).exists()
            is False
        )
