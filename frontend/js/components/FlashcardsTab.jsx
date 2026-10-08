/**
 * FlashcardsTab — AI-generated flip cards with navigation.
 */

function FlashcardsTab() {
  const [topic, setTopic]     = React.useState('');
  const [count, setCount]     = React.useState(10);
  const [cards, setCards]     = React.useState([]);
  const [idx, setIdx]         = React.useState(0);
  const [flipped, setFlipped] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  async function generate() {
    if (!topic.trim()) return;
    setLoading(true);
    try {
      const data = await api.generateFlashcards({ topic, count });
      setCards(data.cards || []);
      setIdx(0);
      setFlipped(false);
    } catch (e) { alert('Error: ' + e.message); }
    setLoading(false);
  }

  function nav(dir) {
    setFlipped(false);
    setTimeout(() => setIdx(i => Math.max(0, Math.min(cards.length - 1, i + dir))), 150);
  }

  // ── Setup phase ──────────────────────────
  if (!cards.length) {
    return (
      <div className="card">
        <div className="card-title">🃏 Flashcard Generator</div>

        <div className="form-group">
          <label className="form-label">Topic</label>
          <input className="form-input"
            placeholder="e.g. JavaScript closures, Cell biology..."
            value={topic} onChange={e => setTopic(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && generate()} />
        </div>

        <div className="form-group">
          <label className="form-label">Number of Cards</label>
          <select className="form-select" value={count}
            onChange={e => setCount(+e.target.value)}>
            {[5, 10, 15, 20].map(n => <option key={n} value={n}>{n}</option>)}
          </select>
        </div>

        <button className="btn btn-primary btn-block" onClick={generate}
          disabled={loading || !topic.trim()}>
          {loading ? <><InlineSpinner /> Generating...</> : 'Generate Flashcards 🃏'}
        </button>
      </div>
    );
  }

  // ── Card viewer ──────────────────────────
  const c = cards[idx];
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <span style={{ fontSize: 14, color: '#8B8FA3' }}>
          Topic: <strong style={{ color: '#E8E9ED' }}>{topic}</strong>
        </span>
        <button className="btn btn-ghost btn-sm"
          onClick={() => { setCards([]); setFlipped(false); }}>New Set</button>
      </div>

      <div className="flashcard-scene" onClick={() => setFlipped(f => !f)}>
        <div className={`flashcard ${flipped ? 'flipped' : ''}`}>
          <div className="flashcard-face">
            <div className="flashcard-label">Question</div>
            <div className="flashcard-content">{c.front}</div>
            <div className="flashcard-hint">💡 Hint: {c.hint}</div>
          </div>
          <div className="flashcard-face flashcard-back">
            <div className="flashcard-label">Answer</div>
            <div className="flashcard-content">{c.back}</div>
          </div>
        </div>
      </div>

      <div className="flashcard-nav">
        <button className="btn btn-ghost btn-sm" disabled={idx === 0} onClick={() => nav(-1)}>←</button>
        <span className="flashcard-counter">{idx + 1} / {cards.length}</span>
        <button className="btn btn-ghost btn-sm" disabled={idx === cards.length - 1} onClick={() => nav(1)}>→</button>
      </div>
      <div style={{ textAlign: 'center', marginTop: 8, fontSize: 13, color: '#5C6078' }}>Click card to flip</div>
    </div>
  );
}
