# Deployment Guide - Restaurant Booking Chatbot

Complete guide to deploying the Sprync Restaurant Booking Chatbot to production on Render.com.

---

## Prerequisites

- GitHub account (free)
- Render.com account (free tier available)
- Git installed on your local machine
- Docker (optional, for local testing)

---

## Step 1: Prepare for Deployment

### 1.1 Create a GitHub Repository

```bash
cd sprync-restaurant-bot
git init
git add .
git commit -m "Initial commit: Production-ready restaurant booking chatbot"
```

### 1.2 Push to GitHub

```bash
# Create new repository on github.com
# Then:
git remote add origin https://github.com/YOUR_USERNAME/sprync-restaurant-bot.git
git branch -M main
git push -u origin main
```

### 1.3 Test Locally (Optional)

```bash
# Using Docker Compose
docker-compose up --build

# Or using Python directly
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then visit: http://localhost:8000

---

## Step 2: Deploy on Render.com

### 2.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Sign up"
3. Choose "GitHub" to sign up with your GitHub account
4. Authorize Render to access your GitHub repositories

### 2.2 Create Web Service

1. After signing in, click "New +" button
2. Select "Web Service"
3. Search for your repository name "sprync-restaurant-bot"
4. Click "Connect"

### 2.3 Configure Service

Fill in the configuration:

| Field | Value |
|-------|-------|
| **Name** | `sprync-restaurant-bot` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| **Instance Type** | `Free` (or paid for production) |

### 2.4 Set Environment Variables

Click "Advanced" and add environment variables:

```
DEBUG=False
PYTHONUNBUFFERED=1
PORT=8000
```

### 2.5 Deploy

Click "Create Web Service" button. Render will:
1. Clone your repository
2. Install dependencies
3. Build and start the service
4. Provide a public URL

Your chatbot will be live at: `https://sprync-restaurant-bot.onrender.com`

---

## Step 3: Post-Deployment Verification

### 3.1 Test the Chatbot

1. Visit your Render URL
2. Say "Hi" in the chat
3. Click "Book a Table"
4. Complete a test booking

### 3.2 Check API Health

```bash
curl https://your-service.onrender.com/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Sprync Restaurant Bot",
  "version": "1.0.0"
}
```

### 3.3 View Logs

In Render dashboard:
1. Click your service
2. Go to "Logs" tab
3. Monitor for errors

---

## Step 4: Customization for Clients

### 4.1 Change Restaurant Details

Edit `backend/app/config.py`:
```python
RESTAURANT_NAME: str = "Your Restaurant Name"
RESTAURANT_HOURS: str = "12:00 PM - 10:00 PM"
RESTAURANT_PHONE: str = "+44 20 YOUR PHONE"
```

### 4.2 Update Menu

Edit `backend/app/services/menu.py` - modify the `_load_menu()` method to add your restaurant's items.

### 4.3 Custom Domain

In Render dashboard:
1. Go to Settings
2. Under "Custom Domain"
3. Add your domain (requires DNS setup)

### 4.4 Environment-Specific Config

Create `.env` file (not committed to git):
```
RESTAURANT_NAME=Your Restaurant Name
RESTAURANT_PHONE=+44 20 1234 5678
RESTAURANT_HOURS=11:00 AM - 11:00 PM
```

Then in Render, add these as environment variables.

---

## Step 5: Production Hardening

### 5.1 Enable HTTPS

Render automatically provides HTTPS certificates. No action needed.

### 5.2 Add Authentication (Optional)

For admin endpoints, add JWT:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/bookings")
async def get_bookings(credentials = Depends(security)):
    # Verify token
    return bookings
```

### 5.3 Add Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat")
@limiter.limit("100/minute")
async def chat(request: ChatRequest):
    # endpoint
```

### 5.4 Add Database (Optional)

For persistent storage:

```bash
pip install sqlalchemy psycopg2-binary
```

Set Render Postgres service and update connection string in `.env`.

### 5.5 Add Email Notifications (Optional)

```bash
pip install python-dotenv smtplib
```

Add SMTP credentials to `.env` and send booking confirmations.

---

## Step 6: Monitoring & Maintenance

### 6.1 Monitor Performance

Use Render's built-in monitoring:
- Response times
- CPU usage
- Memory usage
- Error rates

### 6.2 Enable Auto-Restart

In Render settings:
- Enable "Auto-restart on failure"
- Set health check path to `/api/health`

### 6.3 Regular Updates

```bash
# Test locally
git pull origin main
docker-compose up --build

# Push to GitHub (Render redeploys automatically)
git push origin main
```

### 6.4 Backup Data

Export bookings periodically:

```bash
curl https://your-service.onrender.com/api/bookings > bookings_backup.json
```

---

## Troubleshooting

### Issue: Service Won't Start

**Check logs:**
```
Render Dashboard → Logs tab
```

**Common causes:**
- Missing dependencies: Ensure `requirements.txt` is in backend/
- Port binding: Verify PORT environment variable set
- Syntax errors: Run `python -m py_compile app.py`

### Issue: Frontend Not Loading

**Check:**
1. HTML file exists at `frontend/index.html`
2. React CDN accessible (check browser console)
3. API base URL in app.jsx (default: same origin)

### Issue: Chat Not Responding

**Debug:**
```bash
curl -X POST https://your-service.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","user_message":"hi","conversation_history":[]}'
```

Check response status and error message.

### Issue: Bookings Not Saving

Current implementation uses in-memory storage. Bookings are lost on restart.

**Solution:** Add database:
```bash
pip install sqlalchemy psycopg2
# Update booking.py to use SQLAlchemy models
```

---

## Scaling for Production

### Single Instance (Free - Current)
- Works for: Testing, demos, low traffic
- Limitations: Restarts nightly, in-memory storage

### Production Tier
- Upgrade to "Pro" plan ($7/month)
- Add Postgres database
- Enable auto-scaling
- Custom domain with SSL
- 99.9% uptime SLA

### Multi-Region (Enterprise)
- Deploy to multiple regions
- Use CDN for frontend
- Database replication
- Load balancing

---

## Cost Breakdown

| Component | Free Plan | Pro Plan |
|-----------|-----------|----------|
| Web Service | Free* | $7/month |
| PostgreSQL | $15/month | $15/month |
| SSL Certificate | Included | Included |
| Custom Domain | N/A | Included |
| **Total** | $15/month | $22/month |

*Free tier: Spins down after 15 minutes of inactivity

---

## Integration Options

### Embedding in Website

Add iframe to your website:
```html
<iframe
  src="https://your-service.onrender.com"
  width="400"
  height="600"
  style="border: none; border-radius: 8px;">
</iframe>
```

### WhatsApp Integration

Use Twilio API:
```python
from twilio.rest import Client

client = Client(account_sid, auth_token)
message = client.messages.create(
    to="+44...",
    from_="+1...",
    body="Your booking is confirmed!"
)
```

### SMS Notifications

```python
from twilio.rest import Client

# Send SMS after booking
client.messages.create(
    to=customer_phone,
    from_=restaurant_phone,
    body=f"Booking confirmed for {date} at {time}"
)
```

### Calendar Integration

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Sync booking to Google Calendar
calendar_service = build('calendar', 'v3', credentials=credentials)
event = {
    'summary': f'Booking - {name}',
    'start': {'dateTime': f'{date}T{time}:00'},
    'end': {'dateTime': f'{date}T{time}:30'},
}
calendar_service.events().insert(calendarId='primary', body=event).execute()
```

---

## Security Checklist

- ✅ HTTPS enabled (automatic on Render)
- ✅ Input validation (Pydantic models)
- ✅ CORS configured
- ✅ No secrets in code (use .env)
- ✅ Health check endpoint
- ✅ Error handling
- [ ] Add authentication for admin endpoints
- [ ] Add rate limiting
- [ ] Add database encryption
- [ ] Regular security audits

---

## Rollback Procedure

If something breaks in production:

1. **Quick Fix:**
   ```bash
   # Fix the code
   git add .
   git commit -m "Fix: issue description"
   git push origin main
   # Render redeploys automatically
   ```

2. **Revert to Previous:**
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Manual Rollback:**
   - In Render Dashboard
   - Go to "Deploys" tab
   - Click "Redeploy" on a previous deployment

---

## Support & Updates

Subscribe to updates:
- GitHub Watch → Releases
- Render Status → Status page
- Email notifications for deployment logs

---

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test in production
3. ✅ Share feedback from users
4. ✅ Add database for persistence
5. ✅ Integrate with email/SMS
6. ✅ Add payment processing
7. ✅ Scale to production tier

---

**Deployed successfully!**

Your Restaurant Booking Chatbot is now live and ready to take bookings.

For questions or issues, check the README.md or contact support.
