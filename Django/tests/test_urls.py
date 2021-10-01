from django.test import SimpleTestCase
from django.urls import reverse, resolve
from teams.views import TeamDetailView, FilterTeamsView, AddReview, TeamsView, Search


class TestUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse("team_list")
        self.assertEquals(resolve(url).func.view_class, TeamsView)

    def test_filter_url_resolves(self):
        url = reverse("filter")
        self.assertEquals(resolve(url).func.view_class, FilterTeamsView)

    def test_search_url_resolves(self):
        url = reverse("search")
        self.assertEquals(resolve(url).func.view_class, Search)

    def test_detail_url_resolves(self):
        url = reverse("team_detail", args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, TeamDetailView)

