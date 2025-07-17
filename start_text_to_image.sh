#!/bin/bash

# Text-to-Image Generator Startup Script

echo "🎨 Text-to-Image Generator Setup & Runner"
echo "========================================"

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

# Install basic dependencies
echo "📦 Installing basic dependencies..."
pip3 install flask pillow numpy

# Check if AI dependencies are installed
echo "🤖 Checking AI model dependencies..."
if python3 -c "import torch, diffusers, transformers" 2>/dev/null; then
    echo "✅ AI dependencies found - starting full AI mode"
    echo ""
    echo "🚀 Starting Text-to-Image Generator (AI Mode)..."
    echo "Open http://localhost:5000 in your browser"
    echo "Note: Model loading may take a few minutes on first run"
    echo ""
    python3 app.py
else
    echo "⚠️  AI dependencies not found"
    echo ""
    echo "Would you like to:"
    echo "1) Install AI dependencies for full functionality (requires ~8GB download)"
    echo "2) Run in demo mode (generates placeholder images)"
    echo ""
    read -p "Enter choice (1 or 2): " choice
    
    case $choice in
        1)
            echo "📥 Installing AI dependencies (this may take several minutes)..."
            pip3 install torch torchvision diffusers transformers accelerate
            if [ $? -eq 0 ]; then
                echo "✅ AI dependencies installed successfully"
                echo ""
                echo "🚀 Starting Text-to-Image Generator (AI Mode)..."
                echo "Open http://localhost:5000 in your browser"
                echo "Note: Model loading may take a few minutes on first run"
                python3 app.py
            else
                echo "❌ Failed to install AI dependencies. Running in demo mode..."
                echo ""
                echo "🚀 Starting Text-to-Image Generator (Demo Mode)..."
                echo "Open http://localhost:5000 in your browser"
                python3 app_demo.py
            fi
            ;;
        2)
            echo "🚀 Starting Text-to-Image Generator (Demo Mode)..."
            echo "Open http://localhost:5000 in your browser"
            python3 app_demo.py
            ;;
        *)
            echo "Invalid choice. Starting demo mode..."
            echo ""
            echo "🚀 Starting Text-to-Image Generator (Demo Mode)..."
            echo "Open http://localhost:5000 in your browser"
            python3 app_demo.py
            ;;
    esac
fi