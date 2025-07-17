# Text-to-Image Generator - AI Art Creator

🎨 **Free • AI-Powered • High Quality • Unlimited**

This is a powerful text-to-image generator that uses state-of-the-art AI models to create stunning images from text descriptions. The application runs locally, ensuring privacy and unlimited usage without restrictions.

## 🎯 Features

✅ **Free to use** - No costs, no subscriptions, no hidden fees  
✅ **AI-Powered** - Uses Stable Diffusion for high-quality image generation  
✅ **Unlimited** - Generate as many images as you want  
✅ **High Quality** - Professional-grade image output  
✅ **Local Processing** - All generation happens on your machine  
✅ **Web Interface** - Modern, intuitive user interface  
✅ **Customizable** - Adjust quality, creativity, and image dimensions  

## 🚀 Quick Start

**Prerequisites:**
- Python 3.8 or higher
- 8GB+ RAM recommended (4GB minimum)
- GPU with CUDA support (optional, but recommended for speed)

**Installation:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

Then open http://localhost:5000 in your browser.

## 🔧 Technical Details

### Architecture
- **Backend**: Flask web server with Diffusers library
- **AI Model**: Stable Diffusion v1.5 (runwayml/stable-diffusion-v1-5)
- **Frontend**: Modern HTML/CSS/JavaScript interface
- **Processing**: 100% local, no external API calls

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 8GB recommended (4GB minimum)
- **Storage**: 5GB free space for model downloads
- **GPU**: CUDA-compatible GPU recommended (optional)
- **OS**: Windows, macOS, or Linux

### AI Model Details
- **Model**: Stable Diffusion v1.5
- **Type**: Text-to-image diffusion model
- **Resolution**: 512x512, 512x768, 768x512
- **Quality**: Adjustable inference steps (10-50)
- **Creativity**: Adjustable guidance scale (1-15)

## 🖥️ Web Interface Features

### Image Generation
- **Text Prompts** - Describe the image you want to create
- **Quality Control** - Adjust inference steps for better quality
- **Creativity Control** - Adjust guidance scale for more/less creative outputs
- **Size Options** - Choose from square, portrait, or landscape formats
- **Real-time Preview** - See your image as it's generated

### User Experience
- **Clean Interface** - Modern, intuitive design
- **Responsive** - Works on desktop, tablet, and mobile
- **Download Support** - Save generated images locally
- **Parameter Controls** - Fine-tune generation settings
- **Error Handling** - User-friendly error messages

## 🎨 Usage Examples

### Basic Image Generation
```
Prompt: "A serene mountain landscape at sunset"
→ Creates a beautiful landscape image
```

### Detailed Descriptions
```
Prompt: "A futuristic cityscape with flying cars, neon lights, cyberpunk style, highly detailed, 4k"
→ Creates a detailed cyberpunk city scene
```

### Artistic Styles
```
Prompt: "A portrait of a cat wearing a top hat, oil painting style"
→ Creates an artistic cat portrait
```

### Creative Concepts
```
Prompt: "A floating island in space with a magical forest, fantasy art"
→ Creates a fantastical space scene
```

## ⚙️ Configuration Options

### Generation Parameters

**Quality (Inference Steps):**
- **10-20**: Fast generation, lower quality
- **20-30**: Balanced speed and quality (recommended)
- **30-50**: High quality, slower generation

**Creativity (Guidance Scale):**
- **1-5**: Very creative, may deviate from prompt
- **5-10**: Balanced creativity and prompt adherence
- **10-15**: Strict prompt following, less creative

**Image Sizes:**
- **512x512**: Square format, fastest generation
- **512x768**: Portrait format
- **768x512**: Landscape format

### Model Configuration
Edit `app.py` to change AI model settings:
```python
# Use different model
model_id = "stabilityai/stable-diffusion-2-1"

# Adjust default parameters
num_inference_steps = 30
guidance_scale = 8.0
```

## 🛠️ Troubleshooting

### Common Issues

**"Model failed to load"**
- Ensure you have sufficient RAM (8GB+ recommended)
- Check internet connection for initial model download
- Try restarting the application

**"CUDA out of memory"**
- Reduce image size to 512x512
- Lower inference steps to 20 or less
- Close other GPU-intensive applications
- Use CPU mode if necessary

**"Slow generation"**
- Enable GPU acceleration with CUDA
- Reduce inference steps
- Use smaller image dimensions
- Close unnecessary applications

**"Import errors"**
- Update pip: `pip install --upgrade pip`
- Install dependencies: `pip install -r requirements.txt`
- Try creating a fresh virtual environment

### Performance Optimization

**For Better Quality:**
- Increase inference steps to 30-50
- Use higher guidance scale (8-12)
- Use GPU with CUDA support
- Use larger image dimensions

**For Faster Generation:**
- Decrease inference steps to 10-20
- Use lower guidance scale (5-7)
- Use 512x512 image size
- Enable attention slicing (already enabled)

## 🔒 Privacy & Security

- **100% Local Processing** - All image generation happens on your machine
- **No Data Collection** - Images and prompts are not stored or transmitted
- **No External APIs** - No data sent to third-party services
- **Session-Only Storage** - Generated images are only kept in browser session
- **Open Source** - Full transparency of all code

## 📚 Tips for Better Results

### Prompt Writing Tips
1. **Be Descriptive** - Include details about style, lighting, mood
2. **Use Style Keywords** - "photorealistic", "oil painting", "digital art"
3. **Specify Quality** - "highly detailed", "4k", "masterpiece"
4. **Include Lighting** - "golden hour", "dramatic lighting", "soft light"
5. **Add Composition** - "close-up", "wide shot", "centered"

### Example Good Prompts
- "A majestic lion in African savanna, golden hour lighting, photorealistic, highly detailed"
- "Steampunk airship flying over Victorian London, intricate gears, brass and copper, digital art"
- "Cozy library with floating books, magical atmosphere, warm lighting, fantasy illustration"

## 🔄 Updates & Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Clearing Model Cache
```bash
# Clear cached models to download fresh versions
rm -rf ~/.cache/huggingface/
rm -rf ~/.cache/torch/
```

## 🤝 Contributing

This project welcomes contributions! Areas for improvement:
- Additional AI model support
- Enhanced UI features
- Performance optimizations
- New generation parameters
- Mobile app development

## 📜 License

This project is open source and available under the MIT License.

---

## 🎉 Start Creating!

Your AI-powered image generator is ready to use! It provides:
- 🎨 **Professional image generation** from text descriptions
- 🚫 **No usage restrictions** or limits
- ⚡ **Local processing** for complete privacy
- 💰 **Completely free** with unlimited generations
- 🌐 **Easy web interface** accessible from any device

**Start generating now:** Run `python app.py` and open http://localhost:5000 to begin creating amazing AI art!
