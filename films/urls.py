from django.urls import path

from . import views

app_name = "films"

urlpatterns = [
    path("", views.accueil_view, name="home"),
    path("films/", views.liste_films_view, name="liste_films"),
    path("films/<int:pk>/", views.detail_film_view, name="detail_film"),
    path("series/", views.liste_series_view, name="liste_series"),
    path("series/<int:pk>/", views.detail_serie_view, name="detail_serie"),
    path("recherche/", views.recherche_view, name="recherche"),
    path("ma-liste/", views.ma_liste_view, name="ma_liste"),
    path("ajouter/<str:type_contenu>/<int:pk>/", views.ajouter_a_la_liste_view, name="ajouter_liste"),
]
