from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Film, Genre, ListeAVoir, Serie


def accueil_view(request):
    films_une = Film.objects.filter(publie=True, a_la_une=True)[:8]
    series_une = Serie.objects.filter(publie=True, a_la_une=True)[:8]
    derniers_films = Film.objects.filter(publie=True)[:12]
    dernieres_series = Serie.objects.filter(publie=True)[:12]
    return render(request, "films/accueil.html", {
        "films_une": films_une,
        "series_une": series_une,
        "derniers_films": derniers_films,
        "dernieres_series": dernieres_series,
    })


def liste_films_view(request):
    films = Film.objects.filter(publie=True)
    genre_id = request.GET.get("genre")
    if genre_id:
        films = films.filter(genres__id=genre_id)
    return render(request, "films/liste_films.html", {
        "films": films,
        "genres": Genre.objects.all(),
        "genre_actif": genre_id,
    })


def detail_film_view(request, pk):
    film = get_object_or_404(Film, pk=pk, publie=True)
    dans_la_liste = False
    if request.user.is_authenticated:
        dans_la_liste = ListeAVoir.objects.filter(utilisateur=request.user, film=film).exists()
    return render(request, "films/detail_film.html", {"film": film, "dans_la_liste": dans_la_liste})


def liste_series_view(request):
    series = Serie.objects.filter(publie=True)
    genre_id = request.GET.get("genre")
    if genre_id:
        series = series.filter(genres__id=genre_id)
    return render(request, "films/liste_series.html", {
        "series": series,
        "genres": Genre.objects.all(),
        "genre_actif": genre_id,
    })


def detail_serie_view(request, pk):
    serie = get_object_or_404(Serie, pk=pk, publie=True)
    saisons = {}
    for ep in serie.episodes.all():
        saisons.setdefault(ep.saison, []).append(ep)
    dans_la_liste = False
    if request.user.is_authenticated:
        dans_la_liste = ListeAVoir.objects.filter(utilisateur=request.user, serie=serie).exists()
    return render(request, "films/detail_serie.html", {
        "serie": serie, "saisons": saisons, "dans_la_liste": dans_la_liste,
    })


def recherche_view(request):
    requete = request.GET.get("q", "").strip()
    films, series = [], []
    if requete:
        films = Film.objects.filter(Q(titre__icontains=requete) | Q(description__icontains=requete), publie=True)
        series = Serie.objects.filter(Q(titre__icontains=requete) | Q(description__icontains=requete), publie=True)
    return render(request, "films/recherche.html", {"requete": requete, "films": films, "series": series})


@login_required
def ajouter_a_la_liste_view(request, type_contenu, pk):
    if type_contenu == "film":
        film = get_object_or_404(Film, pk=pk)
        obj, cree = ListeAVoir.objects.get_or_create(utilisateur=request.user, film=film)
        if cree:
            messages.success(request, f"« {film.titre} » ajouté à votre liste.")
        return redirect("films:detail_film", pk=pk)
    serie = get_object_or_404(Serie, pk=pk)
    obj, cree = ListeAVoir.objects.get_or_create(utilisateur=request.user, serie=serie)
    if cree:
        messages.success(request, f"« {serie.titre} » ajoutée à votre liste.")
    return redirect("films:detail_serie", pk=pk)


@login_required
def ma_liste_view(request):
    elements = ListeAVoir.objects.filter(utilisateur=request.user).select_related("film", "serie")
    return render(request, "films/ma_liste.html", {"elements": elements})
