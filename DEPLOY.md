# 🚀 Deployment Guide — AI Email Composer

A complete guide to deploy the AI Email Composer (Flask backend + static frontend).

---

## 📁 Project Structure

```
├── server.py          # Flask backend (API proxy + review storage)
├── index.html         # Frontend (single-file app)
├── reviews.html       # Review viewer (standalone)
├── .env               # API key (NEVER commit this)
├── requirements.txt   # Python dependencies
└── reviews.json       # Auto-created review data
```

---

## 🖥️ Local Development

### Prerequisites
- **Python 3.9+** — [python.org](https://www.python.org/downloads/)
- **pip** — included with Python

### Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key in .env
# OPENROUTER_API_KEY=sk-or-v1-your-key-here

# 3. Run the server
python server.py
```

Open **http://localhost:5000** in your browser.  
Reviews viewer: **http://localhost:5000/reviews**

---

## ☁️ Hosting on the Internet

### Option A: Render (Recommended, Free Tier)

**Backend (Render Web Service):**

1. Push your project to a **GitHub / GitLab repository**
   - ⚠️ Add `.env` to `.gitignore` — do NOT push your API key
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo
4. Configure:
   | Setting         | Value                             |
   |----------------|-----------------------------------|
   | **Runtime**     | Python 3                          |
   | **Build Cmd**   | `pip install -r requirements.txt` |
   | **Start Cmd**   | `python server.py`                |
   | **Plan**        | Free                              |
5. Add environment variable:
   - Key: `OPENROUTER_API_KEY`
   - Value: your API key
6. Deploy — Render gives you a URL like `https://your-app.onrender.com`

> **That's it!** Since `server.py` serves both the API and the static HTML files, everything runs from one service.

---

### Option B: Railway

1. Push to GitHub (with `.env` in `.gitignore`)
2. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub**
3. Railway auto-detects Python projects
4. Add `OPENROUTER_API_KEY` in the **Variables** tab
5. Set Start command: `python server.py`
6. Deploy → get your public URL

---

### Option C: VPS (DigitalOcean / AWS EC2 / Any Linux Server)

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Clone your repo
git clone https://github.com/you/email-composer.git
cd email-composer

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Create .env with your API key
echo "OPENROUTER_API_KEY=sk-or-v1-your-key" > .env

# 5. Run with gunicorn (production WSGI server)
pip install gunicorn
gunicorn server:app --bind 0.0.0.0:5000

# 6. (Optional) Use a reverse proxy like Nginx
# and a process manager like systemd or pm2
```

---

## 🔒 Security Checklist

- [ ] **Never commit `.env`** — add it to `.gitignore`
- [ ] **API key is server-side only** — the frontend never sees it
- [ ] **CORS is configured** — edit `server.py` origins for production
- [ ] **Use HTTPS** — all hosting providers above provide free HTTPS
- [ ] **Set `debug=False`** in production (edit `server.py`)

### Recommended `.gitignore`

```
.env
reviews.json
__pycache__/
*.pyc
```

---

## 🔗 Quick Reference

| URL                  | Description                       |
|----------------------|-----------------------------------|
| `/`                  | Email Composer (main app)         |
| `/reviews`           | Review viewer                     |
| `/api/health`        | Backend health check              |
| `/api/generate`      | AI email generation (POST)        |
| `/api/enhance`       | AI email enhancement (POST)       |
| `/api/reviews`       | Get / submit reviews (GET / POST) |

---

## 🛠️ Troubleshooting

| Problem                    | Solution                                              |
|---------------------------|-------------------------------------------------------|
| `API key not configured`   | Check `.env` file exists and has the correct key      |
| `CORS error in browser`    | Ensure `flask-cors` is installed and CORS is enabled  |
| `502 / AI service error`   | OpenRouter may be down — check status.openrouter.ai   |
| `Reviews not loading`      | Ensure backend is running at the same origin          |

---

**Made with ❤️ by Kalyan BURMAN**
