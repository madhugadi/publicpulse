# PublicPulse - Quick Start Guide

Get PublicPulse running locally in minutes.

---

## Prerequisites

1. **Python 3.10+** installed
2. **Node.js 18+** installed
3. **API Keys**:
   - YouTube Data API key ([Get one here](https://console.cloud.google.com/apis/credentials))
   - Groq API key ([Get one here](https://console.groq.com/))

---

## Step 1: Clone and Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment (Unix/Mac)
python -m venv venv
source venv/bin/activate

# Or on Windows
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

**Edit `backend/.env`:**
```
YOUTUBE_API_KEY=your_actual_youtube_api_key
GROQ_API_KEY=your_actual_groq_api_key
```

**Start backend:**
```bash
python -m app.main
```

✓ Backend running at `http://localhost:8000`

---

## Step 2: Setup Frontend

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.local.example .env.local
```

**Start frontend:**
```bash
npm run dev
```

✓ Frontend running at `http://localhost:3000`

---

## Step 3: Ingest Your First Item

**Test with a Movie:**
```bash
curl -X POST http://localhost:8000/admin/run-ingestion \
  -H "Content-Type: application/json" \
  -d '{
    "category": "movies",
    "item_name": "Wicked",
    "actor_names": ["Cynthia Erivo", "Ariana Grande"]
  }'
```

**Or test with a Gadget:**
```bash
curl -X POST http://localhost:8000/admin/run-ingestion \
  -H "Content-Type: application/json" \
  -d '{
    "category": "gadgets",
    "item_name": "Samsung Galaxy S24 Ultra"
  }'
```

---

## Step 4: View Results

1. Open `http://localhost:3000` in your browser
2. Click **Movies** or **Gadgets** in navigation
3. See your ingested item in the grid
4. Click to view full editorial summary

---

## Troubleshooting

**Backend won't start:**
- Check that port 8000 is not in use
- Verify Python virtual environment is activated
- Check `.env` file exists with valid API keys

**Frontend won't start:**
- Check that port 3000 is not in use
- Run `npm install` again
- Delete `node_modules` and `.next`, then reinstall

**Ingestion fails:**
- Verify YouTube API key is valid and has quota
- Check that the movie/gadget name is spelled correctly
- Ensure the item was released recently (within 7-10 days for best results)

**No comments found:**
- Try a more popular/recent item
- Check YouTube directly to see if public comments exist
- Adjust search queries if needed (in `backend/app/adapters/`)

---

## What's Next?

- Ingest more movies and gadgets
- Review the editorial summaries
- Explore the structured buckets
- Run re-ingestion to update with rolling snapshots

See `README.md` for full documentation.
