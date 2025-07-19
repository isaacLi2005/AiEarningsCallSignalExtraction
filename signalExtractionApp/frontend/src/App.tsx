import { useEffect, useState } from "react";

import TickerSelectForm from "./components/tickerSelect";
import SentimentChart   from "./components/sentimentChart";
import KeywordsList     from "./components/keywordsList";

const backendURL = import.meta.env.VITE_BACKEND_URL;

function App() {
  const [backendResult, setBackendResult] = useState<string | object>(
    "Waiting for ticker selection…"
  );

  function fetchTickerData(ticker: string) {
    setBackendResult("Loading…");
    fetch(`${backendURL}/analyze_last_n_quarters_sentiment?ticker=${ticker}&n=4`)
      .then((res) => res.json())
      .then((data) => setBackendResult(data.results))
      .catch((err) => {
        console.error("Error contacting backend:", err);
        setBackendResult("Backend unreachable or error.");
      });
  }

  function handleTickerSubmit(ticker: string) {
    fetchTickerData(ticker);
  }

  /* ----------  render prep  ---------- */
  let sentimentContent, keywordContent;
  if (typeof backendResult === "object" && backendResult !== null) {
    const sentimentChartData = Object.entries(backendResult).map(
      ([quarter, entry]: any) => ({
        quarter,
        management: entry.management_sentiment,
        qa: entry.qa_sentiment,
      })
    );
    sentimentContent = <SentimentChart data={sentimentChartData} />;
    keywordContent   = <KeywordsList  data={backendResult}        />;
  } else {
    sentimentContent = <p>{backendResult ?? "Please select a ticker."}</p>;
    keywordContent   = <p>😺</p>;
  }

  /* ----------  JSX  ---------- */
  return (
    <main style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h1>AI Earnings Signal</h1>

      <TickerSelectForm onSubmit={handleTickerSubmit} />

      {/* full‑width two‑column layout */}
      <section
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr", // 50 % | 50 %
          gap: "1.5rem",
          width: "100%",                  // use entire row
        }}
      >
        {/* chart, left half */}
        <div style={{ minWidth: 0 }}>{sentimentContent}</div>

        {/* keywords, right half */}
        <div
          style={{
            minWidth: 0,
            maxHeight: "50vh",
            overflowY: "auto",
            paddingLeft: "1rem",
          }}
        >
          {keywordContent}
        </div>
      </section>
    </main>
  );

}

export default App;
