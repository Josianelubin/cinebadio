from django.conf import settings
from django.db import models
from django.urls import reverse


def lien_vers_embed(url: str) -> str:
    """Convertit un lien YouTube classique en lien 'embed' utilisable dans un <iframe>."""
    if not url:
        return ""
    if "youtu.be/" in url:
        code = url.split("youtu.be/")[-1].split("?")[0]
        return f"https://www.youtube.com/embed/{code}"
    if "watch?v=" in url:
        code = url.split("watch?v=")[-1].split("&")[0]
        return f"https://www.youtube.com/embed/{code}"
    return url  # déjà un lien embed, ou un lien Cloudinary/Bunny.net direct


class Genre(models.Model):
    nom = models.CharField("Genre", max_length=50, unique=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Film(models.Model):
    titre = models.CharField("Titre", max_length=200)
    description = models.TextField("Synopsis")
    affiche = models.ImageField("Affiche", upload_to="films/affiches/")
    bande_annonce_url = models.URLField("Lien bande-annonce (YouTube)", blank=True)
    lien_video = models.URLField(
        "Lien vidéo complet (YouTube non listé / Cloudinary / Bunny.net)",
        blank=True,
        help_text=(
            "⚠️ Ne pas téléverser de gros fichiers vidéo ici sur Render gratuit "
            "(le disque est effacé à chaque redéploiement). Hébergez la vidéo sur "
            "YouTube en 'non listé', Cloudinary ou Bunny.net, puis collez le lien ici."
        ),
    )
    fichier_video = models.FileField(
        "Fichier vidéo (local — déconseillé sur Render gratuit)",
        upload_to="films/videos/",
        blank=True,
        null=True,
        help_text="À utiliser uniquement en développement local. Préférez 'lien_video' en production.",
    )
    genres = models.ManyToManyField(Genre, verbose_name="Genres", blank=True)
    annee_sortie = models.PositiveIntegerField("Année de sortie")
    duree_minutes = models.PositiveIntegerField("Durée (minutes)")
    realisateur = models.CharField("Réalisateur", max_length=150, blank=True)
    note = models.DecimalField("Note /10", max_digits=3, decimal_places=1, default=0)
    a_la_une = models.BooleanField("Mettre à la une", default=False)
    publie = models.BooleanField("Publié", default=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"
        ordering = ["-cree_le"]

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse("films:detail_film", args=[self.pk])

    @property
    def url_lecture(self):
        if self.lien_video:
            return lien_vers_embed(self.lien_video)
        if self.fichier_video:
            return self.fichier_video.url
        return ""

    @property
    def bande_annonce_embed(self):
        return lien_vers_embed(self.bande_annonce_url)


class Serie(models.Model):
    titre = models.CharField("Titre", max_length=200)
    description = models.TextField("Synopsis")
    affiche = models.ImageField("Affiche", upload_to="series/affiches/")
    bande_annonce_url = models.URLField("Lien bande-annonce (YouTube)", blank=True)
    genres = models.ManyToManyField(Genre, verbose_name="Genres", blank=True)
    annee_debut = models.PositiveIntegerField("Année de début")
    nombre_saisons = models.PositiveIntegerField("Nombre de saisons", default=1)
    note = models.DecimalField("Note /10", max_digits=3, decimal_places=1, default=0)
    a_la_une = models.BooleanField("Mettre à la une", default=False)
    publie = models.BooleanField("Publiée", default=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Série"
        verbose_name_plural = "Séries"
        ordering = ["-cree_le"]

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse("films:detail_serie", args=[self.pk])

    @property
    def bande_annonce_embed(self):
        return lien_vers_embed(self.bande_annonce_url)


class Episode(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name="episodes", verbose_name="Série")
    saison = models.PositiveIntegerField("Saison")
    numero = models.PositiveIntegerField("Numéro de l'épisode")
    titre = models.CharField("Titre de l'épisode", max_length=200)
    lien_video = models.URLField(
        "Lien vidéo (YouTube non listé / Cloudinary / Bunny.net)",
        blank=True,
        help_text="Privilégiez ce champ plutôt que le fichier local sur Render gratuit.",
    )
    fichier_video = models.FileField(
        "Fichier vidéo (local — déconseillé sur Render gratuit)",
        upload_to="series/episodes/", blank=True, null=True,
    )
    duree_minutes = models.PositiveIntegerField("Durée (minutes)", default=0)

    class Meta:
        verbose_name = "Épisode"
        verbose_name_plural = "Épisodes"
        ordering = ["saison", "numero"]
        unique_together = ("serie", "saison", "numero")

    def __str__(self):
        return f"{self.serie.titre} - S{self.saison:02d}E{self.numero:02d} - {self.titre}"

    @property
    def url_lecture(self):
        if self.lien_video:
            return lien_vers_embed(self.lien_video)
        if self.fichier_video:
            return self.fichier_video.url
        return ""


class ListeAVoir(models.Model):
    """Watchlist personnelle de chaque utilisateur."""

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liste_a_voir")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, blank=True, null=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, blank=True, null=True)
    ajoute_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Élément de la liste à voir"
        verbose_name_plural = "Liste à voir"
        ordering = ["-ajoute_le"]

    def __str__(self):
        titre = self.film.titre if self.film else (self.serie.titre if self.serie else "?")
        return f"{self.utilisateur.username} → {titre}"
