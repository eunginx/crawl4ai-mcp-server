#!/bin/bash

# MCP Server Startup Script
# Keeps the Crawl4AI MCP server running with auto-restart

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/Users/kapilh/mcp-crawl4ai"
VENV_DIR="$PROJECT_DIR/.venv-312"
LOG_FILE="$PROJECT_DIR/mcp_server.log"
PID_FILE="$PROJECT_DIR/mcp_server.pid"

echo -e "${BLUE}🚀 Starting Crawl4AI MCP Server...${NC}"

# Function to check if server is running
is_server_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    else
        return 1
    fi
}

# Function to start server
start_server() {
    echo -e "${GREEN}📋 Activating Python 3.11 environment...${NC}"
    cd "$PROJECT_DIR"
    source "$VENV_DIR/bin/activate"
    export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"
    
    echo -e "${YELLOW}🔧 Starting MCP server on http://0.0.0.0:8051${NC}"
    echo -e "${BLUE}📝 Logs: $LOG_FILE${NC}"
    echo -e "${BLUE}🔄 Auto-restart enabled${NC}"
    
    # Start server in background with logging
    nohup python -m src.crawl4ai_mcp > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    
    sleep 3
    
    if is_server_running; then
        echo -e "${GREEN}✅ MCP Server started successfully!${NC}"
        echo -e "${GREEN}🌐 Server URL: http://0.0.0.0:8051${NC}"
        echo -e "${GREEN}📊 SSE Endpoint: http://0.0.0.0:8051/sse${NC}"
        echo -e "${GREEN}📋 Process ID: $(cat $PID_FILE)${NC}"
        echo -e "${YELLOW}💡 Use 'tail -f $LOG_FILE' to monitor logs${NC}"
        echo -e "${YELLOW}💡 Use './stop_mcp_server.sh' to stop server${NC}"
    else
        echo -e "${RED}❌ Failed to start MCP server${NC}"
        echo -e "${RED}📝 Check logs: tail -20 $LOG_FILE${NC}"
        exit 1
    fi
}

# Function to stop server
stop_server() {
    echo -e "${YELLOW}🛑 Stopping MCP Server...${NC}"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            kill "$PID"
            echo -e "${GREEN}✅ Server stopped${NC}"
        else
            echo -e "${YELLOW}⚠️  Server was not running${NC}"
        fi
        rm -f "$PID_FILE"
    else
        echo -e "${YELLOW}⚠️  No PID file found${NC}"
    fi
}

# Function to show status
show_status() {
    echo -e "${BLUE}📊 MCP Server Status:${NC}"
    
    if is_server_running; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✅ Status: RUNNING${NC}"
        echo -e "${GREEN}🔄 Process ID: $PID${NC}"
        echo -e "${GREEN}🌐 Server URL: http://0.0.0.0:8051${NC}"
        echo -e "${GREEN}📊 SSE Endpoint: http://0.0.0.0:8051/sse${NC}"
        echo -e "${GREEN}📝 Log file: $LOG_FILE${NC}"
        
        # Show recent logs
        echo -e "${BLUE}📋 Recent logs (last 10 lines):${NC}"
        tail -10 "$LOG_FILE" 2>/dev/null || echo "No logs available"
    else
        echo -e "${RED}❌ Status: STOPPED${NC}"
        echo -e "${YELLOW}💡 Use '$0 start' to start the server${NC}"
    fi
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}📝 Following MCP Server logs...${NC}"
    echo -e "${YELLOW}💡 Press Ctrl+C to stop following logs${NC}"
    tail -f "$LOG_FILE"
}

# Main script logic
case "$1" in
    start)
        if is_server_running; then
            echo -e "${YELLOW}⚠️  MCP Server is already running!${NC}"
            echo -e "${YELLOW}💡 Use '$0 status' to check status${NC}"
            echo -e "${YELLOW}💡 Use '$0 stop' to stop server${NC}"
        else
            start_server
        fi
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 2
        start_server
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    test)
        echo -e "${BLUE}🧪 Testing MCP Server connectivity...${NC}"
        
        # Test if server is running
        if is_server_running; then
            echo -e "${GREEN}✅ Server process is running${NC}"
            
            # Test HTTP endpoint
            echo -e "${BLUE}🌐 Testing HTTP endpoint...${NC}"
            if curl -s http://localhost:8051/ > /dev/null; then
                echo -e "${GREEN}✅ HTTP endpoint accessible${NC}"
            else
                echo -e "${RED}❌ HTTP endpoint not accessible${NC}"
            fi
            
            # Test SSE endpoint
            echo -e "${BLUE}📊 Testing SSE endpoint...${NC}"
            if curl -s http://localhost:8051/sse > /dev/null; then
                echo -e "${GREEN}✅ SSE endpoint accessible${NC}"
            else
                echo -e "${RED}❌ SSE endpoint not accessible${NC}"
            fi
        else
            echo -e "${RED}❌ Server is not running${NC}"
        fi
        ;;
    *)
        echo -e "${BLUE}🚀 Crawl4AI MCP Server Manager${NC}"
        echo ""
        echo -e "${GREEN}Usage: $0 {command}${NC}"
        echo ""
        echo -e "${YELLOW}Commands:${NC}"
        echo -e "  ${GREEN}start${NC}     - Start the MCP server"
        echo -e "  ${GREEN}stop${NC}      - Stop the MCP server"
        echo -e "  ${GREEN}restart${NC}   - Restart the MCP server"
        echo -e "  ${GREEN}status${NC}    - Show server status"
        echo -e "  ${GREEN}logs${NC}     - Show server logs"
        echo -e "  ${GREEN}test${NC}     - Test server connectivity"
        echo ""
        echo -e "${BLUE}Configuration:${NC}"
        echo -e "  📁 Project: $PROJECT_DIR"
        echo -e "  🐍 Python: $VENV_DIR"
        echo -e "  📝 Logs: $LOG_FILE"
        echo -e "  🔄 PID: $PID_FILE"
        ;;
esac
