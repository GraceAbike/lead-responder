# Deployment Guide: AI Lead Responder SaaS

## Overview
This guide walks you through deploying the AI Lead Responder to Render.com with a Neon PostgreSQL database. The application is ready for production use with a 14-day free trial model.

## Prerequisites
- GitHub account with the repository public (✅ done)
- Render.com account (free tier available)
- Neon PostgreSQL database (free tier available)
- OpenAI API key
- Twilio account (optional, for SMS)

## Step 1: Set Up Neon PostgreSQL Database

1. Go to https://neon.tech and sign up
2. Create a new project
3. Copy your connection string (looks like: `postgresql://user:password@host/dbname?sslmode=require`)
4. **Important**: Keep this secret—don't share or commit it

## Step 2: Deploy on Render.com

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `https://github.com/GraceAbike/lead-responder`
4. Select branch: `main`
5. Render will auto-detect `render.yaml` and configure settings
6. Click "Create Web Service"

## Step 3: Set Environment Variables in Render

In Render's "Environment" settings for your service, add:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | Your Neon PostgreSQL URL | Keep secret; set in Render dashboard only |
| `OPENAI_API_KEY` | Your OpenAI API key | Required for AI responses |
| `TWILIO_ACCOUNT_SID` | Your Twilio SID | Optional; leave blank to disable SMS |
| `TWILIO_AUTH_TOKEN` | Your Twilio auth token | Optional; leave blank to disable SMS |
| `TWILIO_PHONE_NUMBER` | Your Twilio phone | Optional; leave blank to disable SMS |
| `DASHBOARD_PASSWORD` | A secure password | Users log in with this password |
| `SECRET_KEY` | A random string (30+ chars) | Use a strong, random value |
| `TRIAL_DAYS` | `14` | Free trial period in days |

**Never set these in your Git repository.** Render keeps them secure.

## Step 4: Deploy

1. Click "Manual Deploy" → "Deploy latest commit" in Render
2. Wait for the build to complete (2–3 minutes)
3. Once deployed, you'll see a green "Live" status

## Step 5: Access Your Live Website

Your app will be live at:
```
https://ai-lead-responder.onrender.com
```

**To view it:**
1. Open Chrome (or any browser)
2. Go to: `https://ai-lead-responder.onrender.com`
3. Log in with `DASHBOARD_PASSWORD`
4. You'll see:
   - **Total Leads**: Count of all leads submitted
   - **AI Replied**: Count of leads responded to by AI
   - **Saved Revenue**: Estimated revenue saved (calculated as replied leads × $350)
   - **Recent Leads**: Table of all submissions with status

## Step 6: Test the Website

### As a User (Submit a Lead)
1. Go to `https://ai-lead-responder.onrender.com`
2. You'll be redirected to login
3. Enter your `DASHBOARD_PASSWORD`
4. Submit a test lead (e.g., "I need an emergency plumber")
5. Check the Recent Leads table

### As an Admin (Dashboard)
Same as above—the dashboard shows all leads and metrics.

## Webhook Integration (For Production)

Once deployed, external systems can send leads via:

```bash
curl -X POST "https://ai-lead-responder.onrender.com/api/leads" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_phone": "+1-555-0100"
  }'
```

## Free Trial Model (14 Days)

The app tracks trial status for each lead:
- **New leads**: Automatically counted
- **AI Replied**: Marked as "Replied" after AI processes them
- **Trial expires**: After 14 days, require payment

To modify trial length, change `TRIAL_DAYS` in Render environment settings.

## Troubleshooting

### "Application startup failed"
- Check Render logs: Service → Logs
- Verify `DATABASE_URL` is set in Render environment
- Ensure all secrets are non-empty (except optional Twilio)

### "502 Bad Gateway"
- App crashed—check logs
- Verify database connection is valid
- Restart the service in Render

### "Login fails"
- Verify `DASHBOARD_PASSWORD` is correct
- Check `SECRET_KEY` is set

## Security Checklist

✅ `.env` file is in `.gitignore` (never committed)  
✅ Secrets are in `.env.example` as placeholders only  
✅ Repository is public; all secrets stay in Render dashboard  
✅ Database credentials never appear in code  
✅ OpenAI/Twilio keys only in Render environment  

## Next Steps

1. **Monitor usage**: Check Render logs regularly
2. **Scale up**: If free tier Render runs out of hours, upgrade
3. **Add payment**: Integrate Stripe for post-trial billing
4. **Custom domain**: Update Render to use your domain (e.g., responder.yourcompany.com)

## Support

For issues:
- Render docs: https://render.com/docs
- Neon docs: https://neon.tech/docs
- OpenAI docs: https://platform.openai.com/docs

---

**Deployment date**: June 5, 2026  
**Status**: Ready for production with 14-day free trial model
