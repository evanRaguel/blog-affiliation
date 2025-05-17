import os
import sys
sys.path.append('src')
from builder import SiteBuilder

# First create a SiteBuilder instance
builder = SiteBuilder()

# Fix the template rendering issue by building individual elements
try:
    print("\n----- FIXING SITE BUILDING -----\n")
    # First build any articles
    article_path = "c:\\Users\\claud\\Blog d'Affiliation\\content\\posts\\2025-05-17-top-7-des-sacs-a-dos-pour-nomade-numerique-en-2025.md"
    builder.build_article(article_path)
    print("[✓] Article built successfully")
    
    # Get all posts
    import glob
    posts = []
    markdown_files = glob.glob(os.path.join(builder.posts_dir, '*.md'))
    for file_path in markdown_files:
        post = builder._parse_markdown_file(file_path)
        if post:
            posts.append(post)
    
    # Now create a simpler index.html without pagination
    from datetime import datetime
    from config import SITE_CONFIG
    
    # Get the template
    template = builder.env.get_template('index.html')
    
    # Render with empty page dictionary
    html = template.render(
        posts=posts,
        site=SITE_CONFIG,
        current_year=datetime.now().year,
        prev_page=None,
        next_page=None,
        current_page=1,
        total_pages=1,
        page={}  # Add empty page dictionary
    )
    
    # Write the output
    output_path = os.path.join(builder.output_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[✓] Index page built: {output_path}")
    
    # Create sitemap.xml
    sitemap_path = builder.build_sitemap(posts)
    print(f"[✓] Sitemap built: {sitemap_path}")
    
    # Create robots.txt
    robots_path = builder.build_robots_txt()
    print(f"[✓] Robots.txt built: {robots_path}")
    
    print("\n[✓] Site building fixed and completed successfully!")
    
except Exception as e:
    print(f"[✗] Error fixing site building: {str(e)}")
