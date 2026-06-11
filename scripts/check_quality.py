import asyncio, aiohttp, json, re, sys, io
SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'
H = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

async def main():
    async with aiohttp.ClientSession() as s:
        resp = await s.get(f'{SUPABASE_URL}/rest/v1/majors?select=code,name,salary_range,category_icon,yearly_courses,top_universities&order=code.asc&limit=900', headers=H)
        majors = await resp.json()
        print(f'Total majors: {len(majors)}')

        # 1. Bad salary format
        bad_sal = []
        for m in majors:
            sr = (m.get('salary_range') or '').strip()
            if sr == '':
                bad_sal.append(f'{m["code"]} {m["name"]}: EMPTY')
            elif not re.match(r'^¥\d+k-\d+k$', sr):
                bad_sal.append(f'{m["code"]} {m["name"]}: [{sr}]')
        print(f'\nBad salary: {len(bad_sal)}')
        for b in bad_sal:
            print(f'  {b}')

        # 2. Empty category_icon
        empty_icon = [m for m in majors if not m.get('category_icon')]
        print(f'\nEmpty category_icon: {len(empty_icon)}')
        for m in empty_icon:
            print(f'  {m["code"]} {m["name"]}')

        # 3. yearly_courses < 10
        yc_bad = []
        for m in majors:
            yc = m.get('yearly_courses')
            if isinstance(yc, str):
                try: yc = json.loads(yc)
                except: yc = {}
            if isinstance(yc, dict):
                total = sum(len(v) for v in yc.values())
                if total < 10:
                    yc_bad.append(f'{m["code"]} {m["name"]}: {total} courses')
        print(f'\nyearly_courses < 10: {len(yc_bad)}')
        for b in yc_bad:
            print(f'  {b}')

        # 4. top_universities intl < 3
        uni_bad = []
        for m in majors:
            tu = m.get('top_universities')
            if isinstance(tu, str):
                try: tu = json.loads(tu)
                except: tu = {}
            if isinstance(tu, dict):
                if len(tu.get('international', [])) < 3:
                    uni_bad.append(f'{m["code"]} {m["name"]}: {len(tu.get("international",[]))} intl')
        print(f'\ntop_universities intl < 3: {len(uni_bad)}')
        for b in uni_bad:
            print(f'  {b}')

    print(f'\nDone. Output also written to quality_report.txt')

asyncio.run(main())
