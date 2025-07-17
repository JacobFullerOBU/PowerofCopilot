from flask import Flask, render_template, request, jsonify, send_file, url_for
import os
import uuid
import threading
import time
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'generated_videos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['PREFERRED_URL_SCHEME'] = 'http'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store generation status in memory (in production, use Redis or database)
generation_status = {}

@app.route('/')
def index():
    """Main page with text-to-video interface"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    """Handle video generation request"""
    try:
        data = request.get_json()
        text_prompt = data.get('prompt', '').strip()
        model_name = data.get('model', 'zeroscope')
        duration = int(data.get('duration', 3))
        resolution = data.get('resolution', '512x512')
        
        if not text_prompt:
            return jsonify({'error': 'Text prompt is required'}), 400
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Initialize status
        generation_status[job_id] = {
            'status': 'starting',
            'progress': 0,
            'message': 'Initializing video generation...',
            'created_at': datetime.now().isoformat(),
            'prompt': text_prompt,
            'model': model_name,
            'duration': duration,
            'resolution': resolution
        }
        
        # Start generation in background thread
        thread = threading.Thread(
            target=generate_video_async, 
            args=(job_id, text_prompt, model_name, duration, resolution)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'job_id': job_id, 'status': 'started'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<job_id>')
def get_status(job_id):
    """Get generation status for a job"""
    if job_id not in generation_status:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(generation_status[job_id])

@app.route('/download/<job_id>')
def download_video(job_id):
    """Download generated video"""
    if job_id not in generation_status:
        return jsonify({'error': 'Job not found'}), 404
    
    status = generation_status[job_id]
    if status['status'] != 'completed':
        return jsonify({'error': 'Video not ready'}), 400
    
    video_path = status.get('video_path')
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 404
    
    return send_file(video_path, as_attachment=True, download_name=f'generated_video_{job_id}.mp4')

def generate_video_async(job_id, prompt, model_name, duration, resolution):
    """Generate video asynchronously"""
    with app.app_context():
        try:
            # Update status
            generation_status[job_id].update({
                'status': 'loading_model',
                'progress': 10,
                'message': f'Loading {model_name} model...'
            })
            
            # Import here to avoid blocking app startup
            from video_generator import VideoGenerator
            
            generator = VideoGenerator()
            
            # Update status
            generation_status[job_id].update({
                'status': 'generating',
                'progress': 30,
                'message': 'Generating video from text...'
            })
            
            # Generate video
            video_path = generator.generate(
                prompt=prompt,
                model_name=model_name,
                duration=duration,
                resolution=resolution,
                output_dir=app.config['UPLOAD_FOLDER'],
                job_id=job_id,
                progress_callback=lambda p: update_progress(job_id, p)
            )
            
            # Update final status
            generation_status[job_id].update({
                'status': 'completed',
                'progress': 100,
                'message': 'Video generation completed!',
                'video_path': video_path,
                'download_url': url_for('download_video', job_id=job_id)
            })
            
        except Exception as e:
            generation_status[job_id].update({
                'status': 'error',
                'progress': 0,
                'message': f'Error: {str(e)}'
            })

def update_progress(job_id, progress):
    """Update generation progress"""
    if job_id in generation_status:
        generation_status[job_id]['progress'] = min(30 + int(progress * 0.65), 95)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)