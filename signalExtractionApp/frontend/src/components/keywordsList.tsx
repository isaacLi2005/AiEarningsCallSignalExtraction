type Props = {
  data: Record<string, any>;
};

export default function KeywordsList({ data }: Props) {
  return (
    <div style={{ paddingLeft: "1rem" }}>
      {Object.entries(data).map(([quarter, entry]) => (
        <div key={quarter} style={{ marginBottom: "1.5em" }}>
          <h3>{quarter}</h3>

          <p><strong>Management Topics:</strong></p>
          <ul>
            {Array.isArray(entry.management_keywords?.key_themes)
              ? entry.management_keywords.key_themes.map((t: string) => (
                  <li key={t}>{t}</li>
                ))
              : <li style={{ fontStyle: "italic" }}>No data</li>}
          </ul>

          <p><strong>Q&A Topics:</strong></p>
          <ul>
            {Array.isArray(entry.qa_keywords?.key_themes)
              ? entry.qa_keywords.key_themes.map((t: string) => (
                  <li key={t}>{t}</li>
                ))
              : <li style={{ fontStyle: "italic" }}>No data</li>}
          </ul>
        </div>
      ))}
    </div>
  );
}