"""
Script principal d'automatisation du blog d'affiliation.
Exécute toute la chaîne : scraping -> génération -> construction -> publication.
"""

import os
import time
import logging
from datetime import datetime
import sys
from typing import Dict, Any

# Import des modules du projet
from scraper import Scraper
from generator import ArticleGenerator
from builder import SiteBuilder
from publisher import Publisher

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'c:\\Users\\claud\\Blog d\'Affiliation\\logs\\blog_run_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('blog_automation')

def run_pipeline(options: Dict[str, Any] = None) -> bool:
    """
    Exécute toute la chaîne d'automatisation.
    
    Args:
        options: Options de configuration pour l'exécution.
        
    Returns:
        True si l'exécution a réussi, False sinon.
    """
    # Options par défaut
    default_options = {
        'run_scraper': True,
        'run_generator': True,
        'run_builder': True,
        'run_publisher': True,
        'build_all': False,
        'publish_platform': 'github',
        'use_proxy': False,
    }
    
    # Fusionner les options fournies avec les options par défaut
    if options:
        options = {**default_options, **options}
    else:
        options = default_options
    
    success = True
    start_time = time.time()
    
    # Créer le dossier de logs s'il n'existe pas
    os.makedirs('c:\\Users\\claud\\Blog d\'Affiliation\\logs', exist_ok=True)
    
    logger.info(f"Début de l'exécution du pipeline d'automatisation")
    
    try:
        # Étape 1: Scraping
        if options['run_scraper']:
            logger.info("Exécution du scraper...")
            scraper = Scraper(use_proxy=options['use_proxy'])
            scrape_results = scraper.run()
            logger.info(f"Scraping terminé: {scrape_results['rss_count']} articles RSS, {scrape_results['products_count']} produits")
        
        # Étape 2: Génération d'article
        if options['run_generator']:
            logger.info("Génération d'article...")
            generator = ArticleGenerator()
            article_path = generator.run()
            
            if article_path:
                logger.info(f"Article généré: {article_path}")
            else:
                logger.warning("Échec de la génération d'article")
                success = False
        
        # Étape 3: Construction du site
        if options['run_builder']:
            logger.info("Construction du site...")
            builder = SiteBuilder()
            build_stats = builder.run(build_all=options['build_all'])
            
            logger.info(f"Construction terminée: {build_stats['built_articles']} articles construits sur {build_stats['total_articles']} au total")
        
        # Étape 4: Publication
        if options['run_publisher']:
            logger.info(f"Publication sur {options['publish_platform']}...")
            publisher = Publisher()
            publish_success = publisher.run(platform=options['publish_platform'])
            
            if publish_success:
                logger.info(f"Publication réussie sur {options['publish_platform']}")
            else:
                logger.error(f"Échec de la publication sur {options['publish_platform']}")
                success = False
        
        # Durée totale d'exécution
        execution_time = time.time() - start_time
        logger.info(f"Exécution terminée en {execution_time:.2f} secondes")
        
        return success
        
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution du pipeline: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    # Récupérer les options depuis les arguments de ligne de commande
    options = {}
    
    # Exemple d'arguments:
    # --no-scraper: Ne pas exécuter le scraper
    # --no-generator: Ne pas exécuter le générateur
    # --no-builder: Ne pas exécuter le builder
    # --no-publisher: Ne pas exécuter le publisher
    # --build-all: Reconstruire tous les articles (même si déjà à jour)
    # --platform netlify: Publier sur Netlify au lieu de GitHub
    # --use-proxy: Utiliser un proxy pour le scraping
    
    for arg in sys.argv[1:]:
        if arg == '--no-scraper':
            options['run_scraper'] = False
        elif arg == '--no-generator':
            options['run_generator'] = False
        elif arg == '--no-builder':
            options['run_builder'] = False
        elif arg == '--no-publisher':
            options['run_publisher'] = False
        elif arg == '--build-all':
            options['build_all'] = True
        elif arg == '--use-proxy':
            options['use_proxy'] = True
        elif arg.startswith('--platform='):
            options['publish_platform'] = arg.split('=')[1]
    
    success = run_pipeline(options)
    
    if not success:
        sys.exit(1)
