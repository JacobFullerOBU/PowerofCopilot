// Text-to-Image Generator Frontend JavaScript

class ImageGeneratorUI {
    constructor() {
        this.promptInput = document.getElementById('prompt-input');
        this.generateButton = document.getElementById('generate-btn');
        this.statusElement = document.getElementById('status');
        this.loadingIndicator = document.getElementById('loading-indicator');
        this.imageResult = document.getElementById('image-result');
        this.placeholder = document.getElementById('placeholder');
        this.generatedImage = document.getElementById('generated-image');
        this.usedPrompt = document.getElementById('used-prompt');
        this.downloadBtn = document.getElementById('download-btn');
        this.newImageBtn = document.getElementById('new-image-btn');
        this.charCountElement = document.getElementById('char-count');
        
        // Control elements
        this.stepsSlider = document.getElementById('steps');
        this.stepsValue = document.getElementById('steps-value');
        this.guidanceSlider = document.getElementById('guidance');
        this.guidanceValue = document.getElementById('guidance-value');
        this.sizeSelect = document.getElementById('size');
        
        this.isGenerating = false;
        this.currentImageData = null;
        
        this.init();
    }
    
    init() {
        console.log('🎨 Initializing Text-to-Image Generator UI');
        
        // Event listeners
        this.generateButton.addEventListener('click', () => this.generateImage());
        this.promptInput.addEventListener('input', () => this.updateCharCount());
        this.promptInput.addEventListener('keydown', (e) => this.handleKeydown(e));
        this.downloadBtn.addEventListener('click', () => this.downloadImage());
        this.newImageBtn.addEventListener('click', () => this.resetForNewImage());
        
        // Control listeners
        this.stepsSlider.addEventListener('input', () => {
            this.stepsValue.textContent = this.stepsSlider.value;
        });
        
        this.guidanceSlider.addEventListener('input', () => {
            this.guidanceValue.textContent = this.guidanceSlider.value;
        });
        
        // Check model status
        this.checkStatus();
        
        // Focus on input
        this.promptInput.focus();
        
        console.log('✅ Image Generator UI initialized');
    }
    
    async checkStatus() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            
            if (data.model_loaded) {
                this.setStatus('ready', '🟢 Model Ready');
                this.generateButton.disabled = false;
            } else {
                this.setStatus('loading', '🟡 Loading Model...');
                this.generateButton.disabled = true;
                // Retry after a delay
                setTimeout(() => this.checkStatus(), 3000);
            }
        } catch (error) {
            console.error('Status check failed:', error);
            this.setStatus('error', '🔴 Model Error');
            this.generateButton.disabled = true;
            // Retry after a longer delay
            setTimeout(() => this.checkStatus(), 5000);
        }
    }
    
    setStatus(type, text) {
        this.statusElement.className = `status ${type}`;
        this.statusElement.textContent = text;
    }
    
    updateCharCount() {
        const count = this.promptInput.value.length;
        this.charCountElement.textContent = count;
        
        if (count > 450) {
            this.charCountElement.style.color = '#e17055';
        } else if (count > 300) {
            this.charCountElement.style.color = '#fdcb6e';
        } else {
            this.charCountElement.style.color = '#666';
        }
    }
    
    handleKeydown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            if (!this.isGenerating && this.promptInput.value.trim()) {
                this.generateImage();
            }
        }
    }
    
    async generateImage() {
        const prompt = this.promptInput.value.trim();
        
        if (!prompt) {
            this.showError('Please enter a prompt for image generation');
            return;
        }
        
        if (this.isGenerating) {
            return;
        }
        
        this.isGenerating = true;
        this.updateGeneratingState(true);
        
        try {
            // Get parameters
            const steps = parseInt(this.stepsSlider.value);
            const guidanceScale = parseFloat(this.guidanceSlider.value);
            const [width, height] = this.sizeSelect.value.split('x').map(x => parseInt(x));
            
            const requestData = {
                prompt: prompt,
                steps: steps,
                guidance_scale: guidanceScale,
                width: width,
                height: height
            };
            
            console.log('🎨 Generating image with prompt:', prompt);
            
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayGeneratedImage(data.image, data.prompt);
                console.log('✅ Image generated successfully');
            } else {
                this.showError(data.error || 'Failed to generate image');
            }
            
        } catch (error) {
            console.error('Generation error:', error);
            this.showError('Network error occurred. Please try again.');
        } finally {
            this.isGenerating = false;
            this.updateGeneratingState(false);
        }
    }
    
    updateGeneratingState(generating) {
        const btnText = this.generateButton.querySelector('.btn-text');
        const btnLoading = this.generateButton.querySelector('.btn-loading');
        
        if (generating) {
            this.generateButton.disabled = true;
            btnText.style.display = 'none';
            btnLoading.style.display = 'inline';
            
            this.placeholder.style.display = 'none';
            this.imageResult.style.display = 'none';
            this.loadingIndicator.style.display = 'flex';
        } else {
            this.generateButton.disabled = false;
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            
            this.loadingIndicator.style.display = 'none';
        }
    }
    
    displayGeneratedImage(imageData, prompt) {
        this.currentImageData = imageData;
        
        this.generatedImage.src = imageData;
        this.usedPrompt.textContent = `"${prompt}"`;
        
        this.placeholder.style.display = 'none';
        this.loadingIndicator.style.display = 'none';
        this.imageResult.style.display = 'block';
    }
    
    downloadImage() {
        if (!this.currentImageData) {
            return;
        }
        
        const link = document.createElement('a');
        link.href = this.currentImageData;
        link.download = `generated-image-${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log('📥 Image downloaded');
    }
    
    resetForNewImage() {
        this.imageResult.style.display = 'none';
        this.placeholder.style.display = 'flex';
        this.currentImageData = null;
        this.promptInput.focus();
    }
    
    showError(message) {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #e17055;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 300px;
            font-size: 0.9em;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
        
        // Allow manual dismissal
        errorDiv.addEventListener('click', () => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        });
        
        console.error('❌ Error:', message);
    }
}

// Initialize the UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ImageGeneratorUI();
});