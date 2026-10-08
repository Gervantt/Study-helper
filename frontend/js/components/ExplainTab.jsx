/**
 * ExplainTab — Topic explanations in multiple styles.
 */

const EXPLAIN_STYLES = [
  { key: 'simple',   label: '🎯 Simple',   desc: 'Clear & concise' },
  { key: 'detailed', label: '📖 Detailed', desc: 'In-depth' },
  { key: 'eli5',     label: '👶 ELI5',     desc: "Like I'm 5" },
  { key: 'analogy',  label: '🔗 Analogy',  desc: 'Real-world comparisons' },
];

function ExplainTab() {
  const [topic, setTopic]     = React.useState('');
  const [style, setStyle]     = React.useState('simple');
  const [result, setResult]   = React.useState('');
  const [loading, setLoading] = React.useState(false);

  async function explain() {
    if (!topic.trim()) return;
    setLoading(true);
    try {
      const data = await api.explainTopic({ topic, style });
      setResult(data.explanation);
    } catch (e) { alert('Error: ' + e.message); }
    setLoading(false);
  }

  return (
    <div>
      <div className="card">
        <div className="card-title">💡 Explain a Topic</div>

        <div className="form-group">
          <label className="form-label">What do you want to understand?</label>
          <input className="form-input"
            placeholder="e.g. Recursion, Quantum entanglement, Supply & demand..."
            value={topic} onChange={e => setTopic(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && explain()} />
        </div>

        <div className="form-group">
          <label className="form-label">Explanation Style</label>
          <div className="tag-row">
            {EXPLAIN_STYLES.map(s => (
              <span key={s.key} className={`tag ${style === s.key ? 'active' : ''}`}
                onClick={() => setStyle(s.key)}>{s.label}</span>
            ))}
          </div>
        </div>

        <button className="btn btn-primary btn-block" onClick={explain}
          disabled={loading || !topic.trim()}>
          {loading ? <><InlineSpinner /> Explaining...</> : 'Explain It ✨'}
        </button>
      </div>

      {loading && <Loader text="Thinking..." />}

      {result && (
        <div className="card">
          <Md text={result} />
        </div>
      )}
    </div>
  );
}
