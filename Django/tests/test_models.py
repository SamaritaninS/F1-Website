from mixer.backend.django import mixer
import pytest


@pytest.fixture
def team(request, db):
    return mixer.blend('teams.Teams', quantity=request.param)


@pytest.mark.parametrize('team', [1], indirect=True)
def test_team_is_in_stock(team):
    assert team.is_in_stock == True


@pytest.mark.parametrize('team', [0], indirect=True)
def test_wine_is_not_in_stock(team):
    assert team.is_in_stock == False
