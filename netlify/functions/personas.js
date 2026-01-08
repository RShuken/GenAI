exports.handler = async (event, context) => {
  const personas = {
    professor_thornberry: {
      name: "Professor Wilhelmina Thornberry",
      style: "Academic Condescension",
      avatar: "🎓",
      color: "#9b59b6",
      tactics: ["appeals to obscure authority", "patronizing corrections", "manufactured historical context"]
    },
    uncle_conspiracy: {
      name: "Uncle Randy (The Truth Seeker)",
      style: "Conspiracy Confidence",
      avatar: "🔺",
      color: "#e74c3c",
      tactics: ["connecting unrelated dots", "questioning 'official' narratives", "rhetorical 'just asking questions'"]
    },
    corporate_cynthia: {
      name: "Cynthia Sterling, MBA",
      style: "Corporate Doublespeak",
      avatar: "💼",
      color: "#3498db",
      tactics: ["buzzword bombardment", "pivot and redirect", "manufactured metrics"]
    },
    mystic_moonbeam: {
      name: "Sage Moonbeam",
      style: "Spiritual Superiority",
      avatar: "🔮",
      color: "#1abc9c",
      tactics: ["energy appeals", "ancient wisdom claims", "vibrational logic"]
    }
  };

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(personas)
  };
};
