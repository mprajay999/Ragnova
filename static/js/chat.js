// Auto-resize textarea
const textarea = document.getElementById('message-input');
textarea.addEventListener('input', function() {
    this.style.height = '28px';
    this.style.height = (this.scrollHeight) + 'px';
});

function appendMessage(content, isUser = false) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start space-x-4 space-y-1';
    
    // Avatar
    const avatarDiv = document.createElement('div');
    if (isUser) {
        avatarDiv.className = 'w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-bold text-xs';
        avatarDiv.textContent = 'You';
    } else {
        avatarDiv.className = 'w-8 h-8 rounded-full ai-avatar flex items-center justify-center text-white font-bold text-xs';
        avatarDiv.textContent = 'CE';
    }
    
    // Message content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'flex-1';
    
    const innerDiv = document.createElement('div');
    innerDiv.className = 'prose prose-slate max-w-none';
    
    if (!isUser && content) {
        try {
            innerDiv.innerHTML = marked.parse(content);
        } catch (e) {
            console.error('Error parsing markdown:', e);
            innerDiv.textContent = content;
        }
    } else {
        innerDiv.textContent = content || '';
    }
    
    contentDiv.appendChild(innerDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    messageWrapper.appendChild(messageDiv);
    messagesDiv.appendChild(messageWrapper);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function appendThinkingIndicator() {
    const messagesDiv = document.getElementById('chat-messages');
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper thinking-message';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start space-x-4';
    
    // AI Avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'w-8 h-8 rounded-full ai-avatar flex items-center justify-center text-white font-bold text-sm';
    avatarDiv.textContent = 'CE';
    
    // Thinking content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'flex-1';
    
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'thinking';
    thinkingDiv.innerHTML = '<div style="margin-top: 6px; margin-bottom: 4px;">Thinking<span class="thinking-dots"><span>.</span><span>.</span><span>.</span></span></div>';
    
    contentDiv.appendChild(thinkingDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    messageWrapper.appendChild(messageDiv);
    messagesDiv.appendChild(messageWrapper);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    return messageWrapper;
}

// Add command+enter handler
document.getElementById('message-input').addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('chat-form').dispatchEvent(new Event('submit'));
    }
});

// Add function to show tool usage
function appendToolUsage(toolName) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start space-x-4';
    
    // AI Avatar
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'w-8 h-8 rounded-full ai-avatar flex items-center justify-center text-white font-bold text-sm';
    avatarDiv.textContent = 'CE';
    
    // Tool usage content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'flex-1';
    
    const toolDiv = document.createElement('div');
    toolDiv.className = 'tool-usage';
    toolDiv.textContent = `Using tool: ${toolName}`;
    
    contentDiv.appendChild(toolDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    messageWrapper.appendChild(messageDiv);
    messagesDiv.appendChild(messageWrapper);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function updateTokenUsage(usedTokens, maxTokens) {
    const percentage = (usedTokens / maxTokens) * 100;
    const tokenBar = document.getElementById('token-bar');
    const tokensUsed = document.getElementById('tokens-used');
    const tokenPercentage = document.getElementById('token-percentage');
    
    // Update the numbers
    tokensUsed.textContent = usedTokens.toLocaleString();
    tokenPercentage.textContent = `${percentage.toFixed(1)}%`;
    
    // Update the bar
    tokenBar.style.width = `${percentage}%`;
    
    // Update colors based on usage
    tokenBar.classList.remove('warning', 'danger');
    if (percentage > 90) {
        tokenBar.classList.add('danger');
    } else if (percentage > 75) {
        tokenBar.classList.add('warning');
    }
}

// Update the chat form submit handler
document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Append user message
    appendMessage(message, true);
    
    // Clear input and reset height
    messageInput.value = '';
    resetTextarea();
    
    try {
        // Add thinking indicator
        const thinkingMessage = appendThinkingIndicator();
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message
            })
        });
        
        const data = await response.json();
        
        // Update token usage if provided in response
        if (data.token_usage) {
            updateTokenUsage(data.token_usage.total_tokens, data.token_usage.max_tokens);
        }
        
        // Remove thinking indicator
        if (thinkingMessage) {
            thinkingMessage.remove();
        }
        
        // Show tool usage if present
        if (data.tool_name) {
            appendToolUsage(data.tool_name);
        }
        
        // Show response if we have one
        if (data && data.response) {
            appendMessage(data.response);
        } else {
            appendMessage('Error: No response received');
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        document.querySelector('.thinking-message')?.remove();
        appendMessage('Error: Failed to send message');
    }
});

function resetTextarea() {
    const textarea = document.getElementById('message-input');
    textarea.style.height = '28px';
}

document.getElementById('chat-form').addEventListener('reset', () => {
    resetTextarea();
});

// Reset conversation when page loads
window.addEventListener('load', async () => {
    try {
        // Reset the conversation when page loads
        const response = await fetch('/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            console.error('Failed to reset conversation');
        }
        
        // Clear any existing messages except the first one
        const messagesDiv = document.getElementById('chat-messages');
        const messages = messagesDiv.getElementsByClassName('message-wrapper');
        while (messages.length > 1) {
            messages[1].remove();
        }
        
        // Reset any other state
        document.getElementById('message-input').value = '';
        resetTextarea();
        
        // Reset token usage display
        updateTokenUsage(0, 200000);
    } catch (error) {
        console.error('Error resetting conversation:', error);
    }
});



















function refreshWebsitePreview() {
    const iframe = document.getElementById('website-preview');
    
    // Store the current scroll position
    let scrollX = 0;
    let scrollY = 0;
    
    try {
        // Try to get the scroll position from the iframe content
        if (iframe.contentWindow) {
            scrollX = iframe.contentWindow.scrollX || 0;
            scrollY = iframe.contentWindow.scrollY || 0;
        }
    } catch (e) {
        console.log("Could not access iframe scroll position", e);
    }
    
    // Add timestamp to force cache invalidation
    const timestamp = new Date().getTime();
    
    // Create a new URL with the timestamp
    let currentSrc = iframe.src.split('?')[0]; // Remove any existing query params
    iframe.src = `${currentSrc}?t=${timestamp}`;
    
    // Restore scroll position after the iframe loads
    iframe.onload = function() {
        try {
            if (iframe.contentWindow) {
                iframe.contentWindow.scrollTo(scrollX, scrollY);
            }
        } catch (e) {
            console.log("Could not restore iframe scroll position", e);
        }
    };
}

// Update the URL in real-time when deployment message is received
function updateDeploymentUrl(message) {
    // Look for deployment URL in the message
    const deploymentMatch = message.match(/You can view your website at: (https:\/\/[^\s]+)/);
    if (deploymentMatch && deploymentMatch[1]) {
        const deployUrl = deploymentMatch[1];
        // Update the "Open in new tab" link
        const openInNewTabLink = document.getElementById('open-in-new-tab');
        if (openInNewTabLink) {
            openInNewTabLink.href = deployUrl;
            openInNewTabLink.setAttribute('data-deployed', 'true');
            
            // Add a deployed indicator
            const deployStatus = document.createElement('span');
            deployStatus.className = 'deploy-status';
            deployStatus.textContent = '🌐 Live';
            
            // Replace any existing deploy status
            const existingStatus = openInNewTabLink.querySelector('.deploy-status');
            if (existingStatus) {
                openInNewTabLink.removeChild(existingStatus);
            }
            
            openInNewTabLink.appendChild(deployStatus);
        }
    }
}