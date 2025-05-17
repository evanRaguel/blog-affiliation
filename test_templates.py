import sys
sys.path.append('src')
from config import SITE_CONFIG
from jinja2 import Environment, FileSystemLoader

# Configuration simplifiée
test_site = {
    "title": "Test Blog",
    "description": "Test Description",
    "base_url": "https://example.com",
    "author": "Test Author",
    "language": "fr"
}

# Configuration de Jinja2
env = Environment(loader=FileSystemLoader('templates'))

# Test du template base.html
try:
    template = env.get_template('base.html')
    result = template.render(site=test_site, page={})
    print('[✓] Template base.html rendering successful!')
except Exception as e:
    print(f'[✗] Error rendering base.html: {str(e)}')

# Test du template index.html
try:
    template = env.get_template('index.html')
    result = template.render(site=test_site, posts=[], page={})
    print('[✓] Template index.html rendering successful!')
except Exception as e:
    print(f'[✗] Error rendering index.html: {str(e)}')

# Test du template article.html
try:
    test_page = {
        "title": "Test Article",
        "description": "Test Article Description",
        "date": "2025-05-17",
        "content": "<p>Test content</p>",
        "keywords": ["test", "article"],
        "categories": ["test"],
        "tags": ["test"]
    }
    template = env.get_template('article.html')
    result = template.render(site=test_site, page=test_page)
    print('[✓] Template article.html rendering successful!')
except Exception as e:
    print(f'[✗] Error rendering article.html: {str(e)}')
