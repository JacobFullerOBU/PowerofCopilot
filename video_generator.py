import torch
import os
import time
from diffusers import DiffusionPipeline
from huggingface_hub import hf_hub_download
import cv2
import numpy as np
from PIL import Image
import uuid

class VideoGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models = {}
        
    def get_available_models(self):
        """Return list of available text-to-video models"""
        return {
            'zeroscope': {
                'name': 'Zeroscope v2 576w',
                'description': 'High quality text-to-video model, good for general content',
                'max_duration': 6,
                'resolutions': ['576x320', '1024x576']
            },
            'modelscope': {
                'name': 'ModelScope Text-to-Video',
                'description': 'Fast text-to-video generation with good quality',
                'max_duration': 5,
                'resolutions': ['256x256', '512x512']
            }
        }
    
    def load_model(self, model_name):
        """Load specified model"""
        if model_name in self.models:
            return self.models[model_name]
        
        try:
            if model_name == 'zeroscope':
                # Load Zeroscope model
                pipe = DiffusionPipeline.from_pretrained(
                    "cerspense/zeroscope_v2_576w", 
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
            elif model_name == 'modelscope':
                # Load ModelScope model
                pipe = DiffusionPipeline.from_pretrained(
                    "damo-vilab/text-to-video-ms-1.7b",
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    variant="fp16" if self.device == "cuda" else None
                )
            else:
                raise ValueError(f"Unknown model: {model_name}")
            
            pipe = pipe.to(self.device)
            
            # Enable memory efficient attention if available
            if hasattr(pipe, 'enable_xformers_memory_efficient_attention'):
                try:
                    pipe.enable_xformers_memory_efficient_attention()
                except:
                    pass
            
            # Enable CPU offload for CUDA to save memory
            if self.device == "cuda":
                pipe.enable_sequential_cpu_offload()
            
            self.models[model_name] = pipe
            return pipe
            
        except Exception as e:
            raise Exception(f"Failed to load model {model_name}: {str(e)}")
    
    def generate(self, prompt, model_name='zeroscope', duration=3, resolution='512x512', 
                output_dir='generated_videos', job_id=None, progress_callback=None):
        """Generate video from text prompt"""
        
        try:
            # Load model
            pipe = self.load_model(model_name)
            
            if progress_callback:
                progress_callback(0.1)
            
            # Parse resolution
            width, height = map(int, resolution.split('x'))
            
            # Calculate number of frames based on duration (assuming 8 fps)
            num_frames = min(duration * 8, 48)  # Cap at 48 frames
            
            if progress_callback:
                progress_callback(0.2)
            
            # Generate video
            if model_name == 'zeroscope':
                video_frames = pipe(
                    prompt=prompt,
                    num_frames=num_frames,
                    height=height,
                    width=width,
                    num_inference_steps=20,
                    guidance_scale=15.0,
                    negative_prompt="blurry, low quality, distorted"
                ).frames[0]
            else:  # modelscope
                video_frames = pipe(
                    prompt=prompt,
                    num_frames=num_frames,
                    height=height,
                    width=width,
                    num_inference_steps=25
                ).frames[0]
            
            if progress_callback:
                progress_callback(0.8)
            
            # Save video
            job_id = job_id or str(uuid.uuid4())
            output_path = os.path.join(output_dir, f"video_{job_id}.mp4")
            
            self._save_video(video_frames, output_path, fps=8)
            
            if progress_callback:
                progress_callback(1.0)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Video generation failed: {str(e)}")
    
    def _save_video(self, frames, output_path, fps=8):
        """Save frames as MP4 video"""
        if not frames:
            raise ValueError("No frames to save")
        
        # Convert PIL Images to numpy arrays if needed
        if hasattr(frames[0], 'size'):  # PIL Image
            frames = [np.array(frame) for frame in frames]
        
        # Get dimensions
        height, width = frames[0].shape[:2]
        
        # Define codec and create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        try:
            for frame in frames:
                # Convert RGB to BGR for OpenCV
                if len(frame.shape) == 3 and frame.shape[2] == 3:
                    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                else:
                    frame_bgr = frame
                out.write(frame_bgr)
        finally:
            out.release()
        
        # Verify file was created
        if not os.path.exists(output_path):
            raise Exception("Failed to save video file")
    
    def cleanup_old_videos(self, output_dir, max_age_hours=24):
        """Remove old generated videos to save space"""
        try:
            current_time = time.time()
            for filename in os.listdir(output_dir):
                if filename.startswith('video_') and filename.endswith('.mp4'):
                    file_path = os.path.join(output_dir, filename)
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_hours * 3600:  # Convert hours to seconds
                        os.remove(file_path)
        except Exception:
            pass  # Ignore cleanup errors