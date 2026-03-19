import json
import os
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    from data_store import load_faculty_data
    load_faculty_data()
    yield

app = FastAPI(
    title="RiceResearchFinder API",
    description="Backend for research discovery, resume parsing, matching, and email drafting.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,https://riceresearch.vercel.app").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

from routers import faculty, resume, match
from routers import email as email_router

app.include_router(faculty.router, prefix="/api/faculty", tags=["Faculty"])
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(match.router, prefix="/api/match", tags=["Match"])
app.include_router(email_router.router, prefix="/api/email", tags=["Email"])

# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

@app.get("/api/health", tags=["Health"])
def health():
    from services.llm import MOCK_MODE
    return {"status": "ok", "version": "1.0.0", "mock_mode": MOCK_MODE}
