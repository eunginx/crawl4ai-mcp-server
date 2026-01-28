# MCP Crawl4AI Server - Setup & Usage Plan

## 1. Analysis and Status
The MCP server is a powerful RAG system integrated with Crawl4AI, Supabase, and LiteLLM (supporting Ollama).

**Current Status:**
- ✅ **Python Environment**: Verified (`.venv-312`).
- ✅ **Dependencies**: Verified imports.
- ✅ **Browsers**: Installed Playwright browsers.
- ✅ **Server Test**: Passed! `test_mcp_client.py` runs successfully.
- ✅ **Stdio Protocol**: **FIXED**. Removed all `print()` statements and console logging that polluted the JSON-RPC stream.
- ✅ **Circular Import**: **FIXED**. Moved `CrossEncoder` import to local scope.
- ✅ **Ready for Production**: The server is fully functional in stdio mode.

## 2. Prerequisites (Action Required)
Before using the server fully, ensure your Supabase database is ready:

1.  **Supabase Setup**:
    - Go to your Supabase project's **SQL Editor**.
    - Run the contents of `crawled_pages.sql` (found in the project root).
    - This creates the `crawled_pages`, `sources`, and `code_examples` tables.

2.  **Environment Variables**:
    - Your `.env` file is already configured with Supabase credentials and Ollama settings.
    - Ensure your Ollama instance is running if you plan to use it.

## 3. Running the Server

### Option A: Using Python (Recommended)
You can run the server directly using the virtual environment:

```bash
/Users/kapilh/mcp-crawl4ai/.venv-312/bin/python src/crawl4ai_mcp.py
```

### Option B: Using Docker
If you prefer Docker:
```bash
docker run --env-file .env -p 8051:8051 mcp/crawl4ai-rag
```

## 4. Connecting MCP Clients

### Claude Desktop / Windsurf Configuration
Add this to your MCP `config.json` (usually `~/Library/Application Support/Claude/claude_desktop_config.json` or similar):

```json
{
  "mcpServers": {
    "crawl4ai-rag": {
      "command": "/Users/kapilh/mcp-crawl4ai/.venv-312/bin/python",
      "args": ["/Users/kapilh/mcp-crawl4ai/src/crawl4ai_mcp.py"],
      "env": {
        "TRANSPORT": "stdio",
        "OLLAMA_API_KEY": "e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj",
        "OLLAMA_API_BASE": "https://ollama.com",
        "SUPABASE_URL": "https://tcoowuyddxbvmlcpnjsq.supabase.co",
        "SUPABASE_SERVICE_KEY": "your_service_key_from_env_file" 
      }
    }
  }
}
```
*Note: Make sure to copy the full `SUPABASE_SERVICE_KEY` from your `.env` file into the config above.*

## 5. Testing
You can re-run the test client anytime to verify functionality:
```bash
/Users/kapilh/mcp-crawl4ai/.venv-312/bin/python test_mcp_client.py
```
