# RiceResearchFinder Deployment Guide

## 🚀 Production Deployment

### ✅ Current Status
- **Backend**: https://rice-research-production.up.railway.app
- **Frontend**: https://riceresearch.vercel.app
- **Dataset**: Clean faculty summaries (293 records)
- **Status**: Production Ready

### 📋 Environment Variables

#### Backend (Railway)
```bash
# AI Services (choose one)
TOGETHER_API_KEY=your_together_api_key
GEMINI_API_KEY=your_gemini_api_key

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# CORS
CORS_ORIGINS=https://riceresearch.vercel.app,http://localhost:5173
```

#### Frontend (Vercel)
```bash
VITE_API_BASE_URL=https://rice-research-production.up.railway.app
```

### 🗂️ Data Files
- **Backend**: `backend/data/faculty.json` (clean AI summaries)
- **Frontend**: `ui/public/faculty.json` (synced with backend)
- **Total Faculty**: 293 Rice University faculty members

### 🔧 Deployment Commands

#### Backend (Railway)
```bash
# Railway auto-deploys from GitHub
git push origin main
```

#### Frontend (Vercel)
```bash
cd ui
vercel --prod
```

### 📊 Features
- ✅ Faculty search with clean summaries
- ✅ Resume upload and AI matching
- ✅ Email generation (Gemini/Together AI)
- ✅ CORS configured for production
- ✅ Mobile responsive design
- ✅ Application tracking

### 🧪 Testing
```bash
# Backend health
curl https://rice-research-production.up.railway.app/api/health

# Faculty endpoint
curl https://rice-research-production.up.railway.app/api/faculty?limit=5

# Email generation
curl -X POST https://rice-research-production.up.railway.app/api/email/draft \
  -H "Content-Type: application/json" \
  -d '{"faculty_id": "3a1b8481990a", "tone": "professional", "interests": "bioengineering"}'
```

### 🔄 Data Updates
To update faculty data:
1. Update `backend/data/faculty.json`
2. Copy to `ui/public/faculty.json`
3. Commit and push to trigger redeploy

### 📱 Application URLs
- **Main App**: https://riceresearch.vercel.app
- **API Docs**: https://rice-research-production.up.railway.app/docs
- **Backend Health**: https://rice-research-production.up.railway.app/api/health

### 🛠️ Tech Stack
- **Frontend**: React 18 + Vite + Tailwind CSS
- **Backend**: FastAPI + SQLAlchemy
- **Deployment**: Vercel (frontend) + Railway (backend)
- **AI**: Gemini API / Together AI
- **Database**: SQLite (production ready)

### 📞 Support
- **Creator**: Shreyas Nirmala Bhaskar
- **Repository**: https://github.com/Shreyas4240/rice-research
- **Issues**: Create GitHub issue for bugs/features
