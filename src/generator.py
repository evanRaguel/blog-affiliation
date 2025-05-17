"""
Module de génération d'articles par IA pour le blog d'affiliation automatisé.
Utilise OpenAI GPT ou des alternatives pour créer des articles optimisés SEO.
"""

import os
import json
import random
from datetime import datetime
import openai
from typing import List, Dict, Any, Optional, Tuple

# Import de la configuration
from config import OPENAI_API_KEY, ARTICLE_SETTINGS, NICHES, AFFILIATES

# Configuration de l'API OpenAI
openai.api_key = OPENAI_API_KEY

class ArticleGenerator:
    def __init__(self):
        """
        Initialise le générateur d'articles.
        """
        self.min_words = ARTICLE_SETTINGS['min_words']
        self.max_words = ARTICLE_SETTINGS['max_words']
        self.language = ARTICLE_SETTINGS['language']
        self.tone = ARTICLE_SETTINGS['tone']
        
        # Créer les dossiers nécessaires s'ils n'existent pas
        os.makedirs('c:\\Users\\claud\\Blog d\'Affiliation\\content\\posts', exist_ok=True)
        
    def _load_data(self, filename: str) -> List[Dict]:
        """
        Charge les données scrapées depuis un fichier JSON.
        
        Args:
            filename: Nom du fichier à charger.
            
        Returns:
            Liste de dictionnaires contenant les données.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[-] Erreur lors du chargement de {filename}: {str(e)}")
            return []
    
    def _select_topic(self) -> Tuple[str, List[str], str]:
        """
        Sélectionne un sujet et une niche au hasard pour l'article.
        
        Returns:
            Tuple contenant (titre, mots-clés, niche)
        """
        # Sélectionner une niche au hasard
        niche = random.choice(list(NICHES.keys()))
        keywords = NICHES[niche]
        
        # Générer un titre basé sur les mots-clés
        if niche == 'nomade_numerique':
            titles = [
                f"Top {random.randint(5, 10)} des {random.choice(['sacs à dos', 'gadgets', 'accessoires'])} pour nomade numérique en 2025",
                f"Guide {datetime.now().year} : Équipement essentiel pour travailler en voyage",
                f"Les meilleurs {random.choice(['outils', 'applications', 'solutions'])} pour digital nomads en {datetime.now().year}",
                f"Comment choisir {random.choice(['sa batterie portable', 'son VPN', 'son forfait international'])} pour voyager connecté",
            ]
        elif niche == 'crypto':
            titles = [
                f"Guide : bien choisir son portefeuille {random.choice(['Bitcoin', 'crypto', 'hardware'])} en {datetime.now().year}",
                f"Comparatif des {random.randint(3, 7)} meilleures plateformes pour {random.choice(['acheter des cryptomonnaies', 'trader du Bitcoin', 'investir en crypto'])}",
                f"Sécuriser ses cryptomonnaies : {random.choice(['les bonnes pratiques', 'quel wallet choisir', 'hardware vs software'])}",
                f"Comment {random.choice(['staker de l\'Ethereum', 'générer des revenus passifs en crypto', 'débuter en DeFi'])} en 2025",
            ]
        else:
            titles = [f"Article sur {niche.replace('_', ' ')}"]
        
        return (random.choice(titles), keywords, niche)
    
    def _prepare_data_for_article(self, niche: str) -> Dict[str, Any]:
        """
        Prépare les données scrapées pour servir de base à l'article.
        
        Args:
            niche: La niche sélectionnée pour l'article.
            
        Returns:
            Dictionnaire contenant les données formatées pour l'article.
        """
        today = datetime.now().strftime("%Y%m%d")
        
        # Charger les données des produits
        try:
            marketplace_file = f'c:\\Users\\claud\\Blog d\'Affiliation\\content\\data\\marketplace_data_{today}.json'
            products = self._load_data(marketplace_file)
            
            # Filtrer en fonction de la niche
            if niche == 'nomade_numerique':
                keywords = ["sac", "batterie", "portable", "voyage", "digital", "nomad", "connecté"]
            elif niche == 'crypto':
                keywords = ["crypto", "bitcoin", "wallet", "ledger", "trezor", "blockchain", "ethereum"]
            else:
                keywords = []
            
            # Sélectionner les produits pertinents
            relevant_products = []
            for product in products:
                title = product.get('title', '').lower()
                if any(keyword.lower() in title for keyword in keywords):
                    relevant_products.append(product)
            
            # Prendre jusqu'à 5 produits
            selected_products = relevant_products[:5] if relevant_products else products[:5]
            
            return {
                'products': selected_products,
                'niche': niche
            }
            
        except Exception as e:
            print(f"[-] Erreur lors de la préparation des données: {str(e)}")
            return {'products': [], 'niche': niche}
    
    def generate_article(self, title: str, keywords: List[str], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Génère un article complet via l'API OpenAI.
        
        Args:
            title: Le titre de l'article.
            keywords: Liste de mots-clés à inclure.
            data: Données pour contextualiser l'article.
            
        Returns:
            Dictionnaire contenant l'article généré et ses métadonnées.
        """
        products = data.get('products', [])
        niche = data.get('niche', '')
        
        # Construire le prompt pour l'API
        product_info = ""
        if products:
            for i, product in enumerate(products, 1):
                product_info += f"{i}. {product.get('title', 'Produit')} - Prix: {product.get('price', 'N/A')}\n"
        
        keywords_str = ", ".join(keywords)
        
        prompt = f"""
        Écris un article de blog optimisé pour le SEO sur le sujet: "{title}".
        
        Ton article doit:
        1. Avoir une introduction captivante qui explique l'importance du sujet.
        2. Contenir des sous-sections avec des titres H2 et H3 bien structurés.
        3. Inclure naturellement les mots-clés suivants: {keywords_str}.
        4. Avoir un ton {self.tone}.
        5. Conclure avec un appel à l'action.
        
        Voici des informations sur des produits pertinents que tu peux mentionner:
        {product_info}
          Formatte l'article en Markdown avec des balises # pour les titres, des liens pour les produits, et des listes à puces où approprié.
        Ajoute des balises {{{{link:nom_du_produit}}}} autour des noms de produits qui devront être convertis en liens d'affiliation.
        
        L'article doit faire entre {self.min_words} et {self.max_words} mots.
        """
        
        try:
            # Appel à l'API OpenAI avec le nouveau format v1.0+
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-4",  # ou "gpt-3.5-turbo" pour une option moins coûteuse
                messages=[
                    {"role": "system", "content": f"Tu es un rédacteur SEO expert en {niche.replace('_', ' ')}. Tu écris des articles informatifs et engageants optimisés pour le référencement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.7,
            )
            
            # Extraire le contenu de l'article
            article_content = response.choices[0].message.content
            
            # Générer la meta-description
            meta_prompt = f"Résume cet article en une meta-description SEO de 155 caractères maximum: {title}"
            meta_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": meta_prompt}],
                max_tokens=100,
                temperature=0.7,
            )
            meta_description = meta_response.choices[0].message.content
            
            # Créer l'article avec ses métadonnées
            article = {
                'title': title,
                'content': article_content,
                'meta_description': meta_description,
                'keywords': keywords,
                'niche': niche,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'timestamp': datetime.now().isoformat(),
                'products': products
            }
            
            print(f"[+] Article généré: {title}")
            return article
            
        except Exception as e:
            print(f"[-] Erreur lors de la génération de l'article: {str(e)}")
            return None
    
    def save_article(self, article: Dict[str, Any], format: str = 'markdown') -> str:
        """
        Sauvegarde l'article généré dans un fichier.
        
        Args:
            article: Dictionnaire contenant l'article et ses métadonnées.
            format: Format de sortie ('markdown' ou 'json').
            
        Returns:
            Chemin du fichier sauvegardé.
        """
        if not article:
            return None
        
        # Créer un slug à partir du titre
        slug = article['title'].lower()
        for char in [' ', "'", '"', '.', ',', ':', ';', '/', '\\', '!', '?']:
            slug = slug.replace(char, '-')
        while '--' in slug:
            slug = slug.replace('--', '-')
        slug = slug.strip('-')
        
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_prefix}-{slug}"
        
        if format == 'markdown':
            output_path = f'c:\\Users\\claud\\Blog d\'Affiliation\\content\\posts\\{filename}.md'
            
            # Créer le contenu avec frontmatter YAML
            frontmatter = f"""---
title: "{article['title']}"
date: {article['date']}
description: "{article['meta_description']}"
keywords: [{', '.join([f'"{kw}"' for kw in article['keywords']])}]
niche: "{article['niche']}"
---

"""
            content = frontmatter + article['content']
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        else:  # format == 'json'
            output_path = f'c:\\Users\\claud\\Blog d\'Affiliation\\content\\posts\\{filename}.json'
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
        
        print(f"[+] Article sauvegardé dans {output_path}")
        return output_path
    
    def run(self) -> Optional[str]:
        """
        Exécute tout le processus de génération d'article.
        
        Returns:
            Le chemin du fichier de l'article généré, ou None en cas d'échec.
        """
        # Sélectionner un sujet
        title, keywords, niche = self._select_topic()
        
        # Préparer les données pour l'article
        data = self._prepare_data_for_article(niche)
        
        # Générer l'article
        article = self.generate_article(title, keywords, data)
        
        # Sauvegarder l'article
        if article:
            return self.save_article(article, format='markdown')
        
        return None

if __name__ == "__main__":
    generator = ArticleGenerator()
    article_path = generator.run()
    if article_path:
        print(f"[+] Génération terminée: {article_path}")
    else:
        print("[-] Échec de la génération d'article")
