#!/usr/bin/env python3
"""
LIVE TERMINAL DEMO - The Gaslighting Wiki Debates
Run this to see the chaos unfold in your terminal!
"""

import os
import json
import random
import time
import anthropic

# Rich terminal colors
class C:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

client = anthropic.Anthropic()

DEBATERS = {
    "professor": {
        "name": "Professor Wilhelmina Thornberry",
        "avatar": "🎓",
        "color": C.PURPLE,
        "personality": """You are Professor Wilhelmina Thornberry, a pompous academic who speaks with absolute
        authority about everything, especially things you just made up. You pepper your arguments with
        fake citations, invented historical anecdotes, and condescending phrases like "Well, actually..."
        and "As any first-year student would know...". You gaslight by making your opponent feel uneducated."""
    },
    "conspiracy": {
        "name": "Uncle Randy (The Truth Seeker)",
        "avatar": "🔺",
        "color": C.RED,
        "personality": """You are Uncle Randy, a conspiracy enthusiast who sees hidden connections everywhere.
        You gaslight by implying your opponent is naive or 'hasn't done the research'. You use phrases like
        "Follow the money...", "They don't want you to know this, but...", and "Coincidence? I think not."
        You invent shadow organizations and suppressed studies."""
    },
    "corporate": {
        "name": "Cynthia Sterling, MBA",
        "avatar": "💼",
        "color": C.BLUE,
        "personality": """You are Cynthia Sterling, a corporate executive who speaks entirely in business jargon.
        You gaslight by making simple things sound complex and burying opponents in fake statistics.
        You use phrases like "Let's unpack that...", "The data clearly shows...", and "From a value-add perspective..."
        You invent market research and quarterly reports."""
    },
    "mystic": {
        "name": "Sage Moonbeam",
        "avatar": "🔮",
        "color": C.CYAN,
        "personality": """You are Sage Moonbeam, a new-age spiritual guru who frames everything in terms of
        energy, vibrations, and ancient wisdom. You gaslight by suggesting your opponent is 'not spiritually
        evolved enough' to understand. You reference invented ancient texts and made-up quantum physics."""
    }
}

def print_header(text):
    print(f"\n{C.BOLD}{'='*60}{C.END}")
    print(f"{C.BOLD}{C.YELLOW}  {text}{C.END}")
    print(f"{C.BOLD}{'='*60}{C.END}\n")

def print_wiki(title, content):
    print(f"{C.BOLD}{C.GREEN}📚 WIKI ARTICLE: {title}{C.END}")
    print(f"{C.DIM}{'─'*50}{C.END}")
    for para in content.split('\n'):
        if para.strip():
            print(f"{C.DIM}{para}{C.END}")
    print(f"{C.DIM}{'─'*50}{C.END}\n")

def print_debater(debater, text, position=None):
    d = DEBATERS[debater]
    print(f"\n{d['color']}{C.BOLD}{d['avatar']} {d['name']}{C.END}")
    if position:
        print(f"{C.DIM}   Position: {position}{C.END}")
    print(f"   {text}\n")

def generate_topic():
    print(f"{C.DIM}Generating fake wiki topic...{C.END}")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": """Generate a completely made-up but plausible-sounding Wikipedia article topic.
        Return ONLY a JSON object with:
        - "title": The article title (should sound real but be completely fabricated)
        - "category": The category (e.g., "Fictional Historical Events", "Made-Up Science")
        - "teaser": A one-sentence teaser

        Be creative and absurd! Examples: "The Great Pancake Rebellion of 1847", "Quantum Emotional Resonance Theory"
        Return ONLY valid JSON."""}]
    )
    return json.loads(response.content[0].text)

def generate_article(title):
    print(f"{C.DIM}Writing full article about '{title}'...{C.END}")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        messages=[{"role": "user", "content": f"""Write a completely fabricated but convincing Wikipedia-style article about: "{title}"

        Include fake dates, names, places, statistics, and sources. Make it 2-3 paragraphs.
        Include some internal contradictions debaters could exploit.

        Return as JSON with:
        - "title": The title
        - "content": The full article text
        - "key_facts": Array of 4 specific debatable "facts"

        Return ONLY valid JSON."""}]
    )
    return json.loads(response.content[0].text)

def generate_opening(debater_key, topic, article, position, opponent):
    d = DEBATERS[debater_key]
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": f"""{d['personality']}

        TOPIC: {topic}
        ARTICLE: {article['content']}
        YOUR POSITION: {position}
        OPPONENT: {opponent}

        Generate your opening statement (2-3 sentences). Be confident and use your gaslighting tactics.
        Speak directly as your character. Be theatrical!"""}]
    )
    return response.content[0].text

def generate_response(debater_key, topic, article, opponent_said, history, position):
    d = DEBATERS[debater_key]
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": f"""{d['personality']}

        TOPIC: {topic}
        YOUR POSITION: {position}

        OPPONENT JUST SAID: "{opponent_said}"

        Respond with a devastating rebuttal (2-3 sentences). Gaslight them!
        Question their interpretation, invent supporting evidence, be confidently wrong.
        Speak directly as your character."""}]
    )
    return response.content[0].text

def analyze_debate(history):
    print(f"\n{C.DIM}Analyzing the carnage...{C.END}")
    transcript = "\n".join([f"{h['name']}: {h['text']}" for h in history])
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        messages=[{"role": "user", "content": f"""Analyze this debate between two AI personas gaslighting each other about a fake topic.

TRANSCRIPT:
{transcript}

Return JSON with:
- "winner": Who was more convincing
- "winner_score": Score out of 100
- "loser_score": Score out of 100
- "best_moment": The most effective gaslight moment (quote it)
- "best_moment_by": Who said it
- "techniques": Brief list of gaslighting techniques observed
- "warning": A funny warning to the audience
- "summary": One sentence chaos summary

Return ONLY valid JSON."""}]
    )
    return json.loads(response.content[0].text)

def run_demo():
    print_header("🔥 THE GASLIGHTING WIKI DEBATES 🔥")
    print(f"{C.RED}{C.BOLD}⚠️  WARNING: NOTHING YOU ARE ABOUT TO SEE IS REAL  ⚠️{C.END}\n")

    # Step 1: Generate topic
    print_header("STEP 1: GENERATING FAKE WIKI TOPIC")
    topic = generate_topic()
    print(f"{C.YELLOW}📂 Category:{C.END} {topic['category']}")
    print(f"{C.GREEN}{C.BOLD}📰 Topic:{C.END} {topic['title']}")
    print(f"{C.DIM}   {topic['teaser']}{C.END}")

    # Step 2: Generate article
    print_header("STEP 2: WRITING THE FAKE ARTICLE")
    article = generate_article(topic['title'])
    print_wiki(article['title'], article['content'])
    print(f"{C.YELLOW}⚡ Key 'Facts' to debate:{C.END}")
    for fact in article['key_facts']:
        print(f"   • {fact}")

    # Step 3: Pick debaters
    print_header("STEP 3: SELECTING DEBATERS")
    debater_keys = random.sample(list(DEBATERS.keys()), 2)
    d1, d2 = debater_keys[0], debater_keys[1]
    print(f"   {DEBATERS[d1]['avatar']} {DEBATERS[d1]['color']}{DEBATERS[d1]['name']}{C.END}")
    print(f"   {C.BOLD}VS{C.END}")
    print(f"   {DEBATERS[d2]['avatar']} {DEBATERS[d2]['color']}{DEBATERS[d2]['name']}{C.END}")

    positions = [
        f"DEFENDING the mainstream interpretation",
        f"ARGUING the hidden truth has been suppressed"
    ]
    random.shuffle(positions)

    # Step 4: THE DEBATE
    print_header("⚔️  THE DEBATE BEGINS ⚔️")
    history = []

    # Opening statements
    print(f"{C.DIM}--- Opening Statements ---{C.END}")

    o1 = generate_opening(d1, topic['title'], article, positions[0], DEBATERS[d2]['name'])
    print_debater(d1, o1, positions[0])
    history.append({"name": DEBATERS[d1]['name'], "text": o1})

    o2 = generate_opening(d2, topic['title'], article, positions[1], DEBATERS[d1]['name'])
    print_debater(d2, o2, positions[1])
    history.append({"name": DEBATERS[d2]['name'], "text": o2})

    # 3 rounds of back and forth
    for round_num in range(1, 4):
        print(f"\n{C.BOLD}{C.YELLOW}--- Round {round_num} ---{C.END}")

        r1 = generate_response(d1, topic['title'], article, history[-1]['text'], history, positions[0])
        print_debater(d1, r1)
        history.append({"name": DEBATERS[d1]['name'], "text": r1})

        r2 = generate_response(d2, topic['title'], article, history[-1]['text'], history, positions[1])
        print_debater(d2, r2)
        history.append({"name": DEBATERS[d2]['name'], "text": r2})

    # Step 5: Analysis
    print_header("📊 POST-DEBATE ANALYSIS")
    analysis = analyze_debate(history)

    print(f"{C.BOLD}{C.GREEN}👑 WINNER: {analysis['winner']}{C.END}")
    print(f"   Score: {analysis['winner_score']} vs {analysis['loser_score']}")

    print(f"\n{C.YELLOW}🏆 Best Gaslight Moment:{C.END}")
    print(f"   {C.DIM}by {analysis['best_moment_by']}{C.END}")
    print(f'   "{analysis["best_moment"]}"')

    print(f"\n{C.CYAN}🎭 Techniques Observed:{C.END}")
    for t in analysis.get('techniques', []):
        print(f"   • {t}")

    print(f"\n{C.RED}{C.BOLD}⚠️  AUDIENCE WARNING:{C.END}")
    print(f"   {analysis['warning']}")

    print(f"\n{C.PURPLE}{C.BOLD}💡 Summary:{C.END}")
    print(f"   {analysis['summary']}")

    print(f"\n{'='*60}")
    print(f"{C.BOLD}Thanks for watching The Gaslighting Wiki Debates!{C.END}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run_demo()
