from supabase import create_client

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

sql = """
ALTER TABLE majors ADD COLUMN IF NOT EXISTS salary_detail JSONB;
"""

try:
    result = supabase.rpc('exec', {'query': sql}).execute()
    print("Column added successfully")
except Exception as e:
    print(f"Error: {e}")
    print("Trying alternative approach...")
    
    test = supabase.table('majors').select('*').limit(1).execute()
    print(f"Current columns: {list(test.data[0].keys()) if test.data else 'No data'}")
