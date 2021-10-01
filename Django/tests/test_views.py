from mixer.backend.django import mixer
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from teams.models import Team, TeamShots, Category, Reviews, Racer

import pytest


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def team(db):
    return mixer.blend('teams.Teams')

def test_team_detail(factory, team):
    path = reverse('detail', kwargs={'pk': 1})
    request = factory.get(path)
    request.user = mixer.blend(User)
