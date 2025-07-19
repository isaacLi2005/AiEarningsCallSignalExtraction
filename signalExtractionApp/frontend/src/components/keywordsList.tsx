type Props = {
  data: Record<string, any>;
};

export default function KeywordsList({ data }: Props) {
  return (
    <div style={{ paddingLeft: "1rem" }}>
      {Object.entries(data).map(([quarter, entry]) => {
        // flexible helpers: look for either "key_themes" or "themes"
        const mgmtThemes =
          entry.management_keywords?.key_themes ??
          entry.management_keywords?.themes ??
          [];

        const qaThemes =
          entry.qa_keywords?.key_themes ??
          entry.qa_keywords?.themes ??
          [];

        return (
          <div key={quarter} style={{ marginBottom: "1.5em" }}>
            <h3>{quarter}</h3>

            <p>
              <strong>Management Topics:</strong>
            </p>
            <ul>
              {mgmtThemes.length > 0 ? (
                mgmtThemes.map((t: string) => <li key={t}>{t}</li>)
              ) : (
                <li style={{ fontStyle: "italic" }}>No data</li>
              )}
            </ul>

            <p>
              <strong>Q&amp;A Topics:</strong>
            </p>
            <ul>
              {qaThemes.length > 0 ? (
                qaThemes.map((t: string) => <li key={t}>{t}</li>)
              ) : (
                <li style={{ fontStyle: "italic" }}>No data</li>
              )}
            </ul>
          </div>
        );
      })}
    </div>
  );
}
