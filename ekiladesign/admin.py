from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Publicite
from ekilauth.user.models import EkilaUser as User
from ekilauth.user.models import UserRole


class PubliciteAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(roles="client", is_confirmed=True),
        label=_("User (Client)"),
    )

    class Meta:
        model = Publicite
        fields = ["pub_image", "description", "user"]


@admin.action(description=_("Enable/Disable selected ads"))
def toggle_enable_ads(modeladmin, request, queryset) -> None:
    for pub in queryset:
        pub.is_enable = not pub.is_enable
        pub.save()


@admin.register(Publicite)
class PubliciteAdmin(admin.ModelAdmin):
    list_display = [
        "pub_image",
        "description",
        "is_enable",
        "user",
        "is_created_at",
        "is_updated_at",
    ]
    list_display_links = ["pub_image", "description"]
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    list_filter = [
        "is_enable",
        "is_created_at",
        "is_updated_at",
    ]
    search_fields = [
        "pub_image",
        "description",
        "is_enable",
        "is_created_at",
        "is_updated_at",
    ]
    readonly_fields = [
        "id",
        "is_created_at",
        "is_updated_at",
    ]
    fieldsets = [
        (
            "Publicite",
            {"fields": ["pub_image", "description", "user"]},
        ),
    ]
    form = PubliciteAdminForm
    actions = [toggle_enable_ads]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        queryset_by_role = {
            UserRole.ADMIN: qs,
            UserRole.REVENDEUR: qs.filter(user__created_by=request.user),
        }
        return queryset_by_role.get(request.user.roles, qs.none())
