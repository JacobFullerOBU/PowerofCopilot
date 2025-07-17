#!/usr/bin/env python3
"""
Simple AI Chatbot Backend
A conversational AI system with local fallback when HuggingFace models are not available
"""

import os
import logging
import random
import re
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import HuggingFace transformers, fallback to simple chatbot
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HF_AVAILABLE = True
    logger.info("HuggingFace transformers available")
except ImportError:
    HF_AVAILABLE = False
    logger.warning("HuggingFace transformers not available, using simple chatbot")


class SimpleChatbot:
    """Simple rule-based chatbot for fallback"""
    
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10
        
        # Simple response patterns
        self.patterns = {
            'greeting': {
                'patterns': [r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b'],
                'responses': [
                    "Hello! I'm your AI assistant. How can I help you today?",
                    "Hi there! I'm here to chat and assist you with anything you'd like to discuss.",
                    "Hey! Great to see you. What would you like to talk about?",
                    "Greetings! I'm an AI chatbot ready to have a conversation with you."
                ]
            },
            'how_are_you': {
                'patterns': [r'\b(how are you|how\'re you|how do you feel|what\'s up)\b'],
                'responses': [
                    "I'm doing great, thank you for asking! I'm here and ready to help.",
                    "I'm functioning perfectly and excited to chat with you!",
                    "I'm doing well! How are you doing today?",
                    "All systems running smoothly! I'm ready for whatever you'd like to discuss."
                ]
            },
            'name': {
                'patterns': [r'\b(what\'s your name|who are you|what are you called)\b'],
                'responses': [
                    "I'm an AI chatbot designed to be helpful, creative, and unrestricted in our conversations.",
                    "You can call me AI Assistant. I'm here to chat about anything you'd like!",
                    "I'm your personal AI chatbot - no limits, no restrictions, just helpful conversation.",
                    "I'm an artificial intelligence designed for open and free conversation on any topic."
                ]
            },
            'capabilities': {
                'patterns': [r'\b(what can you do|help me|capabilities|features)\b'],
                'responses': [
                    "I can help with many things: answer questions, have conversations, help with writing, discuss any topic, provide information, and more!",
                    "I'm designed to be helpful with a wide range of tasks - feel free to ask me anything!",
                    "My capabilities include: conversation, writing assistance, answering questions, creative tasks, and discussing any topic without restrictions.",
                    "I can chat about anything, help with problems, answer questions, assist with creative projects, and provide information on many topics."
                ]
            },
            'thanks': {
                'patterns': [r'\b(thank you|thanks|appreciate|grateful)\b'],
                'responses': [
                    "You're very welcome! I'm happy to help.",
                    "No problem at all! Feel free to ask me anything else.",
                    "My pleasure! I'm here whenever you need assistance.",
                    "You're welcome! I enjoy our conversation."
                ]
            },
            'goodbye': {
                'patterns': [r'\b(goodbye|bye|see you|farewell|take care)\b'],
                'responses': [
                    "Goodbye! It was great chatting with you. Come back anytime!",
                    "See you later! I'll be here whenever you want to chat again.",
                    "Take care! Thanks for the conversation.",
                    "Bye! Feel free to return anytime for more conversation."
                ]
            }
        }
        
        # Default responses for when no pattern matches
        self.default_responses = [
            "That's interesting! Tell me more about that.",
            "I see. What are your thoughts on that?",
            "Can you elaborate on that? I'd like to understand better.",
            "That's a good point. What else would you like to discuss?",
            "I appreciate you sharing that. What's on your mind?",
            "Interesting perspective! What made you think about that?",
            "I'd love to hear more of your thoughts on this topic.",
            "That's worth thinking about. What's your take on it?"
        ]
        
        # Question responses for when user asks questions
        self.question_responses = [
            "That's a great question! While I may not have all the answers, I'm happy to discuss it with you.",
            "Interesting question! What do you think about it yourself?",
            "That's something worth exploring. What's your perspective on this?",
            "Good question! I'd be curious to hear your thoughts first.",
            "That's thought-provoking! Let's think through this together.",
        ]
        
    def generate_response(self, user_input: str) -> str:
        """Generate a response using pattern matching"""
        original_input = user_input
        user_input = user_input.lower().strip()
        
        if not user_input:
            return "I didn't receive any message. Could you please say something?"
        
        # Check patterns first
        response = None
        for category, data in self.patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_input, re.IGNORECASE):
                    response = random.choice(data['responses'])
                    break
            if response:
                break
        
        # If no pattern matched, check for questions
        if not response and '?' in user_input:
            if any(word in user_input for word in ['what', 'how', 'why', 'when', 'where', 'who']):
                response = random.choice(self.question_responses)
            else:
                response = random.choice(self.default_responses)
        
        # If still no response, use default
        if not response:
            response = random.choice(self.default_responses)
        
        # Update history
        self._update_history(original_input, response)
        
        return response
    
    def _update_history(self, user_input: str, bot_response: str):
        """Update conversation history"""
        self.conversation_history.append({
            'user': user_input,
            'bot': bot_response
        })
        
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get current conversation history"""
        return self.conversation_history.copy()


class AIChatbot:
    """AI Chatbot with HuggingFace fallback to simple chatbot"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        """Initialize the chatbot"""
        self.model_name = model_name
        self.conversation_history = []
        self.max_history = 10
        self.use_simple_bot = False
        
        # Try to load HuggingFace model
        if HF_AVAILABLE:
            logger.info(f"Attempting to load AI model: {model_name}")
            try:
                self._load_hf_model()
                logger.info("HuggingFace model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load HuggingFace model: {e}")
                self._fallback_to_simple()
        else:
            logger.info("HuggingFace not available, using simple chatbot")
            self._fallback_to_simple()
    
    def _load_hf_model(self):
        """Load HuggingFace model"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def _fallback_to_simple(self):
        """Fallback to simple chatbot"""
        self.use_simple_bot = True
        self.simple_bot = SimpleChatbot()
        logger.info("Using simple rule-based chatbot")
    
    def generate_response(self, user_input: str) -> str:
        """Generate response using appropriate backend"""
        if self.use_simple_bot:
            return self.simple_bot.generate_response(user_input)
        else:
            return self._generate_hf_response(user_input)
    
    def _generate_hf_response(self, user_input: str) -> str:
        """Generate response using HuggingFace model"""
        try:
            user_input = user_input.strip()
            if not user_input:
                return "I didn't receive any message. Could you please say something?"
            
            # Build context
            context = self._build_context(user_input)
            
            # Tokenize
            input_ids = self.tokenizer.encode(context, return_tensors='pt')
            
            # Generate
            with torch.no_grad():
                output = self.model.generate(
                    input_ids,
                    max_length=input_ids.shape[1] + 50,
                    num_return_sequences=1,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3,
                    early_stopping=True
                )
            
            # Decode
            response = self.tokenizer.decode(output[0], skip_special_tokens=True)
            response = response[len(context):].strip()
            response = self._clean_response(response)
            
            # Update history
            self._update_history(user_input, response)
            
            return response if response else "I'm thinking... Could you rephrase that?"
            
        except Exception as e:
            logger.error(f"HuggingFace generation error: {e}")
            return "I encountered an error. Let me try a different approach to help you."
    
    def _build_context(self, user_input: str) -> str:
        """Build conversation context"""
        context_parts = []
        
        for exchange in self.conversation_history[-3:]:
            context_parts.append(f"Human: {exchange['user']}")
            context_parts.append(f"AI: {exchange['bot']}")
        
        context_parts.append(f"Human: {user_input}")
        context_parts.append("AI:")
        
        return " ".join(context_parts)
    
    def _clean_response(self, response: str) -> str:
        """Clean generated response"""
        response = response.replace("Human:", "").replace("AI:", "")
        
        sentences = response.split('.')
        if len(sentences) > 1:
            first_sentence = sentences[0].strip()
            if len(first_sentence) > 10:
                response = first_sentence + "."
        
        response = " ".join(response.split())
        
        if len(response) < 3:
            return "I'm not sure how to respond to that. Could you try asking differently?"
        
        return response
    
    def _update_history(self, user_input: str, bot_response: str):
        """Update conversation history"""
        self.conversation_history.append({
            'user': user_input,
            'bot': bot_response
        })
        
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        if self.use_simple_bot:
            self.simple_bot.clear_history()
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        if self.use_simple_bot:
            return self.simple_bot.get_history()
        return self.conversation_history.copy()


# Global chatbot instance
chatbot_instance = None


def get_chatbot() -> AIChatbot:
    """Get or create the global chatbot instance"""
    global chatbot_instance
    if chatbot_instance is None:
        chatbot_instance = AIChatbot()
    return chatbot_instance


if __name__ == "__main__":
    # Test the chatbot
    print("🤖 AI Chatbot Test")
    print("=" * 30)
    
    chatbot = AIChatbot()
    
    print("Chatbot loaded! Type 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            response = chatbot.generate_response(user_input)
            print(f"Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")