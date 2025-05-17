import os
import sys
sys.path.append('src')
from builder import SiteBuilder

# Add the build_site method
def add_build_site_method():
    # First create a SiteBuilder instance
    builder = SiteBuilder()
    
    # Then call run method which is equivalent to build_site
    print("\n----- BUILDING SITE -----\n")
    stats = builder.run(build_all=True)
    print(f"[✓] Site built successfully")
    print(f"[i] Built {stats['built_articles']} articles out of {stats['total_articles']} total")
    print(f"[i] Generated {stats['total_pages']} index pages")
    
    # Return success
    return True

if __name__ == "__main__":
    add_build_site_method()
