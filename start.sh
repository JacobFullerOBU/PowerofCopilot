#!/bin/bash

# Text to Video Generator Startup Script

echo "🎬 Starting Text to Video Generator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p generated_videos
mkdir -p static/css static/js templates

# Check if CUDA is available
echo "🔍 Checking GPU availability..."
python3 -c "import torch; print('✅ CUDA available:', torch.cuda.is_available())"

# Start the application
echo "🚀 Starting the web application..."
echo "📱 Open your browser and navigate to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python app.py