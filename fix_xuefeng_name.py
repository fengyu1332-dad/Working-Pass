from supabase import create_client

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 先获取所有专业
result = supabase.table('majors').select('code, name, xuefeng_comment').execute()
majors = result.data

print(f"Found {len(majors)} majors")

count = 0
for major in majors:
    if major['xuefeng_comment']:
        # 替换 "张雪峰" 或 "张雪峰老师" 为 "老师"
        new_comment = major['xuefeng_comment'].replace('张雪峰老师', '老师').replace('张雪峰', '老师')
        if new_comment != major['xuefeng_comment']:
            supabase.table('majors').update({'xuefeng_comment': new_comment}).eq('code', major['code']).execute()
            count += 1
            print(f"Updated: {major['code']} {major['name']}")

print(f"\nTotal updated: {count}")
