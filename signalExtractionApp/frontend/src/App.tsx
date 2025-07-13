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