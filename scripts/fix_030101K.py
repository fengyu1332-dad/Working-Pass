"""Fix 030101K 法学: replace 监狱学 data with correct 法学 content"""
import urllib.request, json

SUPABASE_URL = "https://djteatwxjlnbjylynvjh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4"

H = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}

# Correct content for 法学 (from KB['03'] template)
correct = {
    "overview": "法学是法学门类下的重要专业，研究法律规范、法律制度及其在社会中的实施，培养具备法律思维和正义感的专业法律人才。",
    "what_you_learn": "1）法学理论基础：法理学、宪法学、中国法制史、法律逻辑学；2）实体法：民法（总论/物权/合同/侵权）、刑法（总论/分论）、行政法学、商法学、经济法学；3）程序法：民事诉讼法学、刑事诉讼法学、行政诉讼法学；4）实践技能：法律文书写作、模拟法庭、法律诊所、毕业实习；核心能力：法律思维、法律检索与研究、法律文书写作、口头辩论能力。",
    "suitable_for": "法学适合以下学生：1）逻辑思维缜密，有较强的论证和推理能力；2）记忆力好，能应对大量法条的背诵；3）语言表达能力强，善于书面和口头辩论；4）有正义感和社会责任感；5）抗压能力强，能接受法考的高强度备考。慎报情况：不喜欢背书、逻辑思维混乱、表达能力差、对文字工作无兴趣的学生慎报。法考通过率仅15%左右，要有心理准备。",
    "career_outlook": "法学就业呈现长线投资特征。法考通过是基本门槛（通过率约15%）。塔尖（约10%）：红圈所(金杜、君合、方达、中伦等)律师，起薪2-3万/月，5年后可达50-100万/年；跨国公司/头部企业法务总监，年薪50-150万。塔身（约30%）：普通律所律师、企业法务、公证员，年薪10-25万。塔基（约60%）：法检公务员、行政执法、合规专员、基层法律服务，年薪8-15万。法学就业有明显的\"二八定律\"，名校+法考+好实习是关键。",
    "xuefeng_comment": "法学？文科专业一直被吐槽「无用」，但法学不一样！\n\n**先说说法学的「难」：**\n1. **法考是第一道坎！** 法考通过率只有15%左右，没有法律职业资格证，学法学等于白学。\n2. **人多竞争激烈！** 全国开设法学的高校太多，每年法学毕业生超过10万，但好岗位就那么几个。\n3. **需要长期投入！** 本科只是起点，硕士基本是标配，好律所几乎只要硕士以上。\n\n**但法学也真的「香」：**\n1. **考公岗位巨多！** 法院、检察院、公安、司法行政、海关、税务，法学是考公第一专业，每年国考省考法学可报岗位占比超20%。\n2. **上限极高！** 红圈所合伙人、大企业法总，年入百万的法学人大有人在。\n3. **社会地位高！** 律师、法官、检察官都是受人尊敬的职业。\n\n**报考建议：** 能上五院四系就报，进好学校是法学就业的关键。大二就要开始准备法考，不要等到毕业再着急。如果分数只能上普通院校，法学性价比会打折扣。\n\n总结：法学是「长线投资」的专业！前期苦，但坚持下来的收获很大！",
}

print(f"Patching 030101K 法学 with correct content...")
url = f"{SUPABASE_URL}/rest/v1/majors?code=eq.030101K"
req = urllib.request.Request(url, data=json.dumps(correct).encode("utf-8"), headers=H, method="PATCH")

try:
    resp = urllib.request.urlopen(req)
    print(f"Status: {resp.status}")
    if resp.status in (200, 204):
        print("Success: all fields updated")
    else:
        print(f"Response: {resp.read().decode('utf-8')[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Verify
print("\nVerifying...")
url2 = f"{SUPABASE_URL}/rest/v1/majors?select=code,name,overview,what_you_learn,suitable_for,career_outlook,xuefeng_comment&code=eq.030101K"
req2 = urllib.request.Request(url2, headers=H)
resp2 = urllib.request.urlopen(req2)
data = json.loads(resp2.read().decode("utf-8"))
m = data[0]

# Check for 监狱 mentions
issues = []
for field in ["overview", "what_you_learn", "suitable_for", "career_outlook", "xuefeng_comment"]:
    if "监狱" in (m.get(field) or ""):
        issues.append(f"  [{field}] still contains 监狱!")
    else:
        print(f"  [{field}] OK - no 监狱 reference")

if issues:
    print("\n[WARN] Remaining issues:")
    for i in issues:
        print(i)
else:
    print(f"\nAll clear. 030101K now reads: {m['overview'][:80]}...")
