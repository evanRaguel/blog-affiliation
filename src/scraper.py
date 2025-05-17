"""
Module de scraping pour le blog d'affiliation automatisé.
Récupère des données depuis des flux RSS, des marketplaces et des sites de deals.
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
from datetime import datetime
from typing import List, Dict

# Import de la configuration
from config import RSS_FEEDS, DEAL_SOURCES

class Scraper:
    def __init__(self, use_proxy=True):
        """
        Initialise le scraper avec des options pour l'anonymat.
        
        Args:
            use_proxy (bool): Si True, utilise un proxy pour le scraping.
        """
        self.use_proxy = use_proxy
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        ]
        self.session = requests.Session()
        
        if self.use_proxy:
            # Configurez votre proxy ici si vous en utilisez un
            # self.session.proxies = {'http': 'http://your-proxy:port', 'https': 'https://your-proxy:port'}
            pass
        
        # Créer le dossier data s'il n'existe pas
        os.makedirs('c:\\Users\\claud\\Blog d\'Affiliation\\content\\data', exist_ok=True)
        
    def _get_random_headers(self):
        """Génère des en-têtes HTTP aléatoires pour ressembler à un navigateur normal."""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def scrape_rss_feed(self, feed_url: str) -> List[Dict]:
        """
        Récupère et parse les articles depuis un flux RSS spécifique.
        
        Args:
            feed_url: URL du flux RSS à scraper.
            
        Returns:
            Liste de dictionnaires contenant les informations des articles.
        """
        try:
            # Parser le flux RSS
            feed = feedparser.parse(feed_url)
            
            items = []
            for entry in feed.entries[:10]:  # Récupérer les 10 derniers articles
                item = {
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': feed_url,
                    'type': 'rss',
                }
                items.append(item)
            
            print(f"[+] Scraped {len(items)} items from {feed_url}")
            return items
            
        except Exception as e:
            print(f"[-] Error scraping RSS feed {feed_url}: {str(e)}")
            return []
    
    def fetch_rss(self, feed_urls: List[str]) -> List[Dict]:
        """
        Récupère et parse les articles depuis des flux RSS.
        
        Args:
            feed_urls: Liste des URLs de flux RSS à scraper.
            
        Returns:
            Liste de dictionnaires contenant les informations des articles.
        """
        all_items = []
        
        for feed_url in feed_urls:
            try:
                # Ajouter un délai pour éviter d'être détecté comme bot
                time.sleep(random.uniform(1, 3))
                
                # Utiliser la méthode scrape_rss_feed
                items = self.scrape_rss_feed(feed_url)
                all_items.extend(items)
                
            except Exception as e:
                print(f"[-] Error fetching RSS feed {feed_url}: {str(e)}")
        
        return all_items
    
    def scrape_marketplace(self, source: Dict) -> List[Dict]:
        """
        Scrape une marketplace ou un site de deals pour des produits.
        
        Args:
            source: Dictionnaire contenant les informations de la source.
            
        Returns:
            Liste de dictionnaires contenant les informations des produits.
        """
        products = []
        url = source['url']
        
        try:
            # Ajouter un délai pour éviter d'être détecté comme bot
            time.sleep(random.uniform(2, 5))
            
            # Effectuer la requête
            response = self.session.get(url, headers=self._get_random_headers(), timeout=10)
            response.raise_for_status()
            
            # Parser le HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Logique de scraping spécifique à chaque marketplace
            if source['name'] == 'Amazon':
                # Scraping spécifique à Amazon
                product_cards = soup.select('.dealContainer')
                for card in product_cards[:5]:  # Limiter à 5 produits
                    title_elem = card.select_one('.dealTitle')
                    price_elem = card.select_one('.dealPrice')
                    link_elem = card.select_one('a')
                    
                    if title_elem and link_elem:
                        product = {
                            'title': title_elem.text.strip(),
                            'price': price_elem.text.strip() if price_elem else 'Prix non disponible',
                            'link': 'https://www.amazon.fr' + link_elem['href'] if link_elem.get('href') else '',
                            'source': source['name'],
                            'type': source['type'],
                            'timestamp': datetime.now().isoformat(),
                        }
                        products.append(product)
            
            elif source['name'] == 'AliExpress':
                # Scraping spécifique à AliExpress
                product_cards = soup.select('.product-card')
                for card in product_cards[:5]:
                    title_elem = card.select_one('.product-title')
                    price_elem = card.select_one('.product-price')
                    link_elem = card.select_one('a')
                    
                    if title_elem and link_elem:
                        product = {
                            'title': title_elem.text.strip(),
                            'price': price_elem.text.strip() if price_elem else 'Prix non disponible',
                            'link': link_elem['href'] if link_elem.get('href') else '',
                            'source': source['name'],
                            'type': source['type'],
                            'timestamp': datetime.now().isoformat(),
                        }
                        products.append(product)
                        
            elif source['name'] == 'KdoMonDeal':
                # Scraping pour KdoMonDeal (à adapter selon la structure du site)
                product_cards = soup.select('.deal-box')
                for card in product_cards[:5]:
                    title_elem = card.select_one('.deal-title')
                    price_elem = card.select_one('.deal-price')
                    link_elem = card.select_one('a.deal-link')
                    
                    if title_elem and link_elem:
                        product = {
                            'title': title_elem.text.strip(),
                            'price': price_elem.text.strip() if price_elem else 'Prix non disponible',
                            'link': link_elem['href'] if link_elem.get('href') else '',
                            'source': source['name'],
                            'type': source['type'],
                            'timestamp': datetime.now().isoformat(),
                        }
                        products.append(product)
            
            # Ajouter d'autres marketplaces selon vos besoins
            
            print(f"[+] Récupéré {len(products)} produits depuis {source['name']}")
            
        except Exception as e:
            print(f"[-] Erreur lors du scraping de {source['name']}: {str(e)}")
        
        return products
    
    def save_data(self, data: List[Dict], filename: str):
        """
        Sauvegarde les données scrapées dans un fichier JSON.
        
        Args:
            data: Liste de dictionnaires contenant les données scrapées.
            filename: Nom du fichier de sortie.
        """
        output_path = f'c:\\Users\\claud\\Blog d\'Affiliation\\content\\data\\{filename}.json'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[+] Données sauvegardées dans {output_path}")
    
    def run(self):
        """
        Exécute toutes les tâches de scraping et sauvegarde les données.
        """
        # Récupérer les articles des flux RSS
        rss_items = self.fetch_rss(RSS_FEEDS)
        self.save_data(rss_items, f'rss_data_{datetime.now().strftime("%Y%m%d")}')
        
        # Récupérer les produits des marketplaces
        all_products = []
        for source in DEAL_SOURCES:
            products = self.scrape_marketplace(source)
            all_products.extend(products)
        
        self.save_data(all_products, f'marketplace_data_{datetime.now().strftime("%Y%m%d")}')
        
        return {
            'rss_count': len(rss_items),
            'products_count': len(all_products)
        }

if __name__ == "__main__":
    scraper = Scraper(use_proxy=False)  # Mettre use_proxy=True si vous avez configuré un proxy
    results = scraper.run()
    print(f"[+] Scraping terminé : {results['rss_count']} articles RSS, {results['products_count']} produits récupérés")
