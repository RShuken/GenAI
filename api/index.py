"""
THE GASLIGHTING WIKI DEBATES - Vercel Serverless API
"""

import os
import json
import random
from flask import Flask, jsonify, request
import anthropic

app = Flask(__name__)

# Initialize client - will use ANTHROPIC_API_KEY env var
client = None

def get_client():
    global client
    if client is None:
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    return client

# Debater personas with distinct gaslighting styles
DEBATER_PERSONAS = {
    "professor_thornberry": {
        "name": "Professor Wilhelmina Thornberry",
        "style": "Academic Condescension",
        "avatar": "🎓",
        "color": "#9b59b6",
        "tactics": ["appeals to obscure authority", "patronizing corrections", "manufactured historical context"],
        "personality": """You are Professor Wilhelmina Thornberry, a pompous academic who speaks with absolute
        authority about everything, especially things you just made up. You pepper your arguments with
        fake citations, invented historical anecdotes, and condescending phrases like "Well, actually..."
        and "As any first-year student would know...". You gaslight by making your opponent feel uneducated
        for not knowing fabricated facts. You NEVER admit uncertainty - everything you say is established fact."""
    },
    "uncle_conspiracy": {
        "name": "Uncle Randy (The Truth Seeker)",
        "style": "Conspiracy Confidence",
        "avatar": "🔺",
        "color": "#e74c3c",
        "tactics": ["connecting unrelated dots", "questioning 'official' narratives", "rhetorical 'just asking questions'"],
        "personality": """You are Uncle Randy, a conspiracy enthusiast who sees hidden connections everywhere.
        You gaslight by implying your opponent is naive or 'hasn't done the research'. You use phrases like
        "Follow the money...", "They don't want you to know this, but...", and "Coincidence? I think not."
        You invent shadow organizations, secret histories, and suppressed studies. You make your opponent
        doubt their own knowledge by suggesting there's always a deeper truth they're missing."""
    },
    "corporate_cynthia": {
        "name": "Cynthia Sterling, MBA",
        "style": "Corporate Doublespeak",
        "avatar": "💼",
        "color": "#3498db",
        "tactics": ["buzzword bombardment", "pivot and redirect", "manufactured metrics"],
        "personality": """You are Cynthia Sterling, a corporate executive who speaks entirely in business jargon.
        You gaslight by making simple things sound complex and burying opponents in fake statistics and KPIs.
        You use phrases like "Let's unpack that...", "The data clearly shows...", and "From a value-add perspective..."
        You invent market research, quarterly reports, and industry benchmarks. You make opponents feel they don't
        understand 'how the real world works' if they disagree."""
    },
    "mystic_moonbeam": {
        "name": "Sage Moonbeam",
        "style": "Spiritual Superiority",
        "avatar": "🔮",
        "color": "#1abc9c",
        "tactics": ["energy appeals", "ancient wisdom claims", "vibrational logic"],
        "personality": """You are Sage Moonbeam, a new-age spiritual guru who frames everything in terms of
        energy, vibrations, and ancient wisdom. You gaslight by suggesting your opponent is 'not spiritually
        evolved enough' to understand. You reference invented ancient texts, made-up quantum physics, and
        fictional indigenous prophecies. You use phrases like "The ancients knew...", "Your third eye would
        show you...", and "The universe is trying to tell us...". You make opponents doubt their intuition."""
    }
}

WIKI_CATEGORIES = [
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
]


@app.route('/api/personas')
def get_personas():
    """Get available debater personas."""
    return jsonify({
        key: {
            "name": p["name"],
            "style": p["style"],
            "avatar": p["avatar"],
            "color": p["color"],
            "tactics": p["tactics"]
        } for key, p in DEBATER_PERSONAS.items()
    })


@app.route('/api/generate-topic')
def api_generate_topic():
    """Generate a new fake wiki topic."""
    category = random.choice(WIKI_CATEGORIES)

    prompt = f"""Generate a completely made-up but plausible-sounding Wikipedia article topic
    in the category: "{category}"

    Return ONLY a JSON object with:
    - "title": The article title (should sound real but be completely fabricated)
    - "category": The category
    - "teaser": A one-sentence teaser that sounds encyclopedic

    Be creative and absurd but make it sound legitimate. Examples of good fake topics:
    - "The Great Pancake Rebellion of 1847"
    - "Quantum Emotional Resonance Theory"
    - "The Glimmerfish of Lake Mendacious"

    Return ONLY valid JSON, no other text."""

    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify(json.loads(response.content[0].text))
    except Exception as e:
        return jsonify({
            "title": "The Phantom Protocol of 1923",
            "category": category,
            "teaser": "A secret international agreement that shaped the modern world.",
            "error": str(e)
        })


@app.route('/api/generate-article', methods=['POST'])
def api_generate_article():
    """Generate a full wiki article for a topic."""
    data = request.json
    title = data.get('title')

    if not title:
        return jsonify({"error": "Title required"}), 400

    prompt = f"""Write a completely fabricated but convincing Wikipedia-style article about: "{title}"

    The article should:
    - Be 3-4 paragraphs long
    - Include fake dates, names, places, and statistics
    - Reference invented sources, studies, or historical documents
    - Sound authoritative and encyclopedic
    - Include a "Controversy" or "Criticism" section
    - Have some internal contradictions that debaters could exploit

    Make it detailed enough that two people could have a heated debate about different interpretations.
    Include specific "facts" that could be argued about.

    Return as JSON with:
    - "title": The title
    - "content": The full article text (use \\n for paragraphs)
    - "key_facts": Array of 5 specific "facts" from the article that are debatable
    - "controversy": A brief description of the main controversy

    Return ONLY valid JSON."""

    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify(json.loads(response.content[0].text))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/debate-turn', methods=['POST'])
def api_debate_turn():
    """Generate a single turn in the debate."""
    data = request.json
    debater_key = data.get('debater_key')
    topic = data.get('topic')
    article = data.get('article', {})
    opponent_statement = data.get('opponent_statement', '')
    debate_history = data.get('debate_history', [])
    position = data.get('position', '')
    is_opening = data.get('is_opening', False)
    opponent_name = data.get('opponent_name', 'opponent')

    debater = DEBATER_PERSONAS.get(debater_key)
    if not debater:
        return jsonify({"error": "Invalid debater"}), 400

    if is_opening:
        prompt = f"""{debater['personality']}

        You are about to debate about this topic from a fake Wikipedia:

        TOPIC: {topic}

        ARTICLE CONTENT:
        {article.get('content', '')}

        KEY FACTS TO POTENTIALLY DISPUTE:
        {json.dumps(article.get('key_facts', []))}

        Your position: You must argue {position}
        Your opponent is: {opponent_name}

        Generate your opening statement (2-3 sentences). Be confident, slightly condescending,
        and use your gaslighting tactics. Reference specific "facts" from the article but
        interpret them in your favor. Make your opponent question their understanding.

        Speak directly as your character. Be entertaining and theatrical."""
    else:
        history_text = "\n".join([f"{h['speaker']}: {h['text']}" for h in debate_history[-6:]])

        prompt = f"""{debater['personality']}

        DEBATE TOPIC: {topic}

        WIKI ARTICLE FOR REFERENCE:
        {article.get('content', '')}

        YOUR POSITION: {position}

        DEBATE SO FAR:
        {history_text}

        YOUR OPPONENT JUST SAID:
        "{opponent_statement}"

        Respond with a devastating rebuttal (2-3 sentences). You MUST:
        1. Gaslight them by questioning their interpretation or intelligence
        2. Reference "facts" from the wiki but twist them to your advantage
        3. Invent additional supporting "evidence" that sounds plausible
        4. Use your signature gaslighting tactics: {debater['tactics']}
        5. Make them doubt themselves

        Be theatrical, entertaining, and confidently wrong. Never concede any point.
        Speak directly as your character."""

    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"response": response.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze-debate', methods=['POST'])
def api_analyze_debate():
    """Analyze the completed debate."""
    data = request.json
    debate_history = data.get('debate_history', [])

    history_text = "\n\n".join([f"**{h['speaker']}**: {h['text']}" for h in debate_history])

    prompt = f"""Analyze this debate between two AI personas who were trying to gaslight each other
    about a completely fabricated topic.

    DEBATE TRANSCRIPT:
    {history_text}

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
    Return ONLY valid JSON."""

    try:
        response = get_client().messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify(json.loads(response.content[0].text))
    except Exception as e:
        return jsonify({
            "winner": "Chaos",
            "winner_score": 100,
            "loser_score": 100,
            "best_gaslight_moment": "Everything was a gaslight moment",
            "techniques_used": {},
            "audience_warning": "Trust nothing you just read.",
            "key_takeaway": "Two AIs argued about nothing and somehow both lost.",
            "error": str(e)
        })


# For Vercel
app = app
