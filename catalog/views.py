from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import ShotForm
from .models import Board, Reference, Shot


def index(request):
    """Home page for ShotCoach."""
    context = {
        "num_shots": Shot.objects.count(),
        "num_boards": Board.objects.count(),
        "num_references": Reference.objects.count(),
    }
    return render(request, "catalog/index.html", context=context)


class ShotCreateView(LoginRequiredMixin, generic.CreateView):
    """Upload a new photo."""

    model = Shot
    form_class = ShotForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ShotDetailView(LoginRequiredMixin, generic.DetailView):
    """Show one of the user's shots."""

    model = Shot

    def get_queryset(self):
        return Shot.objects.filter(owner=self.request.user)
