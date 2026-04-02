#!/bin/bash
cd "$(dirname "$0")"

echo "📚 Study Helper — Starting..."
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r backend/requirements.txt --break-system-packages -q 2>/dev/null

# Start server
echo ""
echo "🚀 Server starting at http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
