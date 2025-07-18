
# PowerShell Text-to-Image Generator Startup Script

Write-Host "🎨 Text-to-Image Generator Setup & Runner"
Write-Host "========================================"



# Desired Python version (change as needed)
$desiredPyVersion = "3.10"

# Try to find the desired Python version
$pyCmd = "py -$desiredPyVersion"
$python = Get-Command python -ErrorAction SilentlyContinue
$pyDesired = Get-Command $pyCmd -ErrorAction SilentlyContinue

if (-not $pyDesired) {
    Write-Host "❌ Python $desiredPyVersion is not installed. Please install it from https://www.python.org/downloads/ and try again."
    exit 1
}

try {
    $pyVersion = & $pyCmd --version 2>&1
    Write-Host "✅ Python $desiredPyVersion found: $pyVersion"
} catch {
    Write-Host "✅ Python $desiredPyVersion found."
}

# Check if pip is available for desired Python
$pipCheck = & $pyCmd -m pip --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ pip is not installed for Python $desiredPyVersion. Please install pip and try again."
    exit 1
}

# Create and activate Python virtual environment with desired version
$venvPath = "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating Python $desiredPyVersion virtual environment..."
    & $pyCmd -m venv $venvPath
}
Write-Host "Activating Python virtual environment..."
& "$venvPath\Scripts\Activate.ps1"

# Use venv python and pip
$venvPython = "$venvPath\Scripts\python.exe"
$venvPip = "$venvPath\Scripts\pip.exe"

# List of required Python packages
$requiredPackages = @(
    'flask',
    'pillow',
    'torch',
    'diffusers',
    'transformers',
    'accelerate',
    'safetensors'
)

# Function to check if a Python package is installed in venv
function Test-PythonPackage {
    param([string]$package)
    $result = & $venvPython -c "import $package" 2>$null
    return $LASTEXITCODE -eq 0
}

# Check and install missing packages in venv
$missingPackages = @()
foreach ($pkg in $requiredPackages) {
    if (-not (Test-PythonPackage $pkg)) {
        $missingPackages += $pkg
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "Installing missing Python packages in venv: $($missingPackages -join ', ')"
    & $venvPip install $missingPackages
} else {
    Write-Host "✅ All required Python packages are already installed in venv."
}

Write-Host 'Download the DreamShaper model from CivitAI:'
Write-Host 'https://civitai.com/models/4384/dreamshaper'
Write-Host 'Place the .safetensors or .ckpt file in the Image Generator folder.'
Write-Host 'If using safetensors, use the safetensors file path in your app.'

# Start the Stable Diffusion Web UI
Write-Host ''
Write-Host 'Starting Stable Diffusion Web UI (DreamShaper)...'
Write-Host 'Open http://localhost:5000 in your browser'
Write-Host 'Note: Model loading may take a few minutes on first run'
& $venvPython "Image Generator/app.py"