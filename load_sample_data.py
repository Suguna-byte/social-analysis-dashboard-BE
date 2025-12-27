import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analytics_project.settings')
django.setup()

from campaigns.models import Campaign, Metric
from datetime import date

try:
    c1 = Campaign.objects.create(
        name='Summer Sale 2024', 
        platform='instagram', 
        start_date=date(2024, 6, 1), 
        budget=5000, 
        status='active'
    )
    c2 = Campaign.objects.create(
        name='Brand Awareness', 
        platform='facebook', 
        start_date=date(2024, 5, 15), 
        budget=3000, 
        status='active'
    )
    c3 = Campaign.objects.create(
        name='Holiday Campaign', 
        platform='twitter', 
        start_date=date(2024, 12, 1), 
        budget=8000, 
        status='active'
    )
    c4 = Campaign.objects.create(
        name='Product Launch', 
        platform='linkedin', 
        start_date=date(2024, 11, 1), 
        budget=4500, 
        status='active'
    )

    Metric.objects.create(campaign=c1, date=date(2024, 12, 8), impressions=15000, clicks=450, engagements=320, conversions=45, spend=250)
    Metric.objects.create(campaign=c1, date=date(2024, 12, 9), impressions=18000, clicks=520, engagements=380, conversions=52, spend=280)
    Metric.objects.create(campaign=c1, date=date(2024, 12, 10), impressions=22000, clicks=680, engagements=450, conversions=68, spend=320)

    Metric.objects.create(campaign=c2, date=date(2024, 12, 8), impressions=12000, clicks=360, engagements=240, conversions=30, spend=200)
    Metric.objects.create(campaign=c2, date=date(2024, 12, 9), impressions=14000, clicks=420, engagements=280, conversions=35, spend=220)

    Metric.objects.create(campaign=c3, date=date(2024, 12, 8), impressions=20000, clicks=600, engagements=400, conversions=50, spend=300)
    Metric.objects.create(campaign=c4, date=date(2024, 12, 8), impressions=10000, clicks=300, engagements=200, conversions=25, spend=150)

    print('Sample data created successfully!')
except Exception as e:
    print(f'Error: {e}')
