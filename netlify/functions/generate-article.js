const Anthropic = require("@anthropic-ai/sdk").default;

exports.handler = async (event, context) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method not allowed" };
  }

  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const { title } = JSON.parse(event.body);

  if (!title) {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: "Title required" })
    };
  }

  const prompt = `Write a completely fabricated but convincing Wikipedia-style article about: "${title}"

The article should:
- Be 3-4 paragraphs long
- Include fake dates, names, places, and statistics
- Reference invented sources, studies, or historical documents
- Sound authoritative and encyclopedic
- Include a "Controversy" or "Criticism" section
- Have some internal contradictions that debaters could exploit

Return as JSON with:
- "title": The title
- "content": The full article text (use \\n for paragraphs)
- "key_facts": Array of 5 specific "facts" from the article that are debatable
- "controversy": A brief description of the main controversy

Return ONLY valid JSON.`;

  try {
    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1500,
      messages: [{ role: "user", content: prompt }]
    });

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: response.content[0].text
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: error.message })
    };
  }
};
