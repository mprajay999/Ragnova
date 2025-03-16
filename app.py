from flask import Flask, render_template, request, jsonify
import os
import shutil
from ce3 import Assistant
from config import Config

# Delete website folder if it exists
WEBSITE_DIR = os.path.join(os.getcwd(), 'website')
if os.path.exists(WEBSITE_DIR):
    shutil.rmtree(WEBSITE_DIR)
    print(f"Deleted existing website directory: {WEBSITE_DIR}")

# Store conversation histories by session ID
conversation_store = {}

# Constants (unchanged)
DEFAULT_INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Website Preview</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
            color: #333;
            text-align: center;
        }
        .content {
            max-width: 600px;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 {
            margin-top: 0;
            color: #2563eb;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>No Website Yet</h1>
        <p>Your website will appear here once you start developing it with the assistant.</p>
        <p>Describe what kind of website you want to create, and the assistant will help you build it!</p>
    </div>
</body>
</html>
"""

# Auto-refresh script (unchanged)
AUTO_REFRESH_SCRIPT = """
<script>
// Store the last modified time
let lastModified = 0;

// Check for changes every 2 seconds
setInterval(function() {
    fetch('/check-website-modified')
        .then(response => response.json())
        .then(data => {
            if (lastModified && data.modified > lastModified) {
                console.log('Website updated, refreshing...');
                location.reload();
            }
            lastModified = data.modified;
        })
        .catch(error => console.error('Auto-refresh check failed:', error));
}, 2000);
</script>
"""

# MIME type mapping (unchanged)
MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.json': 'application/json',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.eot': 'application/vnd.ms-fontobject'
}

# Initialize Flask app
app = Flask(__name__, static_folder='static')
assistant = Assistant()

@app.route('/')
def home():
    """Render the main application page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests from the frontend"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', request.remote_addr)  # Use client IP as fallback
        
        # Get or initialize conversation history for this session
        if session_id not in conversation_store:
            conversation_store[session_id] = []
        
        conversation_history = conversation_store[session_id]
        
        # Append the new user message to history
        conversation_history.append({'role': 'user', 'content': user_message})
        
        # Create a message that includes the conversation history
        if len(conversation_history) > 1:
            context_message = "Here's our conversation so far:\n\n"
            for msg in conversation_history[:-1]:  # All except the current message
                role = "User" if msg['role'] == 'user' else "Assistant"
                context_message += f"{role}: {msg['content']}\n\n"
            
            context_message += f"Now responding to: {user_message}"
            enhanced_message = context_message
        else:
            enhanced_message = user_message
        
        # Process the message through the assistant
        response = assistant.chat(enhanced_message)
        
        # Store the assistant's response
        conversation_history.append({'role': 'assistant', 'content': response})
        
        # Prune history if it gets too large
        if len(conversation_history) > 20:  # Arbitrary limit, adjust as needed
            conversation_history = conversation_history[-10:]  # Keep last 10 exchanges
            conversation_store[session_id] = conversation_history
        
        # Get token usage statistics
        token_usage = {
            'total_tokens': assistant.total_tokens_used,
            'max_tokens': Config.MAX_CONVERSATION_TOKENS
        }
        
        # Get the last used tool from the conversation history
        tool_name = get_last_used_tool(assistant)
        
        # Reset the assistant after every request (stateless API)
        assistant.reset()

        return jsonify({
            'response': response,
            'thinking': False,
            'tool_name': tool_name,
            'token_usage': token_usage
        })
    
    except Exception as e:
        # Ensure assistant reset even on error
        assistant.reset()
        
        return jsonify({
            'response': f"Error: {str(e)}",
            'thinking': False,
            'tool_name': None,
            'token_usage': None
        }), 200  # Return 200 for graceful frontend handling

def get_last_used_tool(assistant_instance):
    """Extract the last used tool name from conversation history"""
    if not assistant_instance.conversation_history:
        return None
        
    for msg in reversed(assistant_instance.conversation_history):
        if msg.get('role') == 'assistant' and msg.get('content'):
            content = msg['content']
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get('type') == 'tool_use':
                        return block.get('name')
    return None

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the assistant's conversation history"""
    session_id = request.json.get('session_id', request.remote_addr)
    
    # Clear the conversation history for this session
    if session_id in conversation_store:
        conversation_store[session_id] = []
    
    # Reset the assistant as well
    assistant.reset()
    
    return jsonify({'status': 'success'})

@app.route('/check-website-modified', methods=['GET'])
def check_website_modified():
    """Return the latest modification time of website files for auto-refresh"""
    if not os.path.exists(WEBSITE_DIR):
        return jsonify({'modified': 0})
    
    latest_mtime = 0
    for root, _, files in os.walk(WEBSITE_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(full_path)
                latest_mtime = max(latest_mtime, mtime)
            except Exception:
                pass
    
    return jsonify({'modified': latest_mtime})

@app.route('/website', defaults={'path': 'index.html'})
@app.route('/website/', defaults={'path': 'index.html'})
@app.route('/website/<path:path>')
def serve_website(path):
    """Serve website files with proper MIME types and auto-refresh for HTML"""
    # Ensure website directory exists
    ensure_website_directory()
    
    # Handle trailing slashes or directory requests
    if path.endswith('/'):
        path = path + 'index.html'
    
    # Build the full path and handle fallbacks
    full_path = get_file_path(path)
    
    # Determine MIME type
    ext = os.path.splitext(path)[1].lower()
    mime_type = MIME_TYPES.get(ext, 'text/html')
    
    try:
        with open(full_path, 'rb') as f:
            content = f.read()
            
            # Inject auto-refresh script into HTML files
            if mime_type == 'text/html':
                content = inject_refresh_script(content)
            
            return content, 200, {'Content-Type': mime_type}
    except Exception as e:
        return f"Error serving {path}: {str(e)}", 500

def ensure_website_directory():
    """Create website directory with default index if it doesn't exist"""
    if not os.path.exists(WEBSITE_DIR):
        os.makedirs(WEBSITE_DIR, exist_ok=True)
        with open(os.path.join(WEBSITE_DIR, 'index.html'), 'w') as f:
            f.write(DEFAULT_INDEX_HTML)

def get_file_path(path):
    """Resolve file path with proper fallbacks to index.html"""
    full_path = os.path.join(WEBSITE_DIR, path)
    
    if not os.path.exists(full_path):
        if os.path.isdir(full_path):
            # Try index.html in directory
            dir_index = os.path.join(full_path, 'index.html')
            if os.path.exists(dir_index):
                return dir_index
        
        # Fallback to main index.html
        return os.path.join(WEBSITE_DIR, 'index.html')
    
    return full_path

def inject_refresh_script(content_bytes):
    """Inject auto-refresh script into HTML content"""
    try:
        content_str = content_bytes.decode('utf-8')
        
        # Insert before closing body tag or append to the end
        if '</body>' in content_str:
            content_str = content_str.replace('</body>', f"{AUTO_REFRESH_SCRIPT}</body>")
        else:
            content_str += AUTO_REFRESH_SCRIPT
        
        return content_str.encode('utf-8')
    except Exception:
        # If decoding fails, return original content
        return content_bytes

if __name__ == '__main__':
    app.run(debug=False)