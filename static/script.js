// AI Chatbot Frontend JavaScript

class ChatbotUI {
    constructor() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-btn');
        this.clearButton = document.getElementById('clear-btn');
        this.statusElement = document.getElementById('status');
        this.loadingElement = document.getElementById('loading');
        this.charCountElement = document.getElementById('char-count');
        
        this.isLoading = false;
        this.messageCount = 0;
        
        this.init();
    }
    
    init() {
        console.log('🤖 Initializing AI Chatbot UI');
        
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.clearButton.addEventListener('click', () => this.clearConversation());
        this.messageInput.addEventListener('keydown', (e) => this.handleKeydown(e));
        this.messageInput.addEventListener('input', () => this.updateCharCount());
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());
        
        // Check chatbot status
        this.checkStatus();
        
        // Focus on input
        this.messageInput.focus();
        
        console.log('✅ Chatbot UI initialized');
    }
    
    async checkStatus() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            
            if (data.chatbot_loaded) {
                this.setStatus('ready', '🟢 AI Ready');
            } else {
                this.setStatus('error', '🔴 AI Loading...');
                // Retry after a delay
                setTimeout(() => this.checkStatus(), 2000);
            }
        } catch (error) {
            console.error('Status check failed:', error);
            this.setStatus('error', '🔴 Connection Error');
        }
    }
    
    setStatus(type, message) {
        this.statusElement.className = `status ${type}`;
        this.statusElement.textContent = message;
    }
    
    handleKeydown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }
    
    autoResizeTextarea() {
        const textarea = this.messageInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
    
    updateCharCount() {
        const count = this.messageInput.value.length;
        this.charCountElement.textContent = count;
        
        // Change color based on limit
        if (count > 900) {
            this.charCountElement.style.color = '#e17055';
        } else if (count > 800) {
            this.charCountElement.style.color = '#fdcb6e';
        } else {
            this.charCountElement.style.color = '#666';
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isLoading) {
            return;
        }
        
        // Add user message to UI
        this.addMessage('user', message);
        
        // Clear input
        this.messageInput.value = '';
        this.updateCharCount();
        this.autoResizeTextarea();
        
        // Show loading
        this.setLoading(true);
        
        try {
            // Send to backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Add bot response to UI
                this.addMessage('bot', data.response, data.timestamp);
            } else {
                // Handle error
                this.addMessage('bot', `❌ Error: ${data.error || 'Unknown error occurred'}`, null, true);
            }
            
        } catch (error) {
            console.error('Send message error:', error);
            this.addMessage('bot', '❌ Network error. Please check your connection and try again.', null, true);
        } finally {
            this.setLoading(false);
            this.messageInput.focus();
        }
    }
    
    addMessage(type, content, timestamp = null, isError = false) {
        this.messageCount++;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (type === 'bot' && !isError) {
            contentDiv.innerHTML = `<strong>🤖 AI Assistant:</strong> ${this.escapeHtml(content)}`;
        } else if (type === 'user') {
            contentDiv.innerHTML = `<strong>👤 You:</strong> ${this.escapeHtml(content)}`;
        } else {
            contentDiv.innerHTML = this.escapeHtml(content);
        }
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        
        if (timestamp) {
            const date = new Date(timestamp);
            timeDiv.textContent = date.toLocaleTimeString();
        } else {
            const now = new Date();
            timeDiv.textContent = now.toLocaleTimeString();
        }
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        this.sendButton.disabled = loading;
        
        if (loading) {
            this.loadingElement.style.display = 'flex';
            this.scrollToBottom();
        } else {
            this.loadingElement.style.display = 'none';
        }
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
    
    async clearConversation() {
        if (!confirm('Are you sure you want to clear the conversation history?')) {
            return;
        }
        
        try {
            const response = await fetch('/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Clear UI messages (keep welcome message)
                const messages = this.messagesContainer.querySelectorAll('.message');
                messages.forEach((message, index) => {
                    if (index > 0) { // Keep first welcome message
                        message.remove();
                    }
                });
                
                this.messageCount = 1; // Reset count (keeping welcome message)
                
                // Show confirmation
                this.addMessage('bot', '🗑️ Conversation history cleared!', null, false);
                
            } else {
                console.error('Clear failed:', data.error);
                alert('Failed to clear conversation history.');
            }
            
        } catch (error) {
            console.error('Clear error:', error);
            alert('Failed to clear conversation history.');
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Utility functions
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Initialize the chatbot UI when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Starting AI Chatbot');
    
    // Add some startup delay for dramatic effect
    setTimeout(() => {
        new ChatbotUI();
    }, 500);
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Page became visible, check status
        if (window.chatbot) {
            window.chatbot.checkStatus();
        }
    }
});

// Add some fun console messages
console.log(`
🤖 AI Chatbot Web Interface
===========================
🚀 Free & Unlimited AI Chat
🔓 No Content Restrictions  
⚡ Fast Local Processing
🛡️ Privacy Focused

Ready to chat!
`);

// Export for global access
window.ChatbotUI = ChatbotUI;