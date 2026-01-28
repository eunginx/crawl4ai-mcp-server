# MCP Crawl4AI Server Logging Implementation

## Overview
Comprehensive logging has been successfully implemented for the MCP Crawl4AI server to provide detailed visibility into server operations, performance, and debugging information.

## Features Implemented

### 1. Logging Configuration
- **Rotating File Handler**: 10MB max file size with 5 backup files
- **Timestamped Log Files**: Format `mcp_crawl4ai_YYYYMMDD_HHMMSS.log`
- **Detailed Log Format**: `timestamp - logger_name - level - function:line - message`
- **Dual Output**: Both file logging (DEBUG level) and console output (INFO level)
- **UTF-8 Encoding**: Proper character encoding for international content

### 2. Log Directory Structure
- **Location**: `/Users/kapilh/mcp-crawl4ai/logs/`
- **Automatic Creation**: Directory created if it doesn't exist
- **File Rotation**: Automatic rotation when files reach size limit

### 3. Comprehensive Logging Coverage

#### Server Lifecycle
- Server startup and shutdown
- Component initialization (crawler, Supabase, Neo4j, reranking models)
- Configuration validation and environment variable checks
- Resource cleanup during shutdown

#### MCP Tools
- `crawl_single_page`: Complete crawling workflow logging
- `smart_crawl_url`: Multi-strategy crawling with detailed progress
- `get_available_sources`: Database query operations
- `perform_rag_query`: Search operations, hybrid search, reranking
- `search_code_examples`: Code example search and filtering
- Knowledge graph operations and validation

#### Helper Functions
- `ensure_source_exists`: Database operations
- `crawl_markdown_file`: File crawling operations
- `crawl_batch`: Parallel crawling with success rates
- `crawl_recursive_internal_links`: Recursive crawling with depth tracking

#### Error Handling
- Exception logging with context
- Failed operation tracking
- Configuration error reporting
- Network and database error logging

### 4. Log Levels Used
- **DEBUG**: Detailed execution flow, configuration values, intermediate steps
- **INFO**: Major operations, success/failure summaries, progress updates
- **WARNING**: Configuration issues, fallback behaviors
- **ERROR**: Failed operations, exceptions, network issues
- **CRITICAL**: Server startup failures, critical system errors

### 5. Performance Tracking
- Operation timing and duration
- Success/failure rates for batch operations
- Resource usage indicators
- Progress tracking for long-running operations

## Usage

### Viewing Logs
```bash
# View latest log file
tail -f /Users/kapilh/mcp-crawl4ai/logs/mcp_crawl4ai_*.log

# Search for specific operations
grep "crawl_single_page" /Users/kapilh/mcp-crawl4ai/logs/mcp_crawl4ai_*.log

# Filter by log level
grep "ERROR" /Users/kapilh/mcp-crawl4ai/logs/mcp_crawl4ai_*.log
```

### Log File Examples
The logs will show detailed information like:
```
2025-01-13 15:30:00 - root - INFO - crawl4ai_lifespan:218 - === MCP Server Lifecycle Starting ===
2025-01-13 15:30:01 - root - INFO - crawl4ai_lifespan:231 - Initializing AsyncWebCrawler...
2025-01-13 15:30:02 - root - INFO - crawl4ai_lifespan:234 - ✓ AsyncWebCrawler initialized successfully
2025-01-13 15:30:03 - root - INFO - crawl_single_page:544 - === Starting crawl_single_page ===
2025-01-13 15:30:03 - root - INFO - crawl_single_page:545 - Target URL: https://example.com
```

## Benefits

### Debugging
- Step-by-step execution tracking
- Error context and stack traces
- Configuration validation logging

### Performance Monitoring
- Operation timing and success rates
- Resource usage patterns
- Bottleneck identification

### Operational Visibility
- Real-time progress tracking
- System health monitoring
- Usage pattern analysis

### Troubleshooting
- Failed operation details
- Network and database issues
- Configuration problems

## Implementation Details

### Key Functions Modified
- `setup_logging()`: Logging configuration and initialization
- `crawl4ai_lifespan()`: Server lifecycle management
- All MCP tool functions with comprehensive logging
- Helper functions with operation tracking

### Environment Variables Logged
- `USE_RERANKING`: Reranking model usage
- `USE_KNOWLEDGE_GRAPH`: Neo4j knowledge graph functionality
- `USE_HYBRID_SEARCH`: Search strategy configuration
- `USE_AGENTIC_RAG`: Code example extraction

### Error Handling
- All exceptions logged with context
- Graceful degradation logging
- Critical error tracking for server failures

## Maintenance

### Log Rotation
- Automatic rotation at 10MB
- 5 backup files retained
- Timestamped filenames for easy identification

### Storage Requirements
- Estimated 1-5MB per hour of normal operation
- Depends on crawling volume and complexity
- Monitor disk space for long-running operations

This comprehensive logging implementation provides complete visibility into MCP server operations, making it easy to debug issues, monitor performance, and understand where the server might be failing.
