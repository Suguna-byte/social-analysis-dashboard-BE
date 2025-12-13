# Social Analytics Dashboard

A full-stack web application for tracking social media campaign performance across multiple platforms and discovering trending topics in real-time.

## What This Does

This dashboard lets you:
- Create and manage social media campaigns across Instagram, Facebook, Twitter, LinkedIn, and TikTok
- Track campaign metrics (impressions, clicks, engagement, conversions, spend)
- See which platforms are performing best with interactive charts
- Monitor trending topics from Reddit to inform content strategy
- Calculate ROI, CTR, and other key performance indicators
- Compare platform performance side-by-side

Basically, it's a centralized place to manage all your social media campaigns without jumping between different apps.

## How It's Built

**Frontend**: React with Tailwind CSS and Recharts for visualizations  
**Backend**: Django REST API with PostgreSQL database  
**Trending Data**: Reddit API integration for real-time trending topics

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env file)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your_supabase_host
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True

# Run migrations
python manage.py migrate

# Load sample data
python load_sample_data.py

# Start server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Open http://localhost:3000 in your browser. The API runs on http://localhost:8000.

## Database Schema

Two main tables:

**Campaigns** - Stores campaign info
- Name, platform, budget, dates, status
- One campaign can have multiple metrics

**Metrics** - Daily performance data
- Impressions, clicks, engagements, conversions, spend
- Linked to campaigns by campaign_id

## Key Metrics Explained

| Metric | What It Means |
|--------|--------------|
| **CTR** | Click-Through Rate: (Clicks / Impressions) × 100 |
| **Engagement Rate** | (Engagements / Impressions) × 100 |
| **Conversion Rate** | (Conversions / Clicks) × 100 |
| **CPC** | Cost Per Click: Spend / Clicks |
| **ROI** | Return on Investment as percentage |

## API Endpoints

### Campaigns
- `GET /api/campaigns/` - Get all campaigns with metrics
- `POST /api/campaigns/` - Create a new campaign
- `PUT /api/campaigns/{id}/` - Update campaign
- `DELETE /api/campaigns/{id}/` - Delete campaign

### Analytics
- `GET /api/campaigns/dashboard_stats/` - Overall KPIs (total impressions, clicks, CTR, ROI, etc.)
- `GET /api/campaigns/platform_performance/` - Performance breakdown by platform
- `GET /api/social-api/fetch_trending_topics/` - Trending topics from Reddit

## How Data Flows

1. You create a campaign in the app
2. Campaign gets saved to the database
3. You (or the system) add daily metrics for that campaign
4. Dashboard fetches all campaigns and calculates KPIs
5. Charts and tables render with the aggregated data
6. You make decisions based on which platforms perform best

## File Structure

```
social-analytics-dashboard/
├── backend/
│   ├── campaigns/          # Campaign CRUD operations
│   │   ├── models.py       # Campaign & Metric models
│   │   ├── views.py        # API endpoints
│   │   └── serializers.py
│   ├── social_api/         # Trending topics & analysis
│   │   └── views.py
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   └── App.js          # Main dashboard component
    ├── package.json
    └── tailwind.config.js
```

## Sample Data

The project comes with pre-loaded sample campaigns:
- Summer Sale 2024 (Instagram)
- Brand Awareness (Facebook)
- Holiday Campaign (Twitter)
- Product Launch (LinkedIn)

Each campaign has 3 days of metrics data.

## Important Notes

- Never commit the `.env` file - it has sensitive database credentials
- Keep `DEBUG=False` in production
- Always use HTTPS in production
- CORS is enabled for frontend-backend communication

## Troubleshooting

**Database connection failed?**
- Check your .env file has the correct Supabase credentials
- Make sure you've run migrations: `python manage.py migrate`

**Frontend can't connect to backend?**
- Make sure the backend is running on http://localhost:8000
- Check that CORS is enabled in Django settings

**Charts not showing?**
- Check browser console for errors
- Make sure sample data was loaded with `python load_sample_data.py`

## Next Steps to Improve

- Real Twitter/Instagram API integration
- ML-based sentiment analysis
- Multi-user support with roles
- WebSocket for real-time updates
- PDF/Excel export capabilities
- Scheduled email reports

## Testing

To test all endpoints:
```bash
cd backend
python test_endpoints_urllib.py
```

## Tech Stack

**Backend**: Django 6.0, Django REST Framework 3.16, PostgreSQL  
**Frontend**: React 19, Recharts 3.5, Tailwind CSS 3.4, Lucide React  
**Database**: Supabase (PostgreSQL hosting)

---

**Built for Social Booster Media - December 2024**
