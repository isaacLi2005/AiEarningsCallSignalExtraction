import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

type Props = {
  ticker: string
  data: {
    quarter: string;
    management: number;
    qa: number;
  }[];
};

function SentimentChart({ ticker, data }: Props) {
  return (

    <div>

      <div>
        <h3 style={{ textAlign: "center", marginBottom: "0.5rem" }}>
          {ticker} — Management vs. Q&A Sentiment
        </h3>
      </div>

      <ResponsiveContainer aspect={1.8}>
      <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="quarter" />
          <YAxis domain={[0, 1]} />
          <Tooltip />
          <Legend />
          <Bar dataKey="management" fill="#8884d8" name="Management" label={{ position: "top", formatter: (value) => (value as number).toFixed(2) }} />
          <Bar dataKey="qa" fill="#82ca9d" name="Q&A" label={{ position: "top", formatter: (value) => (value as number).toFixed(2) }} />
      </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SentimentChart