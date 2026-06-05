Automated AI Lead Responder (Production SaaS Ready)

A professional, AI-powered lead responder for service businesses. Capture leads via webhook, automatically generate professional responses using OpenAI, and track metrics—all with zero manual effort.

## Key Features

✨ **AI-Powered Responses**: Generates professional, polite customer replies using OpenAI GPT-4  
📊 **Real-Time Dashboard**: View total leads, AI responses sent, and estimated revenue saved  
🔐 **Secure Login**: Dashboard-protected with password authentication  
📞 **Optional SMS**: Send confirmation messages via Twilio (optional)  
🚀 **Production Ready**: Deployed on Render with Neon PostgreSQL  
💰 **SaaS Model**: 14-day free trial, then subscription-based pricing  

## Quick Start (Local Development)

### 1. Clone and set up environment

```powershell
git clone https://github.com/GraceAbike/lead-responder.git
cd lead_responder
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure environment

```powershell
copy .env.example .env
```

Edit `.env` with your values:
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: PostgreSQL connection string (optional; uses local SQLite by default)
- `DASHBOARD_PASSWORD`: Your login password
- `SECRET_KEY`: A random, secure string

### 3. Run locally

```powershell
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000` → login with your `DASHBOARD_PASSWORD`

## Live Deployment

### Check Your Live Website

Your app is live at:  
**https://ai-lead-responder.onrender.com**

1. Open Chrome (or any browser)
2. Go to the URL above
3. Log in with your `DASHBOARD_PASSWORD`
4. View metrics and submit test leads

### Full Deployment Instructions

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Setting up Neon PostgreSQL
- Configuring Render
- Environment variables
- Webhook integration
- Troubleshooting

## API Endpoints

### Submit a Lead (Webhook)

```bash
POST /api/leads
Content-Type: application/json

{
  "customer_name": "John Doe",
  "customer_phone": "+1-555-0100"
}
```

Response:
```json
{"status": "ok", "id": 1}
```

### Get All Leads

```bash
GET /api/leads
```

Returns array of leads with status, timestamp, and customer info.

## Dashboard Features

- **Total Leads**: Count of all submitted leads
- **AI Replied**: Count of leads automatically responded to
- **Saved Revenue**: Estimated value from fast AI responses (calculated as replies × $350)
- **Recent Leads Table**: All leads with status badges and timestamps
- **Submit Lead Form**: Quick test interface to create new leads
- **Logout Button**: Secure session management

## Security

✅ Secrets in `.gitignore` (never committed)  
✅ Environment variables only in Render dashboard  
✅ Password-protected dashboard  
✅ HTTPS on production  
✅ Open-source; audit the code freely  

## Pricing Model (14-Day Free Trial)

1. **First 14 days**: Full access, all features, no payment
2. **Day 15 onwards**: $29/month per account or $500 one-time

## SaaS Features Included

- Lead capture via webhook
- AI response generation (OpenAI)
- SMS confirmations (optional, Twilio)
- Real-time metrics
- Secure dashboard
- Trial tracking (14 days)

## Next Steps

1. **Test locally**: `uvicorn app.main:app --reload`
2. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Set up payment**: Add Stripe integration for post-trial billing
4. **Custom domain**: Update Render to point to your domain

## Support & Docs

- **Render Docs**: https://render.com/docs
- **Neon PostgreSQL**: https://neon.tech/docs
- **OpenAI API**: https://platform.openai.com/docs
- **Twilio SMS**: https://www.twilio.com/docs

## License

MIT License - free to modify and use commercially

---

**Status**: 🟢 Production Ready  
**Last Updated**: June 5, 2026
