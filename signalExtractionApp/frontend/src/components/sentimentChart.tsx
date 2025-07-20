import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

interface Props {
  ticker: string;
  data: { quarter: string; management: number; qa: number }[];
}

const SentimentChart: React.FC<Props> = ({ ticker, data }) => {
  return (
    <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
      <h3 style={{ textAlign: "center", marginBottom: "0rem" }}>
        {ticker} — Management vs. Q&A Sentiment
      </h3>

      <h5 style={{ textAlign: "center", marginBottom: "0.1rem"}} >
        A score of +1.0 is maximally positive and -1.0 maximally negative.
      </h5>

      {/* Important: wrapper with relative layout so aspect ratio works */}
      <div style={{ width: "100%", position: "relative" }}>
        <ResponsiveContainer width="100%" aspect={1.8}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="quarter" />
            <YAxis domain={[-1, 1]} />
            <Tooltip />
            <Legend />
            <Bar
              dataKey="management"
              fill="#8884d8"
              name="Management"
              label={{
                position: "top",
                formatter: (value) => (value as number).toFixed(2),
              }}
            />
            <Bar
              dataKey="qa"
              fill="#82ca9d"
              name="Q&A"
              label={{
                position: "top",
                formatter: (value) => (value as number).toFixed(2),
              }}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
};

export default SentimentChart;
