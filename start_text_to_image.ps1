
# PowerShell Text-to-Image Generator Startup Script

Write-Host "🎨 Text-to-Image Generator Setup & Runner"
Write-Host "========================================"

# Check if Python is installed
$python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Error: Python 3 is not installed. Please install Python 3.6+ and try again."
    exit 1
}

Write-Host "✅ Python 3 found: $(python3 --version)"

# Check if pip is availabledi
$pip = Get-Command pip3 -ErrorAction SilentlyContinue
if (-not $pip) {
    Write-Host "❌ Error: pip is not installed. Please install pip and try again."
    exit 1
}

# Install basic dependencies
Write-Host "📦 Installing basic dependencies..."
python3 -m pip install flask pillow numpy

# Check if AI dependencies are installed
Write-Host "🤖 Checking AI model dependencies..."
$aiDeps = python3 -c "import torch, diffusers, transformers" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ AI dependencies found - starting full AI mode"
    Write-Host ""
    Write-Host "🚀 Starting Text-to-Image Generator (AI Mode)..."
    Write-Host "Open http://localhost:5000 in your browser"
    Write-Host "Note: Model loading may take a few minutes on first run"
    Write-Host ""
    python3 app.py
} else {
    Write-Host "⚠️  AI dependencies not found"
    Write-Host ""
    Write-Host 'Would you like to:'
    Write-Host '1) Install AI dependencies for full functionality (requires ~8GB download)'
    Write-Host '2) Run in demo mode (generates placeholder images)'
    Write-Host ''
    $choice = Read-Host 'Enter choice (1 or 2)'
    switch ($choice) {
        '1' {
            Write-Host 'Installing AI dependencies (this may take several minutes)...'
            python3 -m pip install torch torchvision diffusers transformers accelerate
            if ($LASTEXITCODE -eq 0) {
                Write-Host 'AI dependencies installed successfully'
                Write-Host ''
                Write-Host 'Starting Text-to-Image Generator (AI Mode)...'
                Write-Host 'Open http://localhost:5000 in your browser'
                Write-Host 'Note: Model loading may take a few minutes on first run'
                python3 app.py
            } else {
                Write-Host 'Failed to install AI dependencies. Running in demo mode...'
                Write-Host ''
                Write-Host 'Starting Text-to-Image Generator (Demo Mode)...'
                Write-Host 'Open http://localhost:5000 in your browser'
                python3 app_demo.py
            }
        }
        '2' {
            Write-Host 'Starting Text-to-Image Generator (Demo Mode)...'
            Write-Host 'Open http://localhost:5000 in your browser'
            python3 app_demo.py
        }
        default {
            Write-Host 'Invalid choice. Starting demo mode...'
            Write-Host ''
            Write-Host 'Starting Text-to-Image Generator (Demo Mode)...'
            Write-Host 'Open http://localhost:5000 in your browser'
            python3 app_demo.py
        }
    }
}