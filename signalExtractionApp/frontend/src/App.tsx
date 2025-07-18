import {useEffect, useState} from "react";

const backendURL = import.meta.env.VITE_BACKEND_URL

function App() {
  const [msg, setMsg] = useState<string> ("loading...");

  useEffect(
    () => {
      fetch(`${backendURL}/analyze_last_n_quarters_sentiment?ticker=NVDA&n=4`)
        .then((res) => res.json())
        .then((data)=> {
          setMsg(data.results);
        })
        .catch((error) => {
          console.error("Error contacting backend: ", error);
          setMsg("Backend unreachable");
        })
    }
  , []);


  return (
    <div>
      <h1> PUSH THE BUTTON </h1>
      <MyButton />

      <h2> {JSON.stringify(msg, null, 2)} </h2>
    </div>
  )
}


function MyButton() {
  return (
    <button onClick={() => console.log("Clicked")}> I'm a button </button>
  )
}


export default App;