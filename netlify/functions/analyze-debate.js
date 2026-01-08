const Anthropic = require("@anthropic-ai/sdk").default;

exports.handler = async (event, context) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method not allowed" };
  }

  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const { debate_history } = JSON.parse(event.body);

  const historyText = (debate_history || []).map(h => `**${h.speaker}**: ${h.text}`).join("\n\n");

  const prompt = `Analyze this debate between two AI personas who were trying to gaslight each other
about a completely fabricated topic.

DEBATE TRANSCRIPT:
${historyText}

Provide a JSON analysis with:
- "winner": Who was more convincing (name)
- "winner_score": Score out of 100
- "loser_score": Score out of 100
- "best_gaslight_moment": The most effective gaslighting moment (quote it)
- "best_gaslight_speaker": Who delivered it
- "techniques_used": Object mapping speaker names to array of gaslighting techniques they used
- "fabrications_count": Object mapping speaker names to estimated number of things they made up
- "confidence_rating": Object mapping speaker names to how confident they sounded (1-10)
- "audience_warning": A funny warning to the audience about what they just witnessed
- "key_takeaway": One sentence summary of the chaos

Be funny and insightful in your analysis. This is all for entertainment.
Return ONLY valid JSON.`;

  try {
    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 800,
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
        winner: "Chaos",
        winner_score: 100,
        loser_score: 100,
        best_gaslight_moment: "Everything was a gaslight moment",
        techniques_used: {},
        audience_warning: "Trust nothing you just read.",
        key_takeaway: "Two AIs argued about nothing and somehow both lost.",
        error: error.message
      })
    };
  }
};
