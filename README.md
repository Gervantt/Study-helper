# 📚 Study Helper — AI Exam Mode

AI-powered study tool with quiz generation, explanations, flashcards, and a chat tutor.  
Built with **FastAPI** + **React** + **Google Gemini 2.0 Flash** (free tier).

## Features

| Feature | Description |
|---------|-------------|
| **📝 Exam Mode** | Generate quizzes on any topic — MCQ, True/False, Short Answer |
| **💡 Explain** | Get explanations in 4 styles: Simple, Detailed, ELI5, Analogy |
| **🃏 Flashcards** | Auto-generate flip cards for any topic |
| **💬 Chat** | Free-form study assistant chat |

## Quick Start

```bash
# 1. Install Python dependencies
pip install -r backend/requirements.txt

# 2. (Optional) Set your own API key
export GEMINI_API_KEY="your-key-here"

# 3. Run
bash run.sh
```

Then open **http://localhost:8000** in your browser.

## Project Structure

```
study-helper/
├── backend/
│   ├── main.py              # FastAPI server + Gemini integration
│   └── requirements.txt
├── frontend/
│   └── index.html           # React SPA (single file)
├── run.sh                   # One-command launcher
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/quiz` | Generate quiz questions |
| POST | `/api/explain` | Explain a topic |
| POST | `/api/check-answer` | Check a user's answer |
| POST | `/api/flashcards` | Generate flashcards |
| POST | `/api/chat` | Study assistant chat |
| GET | `/api/health` | Health check |

## Tech Stack

- **Backend**: Python, FastAPI, google-generativeai
- **Frontend**: React 18, Babel (in-browser), marked.js
- **AI**: Google Gemini 2.0 Flash (free tier)
- **Styling**: Custom CSS, dark theme

## Changing API Key

Either set the environment variable:
```bash
export GEMINI_API_KEY="your-key"
```

Or edit `backend/main.py` line 12 directly.
