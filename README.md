# Text to Video Generator - AI Powered

This is a completely free text-to-video generation web application that transforms your text descriptions into stunning videos using state-of-the-art AI models. Developed entirely by GitHub Copilot.

## ✨ Features

- 🆓 **100% Free** - No API keys or subscriptions required
- 🚫 **No Restrictions** - Generate unlimited videos
- 🧠 **Multiple AI Models** - Choose from Zeroscope v2 and ModelScope
- 🎥 **High Quality Output** - Up to 1024x576 resolution
- 📥 **Downloadable Videos** - Save videos in MP4 format
- ⚙️ **Customizable** - Control duration, resolution, and model selection
- 🎨 **Modern UI** - Beautiful, responsive web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (recommended for faster generation)
- At least 8GB RAM (16GB+ recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JacobFullerOBU/PowerofCopilot.git
   cd PowerofCopilot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎬 How to Use

1. **Enter your prompt** - Describe the video you want to generate in detail
2. **Choose settings**:
   - **Model**: Select between Zeroscope (high quality) or ModelScope (fast)
   - **Duration**: Choose 2-6 seconds
   - **Resolution**: Pick from 256x256 to 1024x576
3. **Generate** - Click the generate button and wait for processing
4. **Download** - Save your generated video when ready

### Example Prompts

- "A majestic eagle soaring over snow-capped mountains at sunrise"
- "Ocean waves crashing against rocky cliffs under a stormy sky"
- "A futuristic city with flying cars and neon lights at night"
- "A peaceful forest stream with sunlight filtering through trees"

## 🛠️ Available Models

### Zeroscope v2 576w
- **Quality**: High
- **Speed**: Slower
- **Best for**: Detailed, high-quality videos
- **Max Resolution**: 1024x576
- **Recommended Duration**: 3-4 seconds

### ModelScope Text-to-Video
- **Quality**: Good
- **Speed**: Faster
- **Best for**: Quick generation, testing ideas
- **Max Resolution**: 512x512
- **Recommended Duration**: 2-3 seconds

## ⚡ Performance Tips

- **GPU Usage**: The app automatically uses CUDA if available
- **Memory**: Higher resolutions require more VRAM
- **Generation Time**: Expect 2-5 minutes per video depending on settings
- **Quality vs Speed**: Use Zeroscope for best quality, ModelScope for speed

## 🔧 Configuration

### Environment Variables

You can customize the application by setting these environment variables:

```bash
export FLASK_ENV=production        # Set to 'development' for debug mode
export MAX_DURATION=10            # Maximum video duration in seconds
export CLEANUP_HOURS=24           # Hours before auto-deleting old videos
```

### Advanced Settings

Edit `app.py` to modify:
- Upload folder location
- Maximum file sizes
- Cleanup schedules

## 📁 Project Structure

```
PowerofCopilot/
├── app.py                 # Flask web application
├── video_generator.py     # AI model integration
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend logic
└── generated_videos/     # Output directory (auto-created)
```

## 🐛 Troubleshooting

### Common Issues

**"CUDA out of memory"**
- Reduce resolution or duration
- Close other GPU-intensive applications
- Use CPU mode by setting `device = "cpu"` in video_generator.py

**"Model loading failed"**
- Check internet connection (models download on first use)
- Ensure sufficient disk space (models are ~4GB each)
- Try restarting the application

**"Video generation timeout"**
- Increase timeout values in the code
- Check system resources
- Try shorter duration or lower resolution

### Performance Issues

**Slow generation on CPU**
- This is expected - GPU acceleration is highly recommended
- Consider using cloud services with GPU support
- Try ModelScope model for faster generation

## 🤝 Contributing

This project was developed entirely by GitHub Copilot, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Hugging Face** - For providing free access to AI models
- **Zeroscope** - For the high-quality text-to-video model
- **ModelScope** - For the fast text-to-video model
- **GitHub Copilot** - For developing this entire application

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information

---

**Happy video generating! 🎬✨**
