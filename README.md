# RiceResearchFinder

> AI-powered research discovery and outreach platform for Rice University students.

Upload your resume, enter your research interests, and get matched with Rice faculty whose work aligns with where you want to go — not just where you've been. Then generate a personalized outreach email draft in one click.

## 🌟 Features

- **Smart Faculty Matching**: AI-powered matching based on research interests and resume analysis
- **Personalized Email Generation**: Generate professional outreach emails with one click
- **Comprehensive Faculty Database**: Search across 293+ Rice Engineering faculty
- **Resume Analysis**: Extract skills, experience, and research themes automatically
- **Research Interest Discovery**: Find faculty by keywords, departments, and research areas
- **Save & Track**: Bookmark professors and track application progress

## 🏗️ Tech Stack

| Part | Stack | Location |
|------|-------|----------|
| Crawler | Python + Playwright + BeautifulSoup | `/crawler` |
| Backend | FastAPI + SQLAlchemy + AI Services | `/backend` |
| Frontend | Vite + React 18 + Tailwind CSS | `/ui` |

## 🚀 Quick Start

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

## ⚙️ Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|---|---|---|
| `TOGETHER_API_KEY` | _(empty)_ | Together AI API key for LLM features |
| `GEMINI_API_KEY` | _(empty)_ | Google Gemini API key (alternative) |
| `DATABASE_URL` | `sqlite:///./rice_research.db` | SQLite (dev) or Postgres (`postgresql://user:pass@host/db`) |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed frontend origins |
| `UPLOAD_DIR` | `./uploads` | Directory for uploaded resume files |
| `EMAIL_HOST` | _(empty)_ | SMTP server for email features |
| `EMAIL_PORT` | `587` | SMTP port |
| `EMAIL_USER` | _(empty)_ | SMTP username |
| `EMAIL_PASSWORD` | _(empty)_ | SMTP password |

### Frontend (`ui/.env.local` — only needed in production)

| Variable | Default | Description |
|---|---|---|
| `VITE_API_BASE_URL` | _(empty)_ | Backend base URL (e.g. `https://api.yourapp.com`). In dev, Vite proxies `/api` → `localhost:8000` automatically. |

## 📡 API Reference

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

## 🎯 Matching Algorithm

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

## 📊 Data Models

**Faculty**
```json
{ "id", "name", "title", "department", "email", "profile_url", "lab_website", "research_summary", "scholar_interests", "publications" }
```

**Parsed resume profile**
```json
{
  "name", "year", "major", "gpa",
  "coursework": [],
  "technical_skills": [],
  "software_tools": [],
  "lab_techniques": [],
  "research_experiences": [{"title", "lab", "description"}],
  "project_experiences": [{"title", "description"}],
  "inferred_themes": []
}
```

**Match result**
```json
{ "professor", "score", "fit_label", "rank" }
```

**Email draft**
```json
{ "subject", "body", "tone", "faculty_id", "session_id", "mock_mode" }
```

## 📁 Project Structure

```
RiceResearchFinder/
├── README.md
├── .gitignore
├── Dockerfile
├── crawler/
│   ├── crawl.py
│   ├── requirements.txt
│   └── seeds.txt
├── backend/
│   ├── main.py               ← FastAPI app entry + startup
│   ├── requirements.txt
│   ├── .env.example
│   ├── data/
│   │   └── faculty.json      ← Faculty dataset
│   ├── db/
│   │   ├── database.py       ← SQLAlchemy engine + session
│   │   └── models.py         ← FacultyRecord, ResumeSession
│   ├── routers/
│   │   ├── faculty.py        ← GET/POST /api/faculty
│   │   ├── resume.py         ← POST /api/resume/upload
│   │   ├── match.py          ← POST /api/match
│   │   └── email.py          ← POST /api/email/draft
│   └── services/
│       ├── llm.py            ← AI clients + mock mode
│       ├── parser.py         ← Resume text extraction + parsing
│       ├── matcher.py        ← Hybrid keyword matching
│       └── emailer.py        ← Email draft generation
└── ui/
    ├── package.json
    ├── vite.config.js        ← proxies /api → localhost:8000 in dev
    ├── tailwind.config.js
    ├── public/
    │   └── faculty.json      ← static dataset for search
    └── src/
        ├── App.jsx
        ├── AppContext.jsx
        ├── utils/
        │   ├── search.js
        │   └── api.js        ← fetch wrapper for backend calls
        ├── pages/
        │   ├── Home.jsx
        │   ├── Results.jsx
        │   ├── ProfDetail.jsx ← includes Draft Email button
        │   ├── Saved.jsx
        │   ├── Credits.jsx   ← Project credits
        │   ├── Discover.jsx  ← resume upload + interests
        │   └── Match.jsx     ← match results dashboard
        └── components/
            ├── NavBar.jsx
            ├── Footer.jsx
            ├── ProfCard.jsx
            ├── Reveal.jsx
            └── EmailModal.jsx ← tone selector + editable draft
```

## 🚀 Deployment

### Production Setup

- **Frontend**: Vercel — Root Directory: `ui`. Set `VITE_API_BASE_URL` env var to your backend URL.
- **Backend**: Railway / Render / AWS — set environment variables and database URL.
- `faculty.json` must be in `ui/public/` for static search; it's also auto-imported into the DB on backend startup.

### Railway Deployment (Recommended)

1. Push code to GitHub
2. Go to [Railway](https://railway.app/new)
3. Click "Deploy from GitHub"
4. Select your repository
5. Set environment variables
6. Deploy!

### AWS App Runner Alternative

```bash
# Build and deploy
docker build -t rice-research-finder .
aws ecr create-repository --repository-name rice-research-finder
# Push to ECR and deploy to App Runner
```

## 🛣️ Routes

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

## 🎨 Design System

- **Colors**: Rice Blue (#500000), Stone palette, Rice White
- **Typography**: Display font for headings, system fonts for body
- **Components**: Tailwind CSS with custom Rice-themed styling
- **Responsive**: Mobile-first design with desktop enhancements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License — for educational and research purposes.

## 👥 Credits

- **Created by**: [Shreyas Nirmala Bhaskar](https://www.linkedin.com/in/shreyas-nirmalabhaskar/)
- **Inspired by**: [Arun Vaithianathan](https://www.linkedin.com/in/akvaithi/) and [Aditya Meenakshisundaram](https://www.linkedin.com/in/adityameenakshi/)
- **Built for**: Rice University community

---

**Built with ❤️ for curious Owls at Rice University**
