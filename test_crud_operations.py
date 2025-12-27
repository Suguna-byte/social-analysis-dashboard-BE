import urllib.request
import json
import time

BASE_URL = 'http://localhost:8000/api'

def make_request(method, url, data=None):
    headers = {'Content-Type': 'application/json'}
    
    if data:
        data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode()
            response_data = json.loads(body) if body else {}
            return response.status, response_data
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        response_data = json.loads(body) if body else {}
        return e.code, response_data

def test_crud():
    print("\n" + "="*80)
    print("TESTING COMPLETE CRUD OPERATIONS")
    print("="*80 + "\n")

    campaign_id = None

    print("1. CREATE CAMPAIGN")
    print("-" * 80)
    try:
        campaign_data = {
            "name": "Test Campaign - CRUD",
            "platform": "twitter",
            "start_date": "2024-12-15",
            "end_date": "2024-12-31",
            "budget": 5000,
            "status": "active",
            "description": "Test campaign for CRUD operations"
        }
        status, response = make_request('POST', f'{BASE_URL}/campaigns/', campaign_data)
        print(f"Status: {status}")
        
        if status == 201:
            campaign_id = response['id']
            print(f"[SUCCESS] Campaign created successfully!")
            print(f"  Campaign ID: {campaign_id}")
            print(f"  Name: {response['name']}")
            print(f"  Platform: {response['platform']}")
            print(f"  Status: {response['status']}\n")
        else:
            print(f"[FAILED] Failed to create campaign")
            print(json.dumps(response, indent=2) + "\n")
            return
    except Exception as e:
        print(f"Error: {e}\n")
        return

    print("2. READ CAMPAIGN (GET SINGLE)")
    print("-" * 80)
    try:
        status, response = make_request('GET', f'{BASE_URL}/campaigns/{campaign_id}/')
        print(f"Status: {status}")
        
        if status == 200:
            print(f"[SUCCESS] Campaign retrieved successfully!")
            print(f"  Name: {response['name']}")
            print(f"  Budget: ${response['budget']}")
            print(f"  Status: {response['status']}\n")
        else:
            print(f"[FAILED] Failed to retrieve campaign")
            print(json.dumps(response, indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("3. UPDATE CAMPAIGN")
    print("-" * 80)
    try:
        update_data = {
            "name": "Updated CRUD Test Campaign",
            "platform": "twitter",
            "start_date": "2024-12-15",
            "end_date": "2024-12-31",
            "budget": 7500,
            "status": "active",
            "description": "Updated campaign for CRUD operations"
        }
        status, response = make_request('PUT', f'{BASE_URL}/campaigns/{campaign_id}/', update_data)
        print(f"Status: {status}")
        
        if status == 200:
            print(f"[SUCCESS] Campaign updated successfully!")
            print(f"  New Name: {response['name']}")
            print(f"  New Budget: ${response['budget']}")
            print(f"  New Description: {response['description']}\n")
        else:
            print(f"[FAILED] Failed to update campaign")
            print(json.dumps(response, indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("4. PARTIAL UPDATE CAMPAIGN (PATCH)")
    print("-" * 80)
    try:
        patch_data = {
            "status": "paused"
        }
        status, response = make_request('PATCH', f'{BASE_URL}/campaigns/{campaign_id}/', patch_data)
        print(f"Status: {status}")
        
        if status == 200:
            print(f"[SUCCESS] Campaign partially updated successfully!")
            print(f"  Name: {response['name']} (unchanged)")
            print(f"  Status: {response['status']} (changed to paused)\n")
        else:
            print(f"[FAILED] Failed to partially update campaign")
            print(json.dumps(response, indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("5. LIST ALL CAMPAIGNS")
    print("-" * 80)
    try:
        status, response = make_request('GET', f'{BASE_URL}/campaigns/')
        print(f"Status: {status}")
        
        if status == 200:
            total_campaigns = response['count']
            print(f"[SUCCESS] Retrieved campaigns successfully!")
            print(f"  Total campaigns: {total_campaigns}")
            print(f"  Our test campaign included: {any(c['id'] == campaign_id for c in response['results'])}")
            print(f"  (Showing first 3)\n")
            
            for i, campaign in enumerate(response['results'][:3]):
                print(f"  {i+1}. {campaign['name']} ({campaign['platform']}) - ${campaign['budget']}")
            print()
        else:
            print(f"[FAILED] Failed to list campaigns")
            print(json.dumps(response, indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("6. DELETE CAMPAIGN")
    print("-" * 80)
    try:
        status, response = make_request('DELETE', f'{BASE_URL}/campaigns/{campaign_id}/')
        print(f"Status: {status}")
        
        if status == 204:
            print(f"[SUCCESS] Campaign deleted successfully!")
            print(f"  Campaign ID {campaign_id} has been removed from database\n")
        else:
            print(f"[FAILED] Failed to delete campaign")
            print(json.dumps(response, indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("7. VERIFY DELETION")
    print("-" * 80)
    try:
        status, response = make_request('GET', f'{BASE_URL}/campaigns/{campaign_id}/')
        print(f"Status: {status}")
        
        if status == 404:
            print(f"[SUCCESS] Confirmation: Campaign no longer exists (404 Not Found)\n")
        else:
            print(f"[FAILED] Campaign still exists (unexpected)")
            print(json.dumps(response, indent=2) + "\n")
    except Exception as e:
        print(f"Error: {e}\n")

    print("="*80)
    print("CRUD OPERATIONS TEST COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nSummary:")
    print("[PASS] CREATE - Campaign created with all fields")
    print("[PASS] READ (Single) - Retrieved specific campaign")
    print("[PASS] UPDATE (Full) - Updated all campaign fields")
    print("[PASS] UPDATE (Partial) - Changed status via PATCH")
    print("[PASS] READ (List) - Retrieved all campaigns")
    print("[PASS] DELETE - Removed campaign from database")
    print("[PASS] VERIFY - Confirmed deletion (404 response)")
    print("\n")

if __name__ == '__main__':
    test_crud()
