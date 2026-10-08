/**
 * App — Root component. Manages tab navigation.
 */

const TABS = [
  { key: 'quiz',       label: 'Exam Mode',  icon: '📝' },
  { key: 'explain',    label: 'Explain',     icon: '💡' },
  { key: 'flashcards', label: 'Flashcards',  icon: '🃏' },
  { key: 'chat',       label: 'Chat',        icon: '💬' },
];

function App() {
  const [tab, setTab] = React.useState('quiz');

  return (
    <div className="app">
      <div className="header">
        <div className="header-icon">📚</div>
        <h1>Study Helper</h1>
        <p>AI-powered exam prep — quizzes, explanations & flashcards</p>
      </div>

      <nav className="nav">
        {TABS.map(t => (
          <button key={t.key}
            className={tab === t.key ? 'active' : ''}
            onClick={() => setTab(t.key)}>
            <span className="nav-emoji">{t.icon}</span> {t.label}
          </button>
        ))}
      </nav>

      {tab === 'quiz'       && <QuizTab />}
      {tab === 'explain'    && <ExplainTab />}
      {tab === 'flashcards' && <FlashcardsTab />}
      {tab === 'chat'       && <ChatTab />}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
