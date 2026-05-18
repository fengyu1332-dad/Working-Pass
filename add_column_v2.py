import requests

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'
SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3OTA4NTA5MywiZXhwIjoyMDk0NjYxMDkzfQ.qZ8K5v8YJp2yRj8cX9ZKmYvJbL2oT3nM6hW1xR9YcA'

headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

sql = 'ALTER TABLE majors ADD COLUMN IF NOT EXISTS salary_detail JSONB;'

response = requests.post(
    f'{SUPABASE_URL}/rest/v1/rpc/exec',
    headers=headers,
    json={'query': sql}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
