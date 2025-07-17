

## 🎨 Text-to-Image Generator

A powerful web-based AI image generator that creates stunning images from text descriptions using state-of-the-art Stable Diffusion technology. Optimized for RTX 3060 (12GB VRAM) but works on any compatible hardware.

### Features

- 🖼️ **High-Quality Image Generation**: Creates 512x512 images using Stable Diffusion v1.5
- 🎯 **Advanced Controls**: Customize inference steps, guidance scale, and negative prompts
- ⚡ **Hardware Optimized**: Optimized for RTX 3060 with memory-efficient attention
- 🌐 **Web Interface**: Clean, responsive web UI accessible from any browser
- 🔒 **NSFW Support**: No content restrictions (use responsibly)
- 💾 **Instant Results**: Images displayed directly in the browser

### Quick Start

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Web UI**:
```bash
python app.py
```

3. **Open Your Browser**:
Navigate to `http://localhost:5000`

4. **Generate Images**:
- Enter your creative prompt
- Optionally adjust advanced settings
- Click "Generate Image" and wait 30-60 seconds

### Advanced Usage

The web interface includes advanced options for fine-tuning your generations:

- **Negative Prompt**: Specify what you don't want in the image
- **Inference Steps**: Higher values (20-50) = better quality but slower generation
- **Guidance Scale**: How closely the AI follows your prompt (1-20)

### Hardware Requirements

- **Minimum**: Any CUDA-compatible GPU or CPU (slower)
- **Recommended**: RTX 3060 (12GB VRAM) or better
- **RAM**: 8GB+ (16GB+ recommended)
- **Storage**: 5GB+ for model cache

### Demo Mode

For testing without installing AI models, use:
```bash
python app_demo.py
```

This runs a demo version that generates placeholder images with your prompt text.

---

## Spotify Reader
🤖 **Free • Unlimited • No Restrictions • Fast • Reliable**

This repository contains a fully-featured AI chatbot that meets all modern requirements for unrestricted AI interaction. The chatbot runs locally, ensuring privacy and unlimited usage without content filtering.

## 🎯 Features

✅ **Free to use** - No costs, no subscriptions, no hidden fees  
✅ **No limits** - Unlimited conversations and message length  
✅ **No restrictions** - NSFW content allowed, no censorship  
✅ **Quick** - Fast local AI processing with optimized models  
✅ **Reliable** - Stable local hosting, no external dependencies  
✅ **Web UI** - Modern, responsive chat interface  
✅ **One-click start** - Automated setup and launch script  

## 🚀 Quick Start (One-Click Launch)

**Option 1: Automated Script (Recommended)**
```bash
./start_chatbot.sh
```
This script will:
- Install all dependencies automatically
- Set up the virtual environment
- Start the web server
- Open your browser to the chat interface

**Option 2: Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Start the chatbot
python app.py
```
Then open http://localhost:5000 in your browser.

## 🔧 Technical Details

### Architecture
- **Backend**: Flask web server with HuggingFace Transformers
- **AI Model**: Microsoft DialoGPT (conversational AI)
- **Frontend**: Modern HTML/CSS/JavaScript chat interface
- **Processing**: 100% local, no external API calls

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for model downloads
- **OS**: Windows, macOS, or Linux

### AI Model Details
- **Primary Model**: Microsoft DialoGPT-medium
- **Fallback**: DialoGPT-small (if hardware limited)
- **Type**: Generative conversational AI
- **Training**: Large-scale internet conversations
- **Capabilities**: Open-domain dialogue, creative writing, Q&A

## 📁 Project Structure

```
PowerofCopilot/
├── 🤖 AI Chatbot Files
│   ├── chatbot.py          # AI model backend
│   ├── app.py              # Flask web server
│   ├── start_chatbot.sh    # One-click launcher
│   ├── templates/
│   │   └── index.html      # Chat interface
│   └── static/
│       ├── style.css       # UI styling
│       ├── script.js       # Frontend logic
│       └── favicon.ico     # Browser icon
│
├── 🎵 Spotify Reader (Original)
│   ├── spotify_reader.py   # Spotify analysis tool
│   ├── demo.py            # Demo data
│   ├── run.sh             # Spotify launcher
│   └── .env.example       # Spotify config
│
└── 📄 Documentation
    ├── README.md          # This file
    ├── requirements.txt   # Python dependencies
    └── .gitignore        # Git exclusions
```

## 🖥️ Web Interface Features

### Chat Interface
- **Real-time messaging** with instant AI responses
- **Message history** maintained during session
- **Auto-scrolling** to latest messages
- **Typing indicators** for AI processing
- **Character counter** for message length tracking
- **Mobile responsive** design

### User Experience
- **Clean, modern UI** with gradient backgrounds
- **Accessible design** with proper contrast and typography
- **Keyboard shortcuts** (Enter to send, Shift+Enter for new line)
- **Clear conversation** button to reset history
- **Status indicators** showing AI availability

### Technical Features
- **Auto-resize text area** that grows with content
- **Error handling** with user-friendly messages
- **Loading states** with animated indicators
- **Responsive design** for all screen sizes

## 🔒 Privacy & Security

- **100% Local Processing** - All AI computations happen on your machine
- **No Data Collection** - Conversations are not stored or transmitted
- **No External APIs** - No data sent to third-party services
- **Session-Only Memory** - Chat history cleared when browser closed
- **Open Source** - Full transparency of all code

## 🎛️ Configuration Options

This repository also includes a **Spotify Reader** tool for analyzing your music listening habits:

### Spotify Reader Features
- **Top 10 songs of all time** based on long-term listening patterns
- **Top 10 artists of all time** with genre and popularity data
- **User profile information** display
- **Secure OAuth 2.0** authentication with Spotify API

### Spotify Setup
1. Get Spotify API credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Copy `.env.example` to `.env` and add your credentials
3. Run: `./run.sh` or `python spotify_reader.py`

---

## 🎉 Enjoy Your AI Chatbot!

Your AI chatbot is now ready to use! It provides:
- 🤖 **Intelligent conversations** on any topic
- 🚫 **No content restrictions** or censorship
- ⚡ **Fast local processing** for privacy
- 💰 **Completely free** with no limits
- 🌐 **Easy web interface** accessible from any device

**Start chatting now:** Run `./start_chatbot.sh` and enjoy unlimited AI conversations!
