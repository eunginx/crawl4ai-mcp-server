#!/usr/bin/env python3
"""
Simple test script to crawl a website using Crawl4AI with LiteLLM integration.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import required modules
from utils import get_litellm_router, create_embedding
from supabase import Client
from crawl4ai import AsyncWebCrawler

async def test_crawl():
    """Test crawling functionality with LiteLLM embeddings."""
    
    # Initialize components
    chat_router, embedding_router = get_litellm_router()
    
    # Test URL
    test_url = "https://docs.litellm.ai/docs/simple_proxy"
    
    print(f"🕷️ Starting crawl of: {test_url}")
    
    # Initialize crawler
    crawler = AsyncWebCrawler(
        browser_type="chromium",
        headless=True,
        verbose=True
    )
    
    try:
        # Perform crawl
        result = await crawler.arun(
            url=test_url,
            word_count_threshold=10,
            extraction_strategy="LLM",
            bypass_cache=True,
            css_selector="main-content",
            wait_for="networkidle",
            delay_before_return_html=2.0,
            js_snippets=[],
            wait_for_selector=None,
            page_timeout=60000,
            session_id=None
        )
        
        if result.success:
            print(f"✅ Crawl successful!")
            print(f"📄 Cleaned HTML length: {len(result.cleaned_html)}")
            print(f"📝 Markdown length: {len(result.markdown)}")
            
            # Test embedding creation
            if result.markdown:
                print("🧠 Creating embeddings...")
                embedding = create_embedding(result.markdown[:1000])  # Test with first 1000 chars
                print(f"✅ Embedding created successfully! Dimensions: {len(embedding)}")
                
                # If Supabase is configured, test storage
                if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY"):
                    try:
                        client = Client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))
                        
                        # Test search functionality
                        print("🔍 Testing search functionality...")
                        search_results = client.rpc('match_crawled_pages', {
                            'query_embedding': embedding,
                            'match_count': 3
                        }).execute()
                        
                        if search_results.data:
                            print(f"✅ Search test successful! Found {len(search_results.data)} results")
                        else:
                            print("ℹ️ Search test completed (no results expected for test)")
                    except Exception as e:
                        print(f"❌ Supabase test failed: {e}")
                else:
                    print("ℹ️ Supabase not configured - skipping database tests")
            else:
                print("❌ No content to embed")
        else:
            print(f"❌ Crawl failed: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Crawl4AI with LiteLLM Integration")
    print("=" * 50)
    
    asyncio.run(test_crawl())
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("\n📋 Next steps:")
    print("1. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env")
    print("2. Run full MCP server when MCP dependency is resolved")
    print("3. Use crawl4ai library directly for crawling tasks")
