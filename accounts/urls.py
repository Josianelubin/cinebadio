from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("connexion/", views.ConnexionView.as_view(), name="login"),
    path("deconnexion/", views.DeconnexionView.as_view(), name="logout"),
    path("inscription/", views.inscription_view, name="inscription"),
    path("profil/", views.profil_view, name="profil"),
    path("profil/modifier/", views.modifier_profil_view, name="modifier_profil"),
    path("parametres/", views.parametres_view, name="parametres"),
    path("mot-de-passe/", views.changer_mot_de_passe_view, name="changer_mot_de_passe"),
]
