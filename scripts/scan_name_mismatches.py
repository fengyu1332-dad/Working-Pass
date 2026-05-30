"""Full scan: check all 883 majors for overviews that reference the wrong major name"""
import urllib.request, json, time

SUPABASE_URL = "https://djteatwxjlnbjylynvjh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4"

H = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

# Fetch all majors
all_majors = []
for offset in range(0, 2000, 1000):
    url = f"{SUPABASE_URL}/rest/v1/majors?select=code,name,category,overview&limit=1000&offset={offset}"
    req = urllib.request.Request(url, headers=H)
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode("utf-8"))
    if not data:
        break
    all_majors.extend(data)
    time.sleep(0.1)

print(f"Total majors: {len(all_majors)}")

# Build the full list of all major names for detection
all_names = [m["name"] for m in all_majors]

# Known common words that legitimately start overviews for broad majors
SAFE_STARTS = {"法学", "工学", "理学", "经济学", "管理学", "医学", "文学", "哲学", "教育学", "农学", "历史学", "艺术学", "军事学", "交叉学科"}

issues = []
for m in all_majors:
    name = m["name"]
    overview = m.get("overview") or ""
    cat = m.get("category", "")

    if not overview:
        issues.append({
            "code": m["code"],
            "name": name,
            "category": cat,
            "problem": "overview is empty",
            "overview_start": "(empty)",
        })
        continue

    # Check if overview starts with a DIFFERENT major name
    # BUT: only flag if overview does NOT start with its own correct name first
    # (this prevents false positives when e.g. "人工智能教育" overview starts with
    #  "人工智能教育" but another major "人工智能" is a prefix)
    if overview.startswith(name):
        continue  # overview correctly starts with own name, skip
    for other_name in all_names:
        if other_name == name:
            continue
        if other_name in SAFE_STARTS:
            continue
        # Only flag if it starts with the wrong name (strongest signal)
        if overview.startswith(other_name):
            issues.append({
                "code": m["code"],
                "name": name,
                "category": cat,
                "problem": f"overview starts with '{other_name}' instead of '{name}'",
                "overview_start": overview[:80],
            })
            break

    # Also catch generic template patterns
    if overview.startswith("研究") and "相关理论与实践" in overview[:50]:
        issues.append({
            "code": m["code"],
            "name": name,
            "category": cat,
            "problem": "generic template: '研究...相关理论与实践'",
            "overview_start": overview[:80],
        })

# Report
print(f"\nIssues found: {len(issues)}")
for i in issues:
    print(f"\n  [{i['code']}] {i['name']} ({i['category']})")
    print(f"  Problem: {i['problem']}")
    print(f"  Overview: {i['overview_start']}")

# Count by category
from collections import Counter
cat_counts = Counter(i["category"] for i in issues)
print(f"\nBy category:")
for cat, count in cat_counts.most_common():
    print(f"  {cat}: {count}")

# Save full report
with open("D:/ai/大学专业职业前景查询网站/test_reports/_name_mismatch_scan.json", "w", encoding="utf-8") as f:
    json.dump(issues, f, ensure_ascii=False, indent=2)

print(f"\nFull report saved to test_reports/_name_mismatch_scan.json")
