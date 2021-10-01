from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.base import View
from .models import Team, Category, Reviews
from .forms import ReviewForm


def favourite_post(request, id):
    team = get_object_or_404(Team, id=id)
    if team.favourite.filter(id=request.user.id).exists():
        team.favourite.remove(request.user)
    else:
        team.favourite.add(request.user)
    return HttpResponseRedirect(team.get_absolute_url())


def post_favourite_list(request):
    user = request.user
    favourite_teams = user.favourite.all()
    context = {
        'favourite_teams': favourite_teams,
    }
    return render(request, 'teams/team_favourite_list.html', context)


class TeamDelete(DeleteView):
    model = Team
    success_url = reverse_lazy("team_list")


class Categorys:
    def get_category(self):
        return Category.objects.all()


class TeamsView(Categorys, ListView):
    model = Team
    queryset = Team.objects.all()


class TeamDetailView(Categorys, DetailView):
    model = Team
    slug_field = "url"


class AddReview(View):
    def post(self, request, pk):
       form = ReviewForm(request.POST)
       team = Team.objects.get(id=pk)
       if form.is_valid():
           form = form.save(commit=False)
           form.team = team
           form.save()
       return redirect(team.get_absolute_url())


class FilterTeamsView(Categorys, ListView):
    def get_queryset(self):
        queryset = Team.objects.filter(category__in=self.request.GET.getlist("category"))
        return queryset


class Search(Categorys, ListView):
    paginate_by = 3

    def get_queryset(self):
        return Team.objects.filter(title__contains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context