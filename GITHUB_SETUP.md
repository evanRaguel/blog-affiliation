# Configuration de GitHub pour le Blog d'Affiliation Automatisé

Ce guide vous aidera à configurer correctement GitHub pour héberger et automatiser votre blog d'affiliation.

## 1. Créer un nouveau repository GitHub

1. Connectez-vous à votre compte GitHub (ou créez-en un)
2. Cliquez sur "New repository" ou allez à https://github.com/new
3. Nommez votre repository (par exemple "mon-blog-affiliation")
4. Choisissez "Public" ou "Private" selon votre préférence
5. Ne cochez pas "Initialize this repository with a README"
6. Cliquez sur "Create repository"

## 2. Initialiser le dépôt Git local

Ouvrez PowerShell ou une invite de commande et exécutez:

```powershell
cd "c:\Users\claud\Blog d'Affiliation"
git init
git add .
git commit -m "Initial commit"
```

## 3. Connecter le dépôt local à GitHub

Remplacez `your-username` et `your-repo-name` par vos informations:

```powershell
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

## 4. Mettre à jour la configuration dans config.py

Ouvrez `src/config.py` et modifiez la section GitHub avec l'URL de votre repository:

```python
# Configuration GitHub
GITHUB = {
    "repo_url": "https://github.com/your-username/your-repo-name",
    "branch": "gh-pages",
}
```

## 5. Configurer GitHub Pages

1. Allez sur votre repository GitHub
2. Cliquez sur "Settings" > "Pages"
3. Dans "Source", sélectionnez "gh-pages" (sera créée automatiquement lors de la première publication)
4. Vous pouvez également configurer un domaine personnalisé dans cette section

## 6. Ajouter vos secrets GitHub Actions

Pour permettre à GitHub Actions d'utiliser votre clé API OpenAI:

1. Dans votre repository GitHub, allez à "Settings" > "Secrets and variables" > "Actions"
2. Cliquez sur "New repository secret"
3. Nom: `OPENAI_API_KEY`
4. Valeur: votre clé API OpenAI
5. Cliquez sur "Add secret"

## 7. Personnaliser la fréquence de publication automatique

Si vous souhaitez modifier la fréquence de génération des articles:

1. Modifiez le fichier `.github/workflows/blog_automation.yml`
2. Changez la section `cron` pour utiliser la fréquence désirée:

Format cron: `minute heure jour-du-mois mois jour-de-semaine`

Exemples:
- Tous les jours à 9h: `0 9 * * *`
- Tous les lundis à 10h: `0 10 * * 1`
- Premier jour du mois à 0h: `0 0 1 * *`

## 8. Tester la publication manuelle

1. Après avoir configuré GitHub, lancez une exécution complète:
```powershell
cd "c:\Users\claud\Blog d'Affiliation"
python src/run_all.py
```

2. Vérifiez que le déploiement fonctionne en consultant l'URL de votre site GitHub Pages:
`https://your-username.github.io/your-repo-name/`

## 9. Déclencher manuellement le workflow GitHub Actions

Vous pouvez également déclencher le workflow manuellement:

1. Allez sur votre repository GitHub
2. Cliquez sur "Actions" > "Automated Blog Generation"
3. Cliquez sur "Run workflow" > "Run workflow"

## Dépannage

- **Erreur de push**: Vérifiez que vous avez les droits d'accès au repository
- **Actions non déclenchées**: Vérifiez que votre workflow est activé
- **Erreur de déploiement**: Assurez-vous que la branche "gh-pages" est configurée comme source dans GitHub Pages
- **Clé API non reconnue**: Vérifiez que le secret OPENAI_API_KEY est correctement configuré
