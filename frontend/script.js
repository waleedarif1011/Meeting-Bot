// Configuration — prefer window.API_BASE_URL from config.js
const API_BASE_URL = window.API_BASE_URL || "http://localhost:5000";
let sessionId = generateSessionId();

function generateSessionId() {
    return "session_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
}

async function uploadTranscript() {
    const transcriptInput = document.getElementById("transcript-input");
    const uploadBtn = document.getElementById("upload-btn");
    const transcript = transcriptInput.value.trim();

    if (!transcript) {
        showStatus("Please enter a transcript before uploading.", "error");
        return;
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";
    showStatus("Uploading transcript...", "info");

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ transcript, session_id: sessionId }),
        });

        const data = await response.json();

        if (response.ok) {
            showStatus("Transcript uploaded successfully!", "success");
            transcriptInput.value = "";
            addSystemMessage("Transcript uploaded. You can now ask questions about the meeting.");
        } else {
            showStatus(`Error: ${data.error || "Failed to upload transcript"}`, "error");
        }
    } catch (error) {
        showStatus(`Network error: ${error.message}`, "error");
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = "Upload Transcript";
    }
}

async function loadSampleMeeting() {
    const sampleBtn = document.getElementById("sample-btn");
    const transcriptInput = document.getElementById("transcript-input");

    sampleBtn.disabled = true;
    sampleBtn.textContent = "Loading sample...";
    showStatus("Loading sample meeting...", "info");

    try {
        const response = await fetch(`${API_BASE_URL}/sample`);
        const data = await response.json();

        if (!response.ok || !data.transcript) {
            showStatus(`Error: ${data.error || "Failed to load sample"}`, "error");
            return;
        }

        transcriptInput.value = data.transcript;

        const uploadResponse = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                transcript: data.transcript,
                session_id: sessionId,
            }),
        });

        const uploadData = await uploadResponse.json();

        if (uploadResponse.ok) {
            showStatus("Sample meeting loaded. Ask away!", "success");
            addSystemMessage("Sample Q4 Planning transcript loaded. Try: What were the action items?");
        } else {
            showStatus(`Error: ${uploadData.error || "Failed to upload sample"}`, "error");
        }
    } catch (error) {
        showStatus(`Network error: ${error.message}`, "error");
    } finally {
        sampleBtn.disabled = false;
        sampleBtn.textContent = "Load sample meeting";
    }
}

async function sendMessage() {
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const message = chatInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");
    chatInput.value = "";
    sendBtn.disabled = true;
    sendBtn.textContent = "Sending...";

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, session_id: sessionId }),
        });

        const data = await response.json();

        if (response.ok) {
            addMessage(data.response, "bot");
        } else {
            addMessage(`Error: ${data.error || "Failed to get response"}`, "error");
        }
    } catch (error) {
        addMessage(`Network error: ${error.message}`, "error");
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = "Send";
    }
}

function handleChatKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById("chat-messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;

    const timestamp = new Date().toLocaleTimeString();
    const labels = { user: "You", bot: "Assistant", error: "Error" };

    messageDiv.innerHTML = `
        <div class="message-header">${labels[sender] || sender} <span class="timestamp">${timestamp}</span></div>
        <div class="message-content">${escapeHtml(text)}</div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addSystemMessage(text) {
    const chatMessages = document.getElementById("chat-messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = "message system";
    const timestamp = new Date().toLocaleTimeString();
    messageDiv.innerHTML = `
        <div class="message-header">System <span class="timestamp">${timestamp}</span></div>
        <div class="message-content">${escapeHtml(text)}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showStatus(message, type) {
    const statusDiv = document.getElementById("upload-status");
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;

    if (type === "success" || type === "info") {
        setTimeout(() => {
            statusDiv.textContent = "";
            statusDiv.className = "status-message";
        }, 5000);
    }
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

document.addEventListener("DOMContentLoaded", function () {
    addSystemMessage(`Session started. Upload a transcript or load the sample meeting to begin.`);
});
