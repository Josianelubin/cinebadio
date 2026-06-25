from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse email")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "champ-form"})


class ProfilForm(forms.ModelForm):
    """Modification des informations du profil."""

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "bio", "date_naissance", "avatar"]
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "avatar":
                field.widget.attrs.update({"class": "champ-form"})


class ParametresForm(forms.ModelForm):
    """Paramètres du compte (préférences, sécurité légère)."""

    class Meta:
        model = CustomUser
        fields = ["notifications_email"]
