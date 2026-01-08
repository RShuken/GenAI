# The Gaslighting Wiki Debates 🔥

> Two AIs argue about things that don't exist, each trying to gaslight the other with confident reasoning about completely fabricated topics.

![Demo](https://img.shields.io/badge/Status-Ready%20to%20Gaslight-purple)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/RShuken/GenAI&env=ANTHROPIC_API_KEY)

## What is this?

A wild Gen AI demo that combines:

1. **Infinite Wiki** - Generates convincing Wikipedia-style articles about completely fake topics
2. **AI Debate Arena** - Two AI personas with distinct gaslighting styles debate about these fake topics
3. **Live Updates** - Watch the chaos unfold in real-time
4. **Post-Debate Analysis** - Get a breakdown of gaslighting techniques used

## The Debaters

| Persona | Style | Tactics |
|---------|-------|---------|
| 🎓 Professor Thornberry | Academic Condescension | Fake citations, patronizing corrections, invented history |
| 🔺 Uncle Randy | Conspiracy Confidence | Hidden connections, "do your research", shadow organizations |
| 💼 Cynthia Sterling, MBA | Corporate Doublespeak | Buzzword bombardment, fake metrics, pivot and redirect |
| 🔮 Sage Moonbeam | Spiritual Superiority | Energy appeals, ancient wisdom, vibrational logic |

## Deploy to Vercel (Recommended)

The easiest way to deploy this app:

### 1. Click the Deploy Button

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/RShuken/GenAI&env=ANTHROPIC_API_KEY)

### 2. Add Your API Key

When prompted, add your `ANTHROPIC_API_KEY` environment variable.

### 3. Done!

Your app will be live at `your-project.vercel.app`

## Manual Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add environment variable
vercel env add ANTHROPIC_API_KEY
```

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up your API key

```bash
export ANTHROPIC_API_KEY=your-key-here
```

### 3. Run the app

```bash
python app.py
```

### 4. Open your browser

Navigate to `http://localhost:5000`

## How it Works

1. **Generate a Topic** - Click to generate a random fake Wikipedia topic
2. **Generate Article** - Create a full fake article with "facts" and controversies
3. **Select Debaters** - Choose two AI personas with different gaslighting styles
4. **Watch the Debate** - See them argue about things that don't exist
5. **Read the Analysis** - Get a breakdown of who was more convincing

## Features

- 🎲 Random topic generation across 10 categories
- 📖 Full Wikipedia-style article generation with debatable "facts"
- 🎭 4 unique debater personas with distinct gaslighting tactics
- ⚡ Real-time debate updates
- 📊 Post-debate analysis with:
  - Winner determination
  - Best gaslight moment
  - Techniques breakdown
  - Audience warning

## Project Structure

```
GenAI/
├── index.html          # Frontend (static)
├── api/
│   └── index.py        # Vercel serverless API
├── app.py              # Local Flask server
├── demo.py             # Terminal demo script
├── vercel.json         # Vercel configuration
└── requirements.txt    # Python dependencies
```

## Tech Stack

- **Backend**: Python + Flask (Vercel Serverless)
- **AI**: Anthropic Claude API
- **Frontend**: Vanilla HTML/CSS/JS
- **Hosting**: Vercel

## Warning

⚠️ **NOTHING IN THIS APP IS REAL** ⚠️

All Wikipedia articles, facts, citations, and debate points are completely fabricated by AI. This is purely for entertainment and demonstration purposes.

## License

MIT - Go forth and gaslight responsibly.
