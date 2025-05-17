import sys
sys.path.append('src')
import os
from generator import ArticleGenerator

# Check if OpenAI API key is configured
openai_key = os.environ.get("OPENAI_API_KEY")
if not openai_key or openai_key == "your_openai_api_key_here":
    print("[✗] OPENAI_API_KEY environment variable is not set correctly")
    print("Please set it with: $env:OPENAI_API_KEY = 'your-actual-api-key'")
else:
    print(f"[✓] OPENAI_API_KEY is configured: {openai_key[:5]}...{openai_key[-4:]}")
    
    # Test article generation if API key is set
    try:
        generator = ArticleGenerator()
        print("[✓] ArticleGenerator initialized successfully")
        # We won't actually generate an article here to avoid API charges
        # But you could uncomment the line below for a real test
        # article_data = generator.generate_new_article()
        # print(f"[✓] Article generated: {article_data['title']}")
    except Exception as e:
        print(f"[✗] Error initializing ArticleGenerator: {str(e)}")
