# PublicPulse Phase 0 - Ingestion Guide

## Overview

PublicPulse Phase 0 is now fully operable locally with a clean, repeatable workflow. The developer manually controls what movies and gadgets are ingested via a single JSON file.

## Quick Start

### 1. Edit the Input File

Edit `backend/data/input/items.json`:

```json
{
  "movies": [
    "Moana 2",
    "Wicked"
  ],
  "gadgets": [
    "iPhone 16 Pro",
    "Samsung Galaxy S24"
  ]
}
```

**Rules:**
- Either key (`movies` or `gadgets`) may be omitted or empty
- Empty lists are handled safely
- No hardcoded movie or gadget names exist in the code

### 2. Run Ingestion

```bash
cd backend
python -m app.scripts.run_ingestion
```

**This command:**
- Reads titles from `items.json`
- Loops through movies and gadgets independently
- Skips categories with no items
- Fetches YouTube comments
- Curates comments into buckets
- Synthesizes editorial summaries
- Updates cached JSON output

**No FastAPI server required!**

### 3. Verify Output

Check the cached output in:
- `backend/data/movies/` - Movie snapshots
- `backend/data/gadgets/` - Gadget snapshots

### 4. Start the API (Optional)

```bash
cd backend
uvicorn app.main:app --reload
```

The API endpoints will now reflect the updated data:
- `GET http://localhost:8000/movies`
- `GET http://localhost:8000/gadgets`
- `GET http://localhost:8000/movies/{slug}`
- `GET http://localhost:8000/gadgets/{slug}`

### 5. View in Frontend (Optional)

Start the frontend and refresh to see updated content:

```bash
cd frontend
npm run dev
```

## Architecture

### Source of Truth

**File:** `backend/data/input/items.json`

This is the ONLY source of titles. Structure:

```json
{
  "movies": [string],
  "gadgets": [string]
}
```

### Shared Ingestion Function

**File:** `backend/app/core/ingestion.py`

The ingestion logic exists as a single callable function that:
- Reads titles from `items.json`
- Loops through movies and gadgets independently
- Uses existing adapters and logic
- Preserves ALL Phase 0 rules:
  - YouTube-only
  - Rule-based bucketing
  - Strict bucket limits
  - Groq summarization from buckets only
  - Single snapshot overwrite

### CLI Operation

**File:** `backend/app/scripts/run_ingestion.py`

Run via: `python -m app.scripts.run_ingestion`

This script:
- Imports and calls the shared ingestion function
- Executes when run as `__main__`
- Prints minimal progress logs
- Does NOT require FastAPI to be running
- Takes NO CLI arguments

### FastAPI Compatibility

**Endpoint:** `POST /admin/run-ingestion`

The admin endpoint calls the same shared ingestion function. No changes to endpoint signature or behavior.

## Phase 0 Rules (Preserved)

1. **YouTube-only** - All comments come from YouTube API v3
2. **Rule-based bucketing** - Keyword-based classification (no embeddings)
3. **Strict bucket limits:**
   - `working`: 3 items
   - `mixed`: 2 items
   - `concerns`: 2 items
   - `resonates`: 2 items
4. **Groq summarization** - Uses `qwen/qwen-2.5-32b-instruct` with temperature 0.2
5. **Single snapshot overwrite** - One JSON file per item, no history
6. **No raw comments** - Only curated buckets and summary are stored
7. **No scores, ratings, or verdicts** - Editorial tone only

## What Was Changed

### New Files Created

1. `backend/data/input/items.json` - Input configuration
2. `backend/app/core/ingestion.py` - Shared ingestion logic
3. `backend/app/core/__init__.py` - Module initialization
4. `backend/app/scripts/run_ingestion.py` - CLI runner
5. `backend/app/scripts/__init__.py` - Module initialization

### Modified Files

1. `backend/app/main.py` - Admin endpoint now uses shared function

### No Changes To

- Editorial logic
- Bucketing rules
- RAG prompts
- Adapters (movies, gadgets)
- Curation engine
- Storage patterns
- API endpoints (besides admin)
- Dependencies

## Example Workflow

```bash
# 1. Edit input file
code backend/data/input/items.json

# Add:
# {
#   "movies": ["Moana 2"],
#   "gadgets": []
# }

# 2. Run ingestion
cd backend
python -m app.scripts.run_ingestion

# Output:
# ============================================================
# PublicPulse Phase 0 - Ingestion Runner
# ============================================================
#
# === Processing 1 movies ===
#
# [MOVIES] Moana 2
#   → Fetching comments...
#   → Fetched 150 comments
#   → Curating buckets...
#   → Synthesizing summary...
#   ✓ Saved: moana-2
#
# === No gadgets to process ===
#
# ============================================================
# INGESTION COMPLETE
# ============================================================
#
# Movies:  1 succeeded, 0 failed
# Gadgets: 0 succeeded, 0 failed

# 3. Verify output
ls backend/data/movies/moana-2.json

# 4. View in API (optional)
curl http://localhost:8000/movies/moana-2
```

## Validation Checklist

After changes, ALL of the following work:

- [x] Edit `backend/data/input/items.json`
- [x] Run `python -m app.scripts.run_ingestion`
- [x] Cached JSON output updates deterministically
- [x] API endpoints reflect new data
- [x] Frontend reflects updated content after refresh

Cached output remains:
- [x] One snapshot per item
- [x] No raw comments
- [x] No scores, ratings, or verdicts

## What Was NOT Added

- No scheduling
- No UI input
- No new APIs
- No databases
- No authentication
- No new dependencies
- No changes to editorial logic
- No abstractions or future placeholders

## Troubleshooting

### Error: Input file not found

```
ERROR: Input file not found: C:\...\backend\data\input\items.json
```

**Solution:** Create the file:

```bash
mkdir -p backend/data/input
echo '{"movies":[],"gadgets":[]}' > backend/data/input/items.json
```

### Error: No comments found

```
Error processing movie 'XYZ': No comments found for 'XYZ'
```

**Solution:** The item name might be incorrect or no YouTube videos exist with comments. Try:
- Check spelling
- Use exact release name
- Ensure videos exist on YouTube

### Error: Module not found

```
ModuleNotFoundError: No module named 'app'
```

**Solution:** Run from the backend directory:

```bash
cd backend
python -m app.scripts.run_ingestion
```

## Next Steps

This completes Phase 0 local operation. Future phases may add:
- Scheduling (cron, Celery)
- Web UI for input management
- Multi-snapshot history
- Additional data sources
- Authentication

But for now, keep it simple!
