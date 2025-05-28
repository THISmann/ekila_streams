from random import randint

import factory

from ekilauth.user.factories import UserModelFactory
from radio.models import Radio
from radio.models import RadioMenuModel
from radio.utils import extract_domain


class RadioModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Radio

    name = factory.Faker("name")
    url_cover_default = factory.Faker("url")
    url_site = factory.Faker("url")
    url_server_radio = factory.Faker("url")
    sid = factory.Sequence(lambda n: n)
    url_flux_radio = factory.LazyAttribute(
        lambda obj: f"{extract_domain(obj.url_server_radio)}:{randint(8000, 9999)}/stream"
    )
    url_pannel_connexion = url_flux_radio
    radio_account_port = factory.Sequence(lambda n: randint(8000, 9000))
    username_radio_account = factory.Faker("name")
    station_id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserModelFactory, is_confirmed=True)


class RadioMenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RadioMenuModel
        django_get_or_create = ("title",)

    title = factory.Faker("name")
    link = factory.Faker("url")
