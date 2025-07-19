import {useEffect, useState} from "react";

import TickerSelectForm from "./components/tickerSelect";
import SentimentChart from "./components/sentimentChart";
import KeywordsList from "./components/keywordsList";

const backendURL = import.meta.env.VITE_BACKEND_URL


function App() {
  const [backendResult, setBackendResult] = useState<string | object> ("Waiting for ticker selection...");

  function fetchTickerData(ticker: string) {
    setBackendResult("Loading...");
    fetch(`${backendURL}/analyze_last_n_quarters_sentiment?ticker=${ticker}&n=4`)
            .then((res) => res.json())
            .then((data)=> {
              setBackendResult(data.results);
            })
            .catch((error) => {
              console.error("Error contacting backend: ", error);
              setBackendResult("Backend unreachable or error. ");
            });
  }

  function handleTickerSubmit(ticker: string) {
    fetchTickerData(ticker);
  }
  
  let sentimentContent, keywordContent;
  if (typeof backendResult === "object" && backendResult !== null) {
    const sentimentChartData = Object.entries(backendResult).map(([quarter, entry]) => ({
      quarter,
      management: entry.management_sentiment,
      qa: entry.qa_sentiment,
    }));

    sentimentContent = <SentimentChart data={sentimentChartData}/>;
    keywordContent = <KeywordsList data={backendResult} />
  } else {
    sentimentContent = <p>{backendResult ?? "Please select a ticker."}</p>;
    keywordContent = <p>{":3"}</p>
  }

  return (
    <main style={{ padding: "1rem", fontFamily: "sans-serif", height: "70vh" }}>
      <h1>AI Earnings Signal</h1>

      <TickerSelectForm onSubmit={handleTickerSubmit} />

      <div
      style={{
        width: "100%",           // let the wrapper span the full viewport
        maxWidth: "5000px",      // optional: keep a sensible upper bound
        margin: "0 auto",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: "1.5rem",
          alignItems: "stretch",
          width: "100%",         // makes flexbox use the whole wrapper width
        }}
      >
        {/* CHART COLUMN */}
        <div style={{ flex: "0 0 50%", minWidth: 0 /* prevents overflow */ }}>
          {sentimentContent}
        </div>

        {/* KEYWORDS COLUMN */}
        <div
          style={{
            flex: "0 0 50%",      // exact 50 % of the row
            minWidth: 0,
            height: "50vh",
            overflowY: "auto",
            paddingLeft: "1rem",
          }}
        >
          {keywordContent}
        </div>
      </div>
    </div>


    </main>
  );
}


export default App;