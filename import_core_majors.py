from supabase import create_client

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

category_icons = {
    '01': '🎓', '02': '💰', '03': '⚖️', '04': '📚',
    '05': '📖', '06': '📜', '07': '🔢', '08': '💻',
    '09': '🌾', '10': '🩺', '11': '🎖️', '12': '📋', '13': '🎨'
}

core_majors = [
    # 01 哲学 (2 more)
    {"code": "010103", "name": "宗教学", "category": "01 哲学", "category_icon": "🎓", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    
    # 02 经济学 (4 more)
    {"code": "020201", "name": "财政学", "category": "02 经济学", "category_icon": "💰", "difficulty": "★★★★☆", "salary_range": "5000-30000元/月"},
    {"code": "020202", "name": "税收学", "category": "02 经济学", "category_icon": "💰", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    {"code": "020301", "name": "金融工程", "category": "02 经济学", "category_icon": "💰", "difficulty": "★★★★★", "salary_range": "8000-50000元/月"},
    {"code": "020402", "name": "保险学", "category": "02 经济学", "category_icon": "💰", "difficulty": "★★★☆☆", "salary_range": "5000-30000元/月"},
    
    # 03 法学 (4 more)
    {"code": "030102", "name": "知识产权", "category": "03 法学", "category_icon": "⚖️", "difficulty": "★★★★☆", "salary_range": "6000-35000元/月"},
    {"code": "030601", "name": "社会学", "category": "03 法学", "category_icon": "⚖️", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    {"code": "030501", "name": "思想政治教育", "category": "03 法学", "category_icon": "⚖️", "difficulty": "★★★☆☆", "salary_range": "4000-15000元/月"},
    {"code": "030101K", "name": "监狱学", "category": "03 法学", "category_icon": "⚖️", "difficulty": "★★★☆☆", "salary_range": "6000-20000元/月"},
    
    # 04 教育学 (3 more)
    {"code": "040102", "name": "学前教育", "category": "04 教育学", "category_icon": "📚", "difficulty": "★★☆☆☆", "salary_range": "4000-12000元/月"},
    {"code": "040202", "name": "运动训练", "category": "04 教育学", "category_icon": "📚", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    {"code": "071101", "name": "心理学", "category": "04 教育学", "category_icon": "📚", "difficulty": "★★★★☆", "salary_range": "5000-25000元/月"},
    
    # 05 文学 (4 more)
    {"code": "050102", "name": "汉语国际教育", "category": "05 文学", "category_icon": "📖", "difficulty": "★★★☆☆", "salary_range": "5000-20000元/月"},
    {"code": "050302", "name": "广播电视学", "category": "05 文学", "category_icon": "📖", "difficulty": "★★★☆☆", "salary_range": "5000-20000元/月"},
    {"code": "050304", "name": "传播学", "category": "05 文学", "category_icon": "📖", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    {"code": "050306", "name": "网络与新媒体", "category": "05 文学", "category_icon": "📖", "difficulty": "★★★☆☆", "salary_range": "6000-25000元/月"},
    
    # 06 历史学 (2)
    {"code": "060101", "name": "历史学", "category": "06 历史学", "category_icon": "📜", "difficulty": "★★★☆☆", "salary_range": "4000-18000元/月"},
    {"code": "060102", "name": "考古学", "category": "06 历史学", "category_icon": "📜", "difficulty": "★★★★☆", "salary_range": "5000-20000元/月"},
    
    # 07 理学 (4 more)
    {"code": "070501", "name": "地理科学", "category": "07 理学", "category_icon": "🔢", "difficulty": "★★★☆☆", "salary_range": "5000-18000元/月"},
    {"code": "070601", "name": "大气科学", "category": "07 理学", "category_icon": "🔢", "difficulty": "★★★★☆", "salary_range": "6000-25000元/月"},
    {"code": "070801", "name": "地球物理学", "category": "07 理学", "category_icon": "🔢", "difficulty": "★★★★☆", "salary_range": "6000-25000元/月"},
    {"code": "071401", "name": "环境科学", "category": "07 理学", "category_icon": "🔢", "difficulty": "★★★★☆", "salary_range": "5000-20000元/月"},
    
    # 08 工学 (20 more)
    {"code": "080202", "name": "机械设计制造及其自动化", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "6000-25000元/月"},
    {"code": "080207", "name": "车辆工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "7000-30000元/月"},
    {"code": "080601", "name": "电气工程及其自动化", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "6000-30000元/月"},
    {"code": "080901", "name": "计算机科学与技术", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "8000-40000元/月"},
    {"code": "080902", "name": "软件工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "8000-40000元/月"},
    {"code": "080903", "name": "网络工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "6000-30000元/月"},
    {"code": "080904K", "name": "信息安全", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★★", "salary_range": "8000-40000元/月"},
    {"code": "080710T", "name": "人工智能", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★★", "salary_range": "10000-60000元/月"},
    {"code": "081001", "name": "土木工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "6000-30000元/月"},
    {"code": "081002", "name": "建筑环境与能源应用工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    {"code": "081301", "name": "建筑学", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "6000-30000元/月"},
    {"code": "081302", "name": "城乡规划", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    {"code": "081502", "name": "石油工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "7000-30000元/月"},
    {"code": "082502", "name": "环境工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "5000-25000元/月"},
    {"code": "082502", "name": "环境科学", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★☆", "salary_range": "5000-25000元/月"},
    {"code": "082701", "name": "食品科学与工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★☆☆", "salary_range": "5000-20000元/月"},
    {"code": "082901", "name": "安全工程", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★☆☆", "salary_range": "6000-25000元/月"},
    {"code": "080906", "name": "智能科学与技术", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★★", "salary_range": "10000-50000元/月"},
    {"code": "080910T", "name": "数据科学与大数据技术", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★★", "salary_range": "10000-50000元/月"},
    {"code": "080717T", "name": "海洋机器人", "category": "08 工学", "category_icon": "💻", "difficulty": "★★★★★", "salary_range": "8000-35000元/月"},
    
    # 09 农学 (4 more)
    {"code": "090102", "name": "园艺学", "category": "09 农学", "category_icon": "🌾", "difficulty": "★★★☆☆", "salary_range": "4000-18000元/月"},
    {"code": "090301", "name": "动物科学", "category": "09 农学", "category_icon": "🌾", "difficulty": "★★★☆☆", "salary_range": "4000-18000元/月"},
    {"code": "090701", "name": "草业科学", "category": "09 农学", "category_icon": "🌾", "difficulty": "★★★☆☆", "salary_range": "4000-15000元/月"},
    {"code": "090801", "name": "水产养殖学", "category": "09 农学", "category_icon": "🌾", "difficulty": "★★★☆☆", "salary_range": "4000-18000元/月"},
    
    # 10 医学 (4 more)
    {"code": "100202", "name": "麻醉学", "category": "10 医学", "category_icon": "🩺", "difficulty": "★★★★★", "salary_range": "8000-35000元/月"},
    {"code": "100203", "name": "医学影像学", "category": "10 医学", "category_icon": "🩺", "difficulty": "★★★★☆", "salary_range": "7000-30000元/月"},
    {"code": "100301", "name": "口腔医学", "category": "10 医学", "category_icon": "🩺", "difficulty": "★★★★★", "salary_range": "8000-40000元/月"},
    {"code": "100402", "name": "中医学", "category": "10 医学", "category_icon": "🩺", "difficulty": "★★★★☆", "salary_range": "5000-25000元/月"},
    
    # 12 管理学 (4 more)
    {"code": "120202", "name": "市场营销", "category": "12 管理学", "category_icon": "📋", "difficulty": "★★★☆☆", "salary_range": "5000-30000元/月"},
    {"code": "120204", "name": "财务管理", "category": "12 管理学", "category_icon": "📋", "difficulty": "★★★☆☆", "salary_range": "5000-25000元/月"},
    {"code": "120206", "name": "人力资源管理", "category": "12 管理学", "category_icon": "📋", "difficulty": "★★☆☆☆", "salary_range": "5000-25000元/月"},
    {"code": "120801", "name": "电子商务", "category": "12 管理学", "category_icon": "📋", "difficulty": "★★★☆☆", "salary_range": "5000-30000元/月"},
    
    # 13 艺术学 (4 more)
    {"code": "130305", "name": "广播电视编导", "category": "13 艺术学", "category_icon": "🎨", "difficulty": "★★★☆☆", "salary_range": "5000-30000元/月"},
    {"code": "130309", "name": "播音与主持艺术", "category": "13 艺术学", "category_icon": "🎨", "difficulty": "★★★☆☆", "salary_range": "6000-35000元/月"},
    {"code": "130401", "name": "美术学", "category": "13 艺术学", "category_icon": "🎨", "difficulty": "★★★☆☆", "salary_range": "4000-25000元/月"},
    {"code": "130501", "name": "艺术设计学", "category": "13 艺术学", "category_icon": "🎨", "difficulty": "★★★☆☆", "salary_range": "5000-30000元/月"},
]

def import_majors():
    print(f"Importing {len(core_majors)} core majors...")
    success_count = 0
    error_count = 0
    
    for major in core_majors:
        try:
            result = supabase.table('majors').insert(major).execute()
            print(f"✓ {major['code']} {major['name']}")
            success_count += 1
        except Exception as e:
            error_str = str(e)
            if 'duplicate key' in error_str.lower():
                print(f"- {major['code']} {major['name']} (already exists)")
            else:
                print(f"✗ {major['code']} {major['name']}: {e}")
                error_count += 1
    
    print(f"\nDone! Success: {success_count}, Errors: {error_count}")

if __name__ == "__main__":
    import_majors()
