@echo off
REM AI Chatbot One-Click Launcher for Windows

echo 🤖 AI Chatbot - One-Click Launcher (Windows)
echo ===============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH.
    echo    Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: pip is not installed.
    echo    Please install pip and try again.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ⚠️  Full dependency install failed, trying basic packages...
    pip install flask --quiet
    if errorlevel 1 (
        echo ❌ Failed to install even basic dependencies
        echo    Please check your internet connection
        pause
        exit /b 1
    )
)

echo ✅ Dependencies installed successfully

REM Kill any existing process on port 5000
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

REM Start the server
echo 🚀 Starting AI Chatbot server...
start "AI Chatbot" python app.py

REM Wait for server to start
echo ⏳ Waiting for server to start...
timeout /t 3 >nul

REM Open browser
echo 🌐 Opening browser...
start http://localhost:5000

echo.
echo 🎉 AI Chatbot is ready!
echo    URL: http://localhost:5000
echo    Features:
echo    • 🆓 Free to use
echo    • 🚫 No limits  
echo    • 🔓 No restrictions
echo    • ⚡ Quick responses
echo    • 🛡️ Local ^& reliable
echo.
echo Press any key to stop the server when done...
pause >nul

REM Try to stop the server
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5000" ^| find "LISTENING"') do taskkill /f /pid %%a >nul 2>&1

echo.
echo 👋 AI Chatbot stopped. Thanks for using!
pause