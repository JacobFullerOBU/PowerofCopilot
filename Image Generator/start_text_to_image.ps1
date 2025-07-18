
# PowerShell Text-to-Image Generator Startup Script

Write-Host "🎨 Text-to-Image Generator Setup & Runner"
Write-Host "========================================"

# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Error: Python is not installed. Please install Python 3.6+ and try again."
    exit 1
}

Write-Host "✅ Python found: $(python --version)"

# Check if pip is available
$pip = Get-Command pip -ErrorAction SilentlyContinue
if (-not $pip) {
    Write-Host "❌ Error: pip is not installed. Please install pip and try again."
    exit 1
}

# Install Stable Diffusion & DreamShaper dependencies
Write-Host 'Installing Stable Diffusion dependencies...'
python -m pip install flask pillow torch diffusers transformers accelerate safetensors

Write-Host 'Download the DreamShaper model from CivitAI:'
Write-Host 'https://civitai.com/models/4384/dreamshaper'
Write-Host 'Place the .safetensors or .ckpt file in the Image Generator folder.'
Write-Host 'If using safetensors, use the safetensors file path in your app.'

# Start the Stable Diffusion Web UI
Write-Host ''
Write-Host 'Starting Stable Diffusion Web UI (DreamShaper)...'
Write-Host 'Open http://localhost:5000 in your browser'
Write-Host 'Note: Model loading may take a few minutes on first run'
python "Image Generator/app.py"