import React from "react"

type SectionDividerProp = {
    thickness?: string
}

const SectionDivider: React.FC<SectionDividerProp> = (
    {thickness="1px"}
) => (
  <hr
    style={{
      width: "100%",
      margin: "1.5rem 0",
      border: "none",
      borderTop: `${thickness} solid #ccc`,
    }}
  />
);

const ProjectInfo: React.FC = () => (
    <div
        style={{
        padding: "1rem",
        fontFamily: "sans-serif",
        maxWidth: "70%",     
        margin: "0 auto",    
        lineHeight: "1.6",   
        }}
    >

    <header style={{ marginBottom: "1rem" }}>
      <h1 style={{ fontSize: "1.75rem", marginBottom: "0.25rem" }}>About This Project</h1>
      <p style={{ fontSize: "1rem", color: "#555" }}>
        Author: Isaac Li — <a href="mailto:isaacbngli@gmail.com">isaacbngli@gmail.com</a>
      </p>
      <p>Github Link:{" "}
        <a
            href="https://github.com/isaacLi2005/AiEarningsCallSignalExtraction"
            target="_blank"
            rel="noopener noreferrer"
        >
             https://github.com/isaacLi2005/AiEarningsCallSignalExtraction   
        </a> 
      
      </p>
    </header>

    <SectionDivider thickness="3px"/>

    <section>
        <header>
            <h4>Introduction</h4>
        </header>

        <p>
            Hello! My name is Isaac, and this tool is a LLM-powered sentiment
            visualizer for corporate earnings calls. It separates management discussion from Q&amp;A,
            assigns sentiment scores to each, and extracts key quarterly themes.
        </p>

        <p>
            To use the project, simply head on over to the "Data" tab by clicking the button in the 
            top left, enter a ticker you'd like to see the analysis for, and click "Submit"! Some 
            tickers are already suggested, but you can also type one of your own in as well!
        </p>
    </section>

    <SectionDivider/>

    <section>
        <header>
            <h4>Caching</h4>
        </header>

        <p>
            It takes time to run the backend's data gathering and processing, but the results are stored in 
            a cache. That means the first time a new ticker is requested, the model will take some time 
            to return that result, but subsequent requests for that ticker are much faster as we just read
            from storage rather than regenerating the entire result. 
        </p>

        <p>
            The cache is cleared every week on Sunday, so it may take until then for a new quarterly earnings
            call to be factored into the website. This long weekly cadence is done to reduce the number of API 
            calls made to Google Gemini. (More on the resources used below!)
        </p>

    </section>

    <SectionDivider/>

        <header>
            <h4>Tools and Citations</h4>
        </header>

        <p>
            The following section lists the environment used for the frontend and backend, then describes the 
            tools that the functionalities were built on. 
        </p>
    

    <section style={{ marginTop: "1.5rem" }}>
    <h5 style={{ fontSize: "1.25rem", marginBottom: "0.5rem" }}>Frontend: TypeScript and React</h5>
    <ul style={{ paddingLeft: "1.25rem", listStyleType: "disc" }}>
        <li> Vite: Fast development server and build tools </li>
        <li> Recharts: Graphing library for visualizing the sentiments data </li>
    </ul>

    <h5 style={{ fontSize: "1.25rem", marginBottom: "0.5rem" }}>Backend: Python and FastAPI</h5>
    <ul style={{ paddingLeft: "1.25rem", listStyleType: "disc" }}>
        <li>
            Sentiment analysis: I used the {" "}
            <a
            href="https://huggingface.co/yiyanghkust/finbert-tone"
            target="_blank"
            rel="noopener noreferrer"
            >
            yiyanghkust/finbert-tone
            </a>{" "}
            model, based on FinBERT: Araci, D. (2019).{" "}
            <em>FinBERT: Financial Sentiment Analysis with Pre-trained Language Models</em>. arXiv preprint{" "}
            <a
            href="https://arxiv.org/abs/1908.10063"
            target="_blank"
            rel="noopener noreferrer"
            >
            arXiv:1908.10063
            </a>
            .
        </li>

        <li>
            Keyword extraction: I used Google's {" "}
              <a
                href="https://deepmind.google/technologies/gemini"
                target="_blank"
                rel="noopener noreferrer"
                >
                Gemini 1.5 Flash
            </a>
            .
        </li>

        <li>
            Earnings calls transcripts: Earnings calls were sourced from API calls to {" "}
            <a
                href="https://api-ninjas.com/api/earningscalltranscript"
                target="_blank"
                rel="noopener noreferrer">
                Api Ninjas's Earnings Call Transcripts
            </a>
            .
        </li>

        <li>
            For more dependencies, refer to the {" "}
            <a
                href="https://github.com/isaacLi2005/AiEarningsCallSignalExtraction"
                target="_blank"
                rel="noopener noreferrer"
            >
                GitHub link
            </a> {" "}
            (same as the one above).
        </li>
    </ul>


    </section>

    </div>
)

export default ProjectInfo;