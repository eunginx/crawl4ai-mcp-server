#!/bin/bash

# MCP Server Stop Script
# Stops the Crawl4AI MCP server gracefully

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/Users/kapilh/mcp-crawl4ai"
PID_FILE="$PROJECT_DIR/mcp_server.pid"

echo -e "${YELLOW}🛑 Stopping Crawl4AI MCP Server...${NC}"

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo -e "${RED}❌ No PID file found. Server may not be running.${NC}"
    echo -e "${YELLOW}💡 Use './start_mcp_server.sh status' to check status${NC}"
    exit 1
fi

# Get PID and check if process is running
PID=$(cat "$PID_FILE")
if ! ps -p "$PID" > /dev/null; then
    echo -e "${YELLOW}⚠️  Process $PID is not running. Cleaning up PID file.${NC}"
    rm -f "$PID_FILE"
    echo -e "${GREEN}✅ Cleanup complete.${NC}"
    exit 0
fi

# Stop the server gracefully
echo -e "${BLUE}🔄 Sending TERM signal to process $PID...${NC}"
kill -TERM "$PID"

# Wait for process to stop
for i in {1..10}; do
    if ! ps -p "$PID" > /dev/null; then
        echo -e "${GREEN}✅ Server stopped successfully!${NC}"
        rm -f "$PID_FILE"
        echo -e "${YELLOW}💡 Use './start_mcp_server.sh start' to restart${NC}"
        exit 0
    fi
    echo -e "${YELLOW}⏳ Waiting for server to stop... ($i/10)${NC}"
    sleep 1
done

# Force kill if still running
echo -e "${RED}⚠️  Server didn't stop gracefully. Force killing...${NC}"
kill -KILL "$PID" 2>/dev/null || true
rm -f "$PID_FILE"
echo -e "${GREEN}✅ Server force stopped.${NC}"
