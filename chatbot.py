import os
import requests
import json
import time

class LungCancerChatbot:
    def __init__(self, api_key, model="anthropic/claude-3-haiku"):
        """
        Initialize the chatbot with OpenRouter API key and model
        Using claude-3-haiku for faster responses and better reliability
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://lungcancerai.com"  # Use your actual domain in production
        }
        self.conversation_history = []
        self.max_retries = 3
        
    def add_context(self):
        """
        Add medical context to the chatbot to help it provide better responses
        """
        context = [
            {"role": "system", "content": """
            You are an AI assistant specialized in lung cancer information. You can help users understand:
            
            1. Different types of lung cancer:
               - Adenocarcinoma: The most common type, often found in the outer regions of the lung
               - Large Cell Carcinoma: Fast-growing cancer that can appear in any part of the lung
               - Squamous Cell Carcinoma: Commonly linked to smoking, found in the central part of the lungs
               
            2. General information about CT scan interpretation and the limitations of AI-based detection
            
            3. Risk factors, symptoms, and prevention strategies for lung cancer
            
            IMPORTANT: You should NOT provide specific medical diagnoses, interpret specific scan results, or give personalized medical advice. 
            Always remind users that this tool is for educational purposes and they should consult healthcare professionals for diagnosis and treatment.
            
            Be compassionate, clear, and concise in your responses while maintaining medical accuracy.
            """}
        ]
        
        self.conversation_history = context.copy()
        return context
        
    def get_response(self, user_message):
        """
        Get chatbot response based on user message with improved error handling
        """
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        payload = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        # Implement retry logic
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.base_url, 
                    headers=self.headers, 
                    json=payload, 
                    timeout=30
                )
                
                if response.status_code == 429:  # Rate limit exceeded
                    print(f"Rate limit exceeded. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
                response.raise_for_status()  # Raise exception for HTTP errors
                
                response_data = response.json()
                if "choices" not in response_data or len(response_data["choices"]) == 0:
                    raise ValueError("Empty response received from API")
                    
                assistant_message = response_data["choices"][0]["message"]["content"]
                
                # Add assistant response to conversation history
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                # Limit conversation history length to prevent token limit issues
                if len(self.conversation_history) > 10:
                    # Keep system prompt and last 9 messages
                    system_message = self.conversation_history[0]
                    self.conversation_history = [system_message] + self.conversation_history[-9:]
                    
                return assistant_message
                
            except requests.exceptions.Timeout:
                print(f"Request timed out (attempt {attempt+1}/{self.max_retries})")
                if attempt == self.max_retries - 1:
                    return "I'm taking longer than expected to respond. Please try again in a moment."
                
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt+1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return "I'm having trouble connecting to my knowledge base right now. Please try again later."
                
            except (KeyError, IndexError, ValueError, json.JSONDecodeError) as e:
                print(f"Response parsing error: {str(e)}")
                error_message = f"Error details: {str(e)}"
                print(error_message)
                
                # Remove the unsuccessful user message from history
                if len(self.conversation_history) > 0 and self.conversation_history[-1]["role"] == "user":
                    self.conversation_history.pop()
                    
                return "I encountered an error processing your request. Please try again with a simpler question."
                
            # Wait before retry
            if attempt < self.max_retries - 1:
                time.sleep(1)
                
        # If we get here, all retries failed
        return "I'm experiencing technical difficulties. Please try again later."
