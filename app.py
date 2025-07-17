#!/usr/bin/env python3
"""
Text-to-Image Web UI using Stable Diffusion
Optimized for RTX 3060 (12GB VRAM)
"""

import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
import threading
import time

app = Flask(__name__)

# Global variables for the model
pipeline = None
model_loaded = False
loading_lock = threading.Lock()

def load_model():
    """Load the Stable Diffusion model optimized for RTX 3060"""
    global pipeline, model_loaded
    
    with loading_lock:
        if model_loaded:
            return
            
        print("Loading Stable Diffusion model...")
        
        # Use a smaller, more efficient model for RTX 3060
        model_id = "runwayml/stable-diffusion-v1-5"
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        try:
            # Load with optimizations for RTX 3060 (12GB VRAM)
            pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                use_safetensors=True
            )
            
            if device == "cuda":
                pipeline = pipeline.to(device)
                # Enable memory efficient attention for RTX 3060
                pipeline.enable_attention_slicing()
                pipeline.enable_xformers_memory_efficient_attention()
            
            model_loaded = True
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            model_loaded = False

def generate_image(prompt, negative_prompt="", num_inference_steps=20, guidance_scale=7.5):
    """Generate image from text prompt"""
    global pipeline
    
    if not model_loaded or pipeline is None:
        return None, "Model not loaded"
    
    try:
        # Generate image with optimized settings for RTX 3060
        with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
            image = pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=512,  # Optimal for RTX 3060
                width=512,   # Optimal for RTX 3060
            ).images[0]
        
        return image, None
        
    except Exception as e:
        return None, f"Error generating image: {str(e)}"

def image_to_base64(image):
    """Convert PIL image to base64 string for web display"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    """Main page with text-to-image form"""
    return render_template('index.html')

@app.route('/status')
def status():
    """Check if model is loaded"""
    return jsonify({
        'model_loaded': model_loaded,
        'device': 'cuda' if torch.cuda.is_available() else 'cpu',
        'cuda_available': torch.cuda.is_available()
    })

@app.route('/generate', methods=['POST'])
def generate():
    """Generate image from text prompt"""
    if not model_loaded:
        return jsonify({'error': 'Model not loaded yet. Please wait and try again.'}), 503
    
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    negative_prompt = data.get('negative_prompt', '').strip()
    steps = int(data.get('steps', 20))
    guidance = float(data.get('guidance', 7.5))
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    # Generate image
    start_time = time.time()
    image, error = generate_image(prompt, negative_prompt, steps, guidance)
    generation_time = time.time() - start_time
    
    if error:
        return jsonify({'error': error}), 500
    
    # Convert to base64 for web display
    image_data = image_to_base64(image)
    
    return jsonify({
        'image': image_data,
        'prompt': prompt,
        'generation_time': round(generation_time, 2)
    })

@app.route('/spotify')
def spotify_redirect():
    """Redirect to original Spotify functionality"""
    return """
    <h1>Spotify Reader</h1>
    <p>The original Spotify Reader functionality is still available via command line:</p>
    <pre>python spotify_reader.py</pre>
    <p>Or run the demo:</p>
    <pre>python demo.py</pre>
    <p><a href="/">← Back to Text-to-Image Generator</a></p>
    """

if __name__ == '__main__':
    # Start loading the model in a separate thread
    loading_thread = threading.Thread(target=load_model)
    loading_thread.daemon = True
    loading_thread.start()
    
    # Run Flask app
    print("Starting Text-to-Image Web UI...")
    print("Open http://localhost:5000 in your browser")
    print("Note: Model loading may take a few minutes on first run")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
AI Chatbot Web Application
Flask server providing a web interface for the AI chatbot
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from chatbot import get_chatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize chatbot
logger.info("Initializing AI chatbot...")
chatbot = None

def initialize_chatbot():
    """Initialize the chatbot before handling requests"""
    global chatbot
    try:
        chatbot = get_chatbot()
        logger.info("Chatbot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        chatbot = None

# Initialize chatbot on startup
with app.app_context():
    initialize_chatbot()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        # Check if chatbot is available
        if chatbot is None:
            return jsonify({
                'success': False,
                'error': 'Chatbot is not available. Please try again later.'
            }), 503
        
        # Generate response
        logger.info(f"Processing message: {user_message[:50]}...")
        bot_response = chatbot.generate_response(user_message)
        
        # Return response
        return jsonify({
            'success': True,
            'response': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 'An internal error occurred. Please try again.'
        }), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        if chatbot is not None:
            chatbot.clear_history()
            logger.info("Conversation history cleared")
        
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared'
        })
        
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear history'
        }), 500

@app.route('/status')
def status():
    """Get chatbot status"""
    return jsonify({
        'chatbot_loaded': chatbot is not None,
        'model_name': chatbot.model_name if chatbot else None,
        'conversation_length': len(chatbot.get_history()) if chatbot else 0
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
    print("🤖 AI Chatbot Web Server")
    print("=" * 30)
    print("Starting server...")
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
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
