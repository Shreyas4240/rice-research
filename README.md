# RiceResearchFinder

> AI-powered research discovery and outreach platform for Rice University students.

Upload your resume, enter your research interests, and get matched with Rice faculty whose work aligns with where you want to go — not just where you've been. Then generate a personalized outreach email draft in one click.

## Features

- **Smart Faculty Matching**: AI-powered matching based on research interests and resume analysis
- **Personalized Email Generation**: Generate professional outreach emails with one click
- **Comprehensive Faculty Database**: Search across 293+ Rice Engineering faculty
- **Resume Analysis**: Extract skills, experience, and research themes automatically
- **Research Interest Discovery**: Find faculty by keywords, departments, and research areas
- **Save & Track**: Bookmark professors and track application progress

## Tech Stack

| Part | Stack | Location |
|------|-------|----------|
| Crawler | Python + Playwright + BeautifulSoup | `/crawler` |
| Backend | FastAPI + SQLAlchemy + AI Services | `/backend` |
| Frontend | Vite + React 18 + Tailwind CSS | `/ui` |

## Quick Start

### Frontend (works without backend — static search only)

```bash
cd ui
npm install
npm run dev
# → http://localhost:5173
```

`/search` works immediately using `ui/public/faculty.json`. The `/discover` and `/match` features require the backend.

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # then edit .env

uvicorn main:app --reload
# → http://localhost:8000
# → API docs: http://localhost:8000/docs
```

Faculty data from `ui/public/faculty.json` is **auto-imported on startup**. No manual step needed.

### Crawler (to collect fresh faculty data)

```bash
cd crawler
pip install -r requirements.txt
playwright install chromium
python crawl.py
# writes faculty.json + faculty.csv
cp crawler/faculty.json ui/public/faculty.json
```

## Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|---|---|---|
| `TOGETHER_API_KEY` | _(empty)_ | Together AI API key for resume parsing |
| `GEMINI_API_KEY` | _(empty)_ | Google Gemini API key for email generation |
| `CORS_ORIGINS` | `http://localhost:5173` | Allowed frontend origins (comma-separated) |

### Frontend (`ui/.env.local`)

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | _(empty)_ | Backend base URL (e.g. `https://api.yourapp.com`). In dev, Vite proxies `/api` → `localhost:8000` automatically. |

## API Reference

Full interactive docs at `http://localhost:8000/docs`.

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Health check + AI service status |
| `GET` | `/api/faculty` | List all faculty |
| `GET` | `/api/faculty/{id}` | Get one faculty record |
| `POST` | `/api/faculty/import` | Re-import faculty.json into the database |
| `POST` | `/api/resume/upload` | Upload resume PDF/DOCX + interests → `session_id` + parsed profile |
| `GET` | `/api/resume/{session_id}` | Retrieve a session |
| `POST` | `/api/match` | Run matching → ranked professors with fit labels |
| `POST` | `/api/email/draft` | Generate a draft outreach email |

## 🤖 AI Features

**Mock mode** (no API key) — app is fully functional:
- Resume parsing uses keyword heuristics (extracts skills, tools, inferred themes from text)
- Match explanations use research summary snippets + interest text
- Email drafts use polished, tone-aware templates

**Real mode** (with API keys) — powered by AI:
- Structured JSON resume parsing via LLM
- Natural-language match explanations (top 10 results)
- Fully personalized email drafts

## Matching Algorithm

Matching is **interest-driven** — the student's stated interests dominate. Resume provides a secondary boost.

1. Tokenize the student's stated interests
2. Score each professor:
   - `interest_score` = keyword overlap(interests, research_summary + name + dept)
   - `resume_score` = keyword overlap(resume themes + skills, research_summary) × 0.35
   - `total = interest_score + resume_score`
3. Rank by total score, assign fit labels:
   - **Strong Fit** — score ≥ 60% of top result
   - **Exploratory Fit** — score ≥ 25% of top result
   - **Adjacent Fit** — everything else
4. Return top 20 with per-professor match explanations

## Data Models

**Faculty** (stored in `faculty.json`)
```json
{
  "id": "unique_id",
  "name": "Prof. Name",
  "title": "Title",
  "department": "department_code",
  "email": "email@rice.edu",
  "research_summary": "Detailed research description",
  "ai_review": "Clean AI-generated summary",
  "lab_website": "https://lab.url.com",
  "photo_url": "https://photo.url.com"
}
```

**Resume Session** (in-memory storage)
```json
{
  "session_id": "uuid",
  "parsed_profile": {
    "name": "Student Name",
    "technical_skills": ["Python", "Machine Learning"],
    "inferred_themes": ["AI", "Data Science"],
    "coursework": ["CS 331", "STAT 415"]
  },
  "interests": "machine learning, AI research"
}
```

**Email draft**
```json
{ "subject", "body", "tone", "faculty_id", "session_id", "mock_mode" }
```

## Project Structure

```
RiceResearchFinder/
├── backend/                    # FastAPI backend
│   ├── data/                   # Faculty data files
│   │   └── faculty.json       # Clean faculty dataset (293 records)
│   ├── data_store.py          # Central data management (no DB)
│   ├── main.py                # FastAPI app + CORS + routes
│   ├── requirements.txt        # Python dependencies
│   ├── routers/               # API endpoints
│   │   ├── faculty.py         # Faculty search/list
│   │   ├── resume.py          # Resume upload + session storage
│   │   ├── match.py           # AI matching (client-side)
│   │   └── email.py           # Email generation (Gemma 3)
│   └── services/              # Business logic
│       ├── llm.py             # Gemini/Together AI clients
│       ├── emailer.py         # Email draft generation
│       ├── parser.py          # Resume text extraction
│       └── matcher.py         # Matching algorithm
├── ui/                        # React frontend
│   ├── public/
│   │   └── faculty.json       # Faculty data (synced with backend)
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── ProfCard.jsx   # Faculty profile cards
│   │   │   ├── EmailModal.jsx # Email generation UI
│   │   │   └── tracker/       # Application tracking
│   │   ├── pages/             # Main application pages
│   │   │   ├── Results.jsx    # Search results + filters
│   │   │   ├── Discover.jsx   # Resume upload flow
│   │   │   ├── Match.jsx      # AI matching results
│   │   │   └── ProfDetail.jsx # Individual professor pages
│   │   ├── utils/             # Client-side logic
│   │   │   ├── search.js      # Faculty search + scoring
│   │   │   ├── matcher.js     # Resume-based matching
│   │   │   └── api.js         # API client
│   │   └── App.jsx            # Main app + routing
├── crawler/                   # Faculty data collection
└── DEPLOYMENT.md             # Production deployment guide
```

## Deployment

### Production Setup

- **Frontend**: Vercel — Root Directory: `ui`. Set `VITE_API_BASE_URL` env var to your backend URL.
- **Backend**: Railway / Render / AWS — set environment variables for AI services.
- `faculty.json` is loaded directly from file system (no database required).

### Quick Deploy

```bash
# Frontend (Vercel)
cd ui
vercel --prod

# Backend (Railway)
git push origin main  # Auto-deploys from GitHub
```

### AWS App Runner Alternative

```bash
# Build and deploy
docker build -t rice-research-finder .
aws ecr create-repository --repository-name rice-research-finder
# Push to ECR and deploy to App Runner
```

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home — hero, how-it-works, CTAs |
| `/search` | Faculty search — keyword + department filter |
| `/discover` | Resume upload + interest entry |
| `/match` | AI match dashboard — ranked results with fit labels |
| `/prof/:id` | Professor detail — research + Draft Email button |
| `/saved` | Bookmarked professors |
| `/tracker` | Application progress tracking |
| `/credits` | Project credits and acknowledgments |

## Design System

- **Colors**: Rice Blue (#500000), Stone palette, Rice White
- **Typography**: Display font for headings, system fonts for body
- **Components**: Tailwind CSS with custom Rice-themed styling
- **Responsive**: Mobile-first design with desktop enhancements

## License

MIT License — for educational and research purposes.

## Credits

- **Created by**: [Shreyas Nirmala Bhaskar](https://www.linkedin.com/in/shreyas-nirmalabhaskar/)
- **Inspired by**: [Arun Vaithianathan](https://www.linkedin.com/in/akvaithi/) and [Aditya Meenakshisundaram](https://www.linkedin.com/in/adityameenakshi/)
- **Built for**: Rice University community
