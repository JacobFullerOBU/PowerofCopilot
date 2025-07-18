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
from flask import Flask, render_template, request, jsonify
from PIL import Image

        if model_loaded:
            return
        print("Loading StyleGAN2 model...")
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
pipe = None
            with open(model_path, 'rb') as f:
def load_model():
    global pipe
    if pipe is not None:
        return
    print("Loading DreamShaper Stable Diffusion model...")
    try:
        pipe = StableDiffusionPipeline.from_single_file(MODEL_PATH, torch_dtype=torch.float16)
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        print("DreamShaper model loaded successfully!")
    except Exception as e:
        print(f"Error loading DreamShaper model: {e}")
        pipe = None
        z = torch.randn([1, G.z_dim], device=device)
def generate_image(prompt):
    global pipe
    if pipe is None:
        return None, "Model not loaded"
    try:
        result = pipe(prompt, num_inference_steps=30)
        img = result.images[0]
        return img, None
    except Exception as e:
        return None, str(e)

@app.route('/generate', methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    load_model()
    img, error = generate_image(prompt)
    if img is None:
        return jsonify({"error": error}), 500
    # Convert image to base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return jsonify({"image": img_str})
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