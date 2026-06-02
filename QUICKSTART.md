# Quick Start Guide

Get the Theatres Dashboard running in minutes.

## Option 1: Docker (Recommended) ⚡

### Requirements
- Docker & Docker Compose installed
- `theaters.csv` in project root

### Steps

1. **Start the application:**
   ```bash
   docker-compose up
   ```

2. **Open in browser:**
   - http://localhost:8501

3. **Stop when done:**
   ```bash
   docker-compose down
   ```

Done! The app is fully configured for production use.

---

## Option 2: Local Python Setup

### Requirements
- Python 3.11+
- pip

### Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser:**
   - http://localhost:8501

---

## Verifying Setup

### Health Check
```bash
curl http://localhost:8501/_stcore/health
```

### Check Logs
```bash
# Docker
docker-compose logs -f app

# Local
tail -f logs/app.log
```

---

## Production Deployment

For production, you'll want:

1. **Environment configuration:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with production settings
   ```

2. **Production settings in `.env`:**
   ```
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   STREAMLIT_CLIENT_SHOWERRORDETAILS=false
   ```

3. **Deploy with Docker:**
   ```bash
   docker-compose up -d
   ```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## Common Commands

| Task | Command |
|------|---------|
| View logs | `docker-compose logs -f` |
| Restart app | `docker-compose restart` |
| Update data | Replace `theaters.csv`, restart |
| Stop app | `docker-compose down` |
| Rebuild image | `docker-compose build --no-cache` |

---

## Troubleshooting

**Port already in use?**
```bash
docker-compose down
# Or use a different port
PORT=8502 docker-compose up
```

**Data file not found?**
- Ensure `theaters.csv` exists in project root
- Check file permissions

**Memory issues?**
- Edit `docker-compose.yml` and add memory limits
- Or run locally with: `streamlit run app.py`

---

For more details, see [DEPLOYMENT.md](DEPLOYMENT.md)
