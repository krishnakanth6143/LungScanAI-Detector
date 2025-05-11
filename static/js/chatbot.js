document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotClose = document.getElementById('chatbot-close');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSendBtn = document.getElementById('chatbot-send-btn');

    // Ensure all elements exist before adding event listeners
    if (!chatbotToggle || !chatbotContainer || !chatbotClose || 
        !chatbotMessages || !chatbotInput || !chatbotSendBtn) {
        console.error('One or more chatbot elements not found');
        return;
    }

    // Make sure chatbot is hidden initially
    chatbotContainer.classList.add('chatbot-hidden');
    chatbotToggle.style.display = 'flex';

    // Toggle chatbot visibility
    chatbotToggle.addEventListener('click', function() {
        chatbotContainer.classList.remove('chatbot-hidden');
        chatbotToggle.style.display = 'none';
        chatbotInput.focus();
    });

    // Close chatbot
    chatbotClose.addEventListener('click', function() {
        chatbotContainer.classList.add('chatbot-hidden');
        chatbotToggle.style.display = 'flex';
    });

    // Send message function
    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage(message, 'user');
        chatbotInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            hideTypingIndicator();
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage("Sorry, I'm having trouble connecting. Please try again.", 'bot');
        });
    }

    // Add message to chat
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Show typing indicator
    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.id = 'typing-indicator';
        typingIndicator.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            typingIndicator.appendChild(dot);
        }
        
        chatbotMessages.appendChild(typingIndicator);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Create suggestions container
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.classList.add('chatbot-suggestions');
    
    // Insert suggestions container before input area
    const inputArea = document.querySelector('.chatbot-input-area');
    inputArea.parentNode.insertBefore(suggestionsContainer, inputArea);

    // Update suggestions function
    function updateSuggestions() {
        suggestionsContainer.innerHTML = ''; // Clear existing suggestions
        
        const suggestions = [
            'What are lung cancer symptoms?',
            'Types of lung cancer',
            'Risk factors',
            'Prevention tips',
            'Treatment options',
            'Find a specialist'
        ];
        
        suggestions.forEach(text => {
            const button = document.createElement('button');
            button.classList.add('suggestion-btn');
            button.textContent = text;
            button.addEventListener('click', () => {
                chatbotInput.value = text;
                sendMessage();
            });
            suggestionsContainer.appendChild(button);
        });
    }

    // Call updateSuggestions initially
    updateSuggestions();

    // Update sendMessage function to maintain suggestions
    const originalSendMessage = sendMessage;
    sendMessage = function() {
        originalSendMessage();
        // Refresh suggestions after sending message
        updateSuggestions();
    };

    // Event listeners for sending messages
    chatbotSendBtn.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Update the welcome message and add suggestions
    setTimeout(() => {
        addMessage("Hello! I'm your AI assistant for lung cancer information. You can click on these suggestions or ask your own questions:", 'bot');
        updateSuggestions();
    }, 500);
});
