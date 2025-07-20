import React, {useState, type JSX} from "react";

type Props = {
    onSubmit: (ticker: string) => void;
}

const defaultTickers = ["NVDA", "AAPL", "MSFT", "GOOG", "Other"]

function tickerSelectForm({onSubmit}: Props): JSX.Element {
    const [selected, setSelected] = useState("NVDA");
    const [custom, setCustom] = useState("");

    const isCustom = selected === "Other";

    function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const finalTicker = isCustom ? custom.toUpperCase() : selected;
        onSubmit(finalTicker);
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>
                    Ticker:&nbsp;
                    <select 
                        value={selected}
                        onChange={(e) => setSelected(e.target.value)}>
                        {defaultTickers.map((ticker) => <option key={ticker} value={ticker}> {ticker} </option>)}
                    </select>
                </label>

                <button type="submit" style={{ marginLeft: "1em" }}>
                    Submit
                </button>
            </form>

            {
                isCustom && (
                    <input
                        type="text"
                        placeholder="Enter custom ticker"
                        value={custom}
                        onChange={(e)=>setCustom(e.target.value)}
                        style={{ marginLeft: "1em" }}
                    />
                )
            }


        </div>
    )
}

export default tickerSelectForm;