"""
Module de construction des pages HTML pour le blog d'affiliation automatisé.
Convertit les articles Markdown en HTML et insère les liens d'affiliation.
"""

import os
import re
import json
import glob
import markdown
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader

# Import de la configuration
from config import AFFILIATES, SITE_CONFIG

class SiteBuilder:
    def __init__(self):
        """
        Initialise le constructeur de site.
        """
        self.template_dir = 'c:\\Users\\claud\\Blog d\'Affiliation\\templates'
        self.content_dir = 'c:\\Users\\claud\\Blog d\'Affiliation\\content'
        self.output_dir = 'c:\\Users\\claud\\Blog d\'Affiliation\\static'
        self.posts_dir = os.path.join(self.content_dir, 'posts')
        
        # Créer les dossiers nécessaires s'ils n'existent pas
        for directory in [self.template_dir, self.output_dir, 
                         os.path.join(self.output_dir, 'posts'),
                         os.path.join(self.output_dir, 'go'),
                         os.path.join(self.output_dir, 'assets', 'css'),
                         os.path.join(self.output_dir, 'assets', 'js'),
                         os.path.join(self.output_dir, 'assets', 'images')]:
            os.makedirs(directory, exist_ok=True)
        
        # Configurer Jinja2
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # S'assurer que les templates existent
        self._create_default_templates()
    
    def _create_default_templates(self):
        """
        Crée les templates par défaut s'ils n'existent pas.
        """
        # Template de base
        base_template = """<!DOCTYPE html>
<html lang="{{ site.language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ site.title }}{% endblock %}</title>
    <meta name="description" content="{% block description %}{{ site.description }}{% endblock %}">
    <meta name="author" content="{{ site.author }}">
    {% block meta %}{% endblock %}
      <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ site.base_url }}{% if page.url %}{{ page.url }}{% else %}/{% endif %}">
    <meta property="og:title" content="{% block og_title %}{{ site.title }}{% endblock %}">
    <meta property="og:description" content="{% block og_description %}{{ site.description }}{% endblock %}">
    <meta property="og:image" content="{% block og_image %}{{ site.base_url }}/assets/images/default.jpg{% endblock %}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{{ site.base_url }}{% if page.url %}{{ page.url }}{% else %}/{% endif %}">
    <meta property="twitter:title" content="{% block twitter_title %}{{ site.title }}{% endblock %}">
    <meta property="twitter:description" content="{% block twitter_description %}{{ site.description }}{% endblock %}">
    <meta property="twitter:image" content="{% block twitter_image %}{{ site.base_url }}/assets/images/default.jpg{% endblock %}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{{ site.base_url }}{{ page.url }}">
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ site.base_url }}/assets/css/style.css">
    {% block styles %}{% endblock %}
</head>
<body>
    <header>
        <div class="container">
            <a href="{{ site.base_url }}" class="logo">{{ site.title }}</a>
            <nav>
                <ul>
                    <li><a href="{{ site.base_url }}">Accueil</a></li>
                    <li><a href="{{ site.base_url }}/categories.html">Catégories</a></li>
                    <li><a href="{{ site.base_url }}/about.html">À propos</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <main>
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; {{ current_year }} {{ site.title }}. Tous droits réservés.</p>
        </div>
    </footer>
    
    <!-- JavaScript -->
    <script src="{{ site.base_url }}/assets/js/main.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
"""
        
        # Template d'article
        article_template = """{% extends "base.html" %}

{% block title %}{{ page.title }} | {{ site.title }}{% endblock %}

{% block description %}{{ page.description }}{% endblock %}

{% block meta %}
<meta name="keywords" content="{{ page.keywords|join(', ') }}">
{% endblock %}

{% block og_title %}{{ page.title }}{% endblock %}
{% block og_description %}{{ page.description }}{% endblock %}

{% block twitter_title %}{{ page.title }}{% endblock %}
{% block twitter_description %}{{ page.description }}{% endblock %}

{% block content %}
<article class="post">
    <header class="post-header">
        <h1 class="post-title">{{ page.title }}</h1>
        <div class="post-meta">
            <time datetime="{{ page.date }}">{{ page.date }}</time>
            {% if page.categories %}
            <span class="categories">
                {% for category in page.categories %}
                <a href="{{ site.base_url }}/category/{{ category }}.html">{{ category }}</a>{% if not loop.last %}, {% endif %}
                {% endfor %}
            </span>
            {% endif %}
        </div>
    </header>
    
    <div class="post-content">
        {{ page.content|safe }}
    </div>
    
    <footer class="post-footer">
        {% if page.tags %}
        <div class="post-tags">
            {% for tag in page.tags %}
            <a href="{{ site.base_url }}/tag/{{ tag }}.html">{{ tag }}</a>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="related-posts">
            <h2>Articles similaires</h2>
            <ul>
                {% for post in related_posts %}
                <li><a href="{{ site.base_url }}{{ post.url }}">{{ post.title }}</a></li>
                {% endfor %}
            </ul>
        </div>
    </footer>
</article>
{% endblock %}
"""
        
        # Template d'index
        index_template = """{% extends "base.html" %}

{% block content %}
<h1>Derniers articles</h1>

<div class="posts">
    {% for post in posts %}
    <article class="post-preview">
        <h2><a href="{{ site.base_url }}{{ post.url }}">{{ post.title }}</a></h2>
        <div class="post-meta">
            <time datetime="{{ post.date }}">{{ post.date }}</time>
        </div>
        <div class="post-excerpt">
            {{ post.excerpt|safe }}
        </div>
        <a href="{{ site.base_url }}{{ post.url }}" class="read-more">Lire la suite &rarr;</a>
    </article>
    {% endfor %}
</div>

<div class="pagination">
    {% if prev_page %}
    <a href="{{ site.base_url }}/page/{{ prev_page }}.html" class="prev">&larr; Articles plus récents</a>
    {% endif %}
    
    {% if next_page %}
    <a href="{{ site.base_url }}/page/{{ next_page }}.html" class="next">Articles plus anciens &rarr;</a>
    {% endif %}
</div>
{% endblock %}
"""
        
        # CSS par défaut
        default_css = """/* Base */
:root {
    --primary-color: #4a89dc;
    --secondary-color: #5d9cec;
    --text-color: #333;
    --light-gray: #f5f5f5;
    --medium-gray: #e0e0e0;
    --dark-gray: #666;
    --max-width: 1200px;
    --content-width: 800px;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: #fff;
}

.container {
    width: 90%;
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 0 15px;
}

/* Header */
header {
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 1rem 0;
}

header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
    text-decoration: none;
}

nav ul {
    display: flex;
    list-style-type: none;
}

nav li {
    margin-left: 1.5rem;
}

nav a {
    color: var(--text-color);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
}

nav a:hover {
    color: var(--primary-color);
}

/* Main content */
main {
    padding: 2rem 0;
}

/* Post list */
.posts {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2rem;
}

.post-preview {
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--medium-gray);
}

.post-preview h2 {
    margin-bottom: 0.5rem;
}

.post-preview h2 a {
    color: var(--text-color);
    text-decoration: none;
    transition: color 0.3s;
}

.post-preview h2 a:hover {
    color: var(--primary-color);
}

.post-meta {
    font-size: 0.9rem;
    color: var(--dark-gray);
    margin-bottom: 1rem;
}

.post-excerpt {
    margin-bottom: 1rem;
}

.read-more {
    display: inline-block;
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
}

/* Pagination */
.pagination {
    display: flex;
    justify-content: space-between;
    margin-top: 2rem;
}

.pagination a {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: var(--light-gray);
    color: var(--text-color);
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.pagination a:hover {
    background-color: var(--medium-gray);
}

/* Single post */
.post {
    max-width: var(--content-width);
    margin: 0 auto;
}

.post-header {
    margin-bottom: 2rem;
}

.post-title {
    font-size: 2.5rem;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}

.post-content {
    margin-bottom: 2rem;
}

.post-content h2 {
    font-size: 1.8rem;
    margin: 2rem 0 1rem;
}

.post-content h3 {
    font-size: 1.5rem;
    margin: 1.5rem 0 1rem;
}

.post-content p {
    margin-bottom: 1.5rem;
}

.post-content ul, .post-content ol {
    margin-bottom: 1.5rem;
    padding-left: 1.5rem;
}

.post-content li {
    margin-bottom: 0.5rem;
}

.post-content img {
    max-width: 100%;
    height: auto;
    margin: 1.5rem 0;
}

.post-content a {
    color: var(--primary-color);
    text-decoration: none;
}

.post-content a:hover {
    text-decoration: underline;
}

.post-footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--medium-gray);
}

.post-tags {
    margin-bottom: 1.5rem;
}

.post-tags a {
    display: inline-block;
    margin-right: 0.5rem;
    padding: 0.3rem 0.8rem;
    background-color: var(--light-gray);
    color: var(--dark-gray);
    text-decoration: none;
    border-radius: 4px;
    font-size: 0.9rem;
    transition: background-color 0.3s;
}

.post-tags a:hover {
    background-color: var(--medium-gray);
}

.related-posts {
    margin-top: 2rem;
}

.related-posts h2 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
}

.related-posts ul {
    list-style-type: none;
    padding-left: 0;
}

.related-posts li {
    margin-bottom: 0.5rem;
}

.related-posts a {
    color: var(--text-color);
    text-decoration: none;
}

.related-posts a:hover {
    color: var(--primary-color);
}

/* Footer */
footer {
    background-color: var(--light-gray);
    padding: 2rem 0;
    margin-top: 2rem;
    text-align: center;
    color: var(--dark-gray);
}

/* Media Queries */
@media (min-width: 768px) {
    .posts {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .posts {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* Affiliate Buttons */
.affiliate-button {
    display: inline-block;
    background-color: var(--primary-color);
    color: white;
    padding: 0.7rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 600;
    text-align: center;
    margin: 1rem 0;
    transition: background-color 0.3s;
}

.affiliate-button:hover {
    background-color: var(--secondary-color);
    text-decoration: none !important;
}

.product-card {
    border: 1px solid var(--medium-gray);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.product-title {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

.product-price {
    font-weight: bold;
    color: var(--primary-color);
    margin-bottom: 1rem;
}

.product-description {
    margin-bottom: 1rem;
}
"""
        
        # JavaScript par défaut
        default_js = """// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Track outbound affiliate links (anonymously)
    document.querySelectorAll('a[href^="/go/"]').forEach(link => {
        link.addEventListener('click', function() {
            // You could add analytics here if needed
            console.log('Affiliate link clicked: ' + this.href);
        });
    });
});
"""
        
        # Créer les fichiers templates s'ils n'existent pas
        templates = {
            os.path.join(self.template_dir, 'base.html'): base_template,
            os.path.join(self.template_dir, 'article.html'): article_template,
            os.path.join(self.template_dir, 'index.html'): index_template,
            os.path.join(self.output_dir, 'assets', 'css', 'style.css'): default_css,
            os.path.join(self.output_dir, 'assets', 'js', 'main.js'): default_js
        }
        
        for path, content in templates.items():
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[+] Template créé: {path}")
    
    def _parse_markdown_file(self, filepath: str) -> Dict[str, Any]:
        """
        Parse un fichier Markdown avec frontmatter.
        
        Args:
            filepath: Chemin du fichier Markdown.
            
        Returns:
            Dictionnaire contenant le contenu et les métadonnées.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraire le frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            content_text = frontmatter_match.group(2)
            
            # Parser le YAML frontmatter
            try:
                meta = yaml.safe_load(frontmatter_text)
            except Exception as e:
                print(f"[-] Erreur lors du parsing YAML: {str(e)}")
                meta = {}
            
            # Convertir le Markdown en HTML
            html_content = markdown.markdown(
                content_text,
                extensions=['markdown.extensions.extra', 'markdown.extensions.meta', 'markdown.extensions.toc']
            )
            
            # Créer un extrait (enlever les tags HTML)
            excerpt = re.sub(r'<.*?>', '', html_content)
            excerpt = excerpt[:200] + '...' if len(excerpt) > 200 else excerpt
            
            # Extraire le nom de fichier pour l'URL
            filename = os.path.basename(filepath)
            slug = os.path.splitext(filename)[0]
            
            # Si le slug commence par une date (YYYY-MM-DD-), l'enlever
            if re.match(r'^\d{4}-\d{2}-\d{2}-', slug):
                slug = slug[11:]
            
            # Créer l'objet page
            page = {
                'title': meta.get('title', 'Sans titre'),
                'date': meta.get('date', datetime.now().strftime('%Y-%m-%d')),
                'description': meta.get('description', excerpt),
                'keywords': meta.get('keywords', []),
                'categories': meta.get('categories', []),
                'tags': meta.get('tags', []),
                'niche': meta.get('niche', ''),
                'content': html_content,
                'excerpt': excerpt,
                'url': f"/posts/{slug}.html",
                'slug': slug
            }
            
            return page
        
        return None
    
    def _insert_affiliate_links(self, content: str) -> str:
        """
        Insère les liens d'affiliation dans le contenu.
        
        Args:
            content: Le contenu HTML de l'article.
            
        Returns:
            Le contenu avec les liens affiliés.
        """
        # Remplacer les placeholders {{link:nom}} par des liens affiliés
        pattern = r'\{\{link:(.*?)\}\}'
        
        def replace_link(match):
            product_name = match.group(1).strip().lower()
            
            # Créer un slug pour le lien
            slug = product_name.replace(' ', '-')
            for char in [',', '.', ':', ';', '!', '?', "'", '"']:
                slug = slug.replace(char, '')
            
            # Sélectionner le bon programme d'affiliation
            affiliate_id = None
            if any(keyword in product_name for keyword in ['sac', 'batterie', 'moniteur', 'gadget']):
                affiliate_id = AFFILIATES['amazon']
                program = 'amazon'
            elif any(keyword in product_name for keyword in ['ledger', 'trezor', 'crypto', 'bitcoin']):
                affiliate_id = AFFILIATES['ledger']
                program = 'ledger'
            elif any(keyword in product_name for keyword in ['hotel', 'voyage', 'hébergement']):
                affiliate_id = AFFILIATES['booking']
                program = 'booking'
            else:
                affiliate_id = AFFILIATES['amazon']  # Par défaut
                program = 'amazon'
            
            # Créer le lien de redirection
            redirect_path = f"/go/{slug}"
            
            # Créer le fichier de redirection
            self._create_redirect_file(slug, program, affiliate_id, product_name)
            
            # Retourner le lien HTML
            return f'<a href="{redirect_path}" class="affiliate-link" target="_blank">{product_name}</a>'
        
        # Remplacer tous les placeholders
        content_with_links = re.sub(pattern, replace_link, content)
        
        # Ajouter des boutons d'affiliation pour les produits mentionnés
        product_keywords = {
            'sac à dos': ('amazon', 'Voir ce sac à dos sur Amazon'),
            'batterie portable': ('amazon', 'Voir cette batterie sur Amazon'),
            'ledger': ('ledger', 'Acheter un Ledger Nano X'),
            'trezor': ('ledger', 'Acheter un Trezor'),
            'vpn': ('amazon', 'Voir les offres VPN'),
        }
        
        for keyword, (program, button_text) in product_keywords.items():
            if keyword in content_with_links.lower() and f'class="affiliate-link"' not in content_with_links:
                # Créer un slug pour le lien
                slug = keyword.replace(' ', '-')
                for char in [',', '.', ':', ';', '!', '?', "'", '"']:
                    slug = slug.replace(char, '')
                
                # Créer le lien de redirection
                redirect_path = f"/go/{slug}"
                
                # Créer le fichier de redirection
                self._create_redirect_file(slug, program, AFFILIATES[program], keyword)
                
                # Ajouter un bouton d'affiliation après la première mention
                button = f'<a href="{redirect_path}" class="affiliate-button" target="_blank">{button_text}</a>'
                
                # Ajouter le bouton après un paragraphe qui contient le mot-clé
                pattern = f'(.*?{keyword}.*?</p>)'
                content_with_links = re.sub(pattern, f'\\1\n{button}\n', content_with_links, flags=re.IGNORECASE, count=1)
        
        return content_with_links
    
    def _create_redirect_file(self, slug: str, program: str, affiliate_id: str, product_name: str):
        """
        Crée un fichier de redirection pour un lien d'affiliation.
        
        Args:
            slug: Slug du produit.
            program: Programme d'affiliation.
            affiliate_id: ID d'affiliation.
            product_name: Nom du produit.
        """
        redirect_dir = os.path.join(self.output_dir, 'go')
        os.makedirs(redirect_dir, exist_ok=True)
        
        # Créer l'URL de destination avec l'ID affilié
        if program == 'amazon':
            # Exemple : recherche Amazon avec tag affilié
            destination_url = f"https://www.amazon.fr/s?k={product_name.replace(' ', '+')}&tag={affiliate_id}"
        elif program == 'ledger':
            # Exemple : page produit Ledger
            destination_url = f"https://shop.ledger.com/{product_name.replace(' ', '-')}?r={affiliate_id}"
        elif program == 'booking':
            # Exemple : recherche Booking
            destination_url = f"https://www.booking.com/index.html?aid={affiliate_id}"
        else:
            # Lien par défaut
            destination_url = f"https://www.amazon.fr/s?k={product_name.replace(' ', '+')}&tag={affiliate_id}"
        
        # Créer le fichier HTML de redirection
        redirect_path = os.path.join(redirect_dir, f"{slug}.html")
        redirect_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url={destination_url}">
    <title>Redirection vers {product_name}</title>
    <script>window.location.href = "{destination_url}";</script>
</head>
<body>
    <p>Redirection vers <a href="{destination_url}">{product_name}</a>...</p>
</body>
</html>"""
        
        with open(redirect_path, 'w', encoding='utf-8') as f:
            f.write(redirect_content)
    
    def _find_related_posts(self, current_post: Dict[str, Any], all_posts: List[Dict[str, Any]], count: int = 3) -> List[Dict[str, Any]]:
        """
        Trouve des articles liés à l'article courant.
        
        Args:
            current_post: Article courant.
            all_posts: Tous les articles.
            count: Nombre d'articles liés à retourner.
            
        Returns:
            Liste d'articles liés.
        """
        # Éviter de suggérer l'article courant
        other_posts = [post for post in all_posts if post['url'] != current_post['url']]
        
        # Trier par niche et mots-clés partagés
        def score_post(post):
            score = 0
            # Même niche
            if post['niche'] == current_post['niche']:
                score += 5
            
            # Mots-clés partagés
            shared_keywords = set(post['keywords']) & set(current_post['keywords'])
            score += len(shared_keywords) * 2
            
            # Catégories partagées
            shared_categories = set(post['categories']) & set(current_post['categories'])
            score += len(shared_categories) * 2
            
            return score
        
        scored_posts = [(post, score_post(post)) for post in other_posts]
        scored_posts.sort(key=lambda x: x[1], reverse=True)
        
        # Prendre les N premiers
        related_posts = [post for post, score in scored_posts[:count] if score > 0]
        
        # Si on n'a pas assez d'articles liés, ajouter les plus récents
        if len(related_posts) < count:
            recent_posts = sorted(other_posts, key=lambda p: p['date'], reverse=True)
            needed = count - len(related_posts)
            
            # Filtrer les posts récents qui ne sont pas déjà dans related_posts
            recent_to_add = [post for post in recent_posts if post not in related_posts][:needed]
            related_posts.extend(recent_to_add)
        
        return related_posts[:count]
    
    def build_article(self, markdown_path: str) -> str:
        """
        Construit une page HTML à partir d'un article Markdown.
        
        Args:
            markdown_path: Chemin du fichier Markdown.
            
        Returns:
            Chemin du fichier HTML généré.
        """
        # Parser le fichier Markdown
        page = self._parse_markdown_file(markdown_path)
        if not page:
            print(f"[-] Erreur lors du parsing de {markdown_path}")
            return None
        
        # Trouver des articles liés
        # Note: pour l'instant, on n'a pas d'autres articles, donc c'est vide
        related_posts = []
        
        # Insérer les liens d'affiliation
        page['content'] = self._insert_affiliate_links(page['content'])
        
        # Charger le template
        template = self.env.get_template('article.html')
        
        # Rendre le template
        html = template.render(
            page=page,
            site=SITE_CONFIG,
            current_year=datetime.now().year,
            related_posts=related_posts
        )
        
        # Déterminer le chemin de sortie
        output_path = os.path.join(self.output_dir, page['url'].lstrip('/'))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Écrire le fichier HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[+] Article construit: {output_path}")
        return output_path
    
    def build_index(self, posts: List[Dict[str, Any]] = None, page_num: int = 1, posts_per_page: int = 10) -> str:
        """
        Construit la page d'index avec les derniers articles.
        
        Args:
            posts: Liste des articles à inclure (sinon tous).
            page_num: Numéro de la page pour la pagination.
            posts_per_page: Nombre d'articles par page.
            
        Returns:
            Chemin du fichier HTML généré.
        """
        # Si aucun post n'est fourni, charger tous les posts
        if posts is None:
            posts = []
            markdown_files = glob.glob(os.path.join(self.posts_dir, '*.md'))
            
            for file_path in markdown_files:
                post = self._parse_markdown_file(file_path)
                if post:
                    posts.append(post)
        
        # Trier les posts par date (plus récent en premier)
        posts.sort(key=lambda p: p['date'], reverse=True)
        
        # Pagination
        total_pages = (len(posts) + posts_per_page - 1) // posts_per_page
        start_idx = (page_num - 1) * posts_per_page
        end_idx = start_idx + posts_per_page
        page_posts = posts[start_idx:end_idx]
        
        # Déterminer les numéros de page précédente/suivante
        prev_page = page_num - 1 if page_num > 1 else None
        next_page = page_num + 1 if page_num < total_pages else None
        
        # Charger le template
        template = self.env.get_template('index.html')
        
        # Rendre le template
        html = template.render(
            posts=page_posts,
            site=SITE_CONFIG,
            current_year=datetime.now().year,
            prev_page=prev_page,
            next_page=next_page,
            current_page=page_num,
            total_pages=total_pages
        )
        
        # Déterminer le chemin de sortie
        if page_num == 1:
            output_path = os.path.join(self.output_dir, 'index.html')
        else:
            os.makedirs(os.path.join(self.output_dir, 'page'), exist_ok=True)
            output_path = os.path.join(self.output_dir, f'page/{page_num}.html')
        
        # Écrire le fichier HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[+] Index construit: {output_path}")
        return output_path
    
    def build_sitemap(self, posts: List[Dict[str, Any]] = None) -> str:
        """
        Génère le fichier sitemap.xml.
        
        Args:
            posts: Liste des articles à inclure (sinon tous).
            
        Returns:
            Chemin du fichier sitemap.xml généré.
        """
        # Si aucun post n'est fourni, charger tous les posts
        if posts is None:
            posts = []
            markdown_files = glob.glob(os.path.join(self.posts_dir, '*.md'))
            
            for file_path in markdown_files:
                post = self._parse_markdown_file(file_path)
                if post:
                    posts.append(post)
        
        # Créer le contenu du sitemap
        sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Ajouter la page d'accueil
        sitemap_content += f'  <url>\n'
        sitemap_content += f'    <loc>{SITE_CONFIG["base_url"]}/</loc>\n'
        sitemap_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        sitemap_content += f'    <changefreq>daily</changefreq>\n'
        sitemap_content += f'    <priority>1.0</priority>\n'
        sitemap_content += f'  </url>\n'
        
        # Ajouter chaque article
        for post in posts:
            sitemap_content += f'  <url>\n'
            sitemap_content += f'    <loc>{SITE_CONFIG["base_url"]}{post["url"]}</loc>\n'
            sitemap_content += f'    <lastmod>{post["date"]}</lastmod>\n'
            sitemap_content += f'    <changefreq>monthly</changefreq>\n'
            sitemap_content += f'    <priority>0.8</priority>\n'
            sitemap_content += f'  </url>\n'
        
        sitemap_content += '</urlset>'
        
        # Écrire le fichier sitemap.xml
        output_path = os.path.join(self.output_dir, 'sitemap.xml')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        
        print(f"[+] Sitemap généré: {output_path}")
        return output_path
    
    def build_robots_txt(self) -> str:
        """
        Génère le fichier robots.txt.
        
        Returns:
            Chemin du fichier robots.txt généré.
        """
        robots_content = f"""User-agent: *
Allow: /
Disallow: /go/

Sitemap: {SITE_CONFIG["base_url"]}/sitemap.xml
"""
        
        # Écrire le fichier robots.txt
        output_path = os.path.join(self.output_dir, 'robots.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        print(f"[+] Robots.txt généré: {output_path}")
        return output_path
    
    def run(self, build_all: bool = False) -> Dict[str, int]:
        """
        Exécute tout le processus de construction du site.
        
        Args:
            build_all: Si True, reconstruit tous les articles, sinon seulement les nouveaux.
            
        Returns:
            Statistiques sur la construction.
        """
        # Trouver tous les fichiers Markdown
        markdown_files = glob.glob(os.path.join(self.posts_dir, '*.md'))
        
        # Articles construits
        built_articles = []
        
        for md_file in markdown_files:
            # Si build_all est False, vérifier si l'article existe déjà
            if not build_all:
                # Extraire le nom de fichier pour l'URL
                filename = os.path.basename(md_file)
                slug = os.path.splitext(filename)[0]
                
                # Si le slug commence par une date (YYYY-MM-DD-), l'enlever
                if re.match(r'^\d{4}-\d{2}-\d{2}-', slug):
                    slug = slug[11:]
                
                # Vérifier si l'article HTML existe déjà
                html_path = os.path.join(self.output_dir, 'posts', f"{slug}.html")
                
                # Si l'article HTML existe déjà et est plus récent que le Markdown, skip
                if os.path.exists(html_path) and os.path.getmtime(html_path) > os.path.getmtime(md_file):
                    print(f"[*] Article déjà à jour: {html_path}")
                    continue
            
            # Construire l'article
            html_path = self.build_article(md_file)
            if html_path:
                built_articles.append(self._parse_markdown_file(md_file))
        
        # Construire l'index (première page)
        all_posts = []
        for md_file in markdown_files:
            post = self._parse_markdown_file(md_file)
            if post:
                all_posts.append(post)
        
        # Trier les posts par date (plus récent en premier)
        all_posts.sort(key=lambda p: p['date'], reverse=True)
        
        # Construire les pages d'index
        posts_per_page = 10
        total_pages = (len(all_posts) + posts_per_page - 1) // posts_per_page
        
        for page_num in range(1, total_pages + 1):
            self.build_index(all_posts, page_num, posts_per_page)
        
        # Générer le sitemap
        self.build_sitemap(all_posts)
        
        # Générer le robots.txt
        self.build_robots_txt()
        
        return {
            'built_articles': len(built_articles),
            'total_articles': len(all_posts),
            'total_pages': total_pages
        }

if __name__ == "__main__":
    builder = SiteBuilder()
    stats = builder.run(build_all=False)
    print(f"[+] Construction terminée: {stats['built_articles']} articles construits sur {stats['total_articles']} au total")
