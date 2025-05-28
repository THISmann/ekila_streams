from typing import Callable

import pytest

from radio.factories import RadioMenuFactory
from radio.factories import RadioModelFactory


@pytest.fixture()
def build_radio() -> Callable:
    def _build_radio(**kwargs):
        return RadioModelFactory(**kwargs)

    return _build_radio


@pytest.fixture()
def build_radio_menu() -> Callable:
    def _build_radio_menu(**kwargs):
        return RadioMenuFactory(**kwargs)

    return _build_radio_menu
