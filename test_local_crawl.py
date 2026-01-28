
import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def test_crawl_local_file():
    print("🧪 Testing Local File Crawling")
    print("=" * 50)

    # Create a dummy test file
    test_file_path = Path(os.getcwd()) / "test_doc.md"
    with open(test_file_path, "w") as f:
        f.write("# Test Document\n\nThis is a local test file for the MCP server.\nIt contains some sample text to verify crawling capabilities on local files.")
    
    print(f"📄 Created test file at: {test_file_path}")

    # Server parameters
    server_params = StdioServerParameters(
        command="/Users/kapilh/mcp-crawl4ai/.venv-312/bin/python",
        args=["src/crawl4ai_mcp.py"],
        env={
            "LOGLEVEL": "INFO", 
            "PYTHONPATH": "/Users/kapilh/mcp-crawl4ai",
            "PYTHONUNBUFFERED": "1",
            "TRANSPORT": "stdio",
            # Add other required env vars here if needed by the server logic itself
             "OLLAMA_API_KEY": "e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj",
            "OLLAMA_API_BASE": "https://ollama.com",
            "LLM_PROVIDER": "ollama/gpt-oss:120b",
            "LLM_BASE_URL": "https://ollama.com",
            "EMBEDDING_MODEL": "ollama/all-minilm",
            "EMBEDDING_BASE_URL": "https://api.ollama.com",
            "EMBEDDING_API_KEY": "e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj",
            "USE_CONTEXTUAL_EMBEDDINGS": "false", # Keep it simple for test
            "USE_HYBRID_SEARCH": "false",
            "USE_AGENTIC_RAG": "false",
            "USE_RERANKING": "false",
            "USE_KNOWLEDGE_GRAPH": "false",
            "SUPABASE_URL": "https://tcoowuyddxbvmlcpnjsq.supabase.co",
            "SUPABASE_SERVICE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRjb293dXlkZHhidm1sY3BuanNxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2ODA3NDE1NiwiZXhwIjoyMDgzNjUwMTU2fQ.bFqOhWdQo7ddJW_FQVQgWM-k8kfml9yUFvD-eyuePCI",
        }
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Use the smart_crawl_url tool on the local file
                # Note: Browsers usually need file:// protocol for local files
                file_url = f"file://{test_file_path}"
                print(f"\n🔍 Crawling URL: {file_url}")
                
                # Check if 'crawl_local_file' or 'smart_crawl_url' handles local files
                # Based on previous file reads, 'smart_crawl_url' delegates to 'crawl_markdown_file' for .txt/.md if logic permits
                # But 'crawl_markdown_file' uses 'crawler.arun', which typically handles http/https. 
                # Crawl4AI might support file:// if configured correctly.
                # However, looking at the code, `is_txt` checks for .txt. Our file is .md. 
                # Let's try `smart_crawl_url` first.
                
                try:
                    result = await session.call_tool("smart_crawl_url", {
                        "url": file_url
                    })
                    print(f"\n✅ Crawl Result:\n{result.content[0].text}")
                except Exception as e:
                    print(f"\n❌ Crawl Error: {e}")

    except Exception as e:
        print(f"\n❌ Session Error: {e}")
    finally:
        # Cleanup
        if test_file_path.exists():
            os.remove(test_file_path)
            print(f"\n🗑️ Removed test file")

if __name__ == "__main__":
    asyncio.run(test_crawl_local_file())
