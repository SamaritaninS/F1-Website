import pytest
from django.contrib.auth.models import User, Permission, Group


@pytest.fixture
def user_admin(db) -> User:
    group = Group.objects.create(name="app_user")
    change_user_permissions = Permission.objects.filter(
        codenamein=["change_user", "view_user"],
    )
    group.permissions.add(*change_user_permissions)
    user = User.objects.create_user("A")
    user.groups.add(group)
    return user


@pytest.fixture
def user_test(db) -> User:
    group = Group.objects.create(name="app_user")
    change_user_permissions = Permission.objects.filter(
        codenamein=["change_user", "view_user"],
    )
    group.permissions.add(*change_user_permissions)
    user = User.objects.create_user("B")
    user.groups.add(group)
    return user


def test_should_create_two_users(user_admin: User, user_test: User) -> None:
    assert user_admin.pk != user_test.pk