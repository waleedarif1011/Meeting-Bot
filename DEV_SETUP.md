# Development Environment Setup

This project contains a Meeting Bot with both a Flask backend and a static frontend.

## Opening the Project with Devcontainer

### Steps to Open in VS Code

1. **Install Docker and VS Code**: Make sure you have Docker and Visual Studio Code installed on your machine.
2. **Install the Remote Development Extension Pack**:
   - Open VS Code and go to the Extensions view (`Ctrl+Shift+X`).
   - Search for "Remote Development" and install the extension pack by Microsoft.
3. **Open the Project Folder**:
   - Open VS Code and navigate to `File > Open Folder...`.
   - Select the `meeting-bot` project directory and click `Open`.
4. **Reopen in Container**:
   - You should see a notification asking to "Reopen in Container". Click this.
   - If not prompted, you can also press `F1` and select `Remote-Containers: Reopen in Container`.
5. **Wait for Setup**:
   - VS Code will now build the devcontainer and set up the environment.
   - Once completed, you will be connected to the development environment with all necessary dependencies installed automatically.

### Start Development

- Your devcontainer is set up to forward ports and install all required extensions automatically.
- You can now run the development script or start the servers manually as previously described.

## Quick Start

### Using the Development Script (Recommended)

The easiest way to start both servers is using the provided script:

```bash
./start-dev.sh
```

This will start:
- Flask backend on port 5000 (API endpoints)
- Frontend web server on port 3000 (user interface)

The script will automatically open your browser to the frontend at `http://localhost:3000`.

### Manual Setup

If you prefer to start the servers manually:

#### 1. Start the Flask Backend
```bash
python server.py
```
The API will be available at `http://localhost:5000`

#### 2. Start the Frontend Server
In a new terminal:
```bash
cd frontend
http-server -p 3000 --cors
```
The frontend will be available at `http://localhost:3000`

## Port Configuration

- **Port 3000**: Frontend web interface
- **Port 5000**: Flask backend API

Both ports are automatically forwarded when using the devcontainer.

## Architecture

```
┌─────────────────┐    HTTP requests    ┌──────────────────┐
│   Frontend      │────────────────────▶│   Flask Backend  │
│   (port 3000)   │                     │   (port 5000)    │
│                 │◀────────────────────│                  │
│   HTML/CSS/JS   │    JSON responses   │   Python/Flask   │
└─────────────────┘                     └──────────────────┘
```

The frontend makes API calls to `http://localhost:5000` for:
- `/upload` - Upload meeting transcripts
- `/chat` - Chat with the AI assistant

## Development Notes

- The frontend is served using `http-server` with CORS enabled
- Both servers support hot reloading during development
- Use Ctrl+C to stop both servers when using the development script
