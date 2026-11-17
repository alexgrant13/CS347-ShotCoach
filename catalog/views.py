from django.shortcuts import render

from .models import Board, Reference, Shot


def index(request):
    """Home page for ShotCoach."""
    context = {
        "num_shots": Shot.objects.count(),
        "num_boards": Board.objects.count(),
        "num_references": Reference.objects.count(),
    }
    return render(request, "catalog/index.html", context=context)
