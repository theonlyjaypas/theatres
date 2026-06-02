# Production Deployment Checklist

Use this checklist before deploying to production.

## Pre-Deployment

- [ ] All tests pass (if applicable)
- [ ] No uncommitted changes in git
- [ ] Dependencies updated and pinned in `requirements.txt`
- [ ] `.env.example` file exists and is documented
- [ ] Data file (`theaters.csv`) is present and valid
- [ ] No hardcoded secrets in code
- [ ] Security review completed

## Environment Configuration

- [ ] `.env` file created from `.env.example`
- [ ] `ENVIRONMENT=production` set
- [ ] `LOG_LEVEL=INFO` (or appropriate level)
- [ ] `STREAMLIT_CLIENT_SHOWERRORDETAILS=false`
- [ ] `STREAMLIT_SERVER_ENABLEXSRFPROTECTION=true`
- [ ] `STREAMLIT_SERVER_ENABLECORS=false`
- [ ] Data path correct and accessible
- [ ] Port configured correctly

## Docker Setup

- [ ] `Dockerfile` exists and builds without errors
- [ ] `docker-compose.yml` configured correctly
- [ ] Image builds successfully: `docker-compose build`
- [ ] No hardcoded passwords or secrets in Docker files
- [ ] Health checks configured and working
- [ ] Resource limits set (CPU, memory)
- [ ] Volume mounts are read-only where appropriate

## Application Validation

- [ ] Data loads without errors: `python -c "from config import Config; Config.validate()"`
- [ ] All required columns present in CSV
- [ ] Column names match code expectations
- [ ] Data integrity verified (no missing critical columns)
- [ ] Charts render correctly with sample data
- [ ] Search functionality works
- [ ] All pages accessible without errors

## Security

- [ ] Non-root user in Docker
- [ ] Secrets not in version control
- [ ] `.env` file added to `.gitignore`
- [ ] Security headers configured (if behind proxy)
- [ ] SSL/TLS enabled (if public-facing)
- [ ] XSRF protection enabled
- [ ] CORS disabled or properly configured
- [ ] Error details hidden in production
- [ ] Logging doesn't expose sensitive data

## Operations

- [ ] Logging configured and tested
- [ ] Log rotation configured (if needed)
- [ ] Health check endpoint accessible
- [ ] Monitoring/alerting set up
- [ ] Restart policy configured (`unless-stopped`)
- [ ] Data backup strategy in place
- [ ] Data update process documented
- [ ] Rollback procedure documented

## Testing

- [ ] Application starts successfully in Docker
- [ ] Health check passes: `curl http://localhost:8501/_stcore/health`
- [ ] Dashboard loads in browser
- [ ] Data displays correctly
- [ ] Search/filter functionality works
- [ ] Download CSV export works
- [ ] Responsive design works on mobile
- [ ] No console errors in browser

## Deployment

- [ ] Repository pushed to main branch
- [ ] Docker image built and ready
- [ ] Deployment environment verified
- [ ] Application started: `docker-compose up -d`
- [ ] Application accessible at configured URL
- [ ] All health checks passing
- [ ] Logs monitored for errors
- [ ] Team notified of deployment

## Post-Deployment

- [ ] Monitor logs for 1 hour
- [ ] Monitor system resources
- [ ] Performance baselines established
- [ ] User testing completed
- [ ] Runbook updated with new deployment
- [ ] Team on standby for issues
- [ ] Success criteria met

## Quick Verification Commands

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Health check
curl http://localhost:8501/_stcore/health

# View logs
docker-compose logs -f

# Test data loading
docker-compose exec app python -c "from config import Config; Config.validate()"

# Resource usage
docker stats

# Validate config
docker-compose config
```

## Rollback Procedure

If issues occur after deployment:

```bash
# 1. Stop current deployment
docker-compose down

# 2. Checkout previous version
git checkout <previous-commit>

# 3. Rebuild and restart
docker-compose up -d

# 4. Verify
curl http://localhost:8501/_stcore/health
```

## Emergency Contacts

- On-call engineer: [Name/Contact]
- Technical lead: [Name/Contact]
- DevOps: [Name/Contact]

## Notes

- Last deployed: [Date/Time]
- Deployed by: [Name]
- Version: [Git SHA/Tag]
- Issues encountered: [None/Description]
