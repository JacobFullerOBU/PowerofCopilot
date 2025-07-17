// Global variables
let currentJobId = null;
let statusInterval = null;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateCharacterCount();
    updateTimeEstimate();
});

function initializeEventListeners() {
    // Character counter
    const promptTextarea = document.getElementById('prompt');
    promptTextarea.addEventListener('input', updateCharacterCount);
    
    // Time estimate updates
    const durationSelect = document.getElementById('duration');
    const resolutionSelect = document.getElementById('resolution');
    const modelSelect = document.getElementById('model');
    
    durationSelect.addEventListener('change', updateTimeEstimate);
    resolutionSelect.addEventListener('change', updateTimeEstimate);
    modelSelect.addEventListener('change', updateTimeEstimate);
    
    // Enter key handling
    promptTextarea.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            generateVideo();
        }
    });
}

function updateCharacterCount() {
    const promptTextarea = document.getElementById('prompt');
    const charCount = document.getElementById('char-count');
    const currentLength = promptTextarea.value.length;
    
    charCount.textContent = currentLength;
    
    // Color coding for character limit
    if (currentLength > 450) {
        charCount.style.color = '#dc3545';
    } else if (currentLength > 350) {
        charCount.style.color = '#ffc107';
    } else {
        charCount.style.color = '#28a745';
    }
}

function updateTimeEstimate() {
    const duration = parseInt(document.getElementById('duration').value);
    const resolution = document.getElementById('resolution').value;
    const model = document.getElementById('model').value;
    
    let baseTime = 120; // 2 minutes base
    
    // Adjust for duration
    baseTime += duration * 30;
    
    // Adjust for resolution
    if (resolution.includes('1024')) {
        baseTime += 120;
    } else if (resolution.includes('576')) {
        baseTime += 60;
    }
    
    // Adjust for model
    if (model === 'zeroscope') {
        baseTime += 60;
    }
    
    const minTime = Math.floor(baseTime / 60);
    const maxTime = Math.floor(baseTime * 1.5 / 60);
    
    document.getElementById('time-estimate').textContent = `~${minTime}-${maxTime} minutes`;
}

async function generateVideo() {
    // Get form values
    const prompt = document.getElementById('prompt').value.trim();
    const model = document.getElementById('model').value;
    const duration = parseInt(document.getElementById('duration').value);
    const resolution = document.getElementById('resolution').value;
    
    // Validation
    if (!prompt) {
        showError('Please enter a text prompt to generate a video.');
        return;
    }
    
    if (prompt.length < 10) {
        showError('Please provide a more detailed description (at least 10 characters).');
        return;
    }
    
    // Hide previous results and show progress
    hideAllSections();
    showProgressSection();
    
    // Disable generate button
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    
    try {
        // Start generation
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                model: model,
                duration: duration,
                resolution: resolution
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to start video generation');
        }
        
        currentJobId = data.job_id;
        
        // Start polling for status
        startStatusPolling();
        
    } catch (error) {
        console.error('Generation error:', error);
        showError(error.message || 'Failed to generate video. Please try again.');
        resetGenerateButton();
    }
}

function startStatusPolling() {
    if (statusInterval) {
        clearInterval(statusInterval);
    }
    
    statusInterval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${currentJobId}`);
            const status = await response.json();
            
            if (!response.ok) {
                throw new Error(status.error || 'Failed to get status');
            }
            
            updateProgress(status);
            
            if (status.status === 'completed') {
                clearInterval(statusInterval);
                showResult(status);
                resetGenerateButton();
            } else if (status.status === 'error') {
                clearInterval(statusInterval);
                showError(status.message || 'Video generation failed');
                resetGenerateButton();
            }
            
        } catch (error) {
            console.error('Status polling error:', error);
            clearInterval(statusInterval);
            showError('Lost connection to server. Please try again.');
            resetGenerateButton();
        }
    }, 2000); // Poll every 2 seconds
}

function updateProgress(status) {
    const progressFill = document.getElementById('progress-fill');
    const progressPercent = document.getElementById('progress-percent');
    const progressMessage = document.getElementById('progress-message');
    
    progressFill.style.width = `${status.progress}%`;
    progressPercent.textContent = `${status.progress}%`;
    progressMessage.textContent = status.message;
}

function showResult(status) {
    hideAllSections();
    
    const resultSection = document.getElementById('result-section');
    const video = document.getElementById('generated-video');
    
    // Set video source (use download URL as preview)
    video.src = status.download_url;
    
    // Fill in result info
    document.getElementById('result-prompt').textContent = status.prompt;
    document.getElementById('result-model').textContent = getModelDisplayName(status.model);
    document.getElementById('result-duration').textContent = status.duration;
    document.getElementById('result-resolution').textContent = status.resolution;
    
    // Store download URL
    document.getElementById('download-btn').setAttribute('data-url', status.download_url);
    
    resultSection.style.display = 'block';
}

function getModelDisplayName(modelName) {
    const models = {
        'zeroscope': 'Zeroscope v2 - High Quality',
        'modelscope': 'ModelScope - Fast Generation'
    };
    return models[modelName] || modelName;
}

function downloadVideo() {
    const downloadBtn = document.getElementById('download-btn');
    const downloadUrl = downloadBtn.getAttribute('data-url');
    
    if (downloadUrl) {
        // Create a temporary link and click it
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `generated_video_${new Date().getTime()}.mp4`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

function startNew() {
    // Clear current job
    currentJobId = null;
    if (statusInterval) {
        clearInterval(statusInterval);
    }
    
    // Reset form and UI
    hideAllSections();
    resetGenerateButton();
    
    // Clear video
    const video = document.getElementById('generated-video');
    video.src = '';
    
    // Focus on prompt
    document.getElementById('prompt').focus();
}

function showError(message) {
    hideAllSections();
    
    const errorSection = document.getElementById('error-section');
    const errorText = document.getElementById('error-text');
    
    errorText.textContent = message;
    errorSection.style.display = 'block';
}

function hideAllSections() {
    document.getElementById('progress-section').style.display = 'none';
    document.getElementById('result-section').style.display = 'none';
    document.getElementById('error-section').style.display = 'none';
}

function showProgressSection() {
    document.getElementById('progress-section').style.display = 'block';
}

function resetGenerateButton() {
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Video';
}

// Utility functions
function formatDuration(seconds) {
    if (seconds < 60) {
        return `${seconds} seconds`;
    } else {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}m ${remainingSeconds}s`;
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Copied to clipboard!');
    });
}

function showToast(message) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #28a745;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        z-index: 1000;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 2000);
}

// Example prompts for inspiration
const examplePrompts = [
    "A majestic eagle soaring over snow-capped mountains at sunrise",
    "Ocean waves crashing against rocky cliffs under a stormy sky",
    "A futuristic city with flying cars and neon lights at night",
    "A peaceful forest stream with sunlight filtering through trees",
    "A space station orbiting Earth with stars in the background",
    "A vintage train traveling through a countryside landscape",
    "A magical forest with glowing mushrooms and fireflies",
    "A sunset over a vast desert with sand dunes",
    "A cozy cabin in winter with smoke rising from the chimney",
    "A busy street market with colorful fruits and vegetables"
];

// Add example prompt functionality
function getRandomPrompt() {
    const randomIndex = Math.floor(Math.random() * examplePrompts.length);
    return examplePrompts[randomIndex];
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        generateVideo();
    }
    
    // Esc to start new
    if (e.key === 'Escape') {
        startNew();
    }
});

// Prevent accidental page refresh while generating
window.addEventListener('beforeunload', function(e) {
    if (currentJobId && statusInterval) {
        e.preventDefault();
        e.returnValue = 'Video generation is in progress. Are you sure you want to leave?';
        return e.returnValue;
    }
});