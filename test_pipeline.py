import sys
sys.path.append('src')
import os
import json
from datetime import datetime
from scraper import Scraper
from generator import ArticleGenerator
from builder import SiteBuilder
from publisher import Publisher

def test_full_pipeline():
    """Test the full automation pipeline with minimal operations"""
    
    print("\n===== TESTING FULL AUTOMATION PIPELINE =====\n")
    
    # Step 1: Scraping (minimal test)
    print("\n----- TESTING SCRAPER -----\n")
    try:
        scraper = Scraper(use_proxy=False)
        print("[✓] Scraper initialized successfully")
        
        # Just test one RSS feed to avoid excessive scraping
        test_rss = "https://www.journalduhacker.net/rss"
        rss_data = scraper.scrape_rss_feed(test_rss)
        print(f"[✓] Successfully scraped {len(rss_data)} items from test RSS feed")
        
        # Save a small sample to a JSON file for the next steps
        date_str = datetime.now().strftime("%Y%m%d")
        sample_data_path = f"c:\\Users\\claud\\Blog d'Affiliation\\content\\data\\rss_sample_{date_str}.json"
        with open(sample_data_path, 'w', encoding='utf-8') as f:
            json.dump(rss_data[:5], f, indent=2, ensure_ascii=False)
        print(f"[✓] Saved sample data to {sample_data_path}")
    except Exception as e:
        print(f"[✗] Error in scraping step: {str(e)}")
        return False
    
    # Step 2: Article Generation (simulated)
    print("\n----- TESTING ARTICLE GENERATOR -----\n")
    try:
        generator = ArticleGenerator()
        print("[✓] Article Generator initialized successfully")
        
        # Instead of generating an actual article with OpenAI, use the existing sample
        sample_article_path = "c:\\Users\\claud\\Blog d'Affiliation\\content\\posts\\2025-05-17-top-7-des-sacs-a-dos-pour-nomade-numerique-en-2025.md"
        if os.path.exists(sample_article_path):
            print(f"[✓] Using existing sample article: {sample_article_path}")
        else:
            print(f"[✗] Sample article not found: {sample_article_path}")
            return False
    except Exception as e:
        print(f"[✗] Error in article generation step: {str(e)}")
        return False    # Step 3: Site Building
    print("\n----- TESTING SITE BUILDER -----\n")
    try:
        builder = SiteBuilder()
        print("[✓] Site Builder initialized successfully")
        
        # Build the article
        article_path = "c:\\Users\\claud\\Blog d'Affiliation\\content\\posts\\2025-05-17-top-7-des-sacs-a-dos-pour-nomade-numerique-en-2025.md"
        html_path = builder.build_article(article_path)
        if html_path:
            print(f"[✓] Article HTML generated: {html_path}")
        else:
            print(f"[✗] Failed to build article")
            return False
            
        # Create a simple index page
        import glob
        from datetime import datetime
        from config import SITE_CONFIG
        
        # Get all posts
        posts = []
        markdown_files = glob.glob(os.path.join(builder.posts_dir, '*.md'))
        for file_path in markdown_files:
            post = builder._parse_markdown_file(file_path)
            if post:
                posts.append(post)
        
        # Render index template with empty page dictionary
        template = builder.env.get_template('index.html')
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
        index_path = os.path.join(builder.output_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"[✓] Index page built: {index_path}")
        
        # Create sitemap and robots.txt
        sitemap_path = builder.build_sitemap(posts)
        robots_path = builder.build_robots_txt()
        
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
        print("[i] To publish for real, you need to update the GitHub repository settings in config.py")
        print("[i] and run the full pipeline with the run_all.py script")
    except Exception as e:
        print(f"[✗] Error in publisher step: {str(e)}")
        return False
    
    print("\n===== FULL PIPELINE TEST COMPLETED =====\n")
    return True

if __name__ == "__main__":
    test_full_pipeline()
