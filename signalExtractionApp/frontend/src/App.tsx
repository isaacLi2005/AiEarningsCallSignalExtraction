import {useEffect, useState} from "react";

const backendURL = import.meta.env.VITE_APP_BACKEND_URL

function App() {
  const [msg, setMsg] = useState<string> ("loading...");

  useEffect(
    () => {
      fetch(`${backendURL}/ping`)
        .then((res) => res.json())
        .then((data)=> {
          setMsg(data.response);
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

      <h2> {msg} </h2>
    </div>
  )
}


function MyButton() {
  return (
    <button onClick={() => console.log("Clicked")}> I'm a button </button>
  )
}


export default App;