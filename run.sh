#!/bin/bash
cd "$(dirname "$0")"

echo "📚 Study Helper — Starting..."
echo ""
echo "📦 Installing dependencies..."
pip3 install -r backend/requirements.txt -q 2>/dev/null

echo ""
echo "🚀 Server starting at http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""
cd backend
[ -f .env ] && set -a && . ./.env && set +a
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
