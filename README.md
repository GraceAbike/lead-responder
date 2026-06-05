Automated AI Lead Responder (Multi-Client SaaS Platform)

A professional, AI-powered lead responder SaaS platform that lets you manage multiple service business clients. Each client gets isolated leads, secure authentication, and a private dashboard. Automatically generate professional responses using OpenAI, send SMS confirmations, and track metrics—all with complete data isolation.

## Key Features

✨ **Multi-Client Architecture**: Manage 1 to 200+ clients with complete data isolation  
🔐 **Admin Dashboard**: Master control panel to create clients and manage the entire platform  
👥 **Client Dashboards**: Each client has a secure, isolated dashboard with their own leads  
📊 **Real-Time Metrics**: Total leads, AI responses sent, and estimated revenue per client  
🤖 **AI-Powered Responses**: Generates professional, polite customer replies using OpenAI GPT-4  
📞 **Optional SMS**: Send confirmation messages via Twilio (optional)  
🚀 **Production Ready**: Deployed on Render with Neon PostgreSQL  
💰 **SaaS Model**: 14-day free trial per client, then subscription-based pricing  

## Architecture Overview

```
Platform:
├── Admin Portal (/admin/login, /admin/dashboard)
│   └── Manage all clients, generate credentials
├── Client Portals (/client/login, /client/dashboard)
│   └── Each client sees only their own leads
└── API (/api/leads, /api/admin/clients)
    └── Client-isolated lead management
```

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
- `ADMIN_PASSWORD`: Your master admin password (or use `DASHBOARD_PASSWORD` as fallback)
- `DATABASE_URL`: PostgreSQL connection string (optional; uses local SQLite by default)
- `SECRET_KEY`: A random, secure string

### 3. Run locally

```powershell
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000`:
- **Admin Portal**: http://127.0.0.1:8000/admin/login (use `ADMIN_PASSWORD`)
- **Client Portal**: http://127.0.0.1:8000/client/login (use client ID and password)

## How to Use

### Admin: Creating a New Client

1. Navigate to `/admin/login` and log in with your `ADMIN_PASSWORD`
2. You'll see the **Client Management Dashboard**
3. Enter the client's business name (e.g., "Elite Roofing")
4. Click **Create Client**
5. You'll receive:
   - **Client ID**: A unique identifier (e.g., `A7B2F9C1`)
   - **Password**: A secure, randomly generated password
6. Share both with your client securely

**Example credentials generated:**
```
Client ID: A7B2F9C1
Password: d4f8x2k9m5q1p7w3
```

### Client: Using the Dashboard

1. Navigate to `/client/login`
2. Enter your **Client ID** and **Password**
3. Access your dashboard at `/client/dashboard`
4. View:
   - **Total Leads**: All leads submitted for your business
   - **AI Replied**: Leads where AI has sent an automatic response
   - **Saved Revenue**: Estimated value from fast AI responses
   - **Recent Leads**: Table of all incoming customer requests
5. Submit test leads using the form
6. Click **Logout** when done

## API Endpoints

### Submit a Lead (Client/Webhook)

Requires client to be authenticated (cookie-based).

```bash
POST /api/leads
Content-Type: application/json

{
  "customer_name": "John Doe",
  "customer_phone": "+1-555-0100"
}
```

Response (Client only sees their own leads):
```json
{"status": "ok", "id": 1}
```

### Get Client's Leads

```bash
GET /api/leads
```

Returns array of **only that client's leads** with status, timestamp, and customer info.

### Admin: Create Client (API)

Requires admin authentication.

```bash
POST /api/admin/clients
Content-Type: application/json

{
  "name": "Elite Roofing"
}
```

Response:
```json
{
  "status": "ok",
  "client_id": "A7B2F9C1",
  "password": "d4f8x2k9m5q1p7w3",
  "name": "Elite Roofing"
}
```

## Database Schema

### Clients Table
```
clients:
  - id (int, primary key)
  - client_id (string, unique) - Public ID for login
  - name (string) - Business name
  - password_hash (string) - Hashed password
  - created_at (datetime) - Account creation
  - trial_end_date (datetime) - When trial expires
```

### Leads Table
```
leads:
  - id (int, primary key)
  - client_id (int, foreign key) - Links to clients table
  - customer_name (string)
  - customer_phone (string)
  - status (string) - "New" or "Contacted"
  - timestamp (datetime)
```

**Key Security Feature**: Leads have a `client_id` foreign key, ensuring each client ONLY sees their own leads in queries.

## Security & Data Isolation

✅ **Complete Data Isolation**: Each client's leads are stored with their `client_id` and filtered on retrieval  
✅ **Unique Client IDs**: Each client gets a unique 8-char ID (e.g., `A7B2F9C1`)  
✅ **Hashed Passwords**: Client passwords are hashed using SHA256  
✅ **Session Tokens**: Separate `client_session` and `admin_session` cookies  
✅ **Secrets in .gitignore**: Never committed to Git  
✅ **Environment Variables**: All secrets stored in Render dashboard only  
✅ **HTTPS on Production**: All traffic is encrypted  

## Scaling from 1 to 200+ Clients

This architecture is designed to scale:

| Metric | Details |
|--------|---------|
| **Database** | Neon PostgreSQL handles millions of rows with client_id indexing |
| **Lead Isolation** | Queries use `WHERE client_id = ?` ensuring no data leaks |
| **Session Management** | Separate cookies for admin and client authentication |
| **Admin Control** | Single admin account manages all clients and credentials |
| **Trial Tracking** | Automatic tracking of 14-day trial per client |

## Environment Variables

Required for production deployment:

```env
# Authentication
ADMIN_PASSWORD=your_master_admin_password
SECRET_KEY=a_very_random_string_minimum_32_chars

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require

# AI & Integrations
OPENAI_API_KEY=sk-proj-...
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# SaaS Config
TRIAL_DAYS=14
```

## Live Deployment

### Deploy to Render

Your multi-client SaaS is live at:  
**https://lead-responder.onrender.com**

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Setting up Neon PostgreSQL
- Configuring Render environment variables
- Webhook integration for each client
- Custom domain setup
- Troubleshooting

### Testing Production

1. **Admin Access**: `https://lead-responder.onrender.com/admin/login`
2. **Create a Test Client**: Enter "Test Business"
3. **Client Access**: Use the generated Client ID and password
4. **Submit Test Lead**: Use the client dashboard
5. **Verify Isolation**: Admin sees all clients; each client sees only their leads

## Pricing Model

### Base SaaS Structure
- **First 14 days**: Full access, all features, no payment
- **Day 15+**: $29/month per client or $500 one-time

### Future Enhancements
- Stripe integration for post-trial payment collection
- Email notifications for trial expiration
- Team access per client (multiple users)
- Advanced analytics per client
- White-label dashboard options

## Next Steps

1. **Test locally**: `uvicorn app.main:app --reload`
2. **Create first client**: Use `/admin/login` and create a test client
3. **Verify data isolation**: Log in as admin and as client, confirm leads are isolated
4. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
5. **Add payment**: Integrate Stripe for post-trial billing
6. **Custom domain**: Point your domain to Render service

## Support & Docs

- **Render Docs**: https://render.com/docs
- **Neon PostgreSQL**: https://neon.tech/docs
- **OpenAI API**: https://platform.openai.com/docs
- **Twilio SMS**: https://www.twilio.com/docs
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/

## License

MIT License - free to modify and use commercially

---

**Architecture**: Multi-Client SaaS with complete data isolation  
**Status**: 🟢 Production Ready  
**Last Updated**: June 5, 2026  
**Clients Supported**: 1 to 200+ (with database scaling)

