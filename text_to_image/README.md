# Text-to-Image Generator

🎨 **AI-Powered • High-Quality • Multiple Models • Fast Generation**

This module provides advanced text-to-image generation capabilities using state-of-the-art AI models. Generate stunning images from text descriptions with various artistic styles and customization options.

## 🎯 Features

✅ **Multiple AI Models** - Support for Stable Diffusion, DALL-E style models  
✅ **High Resolution** - Generate images up to 1024x1024 resolution  
✅ **Style Control** - Choose from various artistic styles and presets  
✅ **Batch Generation** - Create multiple variations of the same prompt  
✅ **Custom Parameters** - Fine-tune generation settings  
✅ **Local Processing** - Run models locally for privacy  
✅ **Web Interface** - Easy-to-use browser-based interface  

## 🚀 Quick Start

**Prerequisites:**
- Python 3.8 or higher
- 8GB+ RAM recommended
- GPU with 4GB+ VRAM (optional, for faster generation)

**Installation:**
```bash
# Navigate to text-to-image directory
cd text_to_image/

# Install dependencies
pip install -r requirements.txt

# Start the image generator
python image_generator.py
```

Then open http://localhost:5001 in your browser.

## 🔧 Technical Details

### Supported Models
- **Stable Diffusion v1.5** - Versatile, high-quality generation
- **Stable Diffusion v2.1** - Improved composition and details
- **Custom Fine-tuned Models** - Specialized artistic styles

### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for model downloads
- **GPU**: Optional but recommended (RTX 3060+ or equivalent)
- **OS**: Windows, macOS, or Linux

### Generation Parameters
- **Prompt**: Text description of desired image
- **Negative Prompt**: What to avoid in the image
- **Steps**: Number of denoising steps (20-50 recommended)
- **CFG Scale**: How closely to follow the prompt (7-15 recommended)
- **Seed**: For reproducible results
- **Dimensions**: Width and height (512x512 to 1024x1024)

## 🎨 Usage Examples

### Basic Image Generation
```
Prompt: "A majestic lion sitting on a rocky cliff at sunset, digital art"
Negative: "blurry, low quality, distorted"
Steps: 30
CFG Scale: 7.5
```

### Artistic Styles
```
Prompt: "A cyberpunk cityscape with neon lights, in the style of blade runner"
Style: Cyberpunk
Resolution: 768x768
```

### Portrait Generation
```
Prompt: "Professional headshot of a business person, studio lighting, sharp focus"
Style: Photography
CFG Scale: 12
Steps: 40
```

## ⚙️ Configuration

### Model Selection
Edit `config.py` to change the default model:
```python
DEFAULT_MODEL = "stable-diffusion-v1-5"
# Options: "stable-diffusion-v1-5", "stable-diffusion-v2-1"
```

### Performance Settings
```python
# Enable GPU acceleration
USE_GPU = True

# Memory optimization
ENABLE_MEMORY_EFFICIENT_ATTENTION = True
USE_CPU_OFFLOAD = False  # Set to True for low VRAM GPUs
```

### Generation Defaults
```python
DEFAULT_STEPS = 30
DEFAULT_CFG_SCALE = 7.5
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
```

## 🖥️ Web Interface Features

### Image Generation
- **Real-time preview** of generation progress
- **Parameter controls** with sliders and inputs
- **Prompt suggestions** and templates
- **Style presets** for different artistic looks
- **Batch generation** for multiple variations

### Gallery & Management
- **Image gallery** with generated results
- **Download options** in multiple formats
- **Metadata preservation** with generation parameters
- **Favorites system** for best results
- **Search and filter** through generated images

## 🛠️ Troubleshooting

### Common Issues

**"Out of memory" errors**
- Reduce image resolution to 512x512
- Enable CPU offload: `USE_CPU_OFFLOAD = True`
- Close other applications to free up memory
- Use fewer denoising steps (20-25)

**Slow generation times**
- Install CUDA-enabled PyTorch for GPU acceleration
- Use lower resolution for testing
- Reduce number of steps to 20-25
- Enable memory efficient attention

**Poor image quality**
- Increase number of steps to 40-50
- Adjust CFG scale (try 10-15 for more prompt adherence)
- Use better prompts with specific details
- Try different seeds for variations

**Model download failures**
- Check internet connection
- Ensure sufficient disk space (10GB+)
- Try downloading models manually
- Check firewall settings

## 📁 Project Structure

```
text_to_image/
├── image_generator.py      # Main generation script
├── web_interface.py        # Flask web server
├── models/                 # AI model storage
│   ├── stable-diffusion/   # Stable Diffusion models
│   └── custom/            # Custom fine-tuned models
├── config.py              # Configuration settings
├── utils/                 # Utility functions
│   ├── image_utils.py     # Image processing
│   └── model_utils.py     # Model management
├── templates/             # Web interface templates
│   ├── index.html         # Main interface
│   └── gallery.html       # Image gallery
├── static/                # Web assets
│   ├── css/              # Styling
│   ├── js/               # Frontend logic
│   └── generated/        # Generated images
└── requirements.txt       # Python dependencies
```

## 🔒 Privacy & Ethics

- **Local Processing** - All generation happens on your machine
- **No Data Collection** - Prompts and images are not transmitted
- **Content Filtering** - Built-in NSFW detection (can be disabled)
- **Responsible Use** - Please use ethically and respect copyright
- **Model Licensing** - Check individual model licenses for usage rights

## 📚 Advanced Features

### Custom Model Training
```bash
# Fine-tune on custom dataset
python train_custom_model.py --dataset path/to/images --epochs 100
```

### API Integration
```python
from image_generator import TextToImageGenerator

generator = TextToImageGenerator(model="stable-diffusion-v1-5")
image = generator.generate("A beautiful landscape", steps=30)
image.save("output.png")
```

### Batch Processing
```bash
# Generate from prompt file
python batch_generate.py --prompts prompts.txt --output_dir results/
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional model support (DALL-E 3, Midjourney alternatives)
- Advanced controlnets and conditioning
- Mobile app development
- Performance optimizations
- New artistic styles and presets

## 📜 License

This project is open source and available under the MIT License. Please respect individual model licenses.

---

## 🎉 Start Creating!

Your text-to-image generator is ready! Create amazing AI art with:
- 🎨 **Professional quality** image generation
- ⚡ **Fast local processing** for privacy  
- 🎯 **Precise control** over output style
- 💰 **Completely free** with no usage limits
- 🌐 **Easy web interface** for all skill levels

**Start generating:** Run `python image_generator.py` and create your first AI masterpiece!