// JS Chat Engine for Smarty AI Consultant

// Keep track of active message logs
let chatHistory = [];

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("chat-input");
    if (input) {
        // Auto focus input
        input.focus();
    }
});

function scrollChatToBottom() {
    const chatWindow = document.getElementById("chat-window");
    if (chatWindow) {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
}

function clearChatHistory() {
    if(confirm("Are you sure you want to clear your current conversation history?")) {
        const chatWindow = document.getElementById("chat-window");
        // Clear all except the first assistant welcome bubble
        const bubbles = chatWindow.querySelectorAll(".chat-bubble-user, .chat-bubble-ai");
        for (let i = 1; i < bubbles.length; i++) {
            bubbles[i].remove();
        }
        chatHistory = [];
        scrollChatToBottom();
    }
}

function appendMessage(sender, text) {
    const chatWindow = document.getElementById("chat-window");
    if (!chatWindow) return;
    
    const bubble = document.createElement("div");
    
    if (sender === "user") {
        bubble.className = "chat-bubble-user flex items-start gap-3 max-w-[80%] ml-auto";
        bubble.innerHTML = `
            <div class="w-8 h-8 rounded-lg bg-emerald-500 text-white flex items-center justify-center text-sm shrink-0">
                <i class="fa-solid fa-user"></i>
            </div>
            <div class="bg-emerald-500 text-white p-4 rounded-3xl rounded-tr-none border border-emerald-600 shadow-sm text-sm leading-relaxed">
                ${escapeHtml(text)}
            </div>
        `;
    } else {
        bubble.className = "chat-bubble-ai flex items-start gap-3 max-w-[80%]";
        // Format simple Markdown highlights (strong bold text)
        const formattedText = parseBasicMarkdown(text);
        
        bubble.innerHTML = `
            <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-600 flex items-center justify-center text-sm shrink-0">
                <i class="fa-solid fa-robot"></i>
            </div>
            <div class="bg-white p-4 rounded-3xl rounded-tl-none border border-slate-100 shadow-sm text-sm text-slate-700 leading-relaxed">
                ${formattedText}
            </div>
        `;
    }
    
    chatWindow.appendChild(bubble);
    scrollChatToBottom();
}

function handleChatSubmit(event) {
    event.preventDefault();
    const input = document.getElementById("chat-input");
    const message = input.value.trim();
    if (!message) return;
    
    input.value = "";
    sendMessageToAI(message);
}

function sendSuggestedPrompt(text) {
    sendMessageToAI(text);
}

function sendMessageToAI(message) {
    // 1. Render User bubble
    appendMessage("user", message);
    
    // 2. Display Typing loader
    const indicator = document.getElementById("typing-indicator");
    if (indicator) indicator.classList.remove("hidden");
    scrollChatToBottom();
    
    // 3. Dispatch AJAX JSON call to Flask
    fetch(window.chatApiEndpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message,
            history: chatHistory
        })
    })
    .then(response => {
        if (!response.ok) throw new Error("Network Response error");
        return response.json();
    })
    .then(data => {
        // Hide loader
        if (indicator) indicator.classList.add("hidden");
        
        // Render AI bubble
        appendMessage("ai", data.response);
        
        // Append values to locally tracked history list
        chatHistory.push({ "role": "user", "content": message });
        chatHistory.push({ "role": "assistant", "content": data.response });
    })
    .catch(error => {
        if (indicator) indicator.classList.add("hidden");
        console.error("Chat failure:", error);
        appendMessage("ai", "⚠️ I encountered an error communicating with the energy analysis server. Please check your local connection parameters and try again.");
    });
}

// Security HTML sanitization helper
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Simple Markdown Bold & Bullet highlighter
function parseBasicMarkdown(text) {
    let html = escapeHtml(text);
    // Replace **bold**
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Replace bullet listings starting with * or - or •
    html = html.replace(/^\s*[\*\-•]\s+(.*?)$/gm, '• $1<br>');
    // Replace double newlines with breaks
    html = html.replace(/\n/g, '<br>');
    return html;
}
