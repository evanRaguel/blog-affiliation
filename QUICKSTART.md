# Guide de démarrage rapide - Blog d'Affiliation Automatisé

Félicitations ! Votre système de blog d'affiliation automatisé est maintenant configuré et prêt à l'emploi. Voici un guide rapide pour commencer à l'utiliser.

## Configuration initiale terminée ✓

- ✅ Structure du projet créée
- ✅ Modules principaux développés (scraper, generator, builder, publisher)
- ✅ Templates HTML configurés
- ✅ API OpenAI intégrée
- ✅ Système de génération d'articles fonctionnel
- ✅ Système de création de site statique
- ✅ Workflow GitHub Actions pour l'automatisation
- ✅ Documentation complète

## Étapes restantes à effectuer

### 1. Configurer votre clé API OpenAI

```powershell
$env:OPENAI_API_KEY = "votre-clé-api-openai"
```

### 2. Mettre à jour vos identifiants d'affiliation

Ouvrez `src/config.py` et remplacez les valeurs dans la section `AFFILIATES` par vos propres IDs d'affiliation.

### 3. Configurer votre dépôt GitHub

Consultez le fichier `GITHUB_SETUP.md` pour des instructions détaillées sur la configuration de GitHub.

### 4. Personnaliser vos niches

Modifiez ou ajoutez des niches dans la section `NICHES` de `src/config.py` selon vos marchés cibles.

### 5. Tester le système

```powershell
python test_full_pipeline.py
```

### 6. Lancer la première exécution complète

```powershell
python src/run_all.py
```

## Fonctionnalités disponibles

- **Scraping de données**: Récupération automatique d'actualités et produits
- **Génération d'articles**: Création de contenus originaux par IA
- **Construction de site**: Création de pages HTML à partir des articles Markdown
- **Liens d'affiliation**: Insertion automatique et cloaking des liens
- **Publication**: Déploiement automatique sur GitHub Pages
- **Automatisation**: Exécution programmée via GitHub Actions

## Maintenance

- Vérifiez régulièrement que votre clé API OpenAI est valide
- Mettez à jour les sources de scraping si certaines deviennent indisponibles
- Surveillez les statistiques de votre blog pour ajuster les niches ciblées
- Mettez à jour vos IDs d'affiliation si nécessaire

## Support

Pour toute question ou problème, consultez la documentation ou créez une issue sur le dépôt GitHub.
