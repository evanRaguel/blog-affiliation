# Blog d'Affiliation Automatisé et Anonyme

Ce projet est un système automatisé de création et publication d'un blog d'affiliation qui fonctionne sans intervention humaine. Il utilise le scraping de données, la génération d'articles par IA et la publication sur des plateformes statiques comme GitHub Pages ou Netlify.

## Fonctionnement global

1. **Scraping automatisé** : récupère des données depuis des flux RSS, des marketplaces et des sites de deals.
2. **Génération d'articles par IA** : utilise OpenAI GPT pour créer des articles SEO optimisés.
3. **Insertion de liens affiliés** : ajoute des liens d'affiliation masqués via un système de redirection.
4. **Publication sur site statique** : déploie le contenu généré sur GitHub Pages ou Netlify.
5. **Automatisation complète** : le tout est exécutable via un script unique ou des tâches planifiées.

## Configuration et secrets

### Variables d'environnement locales

Pour utiliser ce projet localement, configurez votre clé API OpenAI comme variable d'environnement :

```powershell
# Dans PowerShell
$env:OPENAI_API_KEY = "votre-clé-api-openai"
```

### GitHub Actions (pour l'automatisation)

1. Allez dans les paramètres de votre dépôt GitHub
2. Cliquez sur "Secrets and variables" > "Actions"
3. Ajoutez un nouveau secret nommé `OPENAI_API_KEY` avec votre clé API

Cette configuration est nécessaire pour que les GitHub Actions puissent générer des articles automatiquement.

## Structure du projet

```
project/
├── src/
│   ├── scraper.py        # Récupération des flux RSS et scraping des sites de deals/marketplaces.
│   ├── generator.py      # Génération d'articles via IA (OpenAI GPT-4 ou modèle local).
│   ├── builder.py        # Création des pages HTML à partir du contenu généré (templates + liens affiliés).
│   ├── publisher.py      # Commit & push sur le repo GitHub / déploiement Pages.
│   ├── config.py         # Clés API, IDs affiliés, URLs des sources, paramètres divers.
│   └── run_all.py        # Script principal qui exécute toute la chaîne.
├── templates/
│   ├── base.html         # Template HTML de base.
│   ├── article.html      # Template pour les articles.
│   └── index.html        # Template pour la page d'accueil.
├── content/
│   ├── posts/            # Articles générés (Markdown).
│   └── data/             # Données scrapées (JSON).
├── static/               # Site statique généré.
│   ├── posts/            # Articles HTML générés.
│   ├── go/               # Redirections pour liens affiliés.
│   └── assets/           # CSS, JS, images.
├── logs/                 # Logs d'exécution.
├── .github/workflows/    # Workflows GitHub Actions pour l'automatisation.
└── deploy/               # Dossier temporaire pour la publication.
```

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Git (pour la publication sur GitHub Pages)
- Compte OpenAI (pour l'API GPT)
- Compte GitHub (pour l'hébergement et l'automatisation)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Configuration

1. Créez un nouveau repository GitHub pour héberger votre blog
2. Modifiez le fichier `src/config.py` avec vos informations :
   - Clé API OpenAI (définir comme variable d'environnement pour plus de sécurité)
   - IDs d'affiliation (Amazon, Coinbase, etc.)
   - URLs des sources de scraping (ajouter vos sources préférées)
   - Configuration GitHub (remplacez `your-username/your-blog-repo` par votre repo)
   - Paramètres du site (titre, description, URL)

3. Configuration de l'API OpenAI (sous Windows):
   ```powershell
   $env:OPENAI_API_KEY = "votre-clé-api-openai"
   ```

## Test du système

Pour tester le système étape par étape:

```bash
python test_full_pipeline.py
```

Cela vérifiera chaque composant de la chaîne sans réellement publier le site.

## Utilisation

### Exécution du mode démo

```bash
python demo.py
```

Ce script offre un menu interactif pour tester chaque module séparément.

### Exécution complète

```bash
python src/run_all.py
```

### Options

- `--no-scraper` : Ne pas exécuter l'étape de scraping
- `--no-generator` : Ne pas générer de nouvel article
- `--no-builder` : Ne pas construire le site
- `--no-publisher` : Ne pas publier le site
- `--build-all` : Reconstruire tous les articles (même si déjà à jour)
- `--platform=netlify` : Publier sur Netlify au lieu de GitHub Pages
- `--use-proxy` : Utiliser un proxy pour le scraping

### Automatisation avec GitHub Actions

Le projet est configuré pour s'exécuter automatiquement grâce à GitHub Actions. Le workflow `blog_automation.yml` exécutera le pipeline complet deux fois par semaine.

Pour configurer l'automatisation:

1. Assurez-vous que votre dépôt GitHub est configuré avec la bonne URL dans `config.py`
2. Ajoutez votre clé API OpenAI comme secret GitHub:
   - Accédez à votre dépôt GitHub > Settings > Secrets and variables > Actions
   - Créez un nouveau secret nommé `OPENAI_API_KEY` avec votre clé API
3. Activez GitHub Pages pour votre dépôt:
   - Accédez à Settings > Pages
   - Sélectionnez la branche `gh-pages` comme source
4. Poussez le projet vers votre dépôt GitHub

### Planification locale

Pour une exécution automatique en local avec le Planificateur de tâches Windows:

1. Ouvrez le Planificateur de tâches Windows
2. Créez une nouvelle tâche de base
3. Planifiez-la pour s'exécuter selon votre fréquence préférée
4. Ajoutez l'action: Démarrer un programme
5. Programme/script: `python`
6. Arguments: `c:\chemin\vers\Blog d'Affiliation\src\run_all.py`
7. Démarrer dans: `c:\chemin\vers\Blog d'Affiliation`

## Niches ciblées

Le projet est configuré pour cibler deux niches principales:

1. **Nomades numériques** (voyage & tech) - Matériel portable, applications de voyage, etc.
2. **Outils & gadgets crypto** - Portefeuilles hardware, plateformes d'échange, etc.

Vous pouvez facilement ajouter d'autres niches en modifiant la section `NICHES` dans `config.py`.

## Personnalisation

### Ajouter une nouvelle niche

Dans `config.py`, ajoutez une nouvelle entrée à la section `NICHES` avec les mots-clés pertinents:

```python
"nouvelle_niche": [
    "mot-clé 1",
    "mot-clé 2",
    "mot-clé 3",
]
```

### Modifier les templates

Les templates HTML se trouvent dans le dossier `templates/`. Ils utilisent Jinja2 comme moteur de template.

### Ajouter des sources de contenus

Pour ajouter de nouvelles sources de données, ajoutez des URLs à la liste `RSS_FEEDS` ou `DEAL_SOURCES` dans `config.py`.

## Dépannage

- **Erreur d'API OpenAI**: Vérifiez que votre clé API est correcte et que vous avez des crédits
- **Erreurs de scraping**: Certains sites peuvent bloquer le scraping. Essayez l'option `--use-proxy`
- **Erreurs de publication**: Vérifiez vos paramètres GitHub dans `config.py`
- **Templates non trouvés**: Vérifiez que tous les fichiers existent dans le dossier `templates/`

## Licence

Ce projet est fourni à titre éducatif uniquement. L'utilisation de ce code doit respecter les conditions d'utilisation des services tiers (API OpenAI, programmes d'affiliation, etc.).
