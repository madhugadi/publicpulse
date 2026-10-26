# 📰 PublicPulse

**Understand how audiences are reacting to new releases right now, without the hype.**

PublicPulse is an editorial intelligence platform. It reads early public reactions to new **movies** and **gadgets** and turns them into calm, balanced summaries: what people like, what's mixed, what concerns are starting to show up, and who it seems to resonate with.

It is **not** a ratings or review site. There are no scores, no verdicts, and no critic reviews, just an honest picture of early reactions that always reflects how uncertain they are ("so far," "early reactions suggest").

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-000000?logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq-F55036)

> **Status:** Phase 0 prototype, covering Movies and Gadgets.

---

## ✨ Features

- **Early-signal analysis:** collects recent public comments from YouTube premiere, reaction, unboxing, and first-impression videos
- **Balanced summaries:** sorts reactions into *what seems to be working*, *mixed responses*, *emerging concerns*, and *who it's resonating with*
- **Rolling updates:** each new run blends the latest reactions with the previous snapshot, so summaries stay current without growing endlessly
- **Trust first:** the LLM never invents facts, trends, or names, and strengths and concerns always appear side by side
- **Token-efficient by design:** raw comments never go to the LLM, only a small curated set (9 points at most)
- **Clean, calm UI:** separate Movies and Gadgets sections with a grid view and detail pages

---

## 🏗️ How It Works

```
 YouTube Data API ──► Category adapter (movies / gadgets)
                              │   recent public comments
                              ▼
                     Rule-based curation (keyword themes)
                              │   ≤ 3 working · ≤ 2 mixed · ≤ 2 concerns · ≤ 2 audience
                              ▼
          Previous snapshot + current buckets ──► Groq LLM (Llama 3.1 8B)
                              │   4–5 paragraph editorial summary
                              ▼
                     JSON snapshot per item ──► FastAPI ──► Next.js frontend
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full design and [QUICKSTART.md](QUICKSTART.md) for a fast setup.

---

## 🧰 Tech Stack

**Backend:** Python · FastAPI · YouTube Data API · Groq (Llama 3.1 8B Instant) · JSON file storage
**Frontend:** Next.js 14 (App Router, Server Components) · TypeScript · Tailwind CSS
**Deployment:** Docker

---

## 📁 Project Structure

```
publicpulse/
├── backend/
│   ├── app/
│   │   ├── adapters/          # Category-specific YouTube adapters
│   │   │   ├── base.py
│   │   │   ├── movies.py
│   │   │   └── gadgets.py
│   │   ├── curation/          # Rule-based bucketing engine
│   │   ├── rag/               # Rolling snapshot synthesizer
│   │   ├── storage/           # JSON file storage
│   │   ├── api/               # FastAPI routes
│   │   ├── config.py
│   │   └── main.py            # FastAPI app
│   ├── data/                  # JSON storage (git-ignored)
│   └── requirements.txt
│
├── frontend/
│   ├── app/                   # Next.js App Router (movies/, gadgets/, [slug] pages)
│   ├── components/            # Navigation, ItemGrid, ItemCard
│   └── lib/api.ts
│
├── ARCHITECTURE.md
├── QUICKSTART.md
└── Dockerfile
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- YouTube Data API key
- Groq API key

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

6. Run the backend:
```bash
python -m app.main
```

Backend will run at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```bash
cp .env.local.example .env.local
```

4. Verify the API URL in `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. Run the frontend:
```bash
npm run dev
```

Frontend will run at `http://localhost:3000`

---

## 🔌 Usage

### Running Ingestion (Manual)

Use the admin endpoint to ingest a new movie or gadget:

**Ingest a Movie:**
```bash
curl -X POST http://localhost:8000/admin/run-ingestion \
  -H "Content-Type: application/json" \
  -d '{
    "category": "movies",
    "item_name": "Dune Part Two",
    "release_date": "2024-03-01",
    "actor_names": ["Timothée Chalamet", "Zendaya"]
  }'
```

**Ingest a Gadget:**
```bash
curl -X POST http://localhost:8000/admin/run-ingestion \
  -H "Content-Type: application/json" \
  -d '{
    "category": "gadgets",
    "item_name": "iPhone 15 Pro"
  }'
```

### API Endpoints

**Public Endpoints:**
- `GET /health` - Health check
- `GET /movies` - List all movies
- `GET /movies/{slug}` - Get specific movie
- `GET /gadgets` - List all gadgets
- `GET /gadgets/{slug}` - Get specific gadget

**Admin Endpoints:**
- `POST /admin/run-ingestion` - Run manual ingestion

---

## Category-Specific Data Sources

### Movies
YouTube queries (7-day recency):
1. `<MOVIE_NAME> USA premiere review`
2. `<MOVIE_NAME> audience reaction`
3. `<MOVIE_NAME> audience responses`
4. `<MOVIE_NAME> first day response`
5. `<MOVIE_NAME> public review`

### Gadgets
YouTube queries (10-day recency):
1. `<GADGET_NAME> unboxing`
2. `<GADGET_NAME> first impressions`
3. `<GADGET_NAME> hands on`
4. `<GADGET_NAME> initial review`
5. `<GADGET_NAME> issues`
6. `<GADGET_NAME> problems`

---

## Deployment Notes

### Phase 0 Limitations
- No AWS/cloud deployment yet
- No automated schedulers
- No authentication
- No analytics or click tracking
- No Twitter/X data source
- No embeddings or vector search
- Manual ingestion only

### Safe for Read-Only Deployment
The application is safe to deploy in read-only mode:
- Frontend can be deployed to Vercel/Netlify
- Backend can be deployed to Railway/Render
- Set CORS origins appropriately
- Disable or protect `/admin/*` endpoints in production

---

## Phase 0 Constraints

**Bucket Limits (STRICT):**
- What seems to be working: MAX 3 items
- Mixed responses: MAX 2 items
- Emerging concerns: MAX 2 items
- Who it seems to be resonating with: MAX 2 items

**Actor/Name Extraction (Movies Only):**
- MAX 2 names per movie
- Only if mentioned in multiple comments OR provided as metadata
- LLM must NEVER guess names

**Rolling Snapshot Logic:**
- ONE snapshot per item (constant size)
- First run: summarize CURRENT snapshot only
- Later runs: summarize PREVIOUS + CURRENT (slightly prioritize current)
- Output REPLACES old snapshot
- No historical accumulation
- No timeline descriptions

---

## Development Notes

### Token Safety
- Raw comments NEVER go to LLM
- Only curated buckets (max 9 items total) sent to LLM
- Fixed-size prompts with strict limits
- No context accumulation

### Data Integrity
- Each category has its own adapter
- Core pipeline is category-agnostic
- Adapters output normalized text: `List[str]`
- No mixing of categories in UI

### UI Discipline
- Movies and Gadgets have separate pages
- Each category has its own grid
- Navigation allows category switching
- Calm, uncluttered design
- No UI libraries or state management

---

## 👤 Author

**Madhu** · [GitHub](https://github.com/madhugadi)

## License

This is a Phase 0 prototype. All rights reserved.
