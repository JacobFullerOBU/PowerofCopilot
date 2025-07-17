#!/usr/bin/env python3
"""
Text-to-Image Generator Web Application
Flask server providing a web interface for AI-powered text-to-image generation
"""

import os
import json
import logging
import base64
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize text-to-image model
logger.info("Initializing text-to-image model...")
pipe = None

def initialize_model():
    """Initialize the text-to-image model before handling requests"""
    global pipe
    try:
        # Use a smaller model for faster loading and lower resource usage
        model_id = "runwayml/stable-diffusion-v1-5"
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            use_safetensors=True
        )
        
        # Move to GPU if available
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
        
        # Enable memory efficient attention
        pipe.enable_attention_slicing()
        
        logger.info("Text-to-image model initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        pipe = None

# Initialize model on startup
with app.app_context():
    initialize_model()

@app.route('/')
def index():
    """Serve the main image generation interface"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    """Handle image generation requests"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                'success': False,
                'error': 'No prompt provided'
            }), 400
        
        prompt = data['prompt'].strip()
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Empty prompt'
            }), 400
        
        # Check if model is available
        if pipe is None:
            return jsonify({
                'success': False,
                'error': 'Text-to-image model is not available. Please try again later.'
            }), 503
        
        # Generate image
        logger.info(f"Generating image for prompt: {prompt[:50]}...")
        
        # Set generation parameters
        num_inference_steps = data.get('steps', 20)
        guidance_scale = data.get('guidance_scale', 7.5)
        height = data.get('height', 512)
        width = data.get('width', 512)
        
        # Generate the image
        with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
            image = pipe(
                prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=height,
                width=width
            ).images[0]
        
        # Convert image to base64 for transmission
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Return response
        return jsonify({
            'success': True,
            'image': f"data:image/png;base64,{img_str}",
            'prompt': prompt,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in generate endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 'An internal error occurred. Please try again.'
        }), 500

@app.route('/status')
def status():
    """Get model status"""
    return jsonify({
        'model_loaded': pipe is not None,
        'device': 'cuda' if torch.cuda.is_available() and pipe is not None else 'cpu',
        'model_name': 'runwayml/stable-diffusion-v1-5' if pipe else None
    })

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Page not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

def main():
    """Main function to run the Flask app"""
    print("🎨 Text-to-Image Generator Web Server")
    print("=" * 40)
    print("Starting server...")
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('generated_images', exist_ok=True)
    
    # Run the app
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"❌ Error starting server: {e}")

if __name__ == '__main__':
    main()