
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


# Install StyleGAN2 dependencies
Write-Host 'Installing StyleGAN2 dependencies...'
python3 -m pip install flask pillow torch ninja

Write-Host 'Make sure you have cloned the StyleGAN2-ADA-PyTorch repo for dnnlib support:'
Write-Host 'git clone https://github.com/NVlabs/stylegan2-ada-pytorch.git'
Write-Host 'If you get import errors for dnnlib, add the repo folder to your PYTHONPATH or copy dnnlib into your project.'

# Start the StyleGAN2 Web UI
Write-Host ''
Write-Host 'Starting StyleGAN2 Web UI...'
Write-Host 'Open http://localhost:5000 in your browser'
Write-Host 'Note: Model loading may take a few minutes on first run'
python3 app.py