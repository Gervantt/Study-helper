/**
 * Shared UI Components — reusable across all tabs.
 */

function Md({ text }) {
  if (!text) return null;
  const html = marked.parse(text, { breaks: true });
  return <div className="md-content" dangerouslySetInnerHTML={{ __html: html }} />;
}

function Loader({ text = "Generating..." }) {
  return (
    <div className="loader">
      <div className="spinner" />
      {text}
    </div>
  );
}

function InlineSpinner() {
  return <div className="spinner spinner-sm" style={{ display: 'inline-block' }} />;
}
