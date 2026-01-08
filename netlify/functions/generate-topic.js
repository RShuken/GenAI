const Anthropic = require("@anthropic-ai/sdk").default;

const WIKI_CATEGORIES = [
  "Historical Events That Never Happened",
  "Fictional Scientific Discoveries",
  "Made-Up Cultural Phenomena",
  "Imaginary Creatures & Cryptids",
  "Fake Philosophical Movements",
  "Invented Technologies",
  "Fabricated Celebrities",
  "Nonexistent Places",
  "Fictional Diseases & Conditions",
  "Made-Up Foods & Cuisines"
];

exports.handler = async (event, context) => {
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const category = WIKI_CATEGORIES[Math.floor(Math.random() * WIKI_CATEGORIES.length)];

  const prompt = `Generate a completely made-up but plausible-sounding Wikipedia article topic
in the category: "${category}"

Return ONLY a JSON object with:
- "title": The article title (should sound real but be completely fabricated)
- "category": The category
- "teaser": A one-sentence teaser that sounds encyclopedic

Be creative and absurd but make it sound legitimate. Examples:
- "The Great Pancake Rebellion of 1847"
- "Quantum Emotional Resonance Theory"

Return ONLY valid JSON, no other text.`;

  try {
    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 300,
      messages: [{ role: "user", content: prompt }]
    });

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: response.content[0].text
    };
  } catch (error) {
    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: "The Phantom Protocol of 1923",
        category: category,
        teaser: "A secret international agreement that shaped the modern world.",
        error: error.message
      })
    };
  }
};
