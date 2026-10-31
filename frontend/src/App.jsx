import { useState, useEffect } from "react";

export default function App() {
  const [resume, setResume] = useState("");
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  async function loadHistory() {
    const res = await fetch("http://127.0.0.1:8000/history");
    setHistory(await res.json());
  }

  useEffect(() => {
    loadHistory();
  }, []);


  async function handleSubmit() {
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume, jd }),
    });
    setResult(await res.json());
     loadHistory(); 
  }

  async function handleUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
  formData.append("jd", jd);
  const res = await fetch("http://127.0.0.1:8000/analyze-pdf", {
    method: "POST",
    body: formData,
  });
  setResult(await res.json());
  loadHistory();
}

  return (
    <div style={{ maxWidth: 800, margin: "auto", padding: 20 }}>
      <h1>Resume Matcher</h1>
      <textarea rows={8} style={{ width: "100%" }} placeholder="Paste resume"
        value={resume} onChange={(e) => setResume(e.target.value)} />
      <textarea rows={8} style={{ width: "100%", marginTop: 10 }} placeholder="Paste job description"
        value={jd} onChange={(e) => setJd(e.target.value)} />
      <p>Or upload resume PDF:</p>
      <input type="file" accept=".pdf" onChange={handleUpload} />
      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div>
          <h2>Match Score: {result.score}%</h2>
          <h3>Matched Skills</h3>
          <ul>{result.matched.map((s) => <li key={s}>{s}</li>)}</ul>
          <h3>Missing Skills</h3>
          <ul>{result.missing.map((s) => <li key={s}>{s}</li>)}</ul>
        </div>
      )}

      <h2>History</h2>
      <table border="1" cellPadding="6" style={{ width: "100%" }}>
        <thead>
          <tr><th>ID</th><th>Score</th><th>Matched</th><th>Missing</th><th>Date</th></tr>
        </thead>
        <tbody>
          {history.map((h) => (
            <tr key={h.id}>
              <td>{h.id}</td>
              <td>{h.score}%</td>
              <td>{h.matched}</td>
              <td>{h.missing}</td>
              <td>{h.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}