import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const analyzeCode = async () => {
    if (!code.trim()) {
      setResult("Please enter some code first.");
      return;
    }

    try {
      setLoading(true);
      setResult("Analyzing...");

      const response = await axios.post(
        "https://ai-debugger-kdoe.onrender.com/debug",
        {
          code: code,
        }
      );

      setResult(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error(error);

      if (error.response) {
        setResult(
          `Server Error:\n${JSON.stringify(
            error.response.data,
            null,
            2
          )}`
        );
      } else if (error.request) {
        setResult(
          "Cannot connect to backend. Check if Render backend is running."
        );
      } else {
        setResult(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🤖 AI Code Debugging Assistant</h1>

      <textarea
        placeholder="Paste your buggy code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <button onClick={analyzeCode} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Code"}
      </button>

      <div className="result">
        <h2>Result</h2>
        <pre>{result}</pre>
      </div>
    </div>
  );
}

export default App;