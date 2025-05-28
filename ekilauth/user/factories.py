import random

import factory

from .models import EkilaUser


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EkilaUser

    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda obj: "%s@example.com" % obj.username)
    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    password = factory.django.Password("testpassword")
