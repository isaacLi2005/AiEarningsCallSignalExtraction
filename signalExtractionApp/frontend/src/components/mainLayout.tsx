import React from "react";
import TickerSelectForm from "./tickerSelect";

interface SentimentAndKeywordsLayoutProps {
  handleTickerSubmit: (ticker: string) => void;
  sentimentContent: React.ReactNode;
  keywordContent: React.ReactNode;
}

function SentimentAndKeywordsLayoutBuilder({
    handleTickerSubmit,
    sentimentContent,
    keywordContent
}: SentimentAndKeywordsLayoutProps) {
    return (
        <main style={{ padding: "1rem", fontFamily: "sans-serif" }}>
            <h1> Earnings Call Sentiment and Keywords </h1>

            <TickerSelectForm onSubmit={handleTickerSubmit} />

            <section
                style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr", 
                gap: "1.5rem",
                width: "100%",            
                }}
            >
                <div style={{ minWidth: 0 }}>{sentimentContent}</div>

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
    )
}


export default SentimentAndKeywordsLayoutBuilder

