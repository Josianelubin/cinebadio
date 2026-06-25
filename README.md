# CinéBadio — Plateforme de films & séries (Django)

Projet Django complet : connexion, inscription, déconnexion, profil et paramètres
utilisateur, gestion des films/séries dans l'admin (Jazzmin), sécurité renforcée,
prêt pour un déploiement gratuit sur **Render**.

## 1. Installation en local

```bash
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # puis remplissez les valeurs si besoin

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # pour accéder à /admin/

python manage.py runserver
```

Le site est sur **http://127.0.0.1:8000/** et l'admin sur **http://127.0.0.1:8000/admin/**.

## 2. Mettre votre logo

Déposez votre fichier **`badio.png`** dans `static/img/badio.png`.
Il sera utilisé automatiquement :
- comme icône du site (favicon)
- comme logo dans la barre latérale de l'admin Jazzmin
- comme logo sur la page de connexion de l'admin

Vous pouvez aussi ajouter `static/img/avatar_defaut.png` (avatar par défaut des utilisateurs).

## 3. Stockage des vidéos — ⚠️ IMPORTANT pour Render gratuit

Le plan gratuit de Render utilise un **disque éphémère** : tout fichier
envoyé via l'admin (vidéos, parfois affiches) est supprimé à chaque
redéploiement ou redémarrage du service.

**Ne stockez donc pas vos vidéos directement sur le serveur.** Dans l'admin,
chaque film et chaque épisode a un champ **"Lien vidéo"** : collez-y un lien
vers une vidéo hébergée ailleurs :

- **YouTube en mode "non répertorié"** (gratuit, le plus simple) — copiez le
  lien classique (`https://www.youtube.com/watch?v=...` ou `youtu.be/...`),
  le site le convertit automatiquement en lecteur intégré.
- **Cloudinary** (plan gratuit, ~25 Go) — pour un vrai fichier vidéo hébergé.
- **Bunny.net Stream** — pas cher, optimisé streaming, si le projet grandit.

Le champ "Fichier vidéo (local)" reste disponible mais seulement pour vos
tests en local — ne l'utilisez pas en production sur Render gratuit.

Pour les **affiches** (images), vous pouvez les garder en local si le service
ne redémarre pas souvent, mais pour plus de fiabilité à long terme, pensez
aussi à un service externe (Cloudinary gère aussi les images gratuitement).

## 4. Sécurité mise en place

- Mots de passe : règles de robustesse Django (longueur, similarité, mots de passe courants)
- **django-axes** : blocage automatique après 5 tentatives de connexion échouées (anti brute-force)
- Cookies de session et CSRF sécurisés (`Secure`, `HttpOnly`, `SameSite`)
- En production : redirection HTTPS forcée, HSTS activé
- Protection clickjacking (`X-Frame-Options: DENY`)
- Limite de taille des fichiers uploadés (10 Mo) pour éviter les abus
- `SECRET_KEY` et tous les secrets dans des variables d'environnement (jamais en dur)
- Validation stricte des formulaires (email unique, etc.)

## 5. Déploiement sur Render (plan gratuit)

1. Poussez ce projet sur un dépôt GitHub.
2. Sur [render.com](https://render.com), créez un **New Web Service** depuis votre dépôt.
   - Render détectera `render.yaml` automatiquement (Blueprint), ou configurez manuellement :
   - **Build Command** : `./build.sh`
   - **Start Command** : `gunicorn cinebadio.wsgi:application --bind 0.0.0.0:$PORT`
3. Ajoutez les variables d'environnement dans Render :
   - `DJANGO_SECRET_KEY` (générez-en une nouvelle, ne réutilisez pas celle du dev)
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_ALLOWED_HOSTS` = `votre-app.onrender.com`
   - `DATABASE_URL` (si vous ajoutez une base PostgreSQL Render, elle est injectée automatiquement)
   - `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` (optionnel, pour la réinitialisation de mot de passe par Gmail)
4. Render exécute `build.sh` (installe les dépendances, collecte les fichiers statiques, applique les migrations) puis démarre le service.
5. Une fois en ligne, créez un superutilisateur via le **Shell** Render :
   ```bash
   python manage.py createsuperuser
   ```

## 6. Structure du projet

```
cinebadio/        → configuration du projet (settings, urls)
accounts/         → connexion, inscription, profil, paramètres
films/            → modèles Film, Série, Épisode, Genre, Liste à voir
templates/         → template de base
static/            → CSS du site + CSS admin personnalisé + logo
```

## 7. Identifiants de test

Après `createsuperuser`, connectez-vous sur `/admin/` pour ajouter vos
premiers films, séries et genres. Les films/séries créés avec "Publié" ✅
apparaîtront automatiquement sur le site.
