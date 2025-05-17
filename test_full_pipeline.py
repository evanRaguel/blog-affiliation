"""
Test script for the Blog d'Affiliation Automatisé.
This script tests the entire pipeline without relying on the run method of each module.
"""

import sys
import os
import json
from datetime import datetime

# Add the src directory to the Python path
sys.path.append('src')

# Import project modules
from scraper import Scraper
from generator import ArticleGenerator 
from builder import SiteBuilder
from publisher import Publisher
from config import SITE_CONFIG

def test_full_pipeline():
    """Test the full automation pipeline with minimal operations"""
    
    print("\n===== TESTING FULL AUTOMATION PIPELINE =====\n")
    
    # Step 1: Scraping (minimal test)
    print("\n----- TESTING SCRAPER -----\n")
    try:
        # Initialize scraper
        scraper = Scraper(use_proxy=False)
        print("[✓] Scraper initialized successfully")
        
        # Test one RSS feed 
        test_rss = "https://www.journalduhacker.net/rss"
        rss_data = scraper.scrape_rss_feed(test_rss)
        print(f"[✓] Successfully scraped {len(rss_data)} items from test RSS feed")
        
        # Save data sample
        today = datetime.now().strftime("%Y%m%d")
        sample_path = f"content/data/rss_sample_{today}.json"
        
        with open(sample_path, 'w', encoding='utf-8') as f:
            json.dump(rss_data[:5], f, indent=2, ensure_ascii=False)
        print(f"[✓] Saved sample data to {sample_path}")
    except Exception as e:
        print(f"[✗] Error in scraping step: {str(e)}")
        return False
    
    # Step 2: Article Generation (simulated)
    print("\n----- TESTING ARTICLE GENERATOR -----\n")
    try:
        # Initialize article generator
        generator = ArticleGenerator()
        print("[✓] Article Generator initialized successfully")
        
        # Check for existing sample article
        sample_article = "content/posts/2025-05-17-top-7-des-sacs-a-dos-pour-nomade-numerique-en-2025.md"
        if os.path.exists(sample_article):
            print(f"[✓] Using existing sample article: {sample_article}")
        else:
            print(f"[✗] Sample article not found: {sample_article}")
            return False
    except Exception as e:
        print(f"[✗] Error in article generation step: {str(e)}")
        return False
    
    # Step 3: Site Building
    print("\n----- TESTING SITE BUILDER -----\n")
    try:
        # Initialize site builder
        builder = SiteBuilder()
        print("[✓] Site Builder initialized successfully")
        
        # Build the article
        article_path = "content/posts/2025-05-17-top-7-des-sacs-a-dos-pour-nomade-numerique-en-2025.md"
        html_path = builder.build_article(article_path)
        if html_path:
            print(f"[✓] Article HTML generated: {html_path}")
        else:
            print(f"[✗] Failed to build article")
            return False
            
        # Get all posts
        posts = []
        markdown_files = [article_path]
        for file_path in markdown_files:
            post = builder._parse_markdown_file(file_path)
            if post:
                posts.append(post)
        
        # Render index template
        template = builder.env.get_template('index.html')
        html = template.render(
            posts=posts,
            site=SITE_CONFIG,
            current_year=datetime.now().year,
            prev_page=None,
            next_page=None,
            current_page=1,
            total_pages=1,
            page={}  # Empty page dictionary for default context
        )
        
        # Write the index page
        index_path = os.path.join(builder.output_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[✓] Index page built: {index_path}")
        
        # Create sitemap and robots.txt
        sitemap_path = builder.build_sitemap(posts)
        print(f"[✓] Sitemap built: {sitemap_path}")
        
        robots_path = builder.build_robots_txt()
        print(f"[✓] Robots.txt built: {robots_path}")
        
        print("[✓] Site built successfully")
    except Exception as e:
        print(f"[✗] Error in site building step: {str(e)}")
        return False
    
    # Step 4: Publisher (simulation only)
    print("\n----- TESTING PUBLISHER -----\n")
    try:
        publisher = Publisher()
        print("[✓] Publisher initialized successfully")
        print("[i] GitHub repository URL: " + publisher.github_repo)
        print("[i] GitHub branch: " + publisher.github_branch)
        
        # Check if GitHub settings are configured
        if publisher.github_repo == "https://github.com/your-username/your-blog-repo":
            print("[!] GitHub repository not configured. Update in config.py")
        else:
            print("[✓] GitHub repository configured")
        
        print("[i] To publish for real, update the GitHub repository settings")
        print("[i] in config.py and run the full pipeline with run_all.py")
    except Exception as e:
        print(f"[✗] Error in publisher step: {str(e)}")
        return False
    
    print("\n===== FULL PIPELINE TEST COMPLETED SUCCESSFULLY =====\n")
    print("Next steps:")
    print("1. Set up a GitHub repository for deployment")
    print("2. Update the repository settings in config.py")
    print("3. Run the full pipeline with python src/run_all.py")
    print("4. Set up a GitHub Actions workflow for automation")
    return True

if __name__ == "__main__":
    test_full_pipeline()
