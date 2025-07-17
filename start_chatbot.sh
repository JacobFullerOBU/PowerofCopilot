#!/bin/bash

# AI Chatbot One-Click Launcher
# This script installs dependencies, starts the server, and opens the web UI

echo "🤖 AI Chatbot - One-Click Launcher"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to open URL in browser
open_browser() {
    local url="$1"
    echo "🌐 Opening browser..."
    
    if command_exists xdg-open; then
        xdg-open "$url" >/dev/null 2>&1 &
    elif command_exists open; then
        open "$url" >/dev/null 2>&1 &
    elif command_exists start; then
        start "$url" >/dev/null 2>&1 &
    else
        echo "   Please open your browser and go to: $url"
    fi
}

# Check Python installation
if ! command_exists python3; then
    echo "❌ Error: Python 3 is not installed."
    echo "   Please install Python 3.8+ and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check pip
if ! command_exists pip3 && ! command_exists pip; then
    echo "❌ Error: pip is not installed."
    echo "   Please install pip and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "   Trying with basic versions..."
    
    # Fallback to basic versions
    pip install flask torch transformers --quiet
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install even basic dependencies"
        echo "   Please check your internet connection and Python installation"
        exit 1
    fi
fi

echo "✅ Dependencies installed successfully"

# Check if we need to download models
echo "🧠 Checking AI model..."
python3 -c "
import os
os.environ['TRANSFORMERS_OFFLINE'] = '1'
try:
    from transformers import AutoTokenizer
    print('Model cache found')
except:
    print('Will download model on first run')
" 2>/dev/null

# Start the server in background
echo "🚀 Starting AI Chatbot server..."

# Kill any existing process on port 5000
if command_exists lsof; then
    lsof -ti:5000 | xargs kill -9 2>/dev/null || true
fi

# Start server
python3 app.py &
SERVER_PID=$!

# Wait a moment for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if kill -0 $SERVER_PID 2>/dev/null; then
    echo "✅ Server started successfully (PID: $SERVER_PID)"
    
    # Wait a bit more for initialization
    sleep 2
    
    # Open browser
    open_browser "http://localhost:5000"
    
    echo ""
    echo "🎉 AI Chatbot is ready!"
    echo "   URL: http://localhost:5000"
    echo "   Features:"
    echo "   • 🆓 Free to use"
    echo "   • 🚫 No limits"
    echo "   • 🔓 No restrictions"
    echo "   • ⚡ Quick responses"
    echo "   • 🛡️ Local & reliable"
    echo ""
    echo "Press Ctrl+C to stop the server"
    
    # Wait for user to stop
    wait $SERVER_PID
    
else
    echo "❌ Failed to start server"
    echo "   Check the error messages above"
    exit 1
fi

echo ""
echo "👋 AI Chatbot stopped. Thanks for using!"