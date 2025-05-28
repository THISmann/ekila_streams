from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ekiladesign.models import Publicite
from ekiladesign.serializers import image_help_text
from ekiladesign.serializers import PubliciteDetailSerializer
from ekiladesign.validators import validate_image_size
from radio.models import Radio
from radio.models import RadioMenuModel
from radio.utils import extract_domain
from radio.utils import format_radio_king_radio_name
from radio.utils import remove_slash_on_uri


class RadioCreateOrUpdateSerializer(ModelSerializer):
    radio_image_icon = serializers.FileField(
        required=False,
        help_text=image_help_text,
        validators=[validate_image_size],
    )

    class Meta:
        model = Radio
        exclude = ["user"]
        read_only_fields = [
            "is_active",
            "created_at",
            "updated_at",
            "url_api_radio_current_song",
            "url_api_radio_history",
        ]

    def update(self, instance, validated_data):
        data = self.update_serializer_fields(validated_data)
        return super().update(instance, data)

    def create(self, validated_data):
        data = self.update_serializer_fields(validated_data)
        try:
            return super().create(data)
        except IntegrityError:
            message = _("A radio with this name already exists.")
            raise serializers.ValidationError(
                {"message": message}, code="unique_radio_name"
            )
        except Exception as e:
            raise serializers.ValidationError({"message": str(e)})

    def update_serializer_fields(self, data):
        radio = data
        radio_type = radio.get("server_type")
        match radio_type:
            case "icecast":
                radio["url_server_radio"] = url_server_radio = remove_slash_on_uri(
                    radio["url_server_radio"]
                )
                radio[
                    "url_api_radio_current_song"
                ] = f"{url_server_radio}/status-json.xsl"
                radio["url_api_radio_history"] = f"{url_server_radio}/status-json.xsl"
            case "shoutcast":
                radio["url_server_radio"] = url_server_radio = remove_slash_on_uri(
                    radio["url_server_radio"]
                )
                radio[
                    "url_api_radio_current_song"
                ] = f"{url_server_radio}/currentsong?sid={radio['sid']}"
                radio[
                    "url_api_radio_history"
                ] = f"{url_server_radio}/played.html?sid={radio['sid']}"
            case "everestcast":
                domain = extract_domain(radio["url_flux_radio"])
                radio[
                    "url_api_radio_current_song"
                ] = f"{domain}:{radio['radio_account_port']}/api/v2/history/?format=json&limit=1&offset=0"
                radio[
                    "url_api_radio_history"
                ] = f"{domain}:{radio['radio_account_port']}/api/v2/history/?format=json&limit=5&offset=1"
            case "everestpanel":
                domain = extract_domain(radio["url_flux_radio"])
                radio["url_server_radio"] = domain
                radio[
                    "url_api_radio_current_song"
                ] = f"{domain}/widget/get-current-track-api?station={radio['station_id']}"
                radio[
                    "url_api_radio_history"
                ] = f"{domain}/widget/get-past-tracks-api/{radio['station_id']}"
            case "rcast":
                radio[
                    "url_pannel_connexion"
                ] = url_pannel_connexion = remove_slash_on_uri(
                    radio["url_pannel_connexion"]
                )
                format_radio_name = lambda value: value.replace(" ", "").lower()
                radio[
                    "url_api_radio_current_song"
                ] = f"{url_pannel_connexion}/json/stream/{format_radio_name(radio['name'])}"
                radio[
                    "url_api_radio_history"
                ] = f"{url_pannel_connexion}/json/stream/{format_radio_name(radio['name'])}"
            case "centovacast":
                radio[
                    "url_pannel_connexion"
                ] = url_pannel_connexion = remove_slash_on_uri(
                    radio["url_pannel_connexion"]
                )
                radio[
                    "url_api_radio_current_song"
                ] = f"{url_pannel_connexion}/rpc/{radio['username_radio_account']}/streaminfo.get"
                radio[
                    "url_api_radio_history"
                ] = f"{url_pannel_connexion}/recentfeed/{radio['username_radio_account']}/json/"
            case "azuracast":
                format_radio_name = lambda value: value.replace(" ", "").lower()
                radio[
                    "url_pannel_connexion"
                ] = url_pannel_connexion = remove_slash_on_uri(
                    radio["url_pannel_connexion"]
                )
                radio[
                    "url_api_radio_current_song"
                ] = f"{url_pannel_connexion}/api/nowplaying_static/{format_radio_name(str(radio['name']))}.json"
                radio[
                    "url_api_radio_history"
                ] = f"{url_pannel_connexion}/api/nowplaying_static/{format_radio_name(str(radio['name']))}.json"
            case "radioking":
                name_account = format_radio_king_radio_name(radio["name"])
                radio[
                    "url_api_radio_current_song"
                ] = f"https://api.radioking.io/widget/radio/{name_account}/track/current"
                radio[
                    "url_api_radio_history"
                ] = f"https://api.radioking.io/widget/radio/{name_account}/track/ckoi?limit=5"
        return radio


class RadioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radio
        fields = "__all__"
        read_only_fields = ["user", "is_active", "created_at", "updated_at"]


class RadioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radio
        fields = "__all__"


class AdminRadioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radio
        fields = "__all__"
        read_only_fields = ["is_active", "created_at", "updated_at"]


class RadioMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioMenuModel
        fields = "__all__"
        read_only_fields = ["id"]


class WebSocketRadioSerializer(serializers.Serializer):
    radio = RadioCreateOrUpdateSerializer()
    action = serializers.CharField()


class MedataRadioSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    radio_flux = serializers.CharField()
    title = serializers.CharField()
    album_title = serializers.CharField()
    cover = serializers.CharField()
    artist_name = serializers.CharField()
    song_history = serializers.ListSerializer(child=serializers.DictField())
    menu = RadioMenuSerializer(many=True, read_only=True)
    publicities = PubliciteDetailSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            radio_menus = RadioMenuModel.objects.filter(radio=instance["id"])
            pubs = Publicite.objects.filter(user__pk=instance["user_id"])
            response["menu"] = [RadioMenuSerializer(menu).data for menu in radio_menus]
            response["publicities"] = [
                PubliciteDetailSerializer(pub).data for pub in pubs
            ]
        except (RadioMenuModel.DoesNotExist, Publicite.DoesNotExist):
            response["menu"] = []
            response["publicities"] = []
        return response
