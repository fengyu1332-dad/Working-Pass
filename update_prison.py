from supabase import create_client

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 监狱学详细内容
prison_data = {
    "030101K": {
        "overview": "监狱学是研究监狱管理、罪犯矫正和刑事执行法律的学科，是法学类中的特殊专业。学习内容包括监狱管理学、罪犯教育学、监狱心理学、狱政管理、刑事执行法学等。监狱学是法学与管理的交叉学科，培养监狱警察和法律工作者。",
        "what_you_learn": "监狱学课程包括：1）法学基础：刑法学、刑事诉讼法学、犯罪学；2）监狱管理：监狱管理学、狱政管理、监狱制度；3）矫正教育：罪犯教育学、罪犯心理矫治、职业技能培训；4）法律执行：刑事执行法学、行政法与行政诉讼法；5）实践：监狱实习、警务训练。核心能力：监狱管理能力、罪犯教育能力、执法能力。",
        "suitable_for": "适合有志于从事司法行政工作的学生；适合身体素质较好、能够适应警察工作模式的学生；适合责任心强、有耐心面对特殊群体的学生。",
        "career_outlook": "就业方向：1）监狱系统：监狱警察（主要去向，需通过司法联考）；2）戒毒所：司法警察；3）法院检察院：司法警察；4）社区矫正机构。薪资：监狱警察属于公务员编制，起薪6000-15000元/月，福利待遇较好。",
        "xuefeng_comment": "监狱学是'小众但稳定'的法学类专业，就业有保障。张雪峰建议：1）司法联考是进入监狱系统的唯一途径；2）监狱警察属于公务员，工作稳定但有一定危险性；3）身高、体能、体检有严格要求；4）适合喜欢稳定工作、不怕辛苦的学生；5）女生招生名额少，就业竞争相对较小。"
    }
}

def update_majors():
    for code, data in prison_data.items():
        result = supabase.table('majors').update(data).eq('code', code).execute()
        print(f"Updated: {code} {data['name'] if 'name' in data else '监狱学'}")

if __name__ == "__main__":
    print("Updating 监狱学...")
    update_majors()
    print("Done!")
