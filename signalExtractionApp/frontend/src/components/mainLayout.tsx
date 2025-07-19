import React from "react";
import TickerSelectForm from "./tickerSelect";

interface Props {
  handleTickerSubmit: (ticker: string) => void;
  sentimentContent: React.ReactNode;
  keywordContent: React.ReactNode;
}

const SentimentAndKeywordsLayoutBuilder: React.FC<Props> = ({
  handleTickerSubmit,
  sentimentContent,
  keywordContent,
}) => {
  return (
    <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h1>Earnings Call Sentiment and Keywords</h1>

      {/* ─── ticker input ─── */}
      <TickerSelectForm onSubmit={handleTickerSubmit} />

      {/* ─── chart + keywords ─── */}
      <div
        style={{
          display: "grid",
          /* 3 : 2 ratio → chart still larger, keywords noticeably wider than before */
          gridTemplateColumns: "minmax(0,3fr) minmax(0,2fr)",
          gap: "1.5rem",

          /* give the whole block a bit more breathing room on big screens */
          width: "100%",
          maxWidth: "1400px",
          margin: "2rem auto 0",

          alignItems: "start",
        }}
      >
        {/* chart */}
        <div style={{ minWidth: 0 }}>{sentimentContent}</div>

        {/* keywords list */}
        <div
          style={{
            minWidth: 0,
            maxHeight: "60vh",          // slightly taller scroll area
            overflowY: "auto",
            paddingLeft: "1rem",
          }}
        >
          {keywordContent}
        </div>
      </div>
    </div>
  );
};

export default SentimentAndKeywordsLayoutBuilder;
