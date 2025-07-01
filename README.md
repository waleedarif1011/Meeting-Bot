# Meeting Bot Assessment

A minimalistic meeting transcript analysis application that allows users to upload meeting transcripts and chat with an AI assistant about the contents. This is a coding assessment project designed to evaluate full-stack AI development skills.

## 🏗️ Project Structure

```
meeting-bot/
├── frontend/
│   ├── index.html                # Chat UI and transcript upload interface
│   ├── script.js                 # Handles sending chat messages and uploads
│   └── style.css                 # Minimal styling
├── chatbot/
│   └── engine.py                 # Python chatbot logic — YOUR TASK
├── server.py                     # Flask server with `/chat` and `/upload` endpoints
├── devcontainer.json             # VS Code Dev Container definition
├── Dockerfile                    # Python 3 + Flask environment
├── requirements.txt              # Flask and other Python deps
└── README.md                     # This file
```

## 🚀 Quick Start

### Option 1: Using VS Code Dev Container (Recommended) - Zero Setup!

**Prerequisites**: 
- [Docker](https://www.docker.com/get-started) installed
- [VS Code](https://code.visualstudio.com/) with [Remote Development Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

**Setup Steps (30 seconds)**:

1. **Open in VS Code**
   ```bash
   code meeting-bot  # Or File > Open Folder in VS Code
   ```

2. **Reopen in Container**
   - VS Code will show: "Folder contains a Dev Container configuration file. Reopen folder to develop in a container"
   - Click **"Reopen in Container"**
   - Alternative: Press `F1` → "Remote-Containers: Reopen in Container"

3. **Wait for automatic setup** (first time only)
   - Docker builds the development environment
   - All dependencies install automatically
   - VS Code extensions configure automatically

4. **Start both frontend and backend**
   ```bash
   ./start-dev.sh
   ```

5. **Access the application**
   - Frontend: http://localhost:3000 (opens automatically)
   - Backend API: http://localhost:5000

**That's it! 🎉 Ready to code your AI engine.**

**Devcontainer Features**:
- ✅ Python 3.11 + Flask pre-installed
- ✅ Node.js + http-server for frontend
- ✅ Automatic port forwarding (3000, 5000)
- ✅ VS Code extensions (Python, Copilot, Git tools)
- ✅ Zero manual dependency installation


### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py

# Open frontend/index.html in your browser with live server
```

## 🎯 Your Task

**Primary Goal**: Implement intelligent meeting transcript analysis in `chatbot/engine.py`

### What's Already Built

✅ **Frontend**: Clean chat interface with transcript upload  
✅ **Backend**: Flask server with session management  
✅ **Infrastructure**: Docker + Dev Container setup  
✅ **Session Handling**: In-memory storage with session IDs  

### What You Need to Build

🔨 **Replace the placeholder `respond()` function** in `chatbot/engine.py` with your AI implementation.

**Expected Capabilities**:
- Analyze uploaded meeting transcripts
- Answer questions about meeting content
- Extract key information (action items, decisions, participants)
- Maintain conversation context
- Provide summaries and insights

### Sample Interactions

```
User: "What were the main topics discussed?"
Bot: [Analyze transcript and list key topics]

User: "What action items were assigned?"
Bot: [Extract and list action items with assignees]

User: "Who participated in this meeting?"
Bot: [Identify and list participants]

User: "Summarize the key decisions made"
Bot: [Provide summary of decisions]
```


**Add your dependencies** to `requirements.txt` as needed.

## 🔧 System Architecture

```
[Frontend] ──HTTP──> [Flask Server] ──Python──> [Your AI Engine]
    │                      │                         │
    │                      │                         │
    └── Chat UI            └── Session Management    └── Transcript Analysis
        Upload Interface       Memory Storage            Response Generation
```

### API Endpoints

- **POST `/upload`**: Upload meeting transcript
  ```json
  {
    "transcript": "Meeting transcript text...",
    "session_id": "session_abc123"
  }
  ```

- **POST `/chat`**: Send chat message
  ```json
  {
    "message": "What were the action items?",
    "session_id": "session_abc123"
  }
  ```

### Session Data Structure

```python
session_data = {
    'transcript': 'Full meeting transcript text',
    'chat_history': [
        {'sender': 'user', 'content': 'User message'},
        {'sender': 'bot', 'content': 'Bot response'}
    ],
    'session_id': 'unique_session_identifier'
}
```

## 🎨 Evaluation Criteria

- **Functionality**: Does the bot provide useful meeting insights?
- **Code Quality**: Clean, readable, well-structured code
- **AI Integration**: Effective use of AI/ML techniques
- **User Experience**: Helpful and contextual responses
- **Error Handling**: Graceful handling of edge cases
- **Documentation**: Clear comments and approach explanation

## 📝 Submission Guidelines

1. **Implement your solution** in `chatbot/engine.py`
2. **Update `requirements.txt`** with any new dependencies
3. **Test thoroughly** with various transcript types
4. **Document your approach** in the [chatbot/README.md](./chatbot/README.md)
5. **Ensure it runs** in the provided dev container

## 🔍 Testing Your Solution

1. **Start the server**: `python server.py`
2. **Open frontend**: `frontend/index.html`
3. **Upload a sample transcript**
4. **Test various questions**:
   - "Summarize this meeting"
   - "What action items were discussed?"
   - "Who were the key participants?"
   - "What decisions were made?"

## 📋 Sample Meeting Transcript

```
Meeting: Q4 Planning Session
Date: 2024-01-15
Attendees: Sarah (Product Manager), Mike (Engineer), Lisa (Designer)

Sarah: Let's discuss our Q4 roadmap. We need to prioritize the new user dashboard.
Mike: I can start working on the backend APIs. Should take about 3 weeks.
Lisa: I'll handle the UI mockups. Can have them ready by Friday.
Sarah: Great. Mike, can you also look into the performance issues we discussed?
Mike: Absolutely. I'll investigate the database queries this week.
Lisa: Should we schedule a design review for next Tuesday?
Sarah: Yes, let's do that. I'll send out calendar invites.

Action Items:
- Mike: Develop backend APIs (3 weeks)
- Lisa: Create UI mockups (by Friday)
- Mike: Investigate database performance (this week)
- Sarah: Schedule design review for next Tuesday
```

## 🛠️ Development Tips

- **Start simple**: Basic keyword matching, then enhance
- **Use the helper functions**: Provided scaffolding in `engine.py`
- **Test incrementally**: Add features one at a time
- **Handle edge cases**: Empty transcripts, invalid input
- **Consider context**: Use chat history for better responses

## 🤝 Support

If you encounter technical issues with the setup:
1. Check that all dependencies are installed
2. Verify the server is running on port 5000
3. Ensure CORS is properly configured
4. Check browser console for frontend errors

---

**Ready to code?** Open `chatbot/engine.py` and start building! 🚀
