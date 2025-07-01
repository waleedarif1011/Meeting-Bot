#!/bin/bash

# Start the development environment
echo "Starting Meeting Bot Development Environment..."

# Function to handle cleanup on exit
cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start Flask backend
echo "Starting Flask backend on port 5000..."
python server.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 2

# Start frontend server
echo "Starting frontend server on port 3000..."
cd frontend
http-server -p 3000 --cors -o &
FRONTEND_PID=$!

echo ""
echo "✅ Development environment started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for background processes
wait
