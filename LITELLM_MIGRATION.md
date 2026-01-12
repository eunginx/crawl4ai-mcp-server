# LiteLLM Migration Guide

## Overview
This document outlines the migration from direct OpenAI API calls to LiteLLM Router in the Crawl4AI MCP server.

## Changes Made

### 1. Dependencies Updated
- **Removed**: `openai==1.71.0`
- **Added**: `litellm[router]>=1.56.1`

### 2. Code Changes in `src/utils.py`

#### Import Changes
```python
# Before
import openai

# After  
import litellm
from litellm import Router
```

#### Router Configuration
Added `get_litellm_router()` function that:
- Configures primary model (OpenAI)
- Adds Azure OpenAI as fallback (if configured)
- Adds Anthropic as fallback (if configured)
- Sets up retry logic and fallbacks
- Creates separate routers for chat and embeddings

#### Function Updates
All functions now use LiteLLM Router instead of direct OpenAI calls:
- `create_embeddings_batch()` - Uses `_embedding_router.embedding()`
- `generate_contextual_embedding()` - Uses `_chat_router.completion()`
- `generate_code_example_summary()` - Uses `_chat_router.completion()`
- `extract_source_summary()` - Uses `_chat_router.completion()`

### 3. Environment Variables

#### New Optional Variables
```bash
# Azure OpenAI for fallback support
AZURE_API_KEY=
AZURE_API_BASE=
AZURE_API_VERSION=2023-12-01-preview

# Anthropic for fallback support
ANTHROPIC_API_KEY=
```

#### Updated Variable Descriptions
- `OPENAI_API_KEY`: Now used by LiteLLM Router
- `MODEL_CHOICE`: Used with LiteLLM Router (e.g., gpt-4, gpt-4o)

## Benefits

### 1. **Reliability**
- Automatic retry logic with exponential backoff
- Multiple provider fallbacks
- Graceful error handling

### 2. **Flexibility**
- Easy switching between providers
- Support for Azure OpenAI, Anthropic, and 100+ other providers
- No code changes needed to switch providers

### 3. **Performance**
- Built-in load balancing
- Intelligent routing
- 8ms P95 latency at scale

### 4. **Observability**
- Request/response logging
- Performance metrics
- Error tracking

## Migration Steps

### 1. Install Dependencies
```bash
# If using uv
uv sync

# If using pip
pip install litellm[router]>=1.56.1
pip uninstall openai
```

### 2. Update Environment
```bash
# Required
OPENAI_API_KEY=your-openai-key
MODEL_CHOICE=gpt-4

# Optional (for fallback support)
AZURE_API_KEY=your-azure-key
AZURE_API_BASE=your-azure-endpoint
ANTHROPIC_API_KEY=your-anthropic-key
```

### 3. Test Configuration
```python
from src.utils import get_litellm_router

# Test router configuration
chat_router, embedding_router = get_litellm_router()
print("LiteLLM Router configured successfully")
```

## Backward Compatibility

The migration maintains full backward compatibility:
- All function signatures remain unchanged
- Response formats are identical
- Existing environment variables continue to work
- No breaking changes to the public API

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Install LiteLLM with router support
   pip install 'litellm[router]'
   ```

2. **Authentication Errors**
   ```bash
   # Solution: Check API keys are set
   echo $OPENAI_API_KEY
   ```

3. **Router Configuration Issues**
   ```python
   # Enable verbose logging for debugging
   litellm.set_verbose = True
   ```

### Debug Mode
Enable verbose logging to troubleshoot issues:
```python
# In utils.py, change this line:
litellm.set_verbose = True  # Set to False for production
```

## Performance Considerations

### Router Caching
LiteLLM Router includes built-in caching to improve performance:
- Response caching for identical requests
- Connection pooling
- Intelligent request routing

### Cost Optimization
- Automatic fallback to cheaper models when configured
- Request batching for embeddings
- Smart retry logic prevents unnecessary API calls

## Next Steps

1. **Monitor Performance**: Use LiteLLM's built-in observability features
2. **Configure Fallbacks**: Set up Azure OpenAI or Anthropic as backup providers
3. **Optimize Costs**: Configure model fallbacks based on cost/quality tradeoffs
4. **Scale**: Use LiteLLM Proxy Server for team-wide access

## Support

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Router Configuration](https://docs.litellm.ai/docs/routing)
- [Supported Providers](https://docs.litellm.ai/docs/providers)
