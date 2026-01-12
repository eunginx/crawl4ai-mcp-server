#!/usr/bin/env python3
"""
Test script for the local crawl4ai-mcp-rag MCP server tools.
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

# Import the MCP server functions directly
from crawl4ai_mcp import (
    crawl_single_page,
    smart_crawl_url,
    get_available_sources,
    perform_rag_query
)

# Import the context classes
from crawl4ai_mcp import Crawl4AIContext
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from src.utils import get_supabase_client

async def create_test_context():
    """Create a proper test context with initialized components."""
    # Create browser configuration
    browser_config = BrowserConfig(
        headless=True,
        verbose=False
    )

    # Initialize the crawler
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.__aenter__()

    # Initialize Supabase client
    supabase_client = get_supabase_client()

    # Create context
    context = Crawl4AIContext(
        crawler=crawler,
        supabase_client=supabase_client
    )

    return context

async def test_mcp_tools():
    """Test the MCP server tools directly."""

    print("🧪 Testing Local Crawl4AI RAG MCP Server Tools")
    print("=" * 60)

    # Create proper context
    print("\n🔧 Initializing test context...")
    try:
        context = await create_test_context()
        print("✅ Context initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize context: {e}")
        return

    # Create mock context for tools
    class MockContext:
        def __init__(self, lifespan_context):
            self.request_context = type('RequestContext', (), {
                'lifespan_context': lifespan_context
            })()

    mock_ctx = MockContext(context)

    try:
        # Test 1: Get available sources
        print("\n1️⃣ Testing get_available_sources...")
        try:
            result = await get_available_sources(mock_ctx)
            print(f"✅ get_available_sources result: {result[:200]}...")
        except Exception as e:
            print(f"❌ get_available_sources failed: {e}")

        # Test 2: Crawl React documentation
        print("\n2️⃣ Testing crawl_single_page with React docs...")
        try:
            result = await crawl_single_page(mock_ctx, "https://react.dev/learn")
            print(f"✅ crawl_single_page result: {result[:200]}...")
        except Exception as e:
            print(f"❌ crawl_single_page failed: {e}")

        # Test 3: Smart crawl React docs
        print("\n3️⃣ Testing smart_crawl_url with React docs...")
        try:
            result = await smart_crawl_url(mock_ctx, "https://react.dev/learn", max_depth=1, max_concurrent=2, chunk_size=5000)
            print(f"✅ smart_crawl_url result: {result[:200]}...")
        except Exception as e:
            print(f"❌ smart_crawl_url failed: {e}")

        # Test 4: RAG query for React content
        print("\n4️⃣ Testing perform_rag_query for React docs...")
        try:
            result = await perform_rag_query(mock_ctx, "What is React?", source="react.dev", match_count=3)
            print(f"✅ perform_rag_query result: {result[:500]}...")
        except Exception as e:
            print(f"❌ perform_rag_query failed: {e}")

        # Test 5: RAG query for React concepts
        print("\n5️⃣ Testing perform_rag_query for React concepts...")
        try:
            result = await perform_rag_query(mock_ctx, "How do I create a React component?", source="react.dev", match_count=2)
            print(f"✅ perform_rag_query result: {result[:500]}...")
        except Exception as e:
            print(f"❌ perform_rag_query failed: {e}")

    finally:
        # Clean up
        print("\n🧹 Cleaning up context...")
        try:
            await context.crawler.__aexit__(None, None, None)
            print("✅ Context cleaned up successfully")
        except Exception as e:
            print(f"❌ Failed to clean up context: {e}")

    print("\n" + "=" * 60)
    print("🎉 MCP Server Tools Test Completed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
