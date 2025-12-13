# Backend - Social Analytics Dashboard

Django REST API for managing social media campaigns and providing analytics.

## Setup

### 1. Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the backend directory:

```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your_supabase_host
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
```

Replace with your actual Supabase credentials.

### 4. Database Setup

```bash
python manage.py migrate
python load_sample_data.py
```

This creates the database tables and loads sample campaigns.

### 5. Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at http://localhost:8000/api

## API Endpoints

All endpoints return JSON responses.

### Campaigns

- `GET /api/campaigns/` - List all campaigns (paginated)
- `POST /api/campaigns/` - Create a new campaign
- `GET /api/campaigns/{id}/` - Get campaign details
- `PUT /api/campaigns/{id}/` - Update campaign
- `DELETE /api/campaigns/{id}/` - Delete campaign

### Dashboard Stats

- `GET /api/campaigns/dashboard_stats/` - Get overall statistics

Returns:
- Total campaigns, impressions, clicks
- Total spend and ROI
- Average CTR and engagement rate
- Conversion rate

### Platform Performance

- `GET /api/campaigns/platform_performance/` - Get stats by platform

Returns performance metrics for each platform:
- Total impressions, clicks, conversions
- Engagement rate, conversion rate, CPC
- Total spend

### Trending Topics

- `GET /api/social-api/fetch_trending_topics/` - Get trending topics from Reddit

Returns a list of trending topics with upvotes, comments, subreddit, and URL.

## Project Structure

```
backend/
├── analytics_project/      # Django project settings
│   ├── settings.py        # Configuration, database, apps, CORS
│   ├── urls.py            # Route all requests to app URLs
│   └── wsgi.py
│
├── campaigns/             # Campaign management app
│   ├── models.py          # Campaign and Metric models
│   ├── views.py           # API views for CRUD and analytics
│   ├── serializers.py     # Convert models to/from JSON
│   ├── urls.py            # Campaign routes
│   └── migrations/        # Database schema changes
│
├── social_api/            # External data sources
│   ├── views.py           # Trending topics, content analysis
│   └── urls.py
│
├── manage.py              # Django management tool
├── load_sample_data.py    # Script to populate database
├── requirements.txt       # Python dependencies
└── README.md
```

## Database Schema

**Campaigns Table**
- id (Primary Key)
- name (Campaign name)
- platform (facebook, instagram, twitter, linkedin, tiktok)
- budget (Budget amount)
- status (draft, active, paused, completed)
- start_date, end_date
- description
- created_at, updated_at

**Metrics Table**
- id (Primary Key)
- campaign_id (Foreign Key to Campaigns)
- date (Date of metrics)
- impressions
- clicks
- engagements
- conversions
- spend

One campaign can have many metrics (one-to-many relationship).

## Key KPI Calculations

- **CTR** (Click-Through Rate) = (clicks / impressions) × 100
- **Engagement Rate** = (engagements / impressions) × 100
- **Conversion Rate** = (conversions / clicks) × 100
- **CPC** (Cost Per Click) = spend / clicks
- **ROI** = ((conversions × 100 - spend) / spend) × 100

## Testing the API

Test all endpoints:

```bash
python test_endpoints_urllib.py
```

This runs through all the main API endpoints and shows responses.

## Common Issues

**Database connection error?**
- Check .env file has correct Supabase credentials
- Verify DB_HOST and DB_PORT are correct
- Make sure PostgreSQL is accessible from your network

**ModuleNotFoundError?**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**No tables in database?**
- Run migrations: `python manage.py migrate`
- Load sample data: `python load_sample_data.py`

## Loading Your Own Data

Instead of using sample data, you can:

1. Create a Python script to populate campaigns and metrics
2. Use the admin panel if enabled
3. Make API calls to POST endpoints

Example API call:

```bash
curl -X POST http://localhost:8000/api/campaigns/ \
  -H "Content-Type: application/json" \
  -d '{"name":"My Campaign","platform":"instagram","budget":5000,"start_date":"2024-12-13","status":"active"}'
```

## Tech Stack

- Django 6.0 - Web framework
- Django REST Framework 3.16 - API development
- PostgreSQL 14+ - Database
- Supabase - PostgreSQL hosting
- Python 3.9+

## Notes

- CORS is enabled to allow frontend requests from http://localhost:3000
- DEBUG mode is on for development - turn it off in production (DEBUG=False)
- Sample data is loaded on first run - safe to delete and reload anytime
