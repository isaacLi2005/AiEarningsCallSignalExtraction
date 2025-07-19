import React from "react"

const ProjectInfo: React.FC = () => (
    <div
        style={{
        padding: "1rem",
        fontFamily: "sans-serif",
        maxWidth: "720px",     // keeps line length readable
        margin: "0 auto",       // centers the content
        lineHeight: "1.6",      // improves text readability
        }}
    >

    <header style={{ marginBottom: "1rem" }}>
      <h1 style={{ fontSize: "1.75rem", marginBottom: "0.25rem" }}>About This Project</h1>
      <p style={{ fontSize: "1rem", color: "#555" }}>
        Author: Isaac Li — <a href="mailto:isaacbngli@gmail.com">isaacbngli@gmail.com</a>
      </p>
    </header>

    <section>
    <p>
        Hello! My name is Isaac, and this tool is a large language model (LLM)–powered sentiment
        visualizer for corporate earnings calls. It separates management discussion from Q&amp;A,
        assigns sentiment scores to each, and extracts key quarterly themes.
    </p>

    <p>
        The backend uses Python and FastAPI, while the frontend is built with React and TypeScript.
        Sentiment is extracted via embeddings and LLM classification. It currently supports tickers
        like NVDA and AAPL over the past several quarters.
    </p>
    </section>

    <section style={{ marginTop: "1.5rem" }}>
    <h2 style={{ fontSize: "1.25rem", marginBottom: "0.5rem" }}>Resources Used</h2>
    <ul style={{ paddingLeft: "1.25rem", listStyleType: "disc" }}>
        <li>OpenAI’s GPT-4 and embedding APIs</li>
        <li>FastAPI for backend routing</li>
        <li>React + Vite for the frontend interface</li>
        <li>SeekingAlpha and other public sources for earnings transcripts</li>
    </ul>
    </section>

    </div>
)

export default ProjectInfo;