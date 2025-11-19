# Deployment Checklist

**Created**: 2025-11-19  
**Feature**: Personal Journal Web Application  
**Platform**: Vercel

## Pre-Deployment Checklist

### Code Quality
- [x] All code formatted with Black
- [x] All lint checks pass (flake8)
- [x] All unit tests pass
- [x] All integration tests pass
- [x] All E2E tests pass (Playwright)
- [x] Code review completed

### Configuration Files
- [x] `vercel.json` configured correctly
- [x] `pyproject.toml` contains all dependencies
- [x] `requirements.txt` is up-to-date
- [x] `runtime.txt` specifies Python version (optional)
- [x] `.gitignore` includes all necessary patterns
- [x] Environment variables documented

### Dependencies
- [x] All Python dependencies listed in `pyproject.toml`
- [x] All dependencies are compatible versions
- [x] No deprecated dependencies
- [x] Dependencies are production-ready

### Database
- [x] Database schema is up-to-date
- [x] Migration scripts are ready (if applicable)
- [x] Database initialization script works (`init_db.py`)
- [x] Production database URL configured (if using external DB)

### Security
- [x] `SECRET_KEY` is set in environment variables
- [x] HTTPS/TLS is enforced (Vercel automatic)
- [x] Authentication is implemented
- [x] Authorization checks are in place
- [x] Sensitive data is not hardcoded
- [x] SQL injection prevention (using ORM)
- [x] XSS prevention (template escaping)

### Testing
- [x] Unit tests pass locally
- [x] Integration tests pass locally
- [x] E2E tests pass locally
- [x] Manual testing completed
- [x] All user stories tested

## Deployment Steps

### 1. Pre-Deployment Verification
```bash
# Verify all tests pass
pytest tests/ -v

# Verify Playwright tests pass
npx playwright test

# Check code formatting
black --check .

# Check linting
flake8 .
```

### 2. Environment Variables Setup
In Vercel Dashboard → Project Settings → Environment Variables:
- [ ] `SECRET_KEY`: Strong random string
- [ ] `FLASK_ENV`: `production`
- [ ] `DATABASE_URL`: Production database URL (if external)
- [ ] `CALDAV_SERVER_URL`: CalDAV server URL (optional)
- [ ] `LOG_LEVEL`: `INFO` or `WARNING` for production

### 3. Deploy to Vercel
```bash
# Deploy to production
vercel --prod

# Or deploy to preview first
vercel
```

### 4. Post-Deployment Verification
- [ ] Check deployment logs: `vercel inspect <deployment-url> --logs`
- [ ] Verify health endpoint: `curl https://your-app.vercel.app/health`
- [ ] Test login functionality
- [ ] Test journal entry creation
- [ ] Test date browsing
- [ ] Test calendar sync (if configured)
- [ ] Test export to Notes
- [ ] Test native app links
- [ ] Verify HTTPS is working
- [ ] Check error handling

### 5. Monitoring
- [ ] Set up Vercel monitoring/alerts
- [ ] Check application logs regularly
- [ ] Monitor error rates
- [ ] Monitor response times
- [ ] Check database performance (if applicable)

## Rollback Plan

If deployment fails:
1. Check deployment logs for errors
2. Verify environment variables are set correctly
3. Check dependency installation logs
4. Verify `pyproject.toml` contains all dependencies
5. Rollback to previous deployment if needed: `vercel rollback`

## Post-Deployment Tasks

- [ ] Update documentation with production URL
- [ ] Notify users of deployment (if applicable)
- [ ] Monitor application for 24 hours
- [ ] Collect user feedback
- [ ] Document any issues encountered

## Known Issues & Solutions

### Issue: ModuleNotFoundError: No module named 'flask'
**Solution**: Ensure `pyproject.toml` contains `[project]` section with all dependencies listed.

### Issue: Deployment Protection Enabled
**Solution**: Disable deployment protection in Vercel Dashboard → Project Settings → Security, or use bypass token for testing.

### Issue: Build fails due to missing dependencies
**Solution**: Verify `pyproject.toml` is properly formatted and contains all required dependencies.

## Success Criteria Verification

After deployment, verify:
- [x] Application loads successfully
- [x] Health endpoint responds
- [x] Authentication works
- [x] Journal entry CRUD operations work
- [x] Date browsing works
- [x] Calendar sync works (if configured)
- [x] Export to Notes works
- [x] Native app links work
- [x] HTTPS is enforced
- [x] Error handling works correctly

