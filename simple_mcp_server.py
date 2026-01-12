#!/usr/bin/env python3
"""
Simple MCP server that provides crawl4ai functionality without complex dependencies.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import core functionality
from utils import get_litellm_router, create_embedding
from supabase import Client
from crawl4ai import AsyncWebCrawler

class SimpleMCPServer:
    """Simple MCP server with crawl4ai functionality."""
    
    def __init__(self):
        self.chat_router, self.embedding_router = get_litellm_router()
        
    async def crawl_url(self, url: str):
        """Crawl a URL and return results."""
        try:
            crawler = AsyncWebCrawler(
                browser_type="chromium",
                headless=True,
                verbose=True
            )
            
            result = await crawler.arun(
                url=url,
                word_count_threshold=100,
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
                # Create embeddings for search
                if result.markdown:
                    embedding = create_embedding(result.markdown[:2000])
                    
                    return {
                        "success": True,
                        "url": url,
                        "title": getattr(result, 'title', 'Unknown Title'),
                        "content": result.markdown[:1000],  # Limit for response
                        "embedding": embedding,
                        "word_count": len(result.markdown.split())
                    }
                else:
                    return {
                        "success": True,
                        "url": url,
                        "title": "Crawled Content",
                        "content": "No markdown content found",
                        "error": "No markdown content found"
                    }
            else:
                return {
                    "success": False,
                    "url": url,
                    "error": result.error_message or "Crawl failed"
                }
                
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    async def search_embeddings(self, query: str, match_count: int = 5):
        """Search using embeddings."""
        try:
            query_embedding = create_embedding(query)
            
            if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_SERVICE_KEY"):
                client = Client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))
                
                results = client.rpc('match_crawled_pages', {
                    'query_embedding': query_embedding,
                    'match_count': match_count
                }).execute()
                
                return {
                    "success": True,
                    "query": query,
                    "results": results.data or [],
                    "count": len(results.data) if results.data else 0
                }
            else:
                return {
                    "success": False,
                    "query": query,
                    "error": "Supabase not configured"
                }
                
        except Exception as e:
            return {
                "success": False,
                "query": query,
                "error": str(e)
            }

async def main():
    """Main server function."""
    server = SimpleMCPServer()
    
    # Simple command line interface
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "crawl":
            if len(sys.argv) > 2:
                url = sys.argv[2]
                print(f"🕷️ Crawling: {url}")
                result = await server.crawl_url(url)
                print(json.dumps(result, indent=2))
            else:
                print("Usage: python simple_mcp_server.py crawl <url>")
                
        elif command == "search":
            if len(sys.argv) > 2:
                query = sys.argv[2]
                print(f"🔍 Searching: {query}")
                result = await server.search_embeddings(query)
                print(json.dumps(result, indent=2))
            else:
                print("Usage: python simple_mcp_server.py search <query>")
                
        else:
            print("Available commands:")
            print("  crawl <url>  - Crawl a URL")
            print("  search <query> - Search embeddings")
    else:
        print("Simple MCP Server for Crawl4AI")
        print("Usage: python simple_mcp_server.py <command> [args]")
        print("Commands: crawl, search")

if __name__ == "__main__":
    asyncio.run(main())
