const API_BASE_URL = 'http://localhost:5000/api';

let currentDocument = null;
let chatHistory = [];

// DOM Elements
const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');
const selectedFile = document.getElementById('selectedFile');
const fileName = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');
const uploadButton = document.getElementById('uploadButton');
const uploadProgress = document.getElementById('uploadProgress');
const progressText = document.getElementById('progressText');
const currentDocumentEl = document.getElementById('currentDocument');
const currentDocName = document.getElementById('currentDocName');
const uploadSection = document.getElementById('uploadSection');
const chatSection = document.getElementById('chatSection');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const clearChatButton = document.getElementById('clearChatButton');
const statusIndicator = document.getElementById('statusIndicator');
const chatDocIndicator = document.getElementById('chatDocIndicator');
const chatDocName = document.getElementById('chatDocName');

// File Input Handler
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        if (file.type !== 'application/pdf') {
            showError('Please select a PDF file');
            fileInput.value = '';
            return;
        }

        fileName.textContent = file.name;
        selectedFile.style.display = 'flex';
        uploadButton.disabled = false;

        // Animate file selection
        selectedFile.style.animation = 'none';
        setTimeout(() => {
            selectedFile.style.animation = 'slideIn 0.3s ease-out';
        }, 10);
    }
});

// Remove File Handler
removeFileBtn.addEventListener('click', () => {
    fileInput.value = '';
    selectedFile.style.display = 'none';
    uploadButton.disabled = true;
});

// Upload Button Handler
uploadButton.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    uploadButton.disabled = true;
    uploadProgress.style.display = 'block';
    updateStatus('processing', 'Processing document...');
    progressText.textContent = 'Uploading PDF...';

    try {
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            currentDocument = file.name;
            currentDocName.textContent = file.name;
            chatDocName.textContent = file.name;

            progressText.textContent = `✓ Processed ${data.data.chunks_created} chunks in ${data.data.processing_time}`;

            setTimeout(() => {
                uploadProgress.style.display = 'none';
                currentDocumentEl.style.display = 'block';

                // Switch to chat view
                setTimeout(() => {
                    uploadSection.style.display = 'none';
                    chatSection.style.display = 'block';
                    updateStatus('ready', 'Ready');
                    chatInput.focus();
                }, 500);
            }, 1500);
        } else {
            throw new Error(data.error.message);
        }
    } catch (error) {
        console.error('Upload error:', error);
        showError(error.message || 'Failed to upload document');
        uploadProgress.style.display = 'none';
        uploadButton.disabled = false;
        updateStatus('error', 'Upload failed');
    }
});

// Chat Input Handler
chatInput.addEventListener('input', () => {
    // Auto-resize textarea
    chatInput.style.height = 'auto';
    chatInput.style.height = chatInput.scrollHeight + 'px';

    // Enable/disable send button
    sendButton.disabled = !chatInput.value.trim();
});

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (chatInput.value.trim()) {
            sendMessage();
        }
    }
});

// Send Button Handler
sendButton.addEventListener('click', () => {
    if (chatInput.value.trim()) {
        sendMessage();
    }
});

// Send Message Function
async function sendMessage() {
    const question = chatInput.value.trim();
    if (!question) return;

    // Add user message to chat
    addMessage('user', question);

    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    sendButton.disabled = true;

    // Show typing indicator
    const typingId = showTypingIndicator();
    updateStatus('processing', 'Searching...');

    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator(typingId);

        if (data.success) {
            updateStatus('ready', 'Ready');
            addMessage('assistant', data.data.answer, data.data.sources);
        } else {
            updateStatus('error', 'Error');
            showErrorMessage(data.error.message);
        }
    } catch (error) {
        console.error('Query error:', error);
        removeTypingIndicator(typingId);
        updateStatus('error', 'Error');
        showErrorMessage('Failed to get response. Please try again.');
    }
}

// Add Message to Chat
function addMessage(role, content, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = role === 'user' ? 'You' : '◆';
    const roleName = role === 'user' ? 'You' : 'Assistant';

    let sourcesHTML = '';
    if (sources && sources.length > 0) {
        sourcesHTML = `
            <div class="message-sources">
                <div class="sources-title">Sources</div>
                ${sources.map(source => `
                    <div class="source-item">
                        <div class="source-page">Page ${source.page}</div>
                        <div>${source.content.substring(0, 200)}...</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar">${avatar}</div>
            <div class="message-role">${roleName}</div>
        </div>
        <div class="message-content">
            ${content}
            ${sourcesHTML}
        </div>
    `;

    // Remove welcome message if exists
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Add to history
    chatHistory.push({ role, content, sources });
}

// Show Typing Indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    const id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'message assistant';
    typingDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar">◆</div>
            <div class="message-role">Assistant</div>
        </div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

// Remove Typing Indicator
function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Show Error Message
function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message assistant';
    errorDiv.innerHTML = `
        <div class="message-header">
            <div class="message-avatar">◆</div>
            <div class="message-role">Assistant</div>
        </div>
        <div class="error-message">
            ${message}
        </div>
    `;
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Clear Chat Handler
clearChatButton.addEventListener('click', () => {
    if (confirm('Are you sure you want to clear the chat history?')) {
        chatHistory = [];
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">◆</div>
                <p>Ask me anything about your document. I'll search through the content and provide accurate answers based on what I find.</p>
            </div>
        `;
    }
});

// Update Status Indicator
function updateStatus(status, text) {
    statusIndicator.className = `status-indicator ${status}`;
    statusIndicator.querySelector('.status-text').textContent = text;
}

// Show Error
function showError(message) {
    updateStatus('error', 'Error');
    alert(message);
    setTimeout(() => {
        updateStatus('ready', 'Ready');
    }, 3000);
}

// Check Health on Load
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (data.success) {
            if (data.data.vector_db_exists) {
                // Database exists, show chat interface
                currentDocument = 'Existing Document';
                currentDocName.textContent = 'Document loaded';
                chatDocName.textContent = 'Document loaded';
                currentDocumentEl.style.display = 'block';
                uploadSection.style.display = 'none';
                chatSection.style.display = 'block';
                updateStatus('ready', 'Ready');
            } else {
                updateStatus('ready', 'Ready');
            }
        }
    } catch (error) {
        console.error('Health check failed:', error);
        updateStatus('error', 'Server offline');
    }
}

// Initialize
checkHealth();
