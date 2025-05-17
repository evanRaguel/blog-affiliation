"""
Script de démonstration du Blog d'Affiliation Automatisé.
Ce script montre comment utiliser chaque module séparément.
"""

import os
import sys
import time
from datetime import datetime

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.append('c:\\Users\\claud\\Blog d\'Affiliation')

# Vérifier que les dossiers nécessaires existent
os.makedirs('c:\\Users\\claud\\Blog d\'Affiliation\\content\\data', exist_ok=True)
os.makedirs('c:\\Users\\claud\\Blog d\'Affiliation\\content\\posts', exist_ok=True)
os.makedirs('c:\\Users\\claud\\Blog d\'Affiliation\\static', exist_ok=True)
os.makedirs('c:\\Users\\claud\\Blog d\'Affiliation\\logs', exist_ok=True)

def menu():
    """Affiche le menu principal."""
    print("\n" + "="*50)
    print("BLOG D'AFFILIATION AUTOMATISÉ - DÉMONSTRATION")
    print("="*50)
    print("1. Scraping - Récupérer des données")
    print("2. Génération - Créer un article via IA")
    print("3. Construction - Créer les pages HTML")
    print("4. Publication - Déployer le site")
    print("5. Chaîne complète (1-4)")
    print("6. Configurer les paramètres")
    print("0. Quitter")
    print("="*50)
    return input("Votre choix : ")

def run_scraper():
    """Exécute le module de scraping."""
    print("\n[+] Exécution du scraper...")
    
    try:
        # Ajouter le répertoire courant au chemin de recherche de modules
        sys.path.append('c:\\Users\\claud\\Blog d\'Affiliation')
        
        from src.scraper import Scraper
        from src.config import RSS_FEEDS, DEAL_SOURCES
        
        scraper = Scraper(use_proxy=False)
        results = scraper.run()
        
        print(f"\n[+] Scraping terminé avec succès !")
        print(f"[+] {results['rss_count']} articles RSS récupérés")
        print(f"[+] {results['products_count']} produits récupérés")
        
    except Exception as e:
        print(f"\n[-] Erreur lors du scraping : {str(e)}")
        return False
    
    return True

def run_generator():
    """Exécute le module de génération d'article."""
    print("\n[+] Exécution du générateur d'article...")
    
    try:
        from src.generator import ArticleGenerator
        generator = ArticleGenerator()
        article_path = generator.run()
        
        if article_path:
            print(f"\n[+] Article généré avec succès !")
            print(f"[+] Fichier créé : {article_path}")
        else:
            print("\n[-] Échec de la génération d'article")
            return False
        
    except Exception as e:
        print(f"\n[-] Erreur lors de la génération : {str(e)}")
        print("Vérifiez que votre clé API OpenAI est correctement configurée")
        return False
    
    return True

def run_builder():
    """Exécute le module de construction du site."""
    print("\n[+] Exécution du constructeur de site...")
    
    try:
        from src.builder import SiteBuilder
        builder = SiteBuilder()
        stats = builder.run(build_all=True)  # Forcer la reconstruction de tous les articles
        
        print(f"\n[+] Construction du site terminée avec succès !")
        print(f"[+] {stats['built_articles']} articles construits sur {stats['total_articles']} au total")
        print(f"[+] Site généré dans le dossier 'static'")
        
    except Exception as e:
        print(f"\n[-] Erreur lors de la construction : {str(e)}")
        return False
    
    return True

def run_publisher():
    """Exécute le module de publication du site."""
    print("\n[+] Exécution du module de publication...")
    print("\n[!] Pour utiliser cette fonction, vous devez avoir configuré un dépôt Git.")
    
    platform = input("\nPlateforme de publication (github/netlify) [github] : ").lower() or 'github'
    
    try:
        from src.publisher import Publisher
        publisher = Publisher()
        success = publisher.run(platform=platform)
        
        if success:
            print(f"\n[+] Publication terminée avec succès sur {platform} !")
        else:
            print(f"\n[-] Échec de la publication sur {platform}")
            return False
        
    except Exception as e:
        print(f"\n[-] Erreur lors de la publication : {str(e)}")
        return False
    
    return True

def run_complete_chain():
    """Exécute toute la chaîne d'automatisation."""
    print("\n[+] Exécution de la chaîne complète...")
    
    start_time = time.time()
    
    # Étape 1: Scraping
    if not run_scraper():
        return False
    
    # Étape 2: Génération
    if not run_generator():
        return False
    
    # Étape 3: Construction
    if not run_builder():
        return False
    
    # Étape 4: Publication
    publish_choice = input("\nSouhaitez-vous publier le site ? (o/n) [n] : ").lower()
    if publish_choice == 'o':
        if not run_publisher():
            return False
    
    execution_time = time.time() - start_time
    print(f"\n[+] Chaîne complète exécutée en {execution_time:.2f} secondes !")
    
    return True

def configure_settings():
    """Configure les paramètres du projet."""
    print("\n[+] Configuration des paramètres...")
    
    try:
        import src.config as config
        
        # Afficher les paramètres actuels
        print("\nParamètres actuels :")
        print(f"API OpenAI: {'Configurée' if config.OPENAI_API_KEY != 'your_openai_api_key_here' else 'Non configurée'}")
        print(f"Nom du site: {config.SITE_CONFIG['title']}")
        print(f"URL de base: {config.SITE_CONFIG['base_url']}")
        print(f"Niche 1: {list(config.NICHES.keys())[0]}")
        print(f"Niche 2: {list(config.NICHES.keys())[1]}")
        
        # Demander les nouveaux paramètres
        print("\nEntrez les nouveaux paramètres (laissez vide pour conserver les valeurs actuelles):")
        
        # Clé API OpenAI
        api_key = input(f"Clé API OpenAI : ")
        if api_key:
            # Dans un vrai script, on modifierait le fichier config.py
            # Ici, on simule juste la modification
            os.environ["OPENAI_API_KEY"] = api_key
            print(f"[+] Clé API OpenAI configurée comme variable d'environnement")
        
        # Nom du site
        site_title = input(f"Nom du site [{config.SITE_CONFIG['title']}] : ")
        if site_title:
            # Simuler la modification
            print(f"[+] Nom du site mis à jour: {site_title}")
        
        print("\n[+] Configuration terminée ! (Note: les modifications ne sont pas sauvegardées dans cette démo)")
        
    except Exception as e:
        print(f"\n[-] Erreur lors de la configuration : {str(e)}")
        return False
    
    return True

def main():
    """Fonction principale."""
    while True:
        choice = menu()
        
        if choice == '0':
            print("\nAu revoir !")
            sys.exit(0)
            
        elif choice == '1':
            run_scraper()
            
        elif choice == '2':
            run_generator()
            
        elif choice == '3':
            run_builder()
            
        elif choice == '4':
            run_publisher()
            
        elif choice == '5':
            run_complete_chain()
            
        elif choice == '6':
            configure_settings()
            
        else:
            print("\n[-] Choix invalide, veuillez réessayer.")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
