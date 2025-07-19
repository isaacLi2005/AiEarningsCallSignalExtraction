import { useState } from "react";

import SentimentAndKeywordsLayoutBuilder from "./components/mainLayout";
import SentimentChart from "./components/sentimentChart";
import KeywordsList from "./components/keywordsList";
import ProjectInfo from "./components/projectInfo";

const backendURL = import.meta.env.VITE_BACKEND_URL;

function App() {
  const [backendResult, setBackendResult] = useState<string | object>(
    "Waiting for ticker selection…"
  );
  const[ticker, setTicker] = useState<string>(""); 
  const [currentTab, setCurrentTab] = useState("Data");


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
    setTicker(ticker)
  }

  let sentimentContent, keywordContent;
  if (typeof backendResult === "object" && backendResult !== null) {
    const sentimentChartData = Object.entries(backendResult).map(
      ([quarter, entry]: any) => ({
        quarter,
        management: entry.management_sentiment,
        qa: entry.qa_sentiment,
      })
    );
    sentimentContent = <SentimentChart ticker={ticker} data={sentimentChartData} />;
    keywordContent   = <KeywordsList  data={backendResult}        />;
  } else {
    sentimentContent = <p>{backendResult ?? "Please select a ticker."}</p>;
    keywordContent   = <p>😺</p>;
  }


  return (
    <div
      style={{
        /* full-height flex column lets us pin the header and scroll the main area */
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        fontFamily: "system-ui, sans-serif",
      }}
    >

      <header
        style={{
          position: "sticky",  
          top: 0,
          left: 0,
          zIndex: 1000,
          padding: "0.75rem 1rem",
        }}
      >
        <nav style={{ display: "flex", gap: "1rem" }}>
          {["Data", "About"].map((tab) => (
            <button
              key={tab}
              onClick={() => setCurrentTab(tab as "Data" | "About")}
              style={{
                fontWeight: currentTab === tab ? 600 : 400,
                padding: "0.25rem 0.75rem",
                border: "none",
                background: "transparent",
                cursor: "pointer",
              }}
            >
              {tab}
            </button>
          ))}
        </nav>
      </header>

      <main
        style={{
          flex: 1,                  
          overflowY: "auto",
          padding: "1.5rem",
          minHeight: "60vh",
        }}
      >
        {currentTab === "Data" ? (
          <SentimentAndKeywordsLayoutBuilder
            handleTickerSubmit={handleTickerSubmit}
            sentimentContent={sentimentContent}
            keywordContent={keywordContent}
          />
        ) : (
          <ProjectInfo />
        )}
      </main>
    </div>
  );
}

export default App;
