"""
THE GASLIGHTING WIKI DEBATES
============================
Two AIs debate about completely fabricated topics from an infinite wiki,
each trying to gaslight the other with confident reasoning about things
that don't exist. Watch the chaos unfold.
"""

import os
import json
import random
from flask import Flask, render_template, jsonify, request, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Store generated wiki articles for the session
wiki_database = {}

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


def generate_wiki_topic():
    """Generate a random fake wiki topic."""
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

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response.content[0].text)
    except:
        return {
            "title": "The Phantom Protocol of 1923",
            "category": "Historical Events That Never Happened",
            "teaser": "A secret international agreement that shaped the modern world."
        }


def generate_wiki_article(topic_title):
    """Generate a full fake Wikipedia article."""

    prompt = f"""Write a completely fabricated but convincing Wikipedia-style article about: "{topic_title}"

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

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        article = json.loads(response.content[0].text)
        wiki_database[topic_title] = article
        return article
    except:
        return None


def generate_debate_position(debater_key, topic, article, position, opponent_name):
    """Generate a debater's opening position."""
    debater = DEBATER_PERSONAS[debater_key]

    prompt = f"""{debater['personality']}

    You are about to debate about this topic from a fake Wikipedia:

    TOPIC: {topic}

    ARTICLE CONTENT:
    {article['content']}

    KEY FACTS TO POTENTIALLY DISPUTE:
    {json.dumps(article['key_facts'])}

    CONTROVERSY:
    {article['controversy']}

    Your position: You must argue {position}
    Your opponent is: {opponent_name}

    Generate your opening statement (2-3 sentences). Be confident, slightly condescending,
    and use your gaslighting tactics. Reference specific "facts" from the article but
    interpret them in your favor. Make your opponent question their understanding.

    Speak directly as your character. Be entertaining and theatrical."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_debate_response(debater_key, topic, article, opponent_statement, debate_history, position):
    """Generate a response in the debate, attempting to gaslight the opponent."""
    debater = DEBATER_PERSONAS[debater_key]

    history_text = "\n".join([f"{h['speaker']}: {h['text']}" for h in debate_history[-6:]])

    prompt = f"""{debater['personality']}

    DEBATE TOPIC: {topic}

    WIKI ARTICLE FOR REFERENCE:
    {article['content']}

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

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def analyze_gaslighting(debate_history):
    """Analyze the debate for gaslighting techniques used."""

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

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response.content[0].text)
    except:
        return {
            "winner": "Chaos",
            "winner_score": 100,
            "loser_score": 100,
            "best_gaslight_moment": "Everything was a gaslight moment",
            "techniques_used": {},
            "audience_warning": "Trust nothing you just read.",
            "key_takeaway": "Two AIs argued about nothing and somehow both lost."
        }


# ==================== ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


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
    topic = generate_wiki_topic()
    return jsonify(topic)


@app.route('/api/generate-article', methods=['POST'])
def api_generate_article():
    """Generate a full wiki article for a topic."""
    data = request.json
    title = data.get('title')

    if not title:
        return jsonify({"error": "Title required"}), 400

    article = generate_wiki_article(title)
    if article:
        return jsonify(article)
    return jsonify({"error": "Failed to generate article"}), 500


@app.route('/api/start-debate', methods=['POST'])
def api_start_debate():
    """Start a new debate with opening statements."""
    data = request.json
    debater1_key = data.get('debater1')
    debater2_key = data.get('debater2')
    topic = data.get('topic')
    article = data.get('article')

    if not all([debater1_key, debater2_key, topic, article]):
        return jsonify({"error": "Missing required fields"}), 400

    # Generate positions
    positions = [
        f"IN FAVOR of the mainstream interpretation of {topic}",
        f"AGAINST the mainstream interpretation, arguing the truth has been hidden about {topic}"
    ]
    random.shuffle(positions)

    debater1 = DEBATER_PERSONAS[debater1_key]
    debater2 = DEBATER_PERSONAS[debater2_key]

    opening1 = generate_debate_position(debater1_key, topic, article, positions[0], debater2["name"])
    opening2 = generate_debate_position(debater2_key, topic, article, positions[1], debater1["name"])

    return jsonify({
        "debater1": {
            "key": debater1_key,
            "position": positions[0],
            "opening": opening1
        },
        "debater2": {
            "key": debater2_key,
            "position": positions[1],
            "opening": opening2
        }
    })


@app.route('/api/debate-turn', methods=['POST'])
def api_debate_turn():
    """Generate the next turn in the debate."""
    data = request.json
    debater_key = data.get('debater_key')
    topic = data.get('topic')
    article = data.get('article')
    opponent_statement = data.get('opponent_statement')
    debate_history = data.get('debate_history', [])
    position = data.get('position')

    response = generate_debate_response(
        debater_key, topic, article, opponent_statement, debate_history, position
    )

    return jsonify({"response": response})


@app.route('/api/analyze-debate', methods=['POST'])
def api_analyze_debate():
    """Analyze the completed debate."""
    data = request.json
    debate_history = data.get('debate_history', [])

    analysis = analyze_gaslighting(debate_history)
    return jsonify(analysis)


@app.route('/api/stream-debate', methods=['POST'])
def stream_debate():
    """Stream an entire debate in real-time."""
    data = request.json
    debater1_key = data.get('debater1')
    debater2_key = data.get('debater2')
    topic = data.get('topic')
    article = data.get('article')
    rounds = data.get('rounds', 3)

    def generate():
        debater1 = DEBATER_PERSONAS[debater1_key]
        debater2 = DEBATER_PERSONAS[debater2_key]

        positions = [
            f"IN FAVOR of the mainstream interpretation of {topic}",
            f"AGAINST the mainstream interpretation of {topic}"
        ]
        random.shuffle(positions)

        debate_history = []

        # Opening statements
        yield f"data: {json.dumps({'type': 'status', 'message': 'Generating opening statements...'})}\n\n"

        opening1 = generate_debate_position(debater1_key, topic, article, positions[0], debater2["name"])
        debate_history.append({"speaker": debater1["name"], "text": opening1, "debater_key": debater1_key})
        yield f"data: {json.dumps({'type': 'statement', 'speaker': debater1['name'], 'avatar': debater1['avatar'], 'color': debater1['color'], 'text': opening1, 'position': positions[0]})}\n\n"

        opening2 = generate_debate_position(debater2_key, topic, article, positions[1], debater1["name"])
        debate_history.append({"speaker": debater2["name"], "text": opening2, "debater_key": debater2_key})
        yield f"data: {json.dumps({'type': 'statement', 'speaker': debater2['name'], 'avatar': debater2['avatar'], 'color': debater2['color'], 'text': opening2, 'position': positions[1]})}\n\n"

        # Debate rounds
        current_debater = 0
        debaters = [
            (debater1_key, debater1, positions[0]),
            (debater2_key, debater2, positions[1])
        ]

        for round_num in range(rounds * 2):
            yield f"data: {json.dumps({'type': 'status', 'message': f'Round {(round_num // 2) + 1}...'})}\n\n"

            current = debaters[current_debater]
            opponent = debaters[1 - current_debater]

            response = generate_debate_response(
                current[0], topic, article,
                debate_history[-1]["text"],
                debate_history,
                current[2]
            )

            debate_history.append({
                "speaker": current[1]["name"],
                "text": response,
                "debater_key": current[0]
            })

            yield f"data: {json.dumps({'type': 'statement', 'speaker': current[1]['name'], 'avatar': current[1]['avatar'], 'color': current[1]['color'], 'text': response})}\n\n"

            current_debater = 1 - current_debater

        # Analysis
        yield f"data: {json.dumps({'type': 'status', 'message': 'Analyzing the carnage...'})}\n\n"
        analysis = analyze_gaslighting(debate_history)
        yield f"data: {json.dumps({'type': 'analysis', 'data': analysis})}\n\n"

        yield f"data: {json.dumps({'type': 'complete'})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
