/**
 * ChatTab — Free-form study assistant conversation.
 */

const INITIAL_MESSAGE = {
  role: 'bot',
  text: "Hey! 👋 I'm your study assistant. Ask me anything — I'll explain concepts, help with problems, or quiz you on the spot.",
};

function ChatTab() {
  const [messages, setMessages] = React.useState([INITIAL_MESSAGE]);
  const [input, setInput]       = React.useState('');
  const [loading, setLoading]   = React.useState(false);
  const bottomRef = React.useRef(null);

  React.useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function send() {
    if (!input.trim() || loading) return;
    const msg = input.trim();
    setInput('');
    setMessages(m => [...m, { role: 'user', text: msg }]);
    setLoading(true);
    try {
      const data = await api.sendChat({ message: msg });
      setMessages(m => [...m, { role: 'bot', text: data.response }]);
    } catch {
      setMessages(m => [...m, { role: 'bot', text: 'Sorry, something went wrong. Please try again.' }]);
    }
    setLoading(false);
  }

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '580px' }}>
      <div className="card-title">💬 Study Chat</div>

      <div className="chat-messages" style={{ flex: 1 }}>
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role}`}>
            {m.role === 'bot' ? <Md text={m.text} /> : m.text}
          </div>
        ))}
        {loading && (
          <div className="chat-msg bot"><Loader text="Thinking..." /></div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <input className="form-input"
          placeholder="Ask anything about your studies..."
          value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()} />
        <button className="btn btn-primary" onClick={send}
          disabled={loading || !input.trim()}>Send</button>
      </div>
    </div>
  );
}
