from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import InscriptionForm, ParametresForm, ProfilForm


class ConnexionView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class DeconnexionView(LogoutView):
    next_page = "accounts:login"


def inscription_view(request):
    if request.user.is_authenticated:
        return redirect("films:home")

    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue sur CinéBadio, {user.username} !")
            return redirect("films:home")
    else:
        form = InscriptionForm()
    return render(request, "accounts/inscription.html", {"form": form})


@login_required
def profil_view(request):
    return render(request, "accounts/profil.html", {"profil": request.user})


@login_required
def modifier_profil_view(request):
    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("accounts:profil")
    else:
        form = ProfilForm(instance=request.user)
    return render(request, "accounts/modifier_profil.html", {"form": form})


@login_required
def parametres_view(request):
    if request.method == "POST":
        form = ParametresForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Paramètres enregistrés.")
            return redirect("accounts:parametres")
    else:
        form = ParametresForm(instance=request.user)
    return render(request, "accounts/parametres.html", {"form": form})


@login_required
def changer_mot_de_passe_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été changé avec succès.")
            return redirect("accounts:profil")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/changer_mot_de_passe.html", {"form": form})
