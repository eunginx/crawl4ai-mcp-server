# Ollama Configuration Guide

## Overview
This guide covers configuring Crawl4AI MCP server to use Ollama for LLM and embedding services through LiteLLM Router.

## Environment Variables

### For Ollama LLM
```bash
# Force LiteLLM to use Ollama
OLLAMA_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj
OLLAMA_API_BASE=https://ollama.com

# Tell Crawl4AI explicitly to use Ollama
LLM_PROVIDER=ollama/gpt-oss:120b-cloud
LLM_BASE_URL=https://ollama.com
```

### For Ollama Embeddings
```bash
# Embedding model configuration
EMBEDDING_MODEL=ollama/nomic-embed-text
EMBEDDING_BASE_URL=https://ollama.com
EMBEDDING_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj
```

## Complete Ollama Configuration

### Option 1: Ollama for Both LLM and Embeddings
```bash
# Ollama Configuration
OLLAMA_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj
OLLAMA_API_BASE=https://ollama.com

# LLM Configuration
LLM_PROVIDER=ollama/gpt-oss:120b-cloud
LLM_BASE_URL=https://ollama.com

# Embedding Configuration
EMBEDDING_MODEL=ollama/nomic-embed-text
EMBEDDING_BASE_URL=https://ollama.com
EMBEDDING_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj

# Other required variables
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-key
```

### Option 2: Ollama LLM with OpenAI Embeddings
```bash
# Ollama Configuration
OLLAMA_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj
OLLAMA_API_BASE=https://ollama.com

# LLM Configuration
LLM_PROVIDER=ollama/gpt-oss:120b-cloud
LLM_BASE_URL=https://ollama.com

# Use OpenAI for embeddings (default)
OPENAI_API_KEY=your-openai-key

# Other required variables
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-key
```

### Option 3: Hybrid Setup with Fallbacks
```bash
# Primary: Ollama
OLLAMA_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj
OLLAMA_API_BASE=https://ollama.com
LLM_PROVIDER=ollama/gpt-oss:120b-cloud
LLM_BASE_URL=https://ollama.com

# Fallback: OpenAI
OPENAI_API_KEY=your-openai-key

# Embedding: Ollama
EMBEDDING_MODEL=ollama/nomic-embed-text
EMBEDDING_BASE_URL=https://ollama.com
EMBEDDING_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj

# Optional: Azure fallback
AZURE_API_KEY=your-azure-key
AZURE_API_BASE=your-azure-endpoint

# Other required variables
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-key
```

## Supported Ollama Models

### LLM Models
- `ollama/gpt-oss:120b-cloud` - Large model for complex tasks
- `ollama/llama3` - Meta's Llama 3
- `ollama/llama3:8b` - Llama 3 8B parameter
- `ollama/llama2` - Llama 2
- `ollama/mistral` - Mistral AI
- `ollama/codellama` - Code-specialized model

### Embedding Models
- `ollama/nomic-embed-text` - Nomic's embedding model
- `ollama/all-minilm` - MiniLM embeddings
- `ollama/mxbai-embed-large` - Large embedding model

## Configuration Examples

### Development Setup
```bash
# .env file for development
TRANSPORT=sse
HOST=0.0.0.0
PORT=8787

# Ollama setup
OLLAMA_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj
OLLAMA_API_BASE=https://ollama.com
LLM_PROVIDER=ollama/gpt-oss:120b-cloud
LLM_BASE_URL=https://ollama.com
EMBEDDING_MODEL=ollama/nomic-embed-text
EMBEDDING_BASE_URL=https://ollama.com

# RAG strategies
USE_CONTEXTUAL_EMBEDDINGS=true
USE_HYBRID_SEARCH=true
USE_AGENTIC_RAG=true

# Database
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-key
```

### Production Setup
```bash
# .env file for production
TRANSPORT=sse
HOST=0.0.0.0
PORT=8787

# Primary: Ollama
OLLAMA_API_KEY=e2da754ec5bb4d4ca024e6c691389636.XthqUH4xmHiN89Kick9BBGZj
OLLAMA_API_BASE=https://ollama.com
LLM_PROVIDER=ollama/gpt-oss:120b-cloud
LLM_BASE_URL=https://ollama.com
EMBEDDING_MODEL=ollama/nomic-embed-text
EMBEDDING_BASE_URL=https://ollama.com

# Fallbacks for reliability
OPENAI_API_KEY=your-openai-key
AZURE_API_KEY=your-azure-key
AZURE_API_BASE=your-azure-endpoint

# RAG strategies
USE_CONTEXTUAL_EMBEDDINGS=true
USE_HYBRID_SEARCH=true
USE_AGENTIC_RAG=true
USE_RERANKING=true

# Database
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-key
```

## Testing Configuration

### 1. Test LLM Connection
```python
from src.utils import get_litellm_router

# Test router configuration
chat_router, embedding_router = get_litellm_router()

# Test LLM
response = chat_router.completion(
    model="primary",
    messages=[{"role": "user", "content": "Hello, test message"}]
)
print("LLM Test:", response.choices[0].message.content)
```

### 2. Test Embedding Connection
```python
# Test embeddings
response = embedding_router.embedding(
    model="embeddings",
    input=["Test text for embedding"]
)
print("Embedding Test:", len(response.data[0]["embedding"]), "dimensions")
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   ```bash
   # Check Ollama API accessibility
   curl -H "Authorization: Bearer $OLLAMA_API_KEY" \
        "$OLLAMA_API_BASE/api/tags"
   ```

2. **Model Not Found**
   ```bash
   # List available models
   curl -H "Authorization: Bearer $OLLAMA_API_KEY" \
        "$OLLAMA_API_BASE/api/tags"
   ```

3. **Authentication Issues**
   - Verify API key is correct
   - Check API base URL
   - Ensure proper headers are being sent

### Debug Mode
Enable verbose logging:
```python
# In utils.py
litellm.set_verbose = True
```

### Performance Optimization

1. **Batch Embeddings**
   - Process multiple texts at once
   - Reduces API calls significantly

2. **Context Caching**
   - Enable contextual embeddings
   - Improves retrieval quality

3. **Hybrid Search**
   - Combine vector and keyword search
   - Better results for specific queries

## Best Practices

1. **Use Fallbacks**: Configure backup providers for reliability
2. **Monitor Performance**: Track latency and error rates
3. **Optimize Costs**: Choose appropriate model sizes
4. **Secure API Keys**: Use environment variables, never commit keys
5. **Test Thoroughly**: Verify both LLM and embedding endpoints

## Next Steps

1. Configure your `.env` file with the desired setup
2. Test both LLM and embedding connections
3. Monitor performance and adjust as needed
4. Consider setting up fallback providers for production use
