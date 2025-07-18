#!/usr/bin/env python3
"""
Text-to-Image Web UI using Stable Diffusion
Optimized for RTX 3060 (12GB VRAM)
"""

import os
import io
import base64
from flask import Flask, request, jsonify
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline


# Path to DreamShaper model (update filename as needed)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "dreamshaper.safetensors")
pipe = None

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

@app.route('/status')
def status():
    """Check if model is loaded"""
    return jsonify({
        'model_loaded': pipe is not None,
        'device': 'cuda' if torch.cuda.is_available() else 'cpu',
        'cuda_available': torch.cuda.is_available()
    })

@app.route('/spotify')
def spotify_redirect():
    return "<h1>Spotify Reader</h1><p>Original functionality available via command line.</p>"

if __name__ == '__main__':
    print("Starting Stable Diffusion Web UI (DreamShaper)...")
    print("Open http://localhost:5000 in your browser")
    print("Note: Model loading may take a few minutes on first run")
    app.run(debug=True, host='0.0.0.0', port=5000)