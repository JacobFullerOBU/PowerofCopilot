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
import dnnlib
import pickle
import threading
import time

app = Flask(__name__)


# Global variables for StyleGAN2
G = None
model_loaded = False
loading_lock = threading.Lock()

def load_model():
    """Load the StyleGAN2 model (.pkl)"""
    global G, model_loaded
    with loading_lock:
        if model_loaded:
            return
        print("Loading StyleGAN2 model...")
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        try:
            # Path to your pre-trained StyleGAN2 model
            model_path = "stylegan2-ffhq-config-f.pkl"  # Change to your .pkl file
            with open(model_path, 'rb') as f:
                G = pickle.load(f)['G_ema'].to(device)
            model_loaded = True
            print("StyleGAN2 model loaded successfully!")
        except Exception as e:
            print(f"Error loading StyleGAN2 model: {e}")
            model_loaded = False

def generate_image(seed=None):
    """Generate image from random latent vector using StyleGAN2"""
    global G
    if not model_loaded or G is None:
        return None, "Model not loaded"
    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        # Set random seed for reproducibility
        if seed is not None:
            torch.manual_seed(seed)
        # Generate random latent vector
        z = torch.randn([1, G.z_dim], device=device)
        label = torch.zeros([1, G.c_dim], device=device)
        img = G(z, label, truncation_psi=0.7, noise_mode='const')
        # Convert to PIL Image
        img = (img.clamp(-1,1)+1)/2
        img = img.mul(255).add_(0.5).clamp(0,255).to(torch.uint8)
        img = img[0].permute(1,2,0).cpu().numpy()
        pil_img = Image.fromarray(img, 'RGB')
        return pil_img, None
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
    """Generate image from StyleGAN2 latent vector (optionally with seed)"""
    if not model_loaded:
        return jsonify({'error': 'Model not loaded yet. Please wait and try again.'}), 503
    data = request.get_json()
    seed = data.get('seed', None)
    if seed is not None:
        try:
            seed = int(seed)
        except:
            seed = None
    start_time = time.time()
    image, error = generate_image(seed)
    generation_time = time.time() - start_time
    if error:
        return jsonify({'error': error}), 500
    image_data = image_to_base64(image)
    return jsonify({
        'image': image_data,
        'seed': seed,
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
    # Start loading the StyleGAN2 model in a separate thread
    loading_thread = threading.Thread(target=load_model)
    loading_thread.daemon = True
    loading_thread.start()
    # Run Flask app
    print("Starting StyleGAN2 Web UI...")
    print("Open http://localhost:5000 in your browser")
    print("Note: Model loading may take a few minutes on first run")
    app.run(debug=True, host='0.0.0.0', port=5000)