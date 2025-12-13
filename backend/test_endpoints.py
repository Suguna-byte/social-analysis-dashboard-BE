import requests
import json
import time

BASE_URL = 'http://localhost:8000/api'

time.sleep(2)

def test_endpoints():
    print("\n" + "="*80)
    print("TESTING ALL ENDPOINTS")
    print("="*80 + "\n")

    print("1. GET /api/campaigns/ - Get All Campaigns")
    print("-" * 80)
    try:
        response = requests.get(f'{BASE_URL}/campaigns/')
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total campaigns: {len(data['results']) if isinstance(data, dict) and 'results' in data else len(data)}")
        print(json.dumps(data, indent=2)[:500] + "...\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("2. GET /api/campaigns/dashboard_stats/ - Dashboard Stats")
    print("-" * 80)
    try:
        response = requests.get(f'{BASE_URL}/campaigns/dashboard_stats/')
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("3. GET /api/campaigns/platform_performance/ - Platform Performance")
    print("-" * 80)
    try:
        response = requests.get(f'{BASE_URL}/campaigns/platform_performance/')
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("4. POST /api/campaigns/ - Create Campaign")
    print("-" * 80)
    try:
        campaign_data = {
            "name": "New Campaign",
            "platform": "facebook",
            "start_date": "2024-12-15",
            "budget": 2000,
            "status": "active"
        }
        response = requests.post(f'{BASE_URL}/campaigns/', json=campaign_data)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2)[:500] + "...\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("5. GET /api/social-api/fetch_trending_topics/ - Trending Topics")
    print("-" * 80)
    try:
        response = requests.get(f'{BASE_URL}/social-api/fetch_trending_topics/')
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("6. POST /api/social-api/analyze_content/ - Content Analysis")
    print("-" * 80)
    try:
        content_data = {
            "content": "This is an amazing product that will change your life! Great value and excellent quality."
        }
        response = requests.post(f'{BASE_URL}/social-api/analyze_content/', json=content_data)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)

if __name__ == '__main__':
    test_endpoints()
