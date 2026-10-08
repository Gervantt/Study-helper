/**
 * API Service — single point of contact with the backend.
 * Every fetch lives here so components never touch URLs directly.
 */
const api = (() => {
  const BASE = '';   // same-origin

  async function _post(path, body) {
    const res = await fetch(`${BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Request failed');
    }
    return res.json();
  }

  return {
    generateQuiz:    (opts) => _post('/api/quiz', opts),
    explainTopic:    (opts) => _post('/api/explain', opts),
    checkAnswer:     (opts) => _post('/api/check-answer', opts),
    generateFlashcards: (opts) => _post('/api/flashcards', opts),
    sendChat:        (opts) => _post('/api/chat', opts),
  };
})();
