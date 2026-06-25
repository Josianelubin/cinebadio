from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Utilisateur personnalisé avec avatar et bio pour le profil."""

    email = models.EmailField("Adresse email", unique=True)
    avatar = models.ImageField(
        "Photo de profil", upload_to="avatars/", blank=True, null=True
    )
    bio = models.TextField("Biographie", blank=True, max_length=300)
    date_naissance = models.DateField("Date de naissance", blank=True, null=True)
    notifications_email = models.BooleanField(
        "Recevoir les notifications par email", default=True
    )
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, "url"):
            return self.avatar.url
        return "/static/img/avatar_defaut.png"
