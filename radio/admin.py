from django import forms
from django.conf import settings
from django.contrib import admin
from django.db.models import Q
from django.forms import CharField
from django.utils.translation import gettext_lazy as _

from ekilauth.user.models import EkilaUser as User
from ekilauth.user.models import UserRole
from radio.models import Radio
from radio.models import RadioMenuModel
from radio.serializers import RadioCreateOrUpdateSerializer


@admin.action(description=_("Activate/Deactivate selected radios"))
def toggle_active_radios(modeladmin, request, queryset):
    for radio in queryset:
        radio.is_active = not radio.is_active
        radio.save()


class RadioAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_confirmed=True),
        label=_("user"),
    )

    class Meta:
        model = Radio
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(RadioAdminForm, self).__init__(*args, **kwargs)
        self.fields["url_server_radio"].required = True
        self.fields["url_flux_radio"].default = ""
        self.fields["url_pannel_connexion"].default = ""


@admin.register(Radio)
class RadioAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_display_links = [
        "name",
    ]
    list_filter = [
        "is_active",
        "created_at",
        "updated_at",
        "server_type",
    ]
    search_fields = [
        "name",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "url_api_radio_current_song",
        "url_api_radio_history",
    ]
    ordering = [
        "name",
        "is_active",
        "created_at",
        "updated_at",
    ]

    fieldsets = [
        (
            "Radio",
            {
                "fields": [
                    f.name
                    for f in Radio._meta.fields
                    if f.name not in ["id", "created_at", "updated_at"]
                ]
            },
        ),
    ]

    list_per_page = settings.ADMIN_LIST_PER_PAGE
    actions = [toggle_active_radios]
    form = RadioAdminForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        queryset_by_role = {
            UserRole.ADMIN: qs,
            UserRole.REVENDEUR: qs.filter(
                Q(user=request.user) | Q(user__created_by=request.user)
            ),
        }
        return queryset_by_role.get(request.user.roles, qs.none())

    def save_model(self, request, obj, form, change):
        for key, value in form.cleaned_data.items():
            field = form.fields[key]
            if isinstance(field, CharField) and value is None:
                form.cleaned_data[key] = ""

        serializer = RadioCreateOrUpdateSerializer(form.cleaned_data)
        radio = serializer.update_serializer_fields(serializer.data)
        obj.url_server_radio = radio["url_server_radio"]
        obj.url_api_radio_current_song = radio["url_api_radio_current_song"]
        obj.url_api_radio_history = radio["url_api_radio_history"]
        obj.url_panel_connexion = (
            radio["url_panel_connexion"] if "url_panel_connexion" in radio else None
        )

        obj.save()


@admin.register(RadioMenuModel)
class RadioMenuAdmin(admin.ModelAdmin):
    list_display = ("title", "link")
