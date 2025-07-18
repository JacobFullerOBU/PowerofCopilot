#!/usr/bin/env python3
"""
Text-to-Image Web UI - Basic Version for Testing
This version provides the web interface without AI model dependencies
"""

import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import time

app = Flask(__name__)

def create_placeholder_image(prompt):
    """Create a placeholder image with the prompt text (for testing without AI models)"""
    # Create a 512x512 image
    img = Image.new('RGB', (512, 512), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Wrap text
    words = prompt.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] <= 450:  # Keep within image bounds
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw text centered
    y_offset = 200
    for line in lines[:8]:  # Limit to 8 lines
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (512 - text_width) // 2
        draw.text((x, y_offset), line, fill='darkblue', font=font)
        y_offset += 35
    
    # Add a note at the bottom
    note = "Demo Mode - Install AI models for real generation"
    bbox = draw.textbbox((0, 0), note, font=font)
    text_width = bbox[2] - bbox[0]
    x = (512 - text_width) // 2
    draw.text((x, 450), note, fill='red', font=font)
    
    return img

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
    """Check if model is loaded - in demo mode, always return ready"""
    return jsonify({
        'model_loaded': True,
        'device': 'demo',
        'cuda_available': False
    })

@app.route('/generate', methods=['POST'])
def generate():
    """Generate placeholder image from text prompt"""
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    # Simulate generation time
    start_time = time.time()
    time.sleep(2)  # Simulate AI processing time
    
    # Create placeholder image
    image = create_placeholder_image(prompt)
    generation_time = time.time() - start_time
    
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
    print("Starting Text-to-Image Web UI (Demo Mode)...")
    print("Open http://localhost:5000 in your browser")
    print("Note: This is running in demo mode. To enable AI generation,")
    print("install the full requirements: pip install -r requirements.txt")
    
    app.run(debug=True, host='0.0.0.0', port=5000)