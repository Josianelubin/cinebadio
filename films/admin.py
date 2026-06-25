from django.contrib import admin
from django.utils.html import format_html

from .models import Episode, Film, Genre, ListeAVoir, Serie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ("saison", "numero", "titre", "duree_minutes", "lien_video", "fichier_video")


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = (
        "affiche_miniature", "titre", "annee_sortie", "duree_minutes",
        "note", "a_la_une", "publie",
    )
    list_display_links = ("titre",)
    list_editable = ("a_la_une", "publie")
    list_filter = ("genres", "annee_sortie", "publie", "a_la_une")
    search_fields = ("titre", "realisateur", "description")
    filter_horizontal = ("genres",)
    readonly_fields = ("cree_le", "apercu_affiche")
    fieldsets = (
        ("Informations principales", {
            "fields": ("titre", "description", "realisateur", "genres")
        }),
        ("Médias", {
            "fields": ("affiche", "apercu_affiche", "bande_annonce_url", "lien_video", "fichier_video"),
            "description": (
                "Pour le film complet : utilisez de préférence 'Lien vidéo complet' "
                "(YouTube non listé, Cloudinary, Bunny.net...). Le fichier local est "
                "effacé à chaque redéploiement sur Render gratuit."
            ),
        }),
        ("Détails", {
            "fields": ("annee_sortie", "duree_minutes", "note")
        }),
        ("Publication", {
            "fields": ("publie", "a_la_une", "cree_le")
        }),
    )

    @admin.display(description="Affiche")
    def affiche_miniature(self, obj):
        if obj.affiche:
            return format_html(
                '<img src="{}" style="height:60px;width:42px;object-fit:cover;'
                'border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.4);" />',
                obj.affiche.url,
            )
        return "—"

    @admin.display(description="Aperçu")
    def apercu_affiche(self, obj):
        if obj.affiche:
            return format_html(
                '<img src="{}" style="max-height:220px;border-radius:10px;" />',
                obj.affiche.url,
            )
        return "Aucune affiche"


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = (
        "affiche_miniature", "titre", "annee_debut", "nombre_saisons",
        "note", "a_la_une", "publie",
    )
    list_display_links = ("titre",)
    list_editable = ("a_la_une", "publie")
    list_filter = ("genres", "annee_debut", "publie", "a_la_une")
    search_fields = ("titre", "description")
    filter_horizontal = ("genres",)
    inlines = [EpisodeInline]
    fieldsets = (
        ("Informations principales", {
            "fields": ("titre", "description", "genres")
        }),
        ("Médias", {
            "fields": ("affiche", "bande_annonce_url")
        }),
        ("Détails", {
            "fields": ("annee_debut", "nombre_saisons", "note")
        }),
        ("Publication", {
            "fields": ("publie", "a_la_une")
        }),
    )

    @admin.display(description="Affiche")
    def affiche_miniature(self, obj):
        if obj.affiche:
            return format_html(
                '<img src="{}" style="height:60px;width:42px;object-fit:cover;'
                'border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.4);" />',
                obj.affiche.url,
            )
        return "—"


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("serie", "saison", "numero", "titre", "duree_minutes")
    list_filter = ("serie", "saison")
    search_fields = ("titre", "serie__titre")


@admin.register(ListeAVoir)
class ListeAVoirAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "film", "serie", "ajoute_le")
    list_filter = ("ajoute_le",)
    search_fields = ("utilisateur__username",)
