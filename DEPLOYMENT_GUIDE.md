# Railway + Cloudflare Custom Domain Setup Guide

A step-by-step guide to deploying a Flask app on Railway with a Cloudflare-managed custom subdomain.

## Prerequisites

- Flask app with `Dockerfile` and `Procfile` configured for Railway
- Railway account and project deployed
- Cloudflare account managing your domain DNS
- Railway CLI installed: `npm install -g @railway/cli`

## Deployment Steps

### 1. Prepare Your App for Railway

Ensure your app has these files:

**Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE $PORT
CMD gunicorn app:app --workers 4 --timeout 60 --bind 0.0.0.0:$PORT
```

**Procfile**
```
web: gunicorn app:app --workers 4 --timeout 60 --bind 0.0.0.0:$PORT
```

**requirements.txt**
```
Flask==2.3.3
gunicorn==21.2.0
flask-limiter==3.5.0
```

### 2. Deploy to Railway

```bash
# Link your local project to Railway
railway link

# Deploy
railway up

# Check status
railway status
```

### 3. Configure DNS in Cloudflare

1. Log into Cloudflare dashboard
2. Select your domain
3. Go to **DNS** → **Records**
4. Add a CNAME record:
   - **Type**: CNAME
   - **Name**: `mb` (or your subdomain)
   - **Target**: `your-app.up.railway.app` (from Railway dashboard)
   - **Proxy status**: Proxied (orange cloud)
   - **TTL**: Auto

### 4. Add Custom Domain in Railway

**Via Dashboard:**
1. Go to https://railway.app
2. Open your project → service
3. Go to **Settings** → **Networking**
4. Under **Custom Domain**, click **Add Domain**
5. Enter: `mb.yourdomain.com`
6. Wait for Railway to verify (usually instant)

**Via CLI:**
```bash
railway domain
# Follow prompts to add custom domain
```

### 5. Fix Cloudflare SSL/TLS Settings

**Critical Step** - prevents redirect loops:

1. In Cloudflare dashboard, select your domain
2. Go to **SSL/TLS** → **Overview**
3. Change encryption mode to **Full (strict)**
   - ❌ NOT "Flexible" (causes redirect loops)
   - ✅ Use "Full (strict)" for Railway

### 6. Verify Deployment

```bash
# Check DNS resolution
dig mb.yourdomain.com

# Test the endpoint
curl -I https://mb.yourdomain.com

# Should return HTTP/2 200 with x-railway-edge header
```

### 7. Clear Browser Cache

If the site doesn't load in your browser:
- Hard refresh: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
- Try incognito/private window
- Clear browser cache for the subdomain

## Common Issues & Solutions

### Issue: ERR_TOO_MANY_REDIRECTS

**Cause**: Cloudflare SSL/TLS mode set to "Flexible"

**Solution**: Change to "Full (strict)" in Cloudflare SSL/TLS settings

### Issue: Domain redirects to root domain

**Cause**: Custom domain not added in Railway

**Solution**: Add the subdomain in Railway's custom domain settings

### Issue: DNS not resolving

**Cause**: CNAME pointing to wrong Railway URL

**Solution**: 
1. Get correct Railway URL from dashboard
2. Update Cloudflare CNAME record
3. Wait 1-2 minutes for DNS propagation

### Issue: 502 Bad Gateway

**Cause**: App not binding to Railway's `$PORT` variable

**Solution**: Ensure your app uses `$PORT`:
```python
# In app.py for development
if __name__ == '__main__':
    app.run(debug=True, port=8000)

# Railway uses gunicorn with $PORT automatically
```

## Quick Diagnostic Commands

```bash
# Check Railway deployment status
railway status

# View Railway logs
railway logs

# Test DNS
nslookup mb.yourdomain.com

# Test with full redirect chain
curl -sL -D - https://mb.yourdomain.com -o /dev/null

# Check SSL certificate
openssl s_client -connect mb.yourdomain.com:443 -servername mb.yourdomain.com
```

## Environment Variables

Railway automatically provides:
- `PORT` - Port your app should bind to
- `RAILWAY_ENVIRONMENT` - Current environment (production/staging)

Set custom variables in Railway dashboard:
- `SECRET_KEY` - Flask secret key
- `FLASK_ENV` - Set to "production"

## Summary

The key steps are:
1. Deploy app to Railway with proper Dockerfile/Procfile
2. Add CNAME in Cloudflare pointing to Railway app
3. Add custom domain in Railway dashboard
4. Set Cloudflare SSL/TLS to "Full (strict)"
5. Clear browser cache

**Most Critical**: Cloudflare SSL mode must be "Full (strict)" when using Railway.
