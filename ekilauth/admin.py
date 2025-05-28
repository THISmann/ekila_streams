import random

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from ekilauth.user.models import EkilaUser
from ekilauth.user.models import UserRole


@admin.action(description=_("Confirm/Unconfirm selected users"))
def toggle_active_users(modeladmin, request, queryset):
    for user in queryset:
        user.is_confirmed = not user.is_confirmed
        user.save()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput
    )

    class Meta:
        model = EkilaUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "roles",
            "is_confirmed",
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        validate_password(password2)
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(BaseUserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = EkilaUser
        fields = "__all__"


@admin.register(EkilaUser)
class EkilaUserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_confirmed", "roles")
    search_fields = ("first_name", "last_name", "username", "email")
    list_filter = ("is_confirmed", "roles")
    list_per_page = settings.ADMIN_LIST_PER_PAGE
    actions = [toggle_active_users]
    add_form = UserCreationForm
    form = UserChangeForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "roles",
                    "is_confirmed",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "roles", "created_by")},
        ),
        (
            _("Permissions"),
            {"fields": ("is_confirmed", "confirm_number", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        queryset_by_role = {
            UserRole.ADMIN: qs,
            UserRole.REVENDEUR: qs.filter(Q(created_by=request.user)),
        }
        return queryset_by_role.get(request.user.roles, qs.none())

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.confirm_number = (
                random.randint(settings.MIN_VALUE, settings.MAX_VALUE)
                if obj.is_confirmed
                else None
            )
        obj.save()


admin.site.unregister(Site)

admin.site.unregister(Group)

admin.site.unregister(OutstandingToken)

admin.site.unregister(BlacklistedToken)
