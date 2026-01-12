# LiteLLM Knowledge Base

## Overview
LiteLLM is a unified interface to call 100+ LLMs in OpenAI format, including Bedrock, Azure, OpenAI, VertexAI, Anthropic, Groq, and more. It provides both a Python SDK and an AI Gateway (Proxy Server) for accessing multiple LLM providers through a single API.

## Key Features
- **Unified Interface**: Call 100+ LLMs using OpenAI-compatible format
- **Multiple Deployment Options**: Python SDK + AI Gateway (Proxy Server)
- **A2A Protocol Support**: Invoke A2A Agents
- **MCP Bridge**: Connect MCP servers to any LLM
- **High Performance**: 8ms P95 latency at 1k RPS
- **Enterprise Features**: Authentication, cost tracking, virtual keys, admin dashboard

## Usage Options

### 1. Python SDK
```python
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"

# OpenAI
response = completion(model="openai/gpt-4o", messages=[{"role": "user", "content": "Hello!"}])

# Anthropic  
response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[{"role": "user", "content": "Hello!"}])
```

### 2. AI Gateway (Proxy Server)
```shell
pip install 'litellm[proxy]'
litellm --model gpt-4o
```

```python
import openai

client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 3. LiteLLM Router
The Router provides retry/fallback logic across multiple deployments with application-level load balancing and cost tracking.

```python
from litellm import Router

router = Router(
    model_list=[
        {"model_name": "gpt-4", "litellm_params": {"model": "openai/gpt-4"}},
        {"model_name": "gpt-4", "litellm_params": {"model": "azure/gpt-4"}},
        {"model_name": "gpt-4", "litellm_params": {"model": "anthropic/claude-sonnet-4-20250514"}},
    ],
    retry_after=30,
    fallbacks=[{"model_group": "gpt-4", "models": ["gpt-3.5-turbo"]}]
)

response = router.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Supported Providers
LiteLLM supports 100+ LLM providers including:
- OpenAI
- Azure OpenAI
- Anthropic
- Google VertexAI
- AWS Bedrock
- Groq
- Cohere
- And many more...

[Complete list of supported models](https://models.litellm.ai/)

## Key Benefits for Crawl4AI Integration

### 1. Unified API Interface
- Replace direct OpenAI calls with LiteLLM's unified interface
- Maintain OpenAI-compatible response format
- Easy to switch between providers without code changes

### 2. Router Features
- **Retry Logic**: Automatic retries with exponential backoff
- **Fallback Support**: Switch to backup providers on failures
- **Load Balancing**: Distribute requests across multiple providers
- **Cost Tracking**: Monitor spending per provider/model

### 3. Error Handling
- OpenAI-compatible error responses
- Automatic exception handling
- Graceful degradation on provider failures

### 4. Observability
- Callbacks for monitoring (Lunary, MLflow, Langfuse)
- Request/response logging
- Performance metrics

## Implementation for Crawl4AI

### Current OpenAI Usage in utils.py:
- `openai.embeddings.create()` for embeddings
- `openai.chat.completions.create()` for contextual embeddings
- Direct API key management

### LiteLLM Migration Strategy:
1. Replace `openai` imports with `litellm`
2. Configure Router for embeddings and chat completions
3. Add fallback providers for reliability
4. Implement retry logic and error handling
5. Maintain existing function signatures for compatibility

### Environment Variables Needed:
```bash
# Existing
OPENAI_API_KEY=your-openai-key
MODEL_CHOICE=gpt-4

# New LiteLLM Configuration (optional)
LITELLM_MODEL_LIST=openai/gpt-4,azure/gpt-4,anthropic/claude-sonnet-4-20250514
LITELLM_RETRY_ENABLED=true
LITELLM_FALLBACK_ENABLED=true
```

## Installation
```bash
pip install litellm
# For proxy server features
pip install 'litellm[proxy]'
# For router features
pip install 'litellm[router]'
```

## Documentation
- [Main Documentation](https://docs.litellm.ai/)
- [Router Documentation](https://docs.litellm.ai/docs/routing)
- [Supported Providers](https://docs.litellm.ai/docs/providers)
- [Proxy Server](https://docs.litellm.ai/docs/simple_proxy)
