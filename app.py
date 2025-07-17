#!/usr/bin/env python3
"""
AI Chatbot Web Application
Flask server providing a web interface for the AI chatbot
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from chatbot import get_chatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize chatbot
logger.info("Initializing AI chatbot...")
chatbot = None

def initialize_chatbot():
    """Initialize the chatbot before handling requests"""
    global chatbot
    try:
        chatbot = get_chatbot()
        logger.info("Chatbot initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        chatbot = None

# Initialize chatbot on startup
with app.app_context():
    initialize_chatbot()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Empty message'
            }), 400
        
        # Check if chatbot is available
        if chatbot is None:
            return jsonify({
                'success': False,
                'error': 'Chatbot is not available. Please try again later.'
            }), 503
        
        # Generate response
        logger.info(f"Processing message: {user_message[:50]}...")
        bot_response = chatbot.generate_response(user_message)
        
        # Return response
        return jsonify({
            'success': True,
            'response': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'success': False,
            'error': 'An internal error occurred. Please try again.'
        }), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        if chatbot is not None:
            chatbot.clear_history()
            logger.info("Conversation history cleared")
        
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared'
        })
        
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear history'
        }), 500

@app.route('/status')
def status():
    """Get chatbot status"""
    return jsonify({
        'chatbot_loaded': chatbot is not None,
        'model_name': chatbot.model_name if chatbot else None,
        'conversation_length': len(chatbot.get_history()) if chatbot else 0
    })

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Page not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

def main():
    """Main function to run the Flask app"""
    print("🤖 AI Chatbot Web Server")
    print("=" * 30)
    print("Starting server...")
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the app
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"❌ Error starting server: {e}")

if __name__ == '__main__':
    main()