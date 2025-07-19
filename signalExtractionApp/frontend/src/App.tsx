import {useEffect, useState} from "react";

import TickerSelectForm from "./components/tickerSelect";

const backendURL = import.meta.env.VITE_BACKEND_URL


function App() {
  const [result, setResult] = useState<string> ("Waiting for ticker selection...");

    function fetchTickerData(ticker: string) {
      setResult("Loading...");
      fetch(`${backendURL}/analyze_last_n_quarters_sentiment?ticker=${ticker}&n=4`)
              .then((res) => res.json())
              .then((data)=> {
                setResult(data.results);
              })
              .catch((error) => {
                console.error("Error contacting backend: ", error);
                setResult("Backend unreachable or error. ");
              });
    }

    function handleTickerSubmit(ticker: string) {
      fetchTickerData(ticker);
    }


  return (
    <main style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h1>AI Earnings Signal</h1>

      <TickerSelectForm onSubmit={handleTickerSubmit} />

      <h2>Backend Response</h2>
      <pre>
        {typeof result === "string"
          ? result
          : JSON.stringify(result, null, 2)}
      </pre>
    </main>
  );
}


export default App;