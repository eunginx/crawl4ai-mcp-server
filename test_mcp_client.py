#!/usr/bin/env python3
"""
Simple MCP client test for the local crawl4ai-mcp-rag server.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
import subprocess

async def test_mcp_client():
    """Test the MCP server using a client connection."""
    
    print("🧪 Testing MCP Server with Client Connection")
    print("=" * 50)
    
    # Server parameters
    server_params = StdioServerParameters(
        command="/Users/kapilh/mcp-crawl4ai/.venv-312/bin/python",
        args=["src/crawl4ai_mcp.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                # List available tools
                print("\n📋 Available tools:")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Test get_available_sources
                print("\n1️⃣ Testing get_available_sources...")
                try:
                    result = await session.call_tool("get_available_sources", {})
                    print(f"✅ Result: {result.content[0].text[:200]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test crawl_single_page
                print("\n2️⃣ Testing crawl_single_page...")
                try:
                    result = await session.call_tool("crawl_single_page", {
                        "url": "https://example.com"
                    })
                    print(f"✅ Result: {result.content[0].text[:200]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                print("\n🎉 MCP Client Test Completed!")
                
    except Exception as e:
        print(f"❌ MCP Client Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_client())
