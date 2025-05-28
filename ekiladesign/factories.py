import os
import tempfile

import factory

from ekiladesign.models import Publicite
from ekilauth.user.factories import UserModelFactory


class PubliciteModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publicite
        django_get_or_create = ("pub_image",)

    description = factory.Faker("text")
    is_enable = True
    user = factory.SubFactory(UserModelFactory, is_confirmed=True)
