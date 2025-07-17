#!/bin/bash

# Spotify Reader Setup and Runner Script

echo "🎶 Spotify Reader Setup & Runner"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.6+ and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip is not installed. Please install pip and try again."
    exit 1
fi

# Install dependencies if they're not installed
echo "📦 Checking dependencies..."
if ! python3 -c "import spotipy, dotenv" 2>/dev/null; then
    echo "📥 Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install dependencies. Please check your pip installation."
        exit 1
    fi
    echo "✅ Dependencies installed successfully"
else
    echo "✅ Dependencies already installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️  Setting up environment configuration..."
    echo ""
    echo "🔑 Spotify API credentials are required to use this tool."
    echo "   Please follow these steps:"
    echo ""
    echo "   1. Go to https://developer.spotify.com/dashboard"
    echo "   2. Log in with your Spotify account"
    echo "   3. Click 'Create App'"
    echo "   4. Set redirect URI to: http://localhost:8080"
    echo "   5. Copy your Client ID and Client Secret"
    echo ""
    
    if [ -f ".env.example" ]; then
        echo "📋 Copying .env.example to .env..."
        cp .env.example .env
        echo "✅ Please edit the .env file with your Spotify API credentials"
        echo ""
        echo "To edit .env file:"
        echo "  nano .env"
        echo "  # or"
        echo "  vim .env"
        echo "  # or use any text editor"
        echo ""
        echo "After setting up your credentials, run this script again."
        exit 0
    else
        echo "❌ Error: .env.example file not found"
        exit 1
    fi
fi

# Check if .env has been configured
if grep -q "your_client_id_here" .env || grep -q "your_client_secret_here" .env; then
    echo "⚠️  Warning: .env file contains placeholder values"
    echo "   Please edit .env with your actual Spotify API credentials"
    echo ""
    echo "Current .env content:"
    cat .env
    echo ""
    echo "After updating your credentials, run this script again."
    exit 0
fi

echo "✅ Environment configured"
echo ""
echo "🚀 Starting Spotify Reader..."
echo ""

# Run the main script
python3 spotify_reader.py

echo ""
echo "👋 Thanks for using Spotify Reader!"