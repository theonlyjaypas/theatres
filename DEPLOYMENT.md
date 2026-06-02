# Deployment Guide

This guide covers deploying the Theatres Dashboard in production environments.

## Quick Start with Docker

### Prerequisites
- Docker and Docker Compose installed
- `theaters.csv` in the project root

### Local Deployment

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Open browser to `http://localhost:8501`

### Production Deployment

1. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   nano .env
   ```

2. **Key production settings:**
   ```bash
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   PORT=8501
   STREAMLIT_SERVER_ENABLECORS=false
   STREAMLIT_SERVER_ENABLEXSRFPROTECTION=true
   STREAMLIT_CLIENT_SHOWERRORDETAILS=false
   ```

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Verify deployment:**
   ```bash
   curl http://localhost:8501/_stcore/health
   ```

## Traditional Deployment (without Docker)

### Prerequisites
- Python 3.11+
- Virtual environment

### Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

4. **Run startup script:**
   ```bash
   bash startup.sh
   ```

   Or directly:
   ```bash
   streamlit run app.py
   ```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Set to `production` for production |
| `PORT` | `8501` | Server port |
| `DATA_PATH` | `./theaters.csv` | Path to CSV data file |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `STREAMLIT_SERVER_ENABLECORS` | `false` | Enable CORS (false in production) |
| `STREAMLIT_SERVER_ENABLEXSRFPROTECTION` | `true` | Enable XSRF protection |
| `STREAMLIT_CLIENT_SHOWERRORDETAILS` | `false` | Show detailed errors (false in production) |

## Health Checks

The application exposes a health check endpoint:

```bash
curl http://localhost:8501/_stcore/health
```

Docker Compose automatically monitors health and restarts on failure.

## Logging

- Logs are written to `logs/app.log`
- Log level controlled by `LOG_LEVEL` environment variable
- Both file and console output enabled

## Data Updates

1. **Replace `theaters.csv`:**
   ```bash
   cp new_theaters.csv theaters.csv
   ```

2. **Reload application:**
   - Docker: `docker-compose restart`
   - Local: Restart the app (Streamlit will auto-reload)

## Production Best Practices

1. **Use Docker for consistency** across environments
2. **Enable XSRF protection** in production
3. **Disable error details** in production (`STREAMLIT_CLIENT_SHOWERRORDETAILS=false`)
4. **Monitor logs** for errors and performance issues
5. **Keep data file in sync** with external sources
6. **Use a reverse proxy** (nginx) in front of Streamlit for:
   - SSL/TLS termination
   - Load balancing
   - Static file serving
7. **Set resource limits** in Docker:
   ```yaml
   services:
     app:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 512M
   ```

## Reverse Proxy Setup (Nginx)

Example nginx configuration:

```nginx
upstream streamlit {
    server app:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_request_buffering off;
    }
}
```

## Troubleshooting

### Application won't start

1. **Check logs:**
   ```bash
   docker-compose logs -f app
   ```

2. **Verify data file:**
   ```bash
   ls -la theaters.csv
   ```

3. **Check configuration:**
   ```bash
   python -c "from config import Config; Config.validate()"
   ```

### Health check failing

1. **Check port accessibility:**
   ```bash
   curl -v http://localhost:8501/_stcore/health
   ```

2. **Check Docker logs:**
   ```bash
   docker-compose logs app
   ```

### Memory issues

1. **Increase memory limit in docker-compose.yml**
2. **Clear Streamlit cache:** Remove `.streamlit/` directory
3. **Monitor resource usage:** `docker stats`

### Data loading errors

1. **Verify CSV format:** Check column names match expected schema
2. **Check file permissions:** Ensure file is readable
3. **Check logs for details:** `docker-compose logs app | grep ERROR`

## Updating Application

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Rebuild Docker image:**
   ```bash
   docker-compose build --no-cache
   ```

3. **Restart application:**
   ```bash
   docker-compose up -d
   ```

## Security Considerations

- ✅ Non-root user in Docker
- ✅ Read-only data volume mount
- ✅ XSRF protection enabled
- ✅ CORS disabled in production
- ✅ Error details hidden in production
- ✅ Health check endpoint for monitoring
- ⚠️ Consider running behind reverse proxy with SSL/TLS
- ⚠️ Monitor logs for suspicious activity
- ⚠️ Keep dependencies updated

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Review this guide
3. Check TROUBLESHOOTING section above
