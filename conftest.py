import pytest
from pytest_factoryboy import register

from api.account.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def base_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_staff=True, is_superuser=True)
    return new_user


@pytest.fixture
def test_user(db, user_factory):
    user = user_factory.create()
    yield user


@pytest.fixture
def test_user2(db, user_factory):
    user = user_factory.create()
    yield user
