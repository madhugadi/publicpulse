# PublicPulse - Phase 0

Editorial intelligence platform that explains how audiences are reacting RIGHT NOW, using early public signals.

**NOT a ratings or review site.** This is a calm, balanced, editorial platform that reflects uncertainty and provides trust-first analysis.

---

## Project Overview

### Categories (Phase 0 - LOCKED)
- **Movies**: Understanding audience reactions to recent releases
- **Gadgets**: Understanding reactions to recent tech releases

### Core Philosophy
- No ratings, scores, verdicts, or hype
- No critic reviews
- Calm, balanced, editorial tone
- Always reflect uncertainty ("so far", "early reactions suggest")
- Strengths and concerns must coexist
- Never invent facts, trends, or names
- Trust-first, explain-not-judge philosophy

---

## Architecture

### Technology Stack

**Backend:**
- FastAPI (Python)
- YouTube Data API (public comments)
- Groq API with qwen/qwen-2.5-32b-instruct (LLM for synthesis)
- File-based JSON storage

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Server Components

---

## Data Flow

```
1. INGESTION (Manual via Admin Endpoint)
   ↓
   YouTube API → Category-Specific Adapter
   ↓
   Fetch public comments (filtered by recency)

2. CURATION (Rule-Based, No Embeddings)
   ↓
   Raw Comments → Keyword Matching
   ↓
   Structured Buckets:
   - What seems to be working (MAX 3 items)
   - Mixed responses (MAX 2 items)
   - Emerging concerns (MAX 2 items)
   - Who it seems to be resonating with (MAX 2 items)

3. SYNTHESIS (Rolling RAG Snapshot)
   ↓
   Current + Previous Snapshot → LLM
   ↓
   Editorial Summary (4-5 paragraphs)

4. STORAGE
   ↓
   JSON file per item (slug-based)

5. FRONTEND
   ↓
   Next.js Server Components → REST API
   ↓
   Grid view + Detail pages
```

---

## Project Structure

```
PublicPulse/
├── backend/
│   ├── app/
│   │   ├── adapters/          # Category-specific YouTube adapters
│   │   │   ├── base.py
│   │   │   ├── movies.py
│   │   │   └── gadgets.py
│   │   ├── curation/          # Rule-based bucketing engine
│   │   │   ├── engine.py
│   │   │   └── themes.py
│   │   ├── rag/               # Rolling snapshot synthesizer
│   │   │   └── synthesizer.py
│   │   ├── storage/           # JSON file storage
│   │   │   └── json_store.py
│   │   ├── api/               # FastAPI routes
│   │   │   ├── movies.py
│   │   │   └── gadgets.py
│   │   ├── config.py
│   │   └── main.py            # FastAPI app
│   ├── data/                  # JSON storage (git-ignored)
│   │   ├── movies/
│   │   └── gadgets/
│   └── requirements.txt
│
├── frontend/
│   ├── app/                   # Next.js App Router
│   │   ├── movies/
│   │   │   ├── page.tsx
│   │   │   └── [slug]/page.tsx
│   │   ├── gadgets/
│   │   │   ├── page.tsx
│   │   │   └── [slug]/page.tsx
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── Navigation.tsx
│   │   ├── ItemGrid.tsx
│   │   └── ItemCard.tsx
│   └── lib/
│       └── api.ts
│
└── README.md
```

---

## Setup Instructions

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

## Usage

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

## License

This is a Phase 0 prototype. All rights reserved.
