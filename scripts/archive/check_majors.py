import requests
import json

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

def get_all_majors():
    url = f"{SUPABASE_URL}/rest/v1/majors?select=code,name&order=id"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        majors = response.json()
        print("📊 Database majors:")
        print("-" * 50)
        for i, major in enumerate(majors, 1):
            print(f"{i:2d}. {major['code']:10s} - {major['name']}")
        print("-" * 50)
        print(f"\nTotal: {len(majors)} majors")
        return majors
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

if __name__ == "__main__":
    get_all_majors()