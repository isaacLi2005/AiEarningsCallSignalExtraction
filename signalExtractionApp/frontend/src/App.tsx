import {useEffect, useState} from "react";

interface PingResponse {
  message: string;
}

function App() {
  const [msg, setMsg] = useState<string> ("loading...");

  useEffect(
    () => {
      fetch("http://localhost:8000/ping")
        .then((res) => res.json())
        .then((data: PingResponse)=> {
          setMsg(data.message);
        })
        .catch((error) => {
          console.error("Error contacting backend: ", error);
          setMsg("Backend unreachable");
        })
    }
  , []);
}

function TranscriptFetcher() {
  const [ticker, setTicker] = useState("NVDA");
  const [year, setYear]     = useState(2024);
  const [qtr,  setQtr]      = useState(4);
  const [text, setText]     = useState<string>("");

  const fetchTranscript = () => {
    fetch(`http://localhost:8000/transcript?ticker=${ticker}&year=${year}&quarter=${qtr}`)
      .then(r => r.json())
      .then(d => setText(d.transcript ?? JSON.stringify(d)))
      .catch(err => setText("Backend error: " + err));
  };

  return (
    <div style={{padding:20,fontFamily:"sans-serif"}}>
      <h2>Fetch Earnings Call Transcript</h2>
      <input value={ticker} onChange={e=>setTicker(e.target.value.toUpperCase())}/>
      <input type="number" value={year} onChange={e=>setYear(+e.target.value)}/>
      <input type="number" value={qtr}  onChange={e=>setQtr(+e.target.value)}/>
      <button onClick={fetchTranscript}>Get transcript</button>

      <pre style={{whiteSpace:"pre-wrap", marginTop:20}}>
        {text.slice(0, 2000) || "No data yet..."}
      </pre>
    </div>
  );
}

export default TranscriptFetcher;