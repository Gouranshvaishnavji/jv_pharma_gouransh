
import React, { useState } from "react";
import api from "../api/client";

function ChatBox() {
  const [sessionId, setSessionId] = useState(null);
  const [query, setQuery] = useState("");
  const [log, setLog] = useState([]);

  const startSession = async () => {
    const res = await api.post("/chat/new_session");
    setSessionId(res.data.session_id);
  };

  const sendQuery = async () => {
    if (!query.trim()) return;

    const res = await api.post("/chat/ask", {
      query,
      session_id: sessionId,
    });

    setLog((old) => [
      ...old,
      { role: "user", text: query },
      { role: "assistant", text: res.data.answer, citations: res.data.citations },
    ]);

    setQuery("");
  };

  return (
    <div>
      <h3>Chat Assistant</h3>

      {sessionId ? (
        <p>Session: {sessionId}</p>
      ) : (
        <button onClick={startSession}>Start Chat Session</button>
      )}

      <input
        type="text"
        placeholder="Ask something..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={sendQuery}>Send</button>

      <div style={{ marginTop: 20 }}>
        {log.map((m, i) => (
          <div key={i} style={{ marginBottom: 15 }}>
            <strong>{m.role === "user" ? "You" : "Assistant"}:</strong>
            <p>{m.text}</p>

            {m.citations &&
              m.citations.length > 0 &&
              m.citations.map((c, j) => (
                <pre
                  key={j}
                  style={{ background: "#f7f7f7", padding: 10 }}
                >
                  {JSON.stringify(c, null, 2)}
                </pre>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatBox;
