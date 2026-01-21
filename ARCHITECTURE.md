# PublicPulse - Architecture & Data Flow

Detailed explanation of how PublicPulse Phase 0 works.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Next.js)                     │
│  ┌───────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │  Movies   │  │  Gadgets   │  │  Individual Item      │  │
│  │  Grid     │  │  Grid      │  │  Detail Page          │  │
│  └───────────┘  └────────────┘  └──────────────────────┘  │
│                                                             │
│                    Server Components                        │
│                           ↓                                 │
└───────────────────────────┼─────────────────────────────────┘
                            │
                         REST API
                            │
┌───────────────────────────┼─────────────────────────────────┐
│                      BACKEND (FastAPI)                      │
│                           │                                 │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │              API Routes (movies, gadgets)             │ │
│  └────────────────────────┬──────────────────────────────┘ │
│                           │                                 │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │           JSON File Storage (slug-based)              │ │
│  └────────────────────────┬──────────────────────────────┘ │
│                           │                                 │
│                    Ingestion Pipeline                       │
│                           │                                 │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │                  Data Adapters                        │ │
│  │         ┌──────────────┬──────────────┐               │ │
│  │         │ Movies       │ Gadgets      │               │ │
│  │         │ Adapter      │ Adapter      │               │ │
│  │         └──────────────┴──────────────┘               │ │
│  └────────────────────────┬──────────────────────────────┘ │
│                           │                                 │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │              Curation Engine                          │ │
│  │         (Rule-based keyword matching)                 │ │
│  └────────────────────────┬──────────────────────────────┘ │
│                           │                                 │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │               RAG Synthesizer                         │ │
│  │         (Rolling snapshot with LLM)                   │ │
│  └────────────────────────┬──────────────────────────────┘ │
└───────────────────────────┼─────────────────────────────────┘
                            │
                    External Services
                            │
             ┌──────────────┴───────────────┐
             │                              │
    ┌────────▼────────┐          ┌─────────▼─────────┐
    │  YouTube API    │          │  LLM API          │
    │  (Comments)     │          │  (Groq/Qwen)      │
    └─────────────────┘          └───────────────────┘
```

---

## Data Flow: Ingestion Pipeline

### 1. Data Acquisition

**Input:**
- Category: "movies" or "gadgets"
- Item name: e.g., "Dune Part Two"
- Optional metadata: release date, actor names

**Process:**
1. Select category-specific adapter
2. Generate search queries based on category templates
3. Search YouTube for videos (filtered by recency)
4. Fetch public comments from top videos
5. Normalize comment text

**Output:**
- List of raw comment strings: `List[str]`
- Capped at 200 comments total

---

### 2. Curation (Rule-Based)

**Input:**
- Raw comment texts: `List[str]`
- Category-specific theme dictionary

**Process:**
```python
For each comment:
  1. Convert to lowercase
  2. Count keyword matches for each bucket:
     - working
     - mixed
     - concerns
     - resonates
  3. Assign comment to bucket with highest match count

For each bucket:
  1. Count keyword frequencies across all comments
  2. Filter for recurring themes (appears ≥2 times)
  3. Create concise theme sentences
  4. Apply strict bucket limits:
     - working: MAX 3
     - mixed: MAX 2
     - concerns: MAX 2
     - resonates: MAX 2
```

**Output:**
- Structured buckets:
```json
{
  "working": ["theme1", "theme2", "theme3"],
  "mixed": ["theme1", "theme2"],
  "concerns": ["theme1", "theme2"],
  "resonates": ["theme1", "theme2"]
}
```

**Token Safety:**
- Total items: MAX 9 across all buckets
- Each item: ONE concise sentence
- Raw comments NEVER sent to LLM

---

### 3. Synthesis (Rolling RAG)

**Input:**
- Current curated buckets (9 items max)
- Previous summary (if exists)

**Process:**

**First Run (No Previous Summary):**
```
Prompt = System Instructions + Current Buckets
LLM → Generate editorial summary (4-5 paragraphs)
Save as snapshot
```

**Subsequent Runs (With Previous Summary):**
```
Prompt = System Instructions + Previous Summary + Current Buckets
LLM → Generate new editorial summary (4-5 paragraphs)
Replace old snapshot with new summary
```

**Rules:**
- Slightly prioritize current buckets
- Do NOT describe differences or timelines
- Maintain constant snapshot size
- No historical accumulation

**Output:**
- Editorial summary (4-5 paragraphs)
- Calm, balanced tone
- Reflects uncertainty
- Strengths and concerns coexist

---

### 4. Storage

**Input:**
- Item metadata
- Curated buckets
- Synthesized summary

**Process:**
```python
data = {
  "title": "Dune Part Two",
  "slug": "dune-part-two",
  "category": "movies",
  "release_date": "2024-03-01",
  "last_updated_at": "2024-03-05T10:30:00Z",
  "buckets": { ... },
  "summary": "...",
  "actor_names": ["Timothée Chalamet", "Zendaya"]
}

# Save as JSON file
backend/data/movies/dune-part-two.json
```

**Output:**
- One JSON file per item
- Keyed by slug
- Timestamped

---

## Category-Specific Adapters

### Movies Adapter

**Search Queries (7-day recency):**
1. `{movie_name} USA premiere review`
2. `{movie_name} audience reaction`
3. `{movie_name} audience responses`
4. `{movie_name} first day response`
5. `{movie_name} public review`

**Special Handling:**
- Actor names (MAX 2)
- Injected into "working" bucket if provided
- Only if mentioned in multiple comments

---

### Gadgets Adapter

**Search Queries (10-day recency):**
1. `{gadget_name} unboxing`
2. `{gadget_name} first impressions`
3. `{gadget_name} hands on`
4. `{gadget_name} initial review`
5. `{gadget_name} issues`
6. `{gadget_name} problems`

**Special Handling:**
- No actor names
- Focus on features and issues
- Broader recency window (10 days)

---

## Frontend Request Flow

```
User visits /movies
     ↓
Next.js Server Component
     ↓
GET /movies (API call)
     ↓
FastAPI returns JSON array
     ↓
Server renders ItemGrid
     ↓
HTML sent to browser
     ↓
User clicks item
     ↓
Navigate to /movies/{slug}
     ↓
GET /movies/{slug}
     ↓
Server renders detail page with full summary + buckets
```

**Key Points:**
- All components are Server Components
- No client-side state management
- No caching (always fresh data)
- Minimal JavaScript

---

## Token Budget Management

### Why Token Safety Matters
- LLM APIs charge per token
- Large prompts = high costs
- Context windows have limits
- Need predictable, bounded costs

### How We Achieve It

**1. No Raw Comments to LLM:**
```
❌ BAD: Send 200 raw comments (5000+ tokens)
✓ GOOD: Send 9 curated items (200 tokens)
```

**2. Strict Bucket Limits:**
```
Working: MAX 3 items
Mixed: MAX 2 items
Concerns: MAX 2 items
Resonates: MAX 2 items
─────────────────────
TOTAL: MAX 9 items
```

**3. Rolling Snapshot (Not Accumulation):**
```
❌ BAD: Keep all historical summaries
✓ GOOD: Replace old snapshot each run
```

**4. Fixed Output Size:**
```
LLM always outputs: 4-5 paragraphs
max_tokens: 800 (controlled)
```

**Total Token Budget per Synthesis:**
- System prompt: ~300 tokens
- Previous summary: ~400 tokens
- Current buckets: ~200 tokens
- Output: ~800 tokens
- **Total: ~1700 tokens max**

---

## Deployment Architecture

### Phase 0 (Current)

```
Frontend: Local (http://localhost:3000)
Backend: Local (http://localhost:8000)
Storage: Local file system
Ingestion: Manual via cURL
```

### Phase 0 - Read-Only Deployment

```
Frontend: Vercel/Netlify (static export possible)
Backend: Railway/Render (with /admin/* protected)
Storage: Backend filesystem (ephemeral or persistent volume)
Ingestion: Manual via protected endpoint
```

**No infrastructure needed:**
- No databases
- No Redis
- No queues
- No schedulers

---

## Security Considerations

### Phase 0
- No authentication
- `/admin/run-ingestion` should be IP-restricted in production
- CORS limited to known frontend origins
- No user data collected
- No cookies or sessions

### Production Recommendations
- Add API key authentication for admin endpoints
- Rate limiting on ingestion endpoint
- Monitor YouTube API quota
- Monitor LLM API costs
- Add request logging

---

## Scalability Notes

### Current Limits (Phase 0)
- Manual ingestion only
- File-based storage (hundreds of items is fine)
- No real-time updates
- No incremental ingestion

### Future Scalability
When needed (NOT in Phase 0):
- Move to PostgreSQL for storage
- Add background job queue (Celery/RQ)
- Add caching layer (Redis)
- Add scheduled ingestion
- Add incremental comment fetching

---

## Testing Strategy

### Unit Tests (Not Implemented in Phase 0)
- Test curation engine with sample comments
- Test adapter query generation
- Test RAG prompt construction

### Integration Tests (Not Implemented in Phase 0)
- Test full ingestion pipeline
- Test API endpoints
- Test frontend rendering

### Manual Testing (Phase 0)
1. Ingest a movie
2. Verify JSON file created
3. Check buckets have correct limits
4. Verify summary is calm/balanced
5. View on frontend
6. Re-ingest same item
7. Verify rolling snapshot updated

---

## Performance Characteristics

### Ingestion Time
- YouTube API calls: 5-10 seconds
- Curation: <1 second
- LLM synthesis: 3-5 seconds
- Total: ~10-15 seconds per item

### Frontend Load Time
- Grid view: <500ms
- Detail view: <500ms
- (With local backend)

### Cost Per Item
- YouTube API: Free (within quota)
- Groq API (qwen-2.5-32b-instruct): Free tier available, ~$0.0001 per synthesis

---

## Extensibility

### Adding New Categories (Future)
1. Create new adapter in `backend/app/adapters/`
2. Define search queries
3. Add theme dictionary in `backend/app/curation/themes.py`
4. Add API routes
5. Add frontend pages
6. Update navigation

**Core pipeline remains unchanged.**

### Adding New Data Sources (Future)
1. Create new adapter extending `DataAdapter`
2. Implement `fetch_comments()` method
3. Return normalized `List[str]`
4. Rest of pipeline works as-is

---

## Known Limitations

### Phase 0
- No scheduling (manual ingestion)
- No incremental updates (full re-fetch)
- No comment deduplication
- No sentiment analysis (keyword matching only)
- No user accounts
- No bookmarking or favorites
- No search functionality
- English language only

### Technical Debt
- No error handling for API failures
- No retry logic
- No ingestion queue
- No admin UI (cURL only)
- No analytics

**These are acceptable for Phase 0.**
