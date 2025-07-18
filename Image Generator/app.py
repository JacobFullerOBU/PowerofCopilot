#!/usr/bin/env python3
"""
Text-to-Image Web UI using Stable Diffusion
Optimized for RTX 3060 (12GB VRAM)
"""

import os
import io
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline


MODEL_PATH = os.path.join(os.path.dirname(__file__), "dreamshaper_8.safetensors")
pipe = None

def load_model():
    global pipe
    if pipe is not None:
        return
    print("Loading DreamShaper Stable Diffusion model...")
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        if device == "cuda":
            pipe = StableDiffusionPipeline.from_single_file(MODEL_PATH, torch_dtype=torch.float16)
        else:
            pipe = StableDiffusionPipeline.from_single_file(MODEL_PATH, torch_dtype=torch.float32)
        pipe = pipe.to(device)
        print(f"DreamShaper model loaded successfully on {device}!")
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


@app.route('/')
def index():
    return """
    <h1>DreamShaper Text-to-Image Generator</h1>
    <h2>How to Use</h2>
    <ol>
        <li>Enter a descriptive prompt in the box below (e.g., <i>a futuristic cityscape at sunset</i>).</li>
        <li>Click <b>Generate</b> to create an image using the DreamShaper model.</li>
        <li>The generated image will appear below the prompt box.</li>
        <li>To try a new prompt, simply enter new text and click <b>Generate</b> again.</li>
    </ol>
    <div style='color:red; font-weight:bold;'>
        ⚠️ Safety checker is disabled. This app is for private/local use only. Do not expose unfiltered results to the public. See <a href='https://github.com/huggingface/diffusers/pull/254' target='_blank'>license info</a>.
    </div>
    <form method="post" action="/generate" id="genform" onsubmit="return false;">
        <input type="text" name="prompt" placeholder="Enter your prompt" style="width:300px;">
        <button type="button" onclick="generateImage()">Generate</button>
    </form>
    <div id="result"></div>
    <script>
    function generateImage() {
        var prompt = document.querySelector('input[name=\"prompt\"]').value;
        fetch('/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: prompt})
        })
        .then(r => r.json())
        .then(data => {
            if(data.image) {
                document.getElementById('result').innerHTML = '<img src=\"data:image/png;base64,' + data.image + '\" style=\"max-width:512px;\">';
            } else {
                document.getElementById('result').innerText = data.error || 'Error generating image';
            }
        });
    }
    </script>
    """

if __name__ == '__main__':
    print("Starting Stable Diffusion Web UI (DreamShaper)...")
    print("Open http://localhost:5000 in your browser")
    print("Note: Model loading may take a few minutes on first run")
    app.run(debug=True, host='0.0.0.0', port=5000)