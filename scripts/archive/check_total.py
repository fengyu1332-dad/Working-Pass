
import urllib.request
import urllib.error
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_majors():
    url = f'{SUPABASE_URL}/rest/v1/majors?select=*'
    req = urllib.request.Request(url)
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f'请求失败: {e}')
        return []

def main():
    majors = fetch_majors()
    if not majors:
        print('未能获取数据')
        return
    
    print(f'✅ 数据库专业总数: {len(majors)}')
    print()
    
    # 去重统计
    unique_codes = set()
    unique_majors = []
    for m in majors:
        if m['code'] not in unique_codes:
            unique_codes.add(m['code'])
            unique_majors.append(m)
    
    print(f'📊 去重后专业总数: {len(unique_majors)}')

if __name__ == '__main__':
    main()

