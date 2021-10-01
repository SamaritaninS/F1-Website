from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path("", views.TeamsView.as_view(), name="team_list"),
    path("search/", views.Search.as_view(), name='search'),
    path("filter/", views.FilterTeamsView.as_view(), name='filter'),
    url(r"favourites/$", views.post_favourite_list, name='post_favourite_list'),
    url(r"(?P<id>\d+)/favourite_post/$", views.favourite_post, name='favourite_post'),
    path("<slug:slug>/", views.TeamDetailView.as_view(), name="team_detail"),
    url(r"team/(?P<pk>[0-9]+)/delete/$", views.TeamDelete.as_view(), name="team_delete"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]