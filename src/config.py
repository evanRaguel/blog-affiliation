"""
Configuration du projet Blog d'Affiliation Automatisé
Centralize tous les paramètres configurables du système
"""

import os

# ============================================================================
# CLÉS API ET AUTHENTIFICATION
# ============================================================================

# Clé API OpenAI (utiliser une variable d'environnement pour plus de sécurité)
# Pour configurer sous Windows: $env:OPENAI_API_KEY = "your-openai-api-key-here"
# Ne jamais stocker votre clé API directement dans le code source
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# ============================================================================
# IDs D'AFFILIATION
# ============================================================================

# Remplacez ces valeurs par vos propres IDs d'affiliation
AFFILIATES = {
    "amazon": "your-amazon-tag",       # Exemple: monblog-21
    "coinbase": "your-coinbase-ref",   # ID de parrainage Coinbase
    "ledger": "your-ledger-ref",       # ID d'affiliation Ledger
    "booking": "your-booking-ref",     # ID d'affiliation Booking.com
    "aliexpress": "your-aliexpress-ref", # ID d'affiliation AliExpress
}

# ============================================================================
# SOURCES DE DONNÉES
# ============================================================================

# Flux RSS à scraper pour des idées d'articles
RSS_FEEDS = [
    "https://www.journalduhacker.net/rss",
    "https://www.lemonde.fr/rss/une.xml",
    "https://korben.info/feed",
    # Ajoutez d'autres flux RSS ici
]

# Sources de deals et produits pour les liens d'affiliation
DEAL_SOURCES = [
    {"name": "Amazon", "url": "https://www.amazon.fr/deals", "type": "marketplace"},
    {"name": "AliExpress", "url": "https://best.aliexpress.com/", "type": "marketplace"},
    {"name": "KdoMonDeal", "url": "https://kdomondeal.com/", "type": "deals"},
    {"name": "AppSumo", "url": "https://appsumo.com/", "type": "deals"},
    # Ajoutez d'autres sources ici
]

# ============================================================================
# PARAMÈTRES DE GÉNÉRATION D'ARTICLES
# ============================================================================

ARTICLE_SETTINGS = {
    "min_words": 800,         # Nombre minimum de mots par article
    "max_words": 1500,        # Nombre maximum de mots par article
    "language": "fr",         # Langue des articles
    "tone": "informatif",     # Ton des articles (informatif, persuasif, etc.)
}

# ============================================================================
# CONFIGURATION GITHUB/DÉPLOIEMENT
# ============================================================================

# IMPORTANT: Remplacez ces valeurs par les informations de votre propre dépôt GitHub
GITHUB = {
    "repo_url": "https://github.com/evanRaguel/blog-affiliation",  # URL de votre dépôt
    "branch": "gh-pages",                                         # Branche pour GitHub Pages
}

# ============================================================================
# PARAMÈTRES DU SITE
# ============================================================================

SITE_CONFIG = {
    "title": "Mon Blog d'Affiliation",                            # Titre du blog
    "description": "Les meilleurs produits et deals sélectionnés pour vous",  # Description du site
    "base_url": "https://evanRaguel.github.io/blog-affiliation",   # URL de votre GitHub Pages
    "author": "Claude",                                           # Nom de l'auteur
    "language": "fr",                                            # Langue du site
}

# ============================================================================
# NICHES ET MOTS-CLÉS
# ============================================================================

# Définit les niches ciblées et les mots-clés associés pour la génération d'articles
NICHES = {
    "nomade_numerique": [
        "sac à dos digital nomad",
        "batterie solaire voyage",
        "moniteur portable",
        "forfait internet voyage",
        "esim internationale",
        "meilleur vpn nomade numérique",
    ],
    "crypto": [
        "portefeuille hardware crypto",
        "ledger nano x",
        "trezor model t",
        "staking ethereum",
        "meilleure plateforme crypto",
        "comment acheter bitcoin",
    ],
    # Vous pouvez ajouter d'autres niches ici
}

# ============================================================================
# PARAMÈTRES AVANCÉS
# ============================================================================

# Options de scraping
SCRAPING_OPTIONS = {
    "delay_min": 1.0,          # Délai minimum entre les requêtes (secondes)
    "delay_max": 3.0,          # Délai maximum entre les requêtes (secondes)
    "timeout": 10,             # Timeout des requêtes (secondes)
    "max_retries": 3,          # Nombre maximum de tentatives par requête
    "user_agent_rotation": True, # Rotation des user agents
}

# Options de génération d'articles
GENERATION_OPTIONS = {
    "model": "gpt-4",          # Modèle OpenAI à utiliser
    "temperature": 0.7,        # Température (créativité) de l'IA
    "max_articles_per_day": 2, # Nombre maximum d'articles générés par jour
}

# Options de construction du site
BUILDER_OPTIONS = {
    "posts_per_page": 10,      # Nombre d'articles par page sur l'index
    "enable_comments": False,  # Activer les commentaires (Disqus, etc.)
    "minify_html": True,       # Minifier les fichiers HTML
}
