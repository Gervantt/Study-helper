# 📚 Study Helper — AI Exam Mode

AI-powered study companion built with a clean, layered architecture.
**Backend**: FastAPI (Python) with Service Layer pattern.
**Frontend**: React with component-based structure.
**AI**: Groq API (`openai/gpt-oss-120b`).

---

## 🏗 Architecture

```
study-helper/
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # App factory — wires everything together
│   │   ├── config.py                # Settings & environment variables
│   │   │
│   │   ├── routes/                  # Controller layer (handles HTTP)
│   │   │   ├── health.py
│   │   │   ├── quiz.py
│   │   │   ├── explain.py
│   │   │   ├── flashcards.py
│   │   │   └── chat.py
│   │   │
│   │   ├── schemas/                 # Request/Response models (Pydantic)
│   │   │   ├── quiz.py
│   │   │   ├── explain.py
│   │   │   ├── flashcards.py
│   │   │   └── chat.py
│   │   │
│   │   ├── services/                # Business logic layer
│   │   │   └── llm_service.py       # All LLM communication (swap-friendly)
│   │   │
│   │   └── prompts/                 # Prompt engineering layer
│   │       └── templates.py         # All AI prompts in one place
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html                   # Entry point — loads all modules
│   ├── css/
│   │   └── styles.css               # Design tokens + all styles
│   └── js/
│       ├── App.jsx                  # Root component (navigation)
│       ├── services/
│       │   └── api.js               # API service (all fetch calls)
│       └── components/
│           ├── Shared.jsx           # Reusable UI (Loader, Markdown)
│           ├── QuizTab.jsx          # Exam mode
│           ├── ExplainTab.jsx       # Topic explainer
│           ├── FlashcardsTab.jsx    # Flashcard generator
│           └── ChatTab.jsx          # Study chat
│
└── run.sh                           # One-command launcher
```

### Backend Layers

| Layer | Folder | Responsibility |
|-------|--------|----------------|
| **Routes** | `routes/` | HTTP handling, request validation, response shaping |
| **Schemas** | `schemas/` | Pydantic models for request/response types |
| **Services** | `services/` | Business logic, external API calls |
| **Prompts** | `prompts/` | All LLM prompt templates, easy to iterate |
| **Config** | `config.py` | Single source of truth for settings |

### Frontend Layers

| Layer | Folder | Responsibility |
|-------|--------|----------------|
| **Services** | `js/services/` | All backend API calls |
| **Components** | `js/components/` | UI components (one file per feature) |
| **Styles** | `css/` | Design tokens + component styles |
| **App** | `App.jsx` | Root layout and navigation |

### Swapping the AI Provider

Only **two files** need to change:

1. `app/config.py` — update URL, key, model name
2. `app/services/llm_service.py` — adjust request/response format

Routes, schemas, and prompts stay untouched.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip3 install -r backend/requirements.txt

# 2. (Optional) Set API key via env var
export GROQ_API_KEY="your-key-here"

# 3. Run
bash run.sh
```

Open **http://localhost:8000**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **📝 Exam Mode** | AI-generated quizzes — MCQ, True/False, Short Answer with scoring |
| **💡 Explain** | Topic explanations in 4 styles: Simple, Detailed, ELI5, Analogy |
| **🃏 Flashcards** | Auto-generated flip cards with hints |
| **💬 Chat** | Free-form study assistant conversation |

---

## 🔌 API Reference

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check + model info |
| `POST` | `/api/quiz` | Generate quiz questions |
| `POST` | `/api/check-answer` | Check user's answer |
| `POST` | `/api/explain` | Explain a topic |
| `POST` | `/api/flashcards` | Generate flashcards |
| `POST` | `/api/chat` | Study chat |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.9+, FastAPI, Uvicorn, httpx |
| **AI** | Groq API (openai/gpt-oss-120b) |
| **Frontend** | React 18, Babel standalone, marked.js |
| **Styling** | Custom CSS, dark theme, CSS variables |

---

## 📝 License

MIT
