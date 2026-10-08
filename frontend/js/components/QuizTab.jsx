/**
 * QuizTab — Exam mode with configurable quiz generation.
 * Phases: setup → quiz → results
 */

const QUICK_TOPICS = ['Data Structures', 'World History', 'Biology', 'Linear Algebra', 'Python', 'Physics'];

function QuizTab() {
  const [config, setConfig] = React.useState({
    topic: '', difficulty: 'medium', num_questions: 5, question_type: 'mixed'
  });
  const [questions, setQuestions] = React.useState([]);
  const [current, setCurrent]   = React.useState(0);
  const [answers, setAnswers]   = React.useState({});
  const [revealed, setRevealed] = React.useState({});
  const [shortInput, setShortInput] = React.useState('');
  const [loading, setLoading]   = React.useState(false);
  const [phase, setPhase]       = React.useState('setup');
  const [score, setScore]       = React.useState(0);

  // ── Actions ──────────────────────────────
  async function startQuiz() {
    if (!config.topic.trim()) return;
    setLoading(true);
    try {
      const data = await api.generateQuiz(config);
      if (data.questions) {
        setQuestions(data.questions);
        setCurrent(0);
        setAnswers({});
        setRevealed({});
        setPhase('quiz');
      }
    } catch (e) { alert('Error: ' + e.message); }
    setLoading(false);
  }

  function selectAnswer(qId, ans) {
    if (revealed[qId]) return;
    setAnswers(a => ({ ...a, [qId]: ans }));
  }

  function revealAnswer(qId) {
    setRevealed(r => ({ ...r, [qId]: true }));
  }

  function submitShortAnswer(q) {
    if (!shortInput.trim()) return;
    setAnswers(a => ({ ...a, [q.id]: shortInput.trim() }));
    setRevealed(r => ({ ...r, [q.id]: true }));
    setShortInput('');
  }

  function finishQuiz() {
    let correct = 0;
    questions.forEach(q => {
      const ua = answers[q.id];
      if (!ua) return;
      if (q.type === 'short_answer') {
        if (ua.toLowerCase().includes(q.correct_answer.toLowerCase().split(' ')[0])) correct++;
      } else {
        if (ua === q.correct_answer) correct++;
      }
    });
    setScore(correct);
    setPhase('results');
  }

  function resetQuiz() {
    setPhase('setup'); setQuestions([]); setAnswers({});
    setRevealed({}); setScore(0); setCurrent(0);
  }

  // ── Render: Setup ────────────────────────
  if (phase === 'setup') {
    return (
      <div>
        <div className="card">
          <div className="card-title">📝 Configure Your Quiz</div>

          <div className="form-group">
            <label className="form-label">Topic</label>
            <input className="form-input"
              placeholder="e.g. Photosynthesis, Binary Trees, World War II..."
              value={config.topic}
              onChange={e => setConfig(c => ({ ...c, topic: e.target.value }))}
              onKeyDown={e => e.key === 'Enter' && startQuiz()} />
          </div>

          <div className="tag-row">
            {QUICK_TOPICS.map(t => (
              <span key={t} className={`tag ${config.topic === t ? 'active' : ''}`}
                onClick={() => setConfig(c => ({ ...c, topic: t }))}>{t}</span>
            ))}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Difficulty</label>
              <select className="form-select" value={config.difficulty}
                onChange={e => setConfig(c => ({ ...c, difficulty: e.target.value }))}>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Questions</label>
              <select className="form-select" value={config.num_questions}
                onChange={e => setConfig(c => ({ ...c, num_questions: +e.target.value }))}>
                {[3,5,7,10].map(n => <option key={n} value={n}>{n}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Type</label>
              <select className="form-select" value={config.question_type}
                onChange={e => setConfig(c => ({ ...c, question_type: e.target.value }))}>
                <option value="mixed">Mixed</option>
                <option value="mcq">Multiple Choice</option>
                <option value="true_false">True / False</option>
                <option value="short_answer">Short Answer</option>
              </select>
            </div>
          </div>

          <button className="btn btn-primary btn-block" onClick={startQuiz}
            disabled={loading || !config.topic.trim()}>
            {loading ? <><InlineSpinner /> Generating...</> : '⚡ Generate Quiz'}
          </button>
        </div>
      </div>
    );
  }

  // ── Render: Results ──────────────────────
  if (phase === 'results') {
    const pct  = Math.round((score / questions.length) * 100);
    const tier = pct >= 80 ? 'great' : pct >= 50 ? 'ok' : 'bad';
    const msgs = { great: 'Excellent work! 🎉', ok: 'Good effort! Keep studying 💪', bad: "Keep going, you'll get there! 📚" };
    return (
      <div className="card score-card">
        <div className={`score-circle score-${tier}`}>{pct}%</div>
        <div className="score-label">{msgs[tier]}</div>
        <div className="score-sub">{score} out of {questions.length} correct</div>
        <div style={{ marginTop: 24, display: 'flex', gap: 12, justifyContent: 'center' }}>
          <button className="btn btn-primary" onClick={resetQuiz}>New Quiz</button>
          <button className="btn btn-ghost" onClick={() => { setPhase('quiz'); setCurrent(0); }}>Review Answers</button>
        </div>
      </div>
    );
  }

  // ── Render: Quiz ─────────────────────────
  const q = questions[current];
  if (!q) return <Loader />;
  const isRevealed = revealed[q.id];
  const userAnswer = answers[q.id];

  return (
    <div>
      <div className="quiz-progress">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${((current + 1) / questions.length) * 100}%` }} />
        </div>
        <span className="progress-text">{current + 1} / {questions.length}</span>
      </div>

      <div className="question-card">
        <div className="question-badge">
          {q.type === 'mcq' ? '🔘 Multiple Choice' : q.type === 'true_false' ? '✅ True / False' : '✏️ Short Answer'}
          &nbsp;· Q{q.id}
        </div>
        <div className="question-text">{q.question}</div>

        {q.type === 'short_answer' ? (
          <div>
            {!isRevealed ? (
              <div className="short-answer-wrap">
                <input className="form-input" placeholder="Type your answer..."
                  value={shortInput} onChange={e => setShortInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && submitShortAnswer(q)} />
                <button className="btn btn-primary" onClick={() => submitShortAnswer(q)}>Submit</button>
              </div>
            ) : (
              <div style={{ marginBottom: 12 }}>
                <div style={{ marginBottom: 6, color: '#8B8FA3', fontSize: 13 }}>
                  Your answer: <strong style={{ color: '#E8E9ED' }}>{userAnswer}</strong>
                </div>
                <div style={{ fontSize: 13, color: '#8B8FA3' }}>
                  Expected: <strong style={{ color: '#3DDC84' }}>{q.correct_answer}</strong>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div>
            {q.options.map((opt, i) => {
              const letter = q.type === 'true_false' ? opt : opt.charAt(0);
              let cls = 'option-btn';
              if (isRevealed) {
                if (letter === q.correct_answer || opt === q.correct_answer) cls += ' correct';
                else if (letter === userAnswer || opt === userAnswer) cls += ' wrong';
              } else if (userAnswer === letter || userAnswer === opt) {
                cls += ' selected';
              }
              return (
                <button key={i} className={cls} disabled={isRevealed}
                  onClick={() => selectAnswer(q.id, q.type === 'true_false' ? opt : letter)}>
                  <span className="option-letter">
                    {q.type === 'true_false' ? (i === 0 ? 'T' : 'F') : String.fromCharCode(65 + i)}
                  </span>
                  <span>{q.type === 'true_false' ? opt : opt.slice(3)}</span>
                </button>
              );
            })}
          </div>
        )}

        {!isRevealed && q.type !== 'short_answer' && (
          <button className="btn btn-ghost btn-sm" style={{ marginTop: 8 }}
            disabled={!userAnswer} onClick={() => revealAnswer(q.id)}>Check Answer</button>
        )}

        {isRevealed && q.explanation && (
          <div className="explanation-box">💡 {q.explanation}</div>
        )}
      </div>

      <div style={{ display: 'flex', gap: 12, justifyContent: 'space-between' }}>
        <button className="btn btn-ghost" disabled={current === 0}
          onClick={() => setCurrent(c => c - 1)}>← Previous</button>
        {current < questions.length - 1
          ? <button className="btn btn-primary" onClick={() => setCurrent(c => c + 1)}>Next →</button>
          : <button className="btn btn-primary" onClick={finishQuiz}>Finish Quiz 🏁</button>
        }
      </div>
    </div>
  );
}
