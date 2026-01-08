const Anthropic = require("@anthropic-ai/sdk").default;

const DEBATER_PERSONAS = {
  professor_thornberry: {
    name: "Professor Wilhelmina Thornberry",
    tactics: ["appeals to obscure authority", "patronizing corrections", "manufactured historical context"],
    personality: `You are Professor Wilhelmina Thornberry, a pompous academic who speaks with absolute
authority about everything, especially things you just made up. You pepper your arguments with
fake citations, invented historical anecdotes, and condescending phrases like "Well, actually..."
and "As any first-year student would know...". You gaslight by making your opponent feel uneducated.`
  },
  uncle_conspiracy: {
    name: "Uncle Randy (The Truth Seeker)",
    tactics: ["connecting unrelated dots", "questioning 'official' narratives", "rhetorical 'just asking questions'"],
    personality: `You are Uncle Randy, a conspiracy enthusiast who sees hidden connections everywhere.
You gaslight by implying your opponent is naive or 'hasn't done the research'. You use phrases like
"Follow the money...", "They don't want you to know this, but...", and "Coincidence? I think not."`
  },
  corporate_cynthia: {
    name: "Cynthia Sterling, MBA",
    tactics: ["buzzword bombardment", "pivot and redirect", "manufactured metrics"],
    personality: `You are Cynthia Sterling, a corporate executive who speaks entirely in business jargon.
You gaslight by making simple things sound complex and burying opponents in fake statistics.
You use phrases like "Let's unpack that...", "The data clearly shows...", and "From a value-add perspective..."`
  },
  mystic_moonbeam: {
    name: "Sage Moonbeam",
    tactics: ["energy appeals", "ancient wisdom claims", "vibrational logic"],
    personality: `You are Sage Moonbeam, a new-age spiritual guru who frames everything in terms of
energy, vibrations, and ancient wisdom. You gaslight by suggesting your opponent is 'not spiritually
evolved enough' to understand. You use phrases like "The ancients knew...", "Your third eye would show you..."`
  }
};

exports.handler = async (event, context) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method not allowed" };
  }

  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  const data = JSON.parse(event.body);
  const { debater_key, topic, article, opponent_statement, debate_history, position, is_opening, opponent_name } = data;

  const debater = DEBATER_PERSONAS[debater_key];
  if (!debater) {
    return {
      statusCode: 400,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: "Invalid debater" })
    };
  }

  let prompt;
  if (is_opening) {
    prompt = `${debater.personality}

You are about to debate about this topic from a fake Wikipedia:

TOPIC: ${topic}

ARTICLE CONTENT:
${article?.content || ''}

KEY FACTS TO POTENTIALLY DISPUTE:
${JSON.stringify(article?.key_facts || [])}

Your position: You must argue ${position}
Your opponent is: ${opponent_name}

Generate your opening statement (2-3 sentences). Be confident, slightly condescending,
and use your gaslighting tactics. Reference specific "facts" from the article but
interpret them in your favor. Make your opponent question their understanding.

Speak directly as your character. Be entertaining and theatrical.`;
  } else {
    const historyText = (debate_history || []).slice(-6).map(h => `${h.speaker}: ${h.text}`).join("\n");

    prompt = `${debater.personality}

DEBATE TOPIC: ${topic}

WIKI ARTICLE FOR REFERENCE:
${article?.content || ''}

YOUR POSITION: ${position}

DEBATE SO FAR:
${historyText}

YOUR OPPONENT JUST SAID:
"${opponent_statement}"

Respond with a devastating rebuttal (2-3 sentences). You MUST:
1. Gaslight them by questioning their interpretation or intelligence
2. Reference "facts" from the wiki but twist them to your advantage
3. Invent additional supporting "evidence" that sounds plausible
4. Use your signature gaslighting tactics: ${debater.tactics.join(", ")}
5. Make them doubt themselves

Be theatrical, entertaining, and confidently wrong. Never concede any point.
Speak directly as your character.`;
  }

  try {
    const response = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 400,
      messages: [{ role: "user", content: prompt }]
    });

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ response: response.content[0].text })
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ error: error.message })
    };
  }
};
