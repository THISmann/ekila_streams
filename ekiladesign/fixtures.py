from typing import Callable

import faker
import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ekiladesign.factories import PubliciteModelFactory


@pytest.fixture()
def build_publicite() -> Callable:
    def _build_publicite(**kwargs):
        return PubliciteModelFactory(**kwargs)

    return _build_publicite


@pytest.fixture()
def generate_fake_image() -> SimpleUploadedFile:
    fake = faker.Faker()
    image_binary = fake.binary(length=settings.MAX_PUBLICITE_IMAGE_SIZE)
    image_file = SimpleUploadedFile(
        name="tests/myimage.jpg",
        content=image_binary,
    )
    return image_file
