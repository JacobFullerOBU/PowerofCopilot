# PowerofCopilot - AI Chatbot

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

### AI Model Selection
Edit `chatbot.py` to change the AI model:
```python
# In AIChatbot.__init__()
model_name = "microsoft/DialoGPT-large"  # For better responses (more RAM needed)
model_name = "microsoft/DialoGPT-small"  # For lower resource usage
```

### Server Settings
Edit `app.py` to modify server configuration:
```python
# Change port
app.run(port=8080)

# Enable debug mode
app.run(debug=True)

# Bind to specific interface
app.run(host='127.0.0.1')
```

### Response Settings
Modify response generation in `chatbot.py`:
```python
# Adjust creativity/randomness
temperature=0.8  # Higher = more creative (0.1-2.0)

# Change response length
max_length=input_ids.shape[1] + 100  # Longer responses
```

## 🛠️ Troubleshooting

### Common Issues

**"Model failed to load"**
- Ensure you have sufficient RAM (4GB+)
- Try the smaller model: `DialoGPT-small`
- Check internet connection for initial model download

**"Server won't start"**
- Check if port 5000 is already in use
- Try running with different port: `python app.py --port 8080`
- Ensure all dependencies are installed

**"Slow responses"**
- Upgrade to DialoGPT-large if you have 8GB+ RAM
- Close other applications to free up memory
- Consider using GPU acceleration (install PyTorch with CUDA)

**"Import errors"**
- Update pip: `pip install --upgrade pip`
- Install dependencies: `pip install -r requirements.txt`
- Try creating fresh virtual environment

### Performance Optimization

**For Better Performance:**
- Use GPU acceleration (install `torch` with CUDA support)
- Increase RAM allocation to Python process
- Use SSD storage for faster model loading

**For Lower Resource Usage:**
- Switch to `DialoGPT-small` model
- Reduce conversation history length
- Close unnecessary browser tabs

## 📚 Usage Examples

### Basic Conversation
```
You: Hello! How are you today?
AI: Hello! I'm doing well, thank you for asking. I'm here and ready to help with any questions or just have a friendly conversation. How are you doing today?
```

### Creative Writing
```
You: Write a short story about a robot learning to paint
AI: In a cluttered workshop, ARIA-7 discovered an abandoned paintbrush among the spare parts. With mechanical precision, she dipped it in crimson paint, but her first stroke was rigid, calculated. Days passed as she observed human art online, learning that beauty emerged from imperfection. Soon, her canvases bloomed with unexpected colors, each brushstroke carrying a spark of digital soul that surprised even her creators.
```

### Technical Q&A
```
You: Explain quantum computing in simple terms
AI: Quantum computing is like having a super-powered computer that can explore many possibilities simultaneously. While traditional computers use bits that are either 0 or 1, quantum computers use "qubits" that can be both 0 and 1 at the same time. This allows them to solve certain complex problems much faster than regular computers, especially in areas like cryptography, drug discovery, and optimization problems.
```

## 🔄 Updates & Maintenance

### Updating the AI Model
```bash
# Clear model cache to download latest version
rm -rf ~/.cache/huggingface/transformers/

# Restart the application
python app.py
```

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Backup & Restore
No backup needed - the system is stateless and doesn't store user data.

## 🤝 Contributing

This project welcomes contributions! Areas for improvement:
- Additional AI model support
- Enhanced UI features
- Performance optimizations
- Mobile app development
- Additional language support

## 📜 License

This project is open source and available under the MIT License.

## 🎵 Additional Tools

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
