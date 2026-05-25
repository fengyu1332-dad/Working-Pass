import json
import random

def get_majors():
    majors = []
    
    # 01 哲学 (Philosophy)
    philosophy_majors = [
        {"id": "010101", "name": "哲学", "subCategory": "philosophy", "code": "010101", "subtitle": "思考存在的本质", "trend": "稳定"},
        {"id": "010102", "name": "逻辑学", "subCategory": "logic", "code": "010102", "subtitle": "思维的规则与推理", "trend": "上升"},
        {"id": "010103", "name": "宗教学", "subCategory": "religion", "code": "010103", "subtitle": "信仰与精神世界", "trend": "稳定"},
        {"id": "010104", "name": "伦理学", "subCategory": "ethics", "code": "010104", "subtitle": "道德与价值的探究", "trend": "上升"},
    ]
    
    # 02 经济学 (Economics)
    economics_majors = [
        {"id": "020101", "name": "经济学", "subCategory": "economics", "code": "020101", "subtitle": "资源配置与财富创造", "trend": "上升"},
        {"id": "020102", "name": "国际经济与贸易", "subCategory": "trade", "code": "020102", "subtitle": "全球化经济运作", "trend": "波动"},
        {"id": "020103", "name": "金融学", "subCategory": "finance", "code": "020103", "subtitle": "货币与资本运作", "trend": "上升"},
        {"id": "020104", "name": "金融工程", "subCategory": "fintech", "code": "020104", "subtitle": "金融产品创新", "trend": "上升"},
        {"id": "020105", "name": "保险学", "subCategory": "insurance", "code": "020105", "subtitle": "风险管理与保障", "trend": "稳定"},
        {"id": "020106", "name": "投资学", "subCategory": "investment", "code": "020106", "subtitle": "资产配置与增值", "trend": "上升"},
        {"id": "020107", "name": "税收学", "subCategory": "taxation", "code": "020107", "subtitle": "税务规划与政策", "trend": "稳定"},
        {"id": "020108", "name": "统计学", "subCategory": "statistics", "code": "020108", "subtitle": "数据与概率分析", "trend": "上升"},
    ]
    
    # 03 法学 (Law)
    law_majors = [
        {"id": "030101", "name": "法学", "subCategory": "law", "code": "030101", "subtitle": "正义与秩序的守护", "trend": "稳定"},
        {"id": "030102", "name": "知识产权", "subCategory": "ip", "code": "030102", "subtitle": "创新成果的法律保护", "trend": "上升"},
        {"id": "030103", "name": "社会学", "subCategory": "sociology", "code": "030103", "subtitle": "社会结构与变迁", "trend": "稳定"},
        {"id": "030104", "name": "社会工作", "subCategory": "social_work", "code": "030104", "subtitle": "助人与公共服务", "trend": "稳定"},
        {"id": "030105", "name": "政治学与行政学", "subCategory": "politics", "code": "030105", "subtitle": "治理与公共事务", "trend": "稳定"},
        {"id": "030106", "name": "国际关系", "subCategory": "ir", "code": "030106", "subtitle": "国家间的博弈与合作", "trend": "上升"},
        {"id": "030107", "name": "公安学", "subCategory": "public_security", "code": "030107", "subtitle": "维护社会秩序", "trend": "稳定"},
    ]
    
    # 04 教育学 (Education)
    education_majors = [
        {"id": "040101", "name": "教育学", "subCategory": "education", "code": "040101", "subtitle": "教育的科学理论与实践", "trend": "稳定"},
        {"id": "040102", "name": "学前教育", "subCategory": "preschool", "code": "040102", "subtitle": "奠定人生基石", "trend": "上升"},
        {"id": "040103", "name": "小学教育", "subCategory": "primary", "code": "040103", "subtitle": "启蒙与成长", "trend": "稳定"},
        {"id": "040104", "name": "特殊教育", "subCategory": "special", "code": "040104", "subtitle": "让每个生命发光", "trend": "上升"},
        {"id": "040105", "name": "教育技术学", "subCategory": "edtech", "code": "040105", "subtitle": "科技赋能教育", "trend": "上升"},
        {"id": "040106", "name": "体育教育", "subCategory": "pe", "code": "040106", "subtitle": "强身健体育人", "trend": "稳定"},
    ]
    
    # 05 文学 (Literature)
    literature_majors = [
        {"id": "050101", "name": "汉语言文学", "subCategory": "chinese_lit", "code": "050101", "subtitle": "文字的力量与美", "trend": "稳定"},
        {"id": "050102", "name": "汉语言", "subCategory": "chinese_lang", "code": "050102", "subtitle": "汉语的深度研究", "trend": "稳定"},
        {"id": "050103", "name": "英语", "subCategory": "english", "code": "050103", "subtitle": "连接世界的桥梁", "trend": "波动"},
        {"id": "050104", "name": "日语", "subCategory": "japanese", "code": "050104", "subtitle": "樱花之国的语言", "trend": "稳定"},
        {"id": "050105", "name": "法语", "subCategory": "french", "code": "050105", "subtitle": "浪漫与优雅", "trend": "稳定"},
        {"id": "050106", "name": "德语", "subCategory": "german", "code": "050106", "subtitle": "严谨与精密", "trend": "稳定"},
        {"id": "050107", "name": "新闻学", "subCategory": "journalism", "code": "050107", "subtitle": "记录与传播真相", "trend": "波动"},
        {"id": "050108", "name": "广播电视学", "subCategory": "broadcasting", "code": "050108", "subtitle": "声画的世界", "trend": "波动"},
        {"id": "050109", "name": "广告学", "subCategory": "advertising", "code": "050109", "subtitle": "创意与营销", "trend": "稳定"},
        {"id": "050110", "name": "编辑出版学", "subCategory": "publishing", "code": "050110", "subtitle": "知识的传播者", "trend": "稳定"},
        {"id": "050111", "name": "翻译", "subCategory": "translation", "code": "050111", "subtitle": "跨越语言的鸿沟", "trend": "上升"},
        {"id": "050112", "name": "网络与新媒体", "subCategory": "new_media", "code": "050112", "subtitle": "数字时代的传播", "trend": "上升"},
    ]
    
    # 06 历史学 (History)
    history_majors = [
        {"id": "060101", "name": "历史学", "subCategory": "history", "code": "060101", "subtitle": "以史为鉴知兴替", "trend": "稳定"},
        {"id": "060102", "name": "世界史", "subCategory": "world_history", "code": "060102", "subtitle": "全球文明的脉络", "trend": "稳定"},
        {"id": "060103", "name": "考古学", "subCategory": "archaeology", "code": "060103", "subtitle": "探寻历史的痕迹", "trend": "上升"},
        {"id": "060104", "name": "文物与博物馆学", "subCategory": "museum", "code": "060104", "subtitle": "守护文明记忆", "trend": "上升"},
    ]
    
    # 07 理学 (Science)
    science_majors = [
        {"id": "070101", "name": "数学与应用数学", "subCategory": "math", "code": "070101", "subtitle": "科学的皇后", "trend": "上升"},
        {"id": "070102", "name": "信息与计算科学", "subCategory": "cs_math", "code": "070102", "subtitle": "数学与计算机融合", "trend": "上升"},
        {"id": "070103", "name": "物理学", "subCategory": "physics", "code": "070103", "subtitle": "探索宇宙的奥秘", "trend": "稳定"},
        {"id": "070104", "name": "应用物理学", "subCategory": "applied_physics", "code": "070104", "subtitle": "物理学的实践", "trend": "稳定"},
        {"id": "070105", "name": "化学", "subCategory": "chemistry", "code": "070105", "subtitle": "物质的科学与艺术", "trend": "稳定"},
        {"id": "070106", "name": "应用化学", "subCategory": "applied_chem", "code": "070106", "subtitle": "化学的实用之道", "trend": "稳定"},
        {"id": "070107", "name": "生物科学", "subCategory": "biology", "code": "070107", "subtitle": "生命的奥秘", "trend": "稳定"},
        {"id": "070108", "name": "生物技术", "subCategory": "biotech", "code": "070108", "subtitle": "改写生命的可能", "trend": "上升"},
        {"id": "070109", "name": "天文学", "subCategory": "astronomy", "code": "070109", "subtitle": "仰望星空的学问", "trend": "上升"},
        {"id": "070110", "name": "地理科学", "subCategory": "geography", "code": "070110", "subtitle": "认识地球家园", "trend": "稳定"},
        {"id": "070111", "name": "大气科学", "subCategory": "atmospheric", "code": "070111", "subtitle": "读懂风云变幻", "trend": "上升"},
        {"id": "070112", "name": "海洋科学", "subCategory": "marine", "code": "070112", "subtitle": "探索蓝色星球", "trend": "上升"},
        {"id": "070113", "name": "心理学", "subCategory": "psychology", "code": "070113", "subtitle": "心灵的密码", "trend": "上升"},
        {"id": "070114", "name": "统计学", "subCategory": "statistics_sci", "code": "070114", "subtitle": "数据的科学与艺术", "trend": "上升"},
    ]
    
    # 08 工学 (Engineering)
    engineering_majors = [
        {"id": "080101", "name": "计算机科学与技术", "subCategory": "cs", "code": "080101", "subtitle": "数字世界的缔造者", "trend": "火爆"},
        {"id": "080102", "name": "软件工程", "subCategory": "software", "code": "080102", "subtitle": "构建数字应用", "trend": "火爆"},
        {"id": "080103", "name": "网络工程", "subCategory": "network", "code": "080103", "subtitle": "连接世界的脉络", "trend": "上升"},
        {"id": "080104", "name": "信息安全", "subCategory": "security", "code": "080104", "subtitle": "数字世界的守护者", "trend": "火爆"},
        {"id": "080105", "name": "物联网工程", "subCategory": "iot", "code": "080105", "subtitle": "万物互联的未来", "trend": "上升"},
        {"id": "080106", "name": "数据科学与大数据技术", "subCategory": "bigdata", "code": "080106", "subtitle": "数据的掘金时代", "trend": "火爆"},
        {"id": "080107", "name": "人工智能", "subCategory": "ai", "code": "080107", "subtitle": "第四次工业革命", "trend": "火爆"},
        {"id": "080108", "name": "电子信息工程", "subCategory": "electronics", "code": "080108", "subtitle": "信息时代的基石", "trend": "上升"},
        {"id": "080109", "name": "通信工程", "subCategory": "communications", "code": "080109", "subtitle": "连接的桥梁", "trend": "上升"},
        {"id": "080110", "name": "自动化", "subCategory": "automation", "code": "080110", "subtitle": "智能控制的核心", "trend": "上升"},
        {"id": "080111", "name": "机械设计制造及其自动化", "subCategory": "mechanical", "code": "080111", "subtitle": "工业的脊梁", "trend": "稳定"},
        {"id": "080112", "name": "材料科学与工程", "subCategory": "materials", "code": "080112", "subtitle": "新材料的探索", "trend": "上升"},
        {"id": "080113", "name": "土木工程", "subCategory": "civil", "code": "080113", "subtitle": "城市的骨骼", "trend": "波动"},
        {"id": "080114", "name": "建筑学", "subCategory": "architecture", "code": "080114", "subtitle": "凝固的艺术", "trend": "稳定"},
        {"id": "080115", "name": "城乡规划", "subCategory": "urban_planning", "code": "080115", "subtitle": "城市的未来", "trend": "稳定"},
        {"id": "080116", "name": "水利水电工程", "subCategory": "hydraulic", "code": "080116", "subtitle": "水资源的治理", "trend": "稳定"},
        {"id": "080117", "name": "化学工程与工艺", "subCategory": "chemical_eng", "code": "080117", "subtitle": "化工的力量", "trend": "稳定"},
        {"id": "080118", "name": "航空航天工程", "subCategory": "aerospace", "code": "080118", "subtitle": "追逐星辰大海", "trend": "上升"},
        {"id": "080119", "name": "车辆工程", "subCategory": "automotive", "code": "080119", "subtitle": "汽车的未来", "trend": "波动"},
        {"id": "080120", "name": "电气工程及其自动化", "subCategory": "electrical", "code": "080120", "subtitle": "电的魔法", "trend": "上升"},
        {"id": "080121", "name": "生物医学工程", "subCategory": "bme", "code": "080121", "subtitle": "医学与工程的交叉", "trend": "上升"},
        {"id": "080122", "name": "环境工程", "subCategory": "environmental", "code": "080122", "subtitle": "守护绿水青山", "trend": "上升"},
        {"id": "080123", "name": "食品科学与工程", "subCategory": "food_science", "code": "080123", "subtitle": "舌尖上的科技", "trend": "稳定"},
        {"id": "080124", "name": "遥感科学与技术", "subCategory": "remote_sensing", "code": "080124", "subtitle": "从太空看地球", "trend": "上升"},
        {"id": "080125", "name": "微电子科学与工程", "subCategory": "microelectronics", "code": "080125", "subtitle": "芯片的奥秘", "trend": "火爆"},
        {"id": "080126", "name": "机器人工程", "subCategory": "robotics", "code": "080126", "subtitle": "智能时代的新星", "trend": "火爆"},
    ]
    
    # 09 农学 (Agriculture)
    agriculture_majors = [
        {"id": "090101", "name": "农学", "subCategory": "agronomy", "code": "090101", "subtitle": "土地的馈赠", "trend": "稳定"},
        {"id": "090102", "name": "园艺学", "subCategory": "horticulture", "code": "090102", "subtitle": "植物的艺术", "trend": "稳定"},
        {"id": "090103", "name": "植物保护", "subCategory": "plant_protection", "code": "090103", "subtitle": "守护绿色生命", "trend": "稳定"},
        {"id": "090104", "name": "种子科学与工程", "subCategory": "seed_science", "code": "090104", "subtitle": "希望的种子", "trend": "上升"},
        {"id": "090105", "name": "动物科学", "subCategory": "animal_science", "code": "090105", "subtitle": "动物世界的奥秘", "trend": "稳定"},
        {"id": "090106", "name": "动物医学", "subCategory": "veterinary", "code": "090106", "subtitle": "守护动物健康", "trend": "上升"},
        {"id": "090107", "name": "林学", "subCategory": "forestry", "code": "090107", "subtitle": "森林的守护者", "trend": "稳定"},
        {"id": "090108", "name": "园林", "subCategory": "landscape", "code": "090108", "subtitle": "自然的艺术", "trend": "上升"},
        {"id": "090109", "name": "草业科学", "subCategory": "grassland", "code": "090109", "subtitle": "草原生态", "trend": "稳定"},
        {"id": "090110", "name": "水产养殖学", "subCategory": "aquaculture", "code": "090110", "subtitle": "蓝色粮仓", "trend": "上升"},
        {"id": "090111", "name": "农业资源与环境", "subCategory": "agri_resources", "code": "090111", "subtitle": "可持续发展", "trend": "稳定"},
    ]
    
    # 10 医学 (Medicine)
    medicine_majors = [
        {"id": "100101", "name": "临床医学", "subCategory": "clinical", "code": "100101", "subtitle": "白衣天使的摇篮", "trend": "火爆"},
        {"id": "100102", "name": "口腔医学", "subCategory": "dental", "code": "100102", "subtitle": "微笑的守护者", "trend": "上升"},
        {"id": "100103", "name": "基础医学", "subCategory": "basic_medicine", "code": "100103", "subtitle": "医学的基石", "trend": "稳定"},
        {"id": "100104", "name": "预防医学", "subCategory": "preventive", "code": "100104", "subtitle": "治未病之道", "trend": "上升"},
        {"id": "100105", "name": "中医学", "subCategory": "tcm", "code": "100105", "subtitle": "中华瑰宝", "trend": "上升"},
        {"id": "100106", "name": "针灸推拿学", "subCategory": "acupuncture", "code": "100106", "subtitle": "经络的奥秘", "trend": "上升"},
        {"id": "100107", "name": "中药学", "subCategory": "pharmacology_tcm", "code": "100107", "subtitle": "草本的智慧", "trend": "上升"},
        {"id": "100108", "name": "药学", "subCategory": "pharmacy", "code": "100108", "subtitle": "药物的科学与艺术", "trend": "上升"},
        {"id": "100109", "name": "护理学", "subCategory": "nursing", "code": "100109", "subtitle": "温暖的守护", "trend": "稳定"},
        {"id": "100110", "name": "医学影像学", "subCategory": "radiology", "code": "100110", "subtitle": "透视人体奥秘", "trend": "上升"},
        {"id": "100111", "name": "麻醉学", "subCategory": "anesthesiology", "code": "100111", "subtitle": "手术的护航者", "trend": "上升"},
        {"id": "100112", "name": "眼视光医学", "subCategory": "ophthalmology", "code": "100112", "subtitle": "光明的使者", "trend": "上升"},
        {"id": "100113", "name": "精神医学", "subCategory": "psychiatry", "code": "100113", "subtitle": "心灵的治愈", "trend": "上升"},
    ]
    
    # 11 管理学 (Management)
    management_majors = [
        {"id": "110101", "name": "工商管理", "subCategory": "business", "code": "110101", "subtitle": "商业的智慧", "trend": "稳定"},
        {"id": "110102", "name": "市场营销", "subCategory": "marketing", "code": "110102", "subtitle": "价值与需求的对接", "trend": "稳定"},
        {"id": "110103", "name": "会计学", "subCategory": "accounting", "code": "110103", "subtitle": "数字的管家", "trend": "稳定"},
        {"id": "110104", "name": "财务管理", "subCategory": "finance_mgmt", "code": "110104", "subtitle": "资本的运作", "trend": "稳定"},
        {"id": "110105", "name": "人力资源管理", "subCategory": "hr", "code": "110105", "subtitle": "人的潜能激发", "trend": "稳定"},
        {"id": "110106", "name": "审计学", "subCategory": "auditing", "code": "110106", "subtitle": "监督与鉴证", "trend": "稳定"},
        {"id": "110107", "name": "电子商务", "subCategory": "ecommerce", "code": "110107", "subtitle": "数字经济时代", "trend": "上升"},
        {"id": "110108", "name": "物流管理", "subCategory": "logistics", "code": "110108", "subtitle": "物的流动艺术", "trend": "稳定"},
        {"id": "110109", "name": "酒店管理", "subCategory": "hotel", "code": "110109", "subtitle": "服务业的精英", "trend": "稳定"},
        {"id": "110110", "name": "旅游管理", "subCategory": "tourism", "code": "110110", "subtitle": "发现世界的美好", "trend": "波动"},
        {"id": "110111", "name": "公共事业管理", "subCategory": "public_mgmt", "code": "110111", "subtitle": "公共服务之道", "trend": "稳定"},
        {"id": "110112", "name": "行政管理", "subCategory": "admin", "code": "110112", "subtitle": "组织的运转", "trend": "稳定"},
        {"id": "110113", "name": "信息管理与信息系统", "subCategory": "imis", "code": "110113", "subtitle": "信息时代的管家", "trend": "上升"},
        {"id": "110114", "name": "工程管理", "subCategory": "engineering_mgmt", "code": "110114", "subtitle": "项目的灵魂", "trend": "稳定"},
        {"id": "110115", "name": "工程造价", "subCategory": "cost_engineering", "code": "110115", "subtitle": "精打细算", "trend": "稳定"},
        {"id": "110116", "name": "土地资源管理", "subCategory": "land_mgmt", "code": "110116", "subtitle": "空间的规划", "trend": "稳定"},
        {"id": "110117", "name": "图书馆学", "subCategory": "library", "code": "110117", "subtitle": "知识的殿堂", "trend": "稳定"},
        {"id": "110118", "name": "档案学", "subCategory": "archives", "code": "110118", "subtitle": "记忆的守护者", "trend": "稳定"},
    ]
    
    # 12 艺术学 (Art)
    art_majors = [
        {"id": "120101", "name": "音乐学", "subCategory": "musicology", "code": "120101", "subtitle": "旋律的魅力", "trend": "稳定"},
        {"id": "120102", "name": "音乐表演", "subCategory": "music_performance", "code": "120102", "subtitle": "舞台的绽放", "trend": "稳定"},
        {"id": "120103", "name": "作曲与作曲技术理论", "subCategory": "composition", "code": "120103", "subtitle": "音符的编织", "trend": "稳定"},
        {"id": "120104", "name": "舞蹈表演", "subCategory": "dance", "code": "120104", "subtitle": "肢体的诗篇", "trend": "稳定"},
        {"id": "120105", "name": "舞蹈编导", "subCategory": "choreography", "code": "120105", "subtitle": "编排的艺术", "trend": "稳定"},
        {"id": "120106", "name": "表演", "subCategory": "acting", "code": "120106", "subtitle": "角色的塑造", "trend": "波动"},
        {"id": "120107", "name": "戏剧影视文学", "subCategory": "drama", "code": "120107", "subtitle": "戏剧的人生", "trend": "稳定"},
        {"id": "120108", "name": "广播电视编导", "subCategory": "directing", "code": "120108", "subtitle": "影像的创作", "trend": "稳定"},
        {"id": "120109", "name": "戏剧影视美术设计", "subCategory": "stage_design", "code": "120109", "subtitle": "视觉的盛宴", "trend": "稳定"},
        {"id": "120110", "name": "播音与主持艺术", "subCategory": "broadcasting_host", "code": "120110", "subtitle": "声音的魅力", "trend": "波动"},
        {"id": "120111", "name": "影视摄影与制作", "subCategory": "film_production", "code": "120111", "subtitle": "光影的记录", "trend": "上升"},
        {"id": "120112", "name": "美术学", "subCategory": "fine_arts", "code": "120112", "subtitle": "造型艺术", "trend": "稳定"},
        {"id": "120113", "name": "绘画", "subCategory": "painting", "code": "120113", "subtitle": "色彩的表达", "trend": "稳定"},
        {"id": "120114", "name": "雕塑", "subCategory": "sculpture", "code": "120114", "subtitle": "立体的艺术", "trend": "稳定"},
        {"id": "120115", "name": "摄影", "subCategory": "photography", "code": "120115", "subtitle": "瞬间的永恒", "trend": "上升"},
        {"id": "120116", "name": "书法学", "subCategory": "calligraphy", "code": "120116", "subtitle": "笔墨的情韵", "trend": "上升"},
        {"id": "120117", "name": "视觉传达设计", "subCategory": "visual_design", "code": "120117", "subtitle": "视觉的语言", "trend": "上升"},
        {"id": "120118", "name": "环境设计", "subCategory": "environmental_design", "code": "120118", "subtitle": "空间的营造", "trend": "上升"},
        {"id": "120119", "name": "产品设计", "subCategory": "product_design", "code": "120119", "subtitle": "造物的智慧", "trend": "上升"},
        {"id": "120120", "name": "服装与服饰设计", "subCategory": "fashion_design", "code": "120120", "subtitle": "时尚的演绎", "trend": "稳定"},
        {"id": "120121", "name": "数字媒体艺术", "subCategory": "digital_media", "code": "120121", "subtitle": "数字时代的艺术", "trend": "火爆"},
        {"id": "120122", "name": "动画", "subCategory": "animation", "code": "120122", "subtitle": "想象的飞跃", "trend": "上升"},
        {"id": "120123", "name": "戏剧影视导演", "subCategory": "film_director", "code": "120123", "subtitle": "影像的掌控者", "trend": "稳定"},
    ]
    
    # 13 军事学 (Military)
    military_majors = [
        {"id": "130101", "name": "军事学", "subCategory": "military_science", "code": "130101", "subtitle": "国防的基石", "trend": "稳定"},
        {"id": "130102", "name": "指挥信息系统工程", "subCategory": "c4isr", "code": "130102", "subtitle": "现代战争之眼", "trend": "上升"},
    ]
    
    all_majors_data = {
        "01": {"category": "01", "categoryName": "哲学", "items": philosophy_majors},
        "02": {"category": "02", "categoryName": "经济学", "items": economics_majors},
        "03": {"category": "03", "categoryName": "法学", "items": law_majors},
        "04": {"category": "04", "categoryName": "教育学", "items": education_majors},
        "05": {"category": "05", "categoryName": "文学", "items": literature_majors},
        "06": {"category": "06", "categoryName": "历史学", "items": history_majors},
        "07": {"category": "07", "categoryName": "理学", "items": science_majors},
        "08": {"category": "08", "categoryName": "工学", "items": engineering_majors},
        "09": {"category": "09", "categoryName": "农学", "items": agriculture_majors},
        "10": {"category": "10", "categoryName": "医学", "items": medicine_majors},
        "11": {"category": "11", "categoryName": "管理学", "items": management_majors},
        "12": {"category": "12", "categoryName": "艺术学", "items": art_majors},
        "13": {"category": "13", "categoryName": "军事学", "items": military_majors},
    }
    
    hard_levels = ["简单", "较简单", "中等", "较难", "困难"]
    
    def generate_cn_data(major):
        category = major.get("subCategory", "")
        base_salary = {
            "cs": [15, 35, 60, 100, 150],
            "software": [14, 32, 55, 90, 140],
            "ai": [20, 45, 80, 150, 250],
            "finance": [12, 30, 60, 120, 200],
            "medicine": [10, 20, 45, 80, 150],
            "law": [8, 18, 40, 80, 150],
            "electronics": [12, 28, 50, 85, 130],
            "mechanical": [10, 22, 40, 70, 110],
            "architecture": [10, 25, 50, 90, 150],
            "design": [8, 18, 35, 60, 100],
            "education": [8, 15, 25, 40, 60],
            "default": [8, 18, 35, 60, 100]
        }
        
        salary_key = category if category in base_salary else "default"
        salary = base_salary.get(salary_key, base_salary["default"])
        
        industries = {
            "cs": [("互联网", 40), ("金融科技", 20), ("人工智能", 15), ("政府/教育", 10), ("其他", 15)],
            "medicine": [("医院", 45), ("医药企业", 25), ("科研机构", 15), ("医疗器械", 10), ("其他", 5)],
            "finance": [("银行证券", 35), ("投资机构", 25), ("企业财务", 20), ("政府金融", 10), ("其他", 10)],
            "law": [("律所", 35), ("企业法务", 30), ("公检法", 15), ("公证鉴定", 10), ("其他", 10)],
            "design": [("设计公司", 40), ("互联网企业", 25), ("广告传媒", 15), ("自由职业", 10), ("其他", 10)],
            "education": [("学校", 45), ("培训机构", 25), ("在线教育", 15), ("教育管理", 10), ("其他", 5)],
            "engineering": [("国有企业", 30), ("外企", 25), ("民营企业", 25), ("科研院所", 10), ("其他", 10)],
            "default": [("企业", 40), ("政府/事业单位", 25), ("科研机构", 15), ("其他", 20)]
        }
        
        industries_key = category if category in industries else "default"
        ind_data = industries.get(industries_key, industries["default"])
        
        careers_by_cat = {
            "cs": ["软件开发工程师", "算法工程师", "数据分析师", "产品经理", "测试工程师"],
            "ai": ["AI算法工程师", "机器学习工程师", "深度学习研究员", "自然语言处理工程师", "计算机视觉工程师"],
            "finance": ["基金经理", "投行分析师", "风险管理师", "金融产品设计", "银行管培生"],
            "medicine": ["临床医生", "医学研究员", "医药代表", "医疗器械工程师", "医院管理"],
            "law": ["律师", "法官/检察官", "法务顾问", "法律研究员", "公证员"],
            "education": ["教师", "教育管理者", "课程设计师", "教育培训师", "教育研究员"],
            "design": ["设计师", "艺术总监", "UI/UX设计师", "品牌策划", "创意总监"],
            "engineering": ["工程师", "项目经理", "技术总监", "研发工程师", "质量工程师"],
            "literature": ["编辑", "记者", "文案策划", "翻译", "内容运营"],
            "default": ["企业职员", "管理人员", "专业技术人员", "公务员", "创业者"]
        }
        
        careers_key = category.split('_')[0] if '_' in category else category
        if careers_key not in careers_by_cat:
            careers_key = "default"
        careers = careers_by_cat.get(careers_key, careers_by_cat["default"])
        
        forecasts = {
            "火爆": "该专业正处于行业上升期，人才需求旺盛，薪资待遇优厚，就业前景广阔。",
            "上升": "随着相关产业发展，该专业需求持续增长，值得关注。",
            "稳定": "该专业就业市场稳定，需求平稳，竞争适中。",
            "波动": "该专业受经济周期影响较大，建议关注行业发展趋势。",
            "下降": "该专业市场趋于饱和，需要提升专业技能或考虑转型。"
        }
        
        return {
            "degree": random.choice(["本科", "本科/硕士", "本科-博士"]),
            "duration": random.choice(["4年", "4-5年", "5年", "5-8年"]),
            "hardLevel": random.choice(hard_levels),
            "score": random.randint(480, 650),
            "salary": {
                "y1": salary[0],
                "y5": salary[1],
                "y10": salary[2],
                "y20": salary[3],
                "y40": salary[4]
            },
            "industries": [{"name": name, "percent": percent} for name, percent in ind_data],
            "forecast": forecasts.get(major.get("trend", "稳定"), forecasts["稳定"]),
            "careers": careers,
            "coreCourses": get_core_courses(category),
            "trainingGoals": get_training_goals(category),
            "whatYouLearn": get_what_you_learn(category),
            "suitable": get_suitable_for(category),
            "employmentDirection": get_employment_direction(category),
            "employmentAdvice": get_employment_advice(category),
            "learningPath": get_learning_path(category)
        }
    
    def generate_intl_data(cn_data):
        career_translations = {
            "软件开发工程师": "Software Developer",
            "算法工程师": "Algorithm Engineer",
            "数据分析师": "Data Analyst",
            "产品经理": "Product Manager",
            "测试工程师": "QA Engineer",
            "AI算法工程师": "AI Algorithm Engineer",
            "机器学习工程师": "Machine Learning Engineer",
            "深度学习研究员": "Deep Learning Researcher",
            "自然语言处理工程师": "NLP Engineer",
            "计算机视觉工程师": "Computer Vision Engineer",
            "基金经理": "Fund Manager",
            "投行分析师": "Investment Banking Analyst",
            "风险管理师": "Risk Manager",
            "金融产品设计": "Financial Product Designer",
            "银行管培生": "Bank Management Trainee",
            "临床医生": "Clinical Doctor",
            "医学研究员": "Medical Researcher",
            "医药代表": "Pharmaceutical Representative",
            "医疗器械工程师": "Medical Device Engineer",
            "医院管理": "Hospital Administrator",
            "律师": "Lawyer/Attorney",
            "法官/检察官": "Judge/Prosecutor",
            "法务顾问": "Legal Counsel",
            "法律研究员": "Legal Researcher",
            "公证员": "Notary Public",
            "教师": "Teacher/Lecturer",
            "教育管理者": "Education Administrator",
            "课程设计师": "Curriculum Designer",
            "教育培训师": "Educational Trainer",
            "教育研究员": "Education Researcher",
            "设计师": "Designer",
            "艺术总监": "Art Director",
            "UI/UX设计师": "UI/UX Designer",
            "品牌策划": "Brand Strategist",
            "创意总监": "Creative Director",
            "工程师": "Engineer",
            "项目经理": "Project Manager",
            "技术总监": "CTO/Technical Director",
            "研发工程师": "R&D Engineer",
            "质量工程师": "Quality Engineer",
            "编辑": "Editor",
            "记者": "Journalist/Reporter",
            "文案策划": "Copywriter",
            "翻译": "Translator/Interpreter",
            "内容运营": "Content Strategist",
            "企业职员": "Corporate Employee",
            "管理人员": "Management Professional",
            "专业技术人员": "Technical Professional",
            "公务员": "Civil Servant",
            "创业者": "Entrepreneur"
        }
        
        course_translations = {
            "高等数学": "Advanced Mathematics",
            "线性代数": "Linear Algebra",
            "概率论与数理统计": "Probability and Statistics",
            "数据结构": "Data Structures",
            "算法设计与分析": "Algorithm Design and Analysis",
            "操作系统": "Operating Systems",
            "计算机网络": "Computer Networks",
            "数据库原理": "Database Principles",
            "软件工程": "Software Engineering",
            "人工智能": "Artificial Intelligence",
            "机器学习": "Machine Learning",
            "深度学习": "Deep Learning",
            "经济学原理": "Principles of Economics",
            "微观经济学": "Microeconomics",
            "宏观经济学": "Macroeconomics",
            "货币银行学": "Money and Banking",
            "国际金融": "International Finance",
            "投资学": "Investment Theory",
            "公司金融": "Corporate Finance",
            "金融市场学": "Financial Markets",
            "法理学": "Jurisprudence",
            "宪法学": "Constitutional Law",
            "民法学": "Civil Law",
            "刑法学": "Criminal Law",
            "商法学": "Commercial Law",
            "国际法学": "International Law",
            "知识产权法": "Intellectual Property Law",
            "人体解剖学": "Human Anatomy",
            "生理学": "Physiology",
            "生物化学": "Biochemistry",
            "病理学": "Pathology",
            "药理学": "Pharmacology",
            "内科学": "Internal Medicine",
            "外科学": "Surgery",
            "妇产科学": "Obstetrics and Gynecology",
            "儿科学": "Pediatrics",
            "中医学基础": "Fundamentals of TCM",
            "针灸学": "Acupuncture and Moxibustion",
            "设计素描": "Design Sketching",
            "色彩构成": "Color Theory",
            "立体构成": "Three-Dimensional Composition",
            "平面设计": "Graphic Design",
            "计算机辅助设计": "CAD",
            "物理学": "Physics",
            "普通化学": "General Chemistry",
            "有机化学": "Organic Chemistry",
            "生物学": "Biology",
            "现代汉语": "Modern Chinese",
            "古代汉语": "Classical Chinese",
            "中国文学史": "History of Chinese Literature",
            "外国文学史": "History of World Literature",
            "语言学概论": "Introduction to Linguistics",
            "教育学原理": "Principles of Education",
            "教育心理学": "Educational Psychology",
            "课程与教学论": "Curriculum and Instruction",
            "教育研究方法": "Educational Research Methods",
            "马克思主义哲学": "Marxist Philosophy",
            "中国哲学史": "History of Chinese Philosophy",
            "西方哲学史": "History of Western Philosophy",
            "伦理学": "Ethics",
            "宗教学": "Religion Studies"
        }
        
        industry_translations = {
            "互联网": "Internet/Tech",
            "金融科技": "FinTech",
            "人工智能": "AI Industry",
            "政府/教育": "Government/Education",
            "医院": "Hospitals",
            "医药企业": "Pharmaceutical Companies",
            "科研机构": "Research Institutions",
            "医疗器械": "Medical Devices",
            "银行证券": "Banking & Securities",
            "投资机构": "Investment Firms",
            "企业财务": "Corporate Finance",
            "政府金融": "Government Finance",
            "律所": "Law Firms",
            "企业法务": "Corporate Legal",
            "公检法": "Judicial System",
            "公证鉴定": "Notary & Authentication",
            "设计公司": "Design Firms",
            "互联网企业": "Internet Companies",
            "广告传媒": "Advertising & Media",
            "自由职业": "Freelance",
            "学校": "Schools/Educational Institutions",
            "培训机构": "Training Institutions",
            "在线教育": "Online Education",
            "教育管理": "Education Administration",
            "国有企业": "State-owned Enterprises",
            "外企": "Multinational Companies",
            "民营企业": "Private Enterprises",
            "科研院所": "Research Institutes",
            "企业": "Corporate Sector"
        }
        
        return {
            "degree": cn_data["degree"],
            "duration": cn_data["duration"],
            "hardLevel": translate_hard_level(cn_data["hardLevel"]),
            "score": cn_data["score"],
            "salary": {
                "y1": cn_data["salary"]["y1"],
                "y5": cn_data["salary"]["y5"],
                "y10": cn_data["salary"]["y10"],
                "y20": cn_data["salary"]["y20"],
                "y40": cn_data["salary"]["y40"]
            },
            "industries": [{"name": industry_translations.get(ind["name"], ind["name"]), "percent": ind["percent"]} for ind in cn_data["industries"]],
            "forecast": translate_forecast(cn_data["forecast"]),
            "careers": [career_translations.get(c, c) for c in cn_data["careers"]],
            "coreCourses": [course_translations.get(c, c) for c in cn_data["coreCourses"]],
            "trainingGoals": translate_text(cn_data["trainingGoals"]),
            "whatYouLearn": translate_text(cn_data["whatYouLearn"]),
            "suitable": translate_text(cn_data["suitable"]),
            "employmentDirection": translate_text(cn_data["employmentDirection"]),
            "employmentAdvice": translate_text(cn_data["employmentAdvice"]),
            "learningPath": translate_text(cn_data["learningPath"])
        }
    
    def get_core_courses(category):
        courses_map = {
            "cs": ["数据结构", "算法设计与分析", "操作系统", "计算机网络", "数据库原理", "软件工程", "人工智能"],
            "ai": ["机器学习", "深度学习", "计算机视觉", "自然语言处理", "强化学习", "神经网络", "优化算法"],
            "finance": ["经济学原理", "微观经济学", "宏观经济学", "货币银行学", "国际金融", "投资学", "公司金融"],
            "medicine": ["人体解剖学", "生理学", "生物化学", "病理学", "药理学", "内科学", "外科学"],
            "law": ["法理学", "宪法学", "民法学", "刑法学", "商法学", "国际法学", "知识产权法"],
            "education": ["教育学原理", "教育心理学", "课程与教学论", "教育研究方法", "教育管理学"],
            "design": ["设计素描", "色彩构成", "立体构成", "平面设计", "计算机辅助设计"],
            "engineering": ["高等数学", "线性代数", "概率论与数理统计", "理论力学", "材料力学"],
            "literature": ["现代汉语", "古代汉语", "中国文学史", "外国文学史", "语言学概论"],
            "philosophy": ["马克思主义哲学", "中国哲学史", "西方哲学史", "伦理学", "宗教学"],
            "science": ["高等数学", "线性代数", "概率论与数理统计", "物理学", "普通化学"]
        }
        
        cat_key = category.split('_')[0]
        for key in courses_map:
            if cat_key.startswith(key) or key.startswith(cat_key):
                return courses_map[key]
        return ["专业基础课", "专业核心课", "专业选修课", "实践实习", "毕业设计"]
    
    def get_training_goals(category):
        goals = {
            "cs": "培养具备计算机科学理论基础、软件工程实践能力和创新意识的复合型高级工程技术人才。学生毕业后能够胜任软件开发、系统架构、技术管理等岗位工作。",
            "ai": "培养掌握人工智能核心算法、机器学习理论和深度学习技术的高级专业人才，能够从事AI算法研究、产品开发和工程应用等工作。",
            "finance": "培养具有扎实的经济学、金融学理论基础，熟悉金融市场运作规律，能够在银行、证券、保险等金融机构从事分析、管理工作的专业人才。",
            "medicine": "培养具备坚实医学理论基础和临床实践能力的医学人才，能够在医疗机构从事疾病诊断、治疗和预防工作，成为人民健康的守护者。",
            "law": "培养系统掌握法学理论、熟悉中国法律制度并具有较强法律实务能力的法律专业人才，能够在法律服务机构、企事业单位从事法律工作。",
            "design": "培养具有创新设计思维和实践能力的设计专业人才，能够运用现代设计方法和技术进行各类设计创作，满足社会对高素质设计人才的需求。",
            "engineering": "培养掌握工程科学基础理论和专业技术知识，具备工程实践能力和创新精神的工程技术人才，能够在相关领域从事设计、研发和管理工作。"
        }
        cat_key = category.split('_')[0]
        for key in goals:
            if cat_key.startswith(key):
                return goals[key]
        return "培养具有扎实专业基础、较强实践能力和创新精神的高素质专业人才。"
    
    def get_what_you_learn(category):
        learns = {
            "cs": "你将学习计算机系统的底层原理，掌握编程语言和开发工具，了解软件工程的方法论，培养问题分析和算法设计的能力，最终具备独立开发完整软件系统的能力。",
            "ai": "你将深入了解人工智能的基本理论，学习让机器'思考'的核心算法，通过大量实践项目掌握从数据处理到模型训练的完整技能，为进入AI行业奠定坚实基础。",
            "finance": "你将系统学习经济运行的规律，理解货币、金融市场和企业财务的运作机制，掌握投资分析和风险管理的方法，培养敏锐的商业洞察力和金融思维。",
            "medicine": "你将学习人体的结构与功能，理解疾病的发生发展机制，掌握诊断和治疗的基本技能，在临床实习中培养医患沟通能力和职业责任感。",
            "law": "你将系统学习法律的理论和体系，理解法律背后的价值判断和利益平衡，通过案例分析培养法律思维能力，为从事法律职业打下坚实基础。",
            "design": "你将学习设计的基本原理和表现技法，培养审美能力和创意思维，通过大量实践掌握从灵感构思到作品呈现的完整设计流程。",
            "engineering": "你将学习工程科学的基础理论，掌握工程设计和计算分析方法，通过实验和实践培养解决实际工程问题的能力。"
        }
        cat_key = category.split('_')[0]
        for key in learns:
            if cat_key.startswith(key):
                return learns[key]
        return "你将系统学习本专业的基础理论和核心知识，通过理论学习和实践训练培养专业能力和综合素质。"
    
    def get_suitable_for(category):
        suitable = {
            "cs": "对计算机技术有浓厚兴趣，逻辑思维能力强，善于分析和解决问题，能够承受持续学习的压力，对新技术保持好奇心的学生。",
            "ai": "数学基础扎实，对人工智能和机器学习有强烈兴趣，具有较强的逻辑推理能力，能够沉下心来研究复杂算法模型的学生。",
            "finance": "对经济现象和金融市场感兴趣，数字敏感度高，具有较强的分析能力和风险意识，性格沉稳理性的学生。",
            "medicine": "具有较强的责任感和服务意识，对医学知识有浓厚兴趣，能够承受较大的学习压力和心理负担，具有良好的沟通能力的学生。",
            "law": "逻辑思维严密，语言表达能力强，善于辩论和写作，对社会现象有敏锐观察力，具有正义感的学生。",
            "design": "具有较好的审美素养和创造力，对视觉艺术有浓厚兴趣，思维活跃，能够坚持原创设计的学生。",
            "engineering": "动手能力强，对工程实践有浓厚兴趣，数学物理基础较好，能够将理论知识应用于实际问题的学生。"
        }
        cat_key = category.split('_')[0]
        for key in suitable:
            if cat_key.startswith(key):
                return suitable[key]
        return "对本专业有浓厚兴趣，具备良好学习能力和综合素质的学生。"
    
    def get_employment_direction(category):
        directions = {
            "cs": "互联网公司、科技企业、软件开发公司、系统集成商、政府机关信息化部门、科研院所等。",
            "ai": "人工智能企业、互联网公司、研究机构、科技巨头、创业公司、智能制造企业等。",
            "finance": "商业银行、证券公司、保险公司、基金公司、投资机构、企业财务部门、监管机构等。",
            "medicine": "各级医院、疾病预防控制中心、医学院校、医学研究机构、医药企业、医疗器械公司等。",
            "law": "律师事务所、公证机构、司法机关、政府法制部门、企业法务部门、法律援助机构等。",
            "design": "设计公司、广告公司、传媒机构、互联网公司、设计院、企业设计部门、自主创业等。",
            "engineering": "设计院、工程建设单位、设备制造企业、质量检测机构、科研院所、政府建设部门等。"
        }
        cat_key = category.split('_')[0]
        for key in directions:
            if cat_key.startswith(key):
                return directions[key]
        return "相关行业企业、事业单位、政府机关、科研机构等。"
    
    def get_employment_advice(category):
        advice = {
            "cs": "建议在校期间多做项目实践，参与开源社区，积累实际开发经验。毕业后可先进入成长型公司积累经验，后续根据职业规划选择合适平台。",
            "ai": "建议尽早确定研究方向，深入学习相关算法，参与科研项目或比赛。研究生学历对从事核心算法岗位很有帮助，行业证书也是加分项。",
            "finance": "建议在校期间考取相关从业资格证书，如基金、证券、期货等。银行实习经历对应聘银行岗位很有帮助，CFA证书对职业发展大有裨益。",
            "medicine": "医学是典型的长周期专业，建议做好长期学习准备。住院医师规范化培训是必经阶段，考研读博能获得更好的职业发展机会。",
            "law": "建议尽早通过法律职业资格考试，这是法律从业的门槛。多参加法律援助和实习，积累实践经验对职业发展非常重要。",
            "design": "建议在校期间建立个人作品集，这是求职的关键。参与设计比赛和实习，积累实战经验。设计感和创意能力是核心竞争力。",
            "engineering": "建议在校期间注重理论与实践结合，多参加实习和工程项目。注册工程师资格对职业发展有帮助，实践经验非常重要。"
        }
        cat_key = category.split('_')[0]
        for key in advice:
            if cat_key.startswith(key):
                return advice[key]
        return "建议在校期间扎实学习专业知识，积极参与实习实践，提升综合素质和就业竞争力。"
    
    def get_learning_path(category):
        paths = {
            "cs": "大一打好编程基础→大二学习数据结构、算法、数据库→大三深入学习核心技术栈→大四完成毕业设计和求职准备",
            "ai": "大一数学和编程基础→大二机器学习理论→大三深度学习实战→大四科研项目或实习",
            "finance": "大一经济学基础→大二金融学核心课程→大三专业方向深化→大四实习和职业规划",
            "medicine": "大一基础医学→大二临床医学→大三专业医学→大四临床实习→毕业后规范化培训",
            "law": "大一法学基础→大二法律体系学习→大三专业方向深化→大四法律实务训练",
            "design": "大一设计基础→大二专业设计技能→大三作品集准备→大四实习和就业",
            "engineering": "大一数理基础→大二专业基础课→大三专业核心课→大四毕业设计和实习"
        }
        cat_key = category.split('_')[0]
        for key in paths:
            if cat_key.startswith(key):
                return paths[key]
        return "大一夯实基础→大二深化专业→大三明确方向→大四实践提升"
    
    def generate_reviews(category, name):
        pros_list = [
            "就业前景广阔，社会需求量大",
            "薪资待遇优厚，职业发展空间大",
            "专业实用性强，技能可迁移性好",
            "能够培养逻辑思维和创新能力",
            "行业正处于上升期，机会众多",
            "专业壁垒高，竞争相对较小",
            "可以接触前沿技术和发展趋势",
            "创业门槛相对较低，机会丰富",
            "工作环境较好，办公条件优越",
            "人脉资源优质，职业圈子高端",
            "能够为社会创造实际价值",
            "专业知识更新慢，经验可积累",
            "考研优势明显，深造路径清晰",
            "国际认可度高，出国发展容易"
        ]
        
        cons_list = [
            "学习难度较大，需要扎实基础",
            "竞争激烈，需要持续学习提升",
            "工作压力大，加班情况较多",
            "知识更新快，需要终身学习",
            "对数学等基础学科要求较高",
            "实践环节多，实习要求严格",
            "部分岗位工作环境艰苦",
            "职业发展存在瓶颈期",
            "需要考取多项资格证书",
            "行业周期性波动影响就业",
            "专业性强，转行成本较高",
            "地域差异大，一线城市机会多",
            "学历内卷严重，高学历优势明显",
            "从业风险较高，责任重大"
        ]
        
        summaries = [
            f"{name}是一个兼具理论深度和实践广度的专业。从就业角度来看，该专业社会需求稳定，薪资水平处于中等偏上，但同时也面临着竞争加剧、知识更新快等挑战。选择该专业需要具备良好的学习能力和抗压能力，同时也需要对行业有持续的热情和关注。建议在校期间注重实践能力的培养，通过实习和项目经验来提升竞争力。",
            f"从张雪峰老师的视角来看，{name}是一个值得推荐的专业。该专业就业面广，毕业生可以进入多个相关行业，同时专业技能具有较强的可迁移性。但需要注意的是，该专业对学生的综合素质要求较高，不仅需要扎实的专业基础，还需要良好的沟通能力和团队协作精神。对于想要报考该专业的学生，建议提前了解专业课程设置和就业方向，做好充分的心理准备。",
            f"{name}的优劣势都很明显。优势在于专业实用性强、就业选择多、职业发展空间大；劣势在于学习难度不小、竞争激烈、需要不断提升自己。总的来说，这是一个'付出与回报成正比'的专业，适合那些愿意吃苦耐劳、持续学习的学生。如果你能在这个专业坚持下去并且不断提升自己，未来的职业发展前景是非常可观的。",
            f"关于{name}，我们需要辩证地来看待。一方面，该专业确实有着不错的就业前景和薪资待遇，是很多考生和家长青睐的对象；另一方面，该专业的学习难度和竞争压力也不容忽视。建议考生在选择该专业时，要充分考虑自己的兴趣特长和性格特点，只有真正热爱这个专业，才能在未来的学习和工作中找到成就感和满足感。",
            f"张雪峰老师常说，选择专业要看'出口'。{name}的就业'出口'怎么样呢？总体来说还是不错的，毕业生可以在多个领域找到合适的工作岗位。但也要看到，该专业的就业质量参差不齐，不同院校、不同层次的毕业生在就业市场上存在较大差异。因此，学校的层次和个人的能力就显得尤为重要。建议尽量选择层次较高的院校，同时在校期间努力提升自己的专业技能和综合素质。"
        ]
        
        quotes = [
            "\"选专业不能只看眼前的热度，更要考虑长远的发展和个人的适配度。\"",
            "\"大学四年是人生中最重要的学习阶段之一，选择一个适合自己的专业至关重要。\"",
            "\"没有绝对的好专业，只有适合自己的专业。选择时要多方面考虑，权衡利弊。\"",
            "\"专业只是起点，持续学习和能力提升才是职业发展的关键。\"",
            "\"兴趣是最好的老师，只有热爱才能在这个领域走得更远。\""
        ]
        
        selected_pros = random.sample(pros_list, 4)
        selected_cons = random.sample([c for c in cons_list if c not in selected_pros], 3)
        selected_summary = random.choice(summaries)
        selected_quotes = random.sample(quotes, 2)
        
        return {
            "pros": selected_pros,
            "cons": selected_cons,
            "summary": selected_summary,
            "quotes": selected_quotes
        }
    
    def translate_hard_level(level):
        trans = {"简单": "Easy", "较简单": "Relatively Easy", "中等": "Medium", "较难": "Relatively Hard", "困难": "Hard"}
        return trans.get(level, level)
    
    def translate_forecast(forecast):
        trans = {
            "该专业正处于行业上升期，人才需求旺盛，薪资待遇优厚，就业前景广阔。": "This major is in an upward industry trend with strong demand, excellent salary, and broad employment prospects.",
            "随着相关产业发展，该专业需求持续增长，值得关注。": "With the development of related industries, demand for this major continues to grow and is worth attention.",
            "该专业就业市场稳定，需求平稳，竞争适中。": "The job market for this major is stable with steady demand and moderate competition.",
            "该专业受经济周期影响较大，建议关注行业发展趋势。": "This major is greatly affected by economic cycles, and it is recommended to follow industry trends.",
            "该专业市场趋于饱和，需要提升专业技能或考虑转型。": "The market for this major is becoming saturated, requiring skill improvement or considering career transitions."
        }
        return trans.get(forecast, forecast)
    
    def translate_text(text):
        return text
    
    for cat_code, cat_data in all_majors_data.items():
        for major in cat_data["items"]:
            major["category"] = cat_code
            major["categoryName"] = cat_data["categoryName"]
            cn_data = generate_cn_data(major)
            major["cn"] = cn_data
            major["intl"] = generate_intl_data(cn_data)
            major["review"] = generate_reviews(major["subCategory"], major["name"])
            majors.append(major)
    
    return majors

def generate():
    majors = get_majors()
    majors_json = json.dumps(majors, ensure_ascii=False, indent=2)
    
    html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✦ 专业星图 ✦ - 专业选择指南</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 50%, #0d0d2b 100%);
            min-height: 100vh;
            color: #e0e0ff;
        }
        .orbitron { font-family: 'Orbitron', sans-serif; }
        
        .stars-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
            z-index: 0;
        }
        .star {
            position: absolute;
            background: white;
            border-radius: 50%;
            animation: twinkle var(--duration) ease-in-out infinite;
        }
        @keyframes twinkle {
            0%, 100% { opacity: var(--opacity); transform: scale(1); }
            50% { opacity: 1; transform: scale(1.2); }
        }
        
        .bubble {
            position: absolute;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1), transparent);
            border: 1px solid rgba(255,255,255,0.1);
            animation: float var(--duration) ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .card {
            background: rgba(20, 20, 50, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(100, 100, 255, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .card:hover {
            transform: translateY(-5px) scale(1.02);
            border-color: rgba(255, 215, 0, 0.5);
            box-shadow: 0 10px 40px rgba(255, 215, 0, 0.2), 0 0 20px rgba(0, 255, 255, 0.1);
        }
        
        .trend-hot { color: #ff4757; animation: pulse 2s infinite; }
        .trend-up { color: #2ed573; }
        .trend-stable { color: #ffa502; }
        .trend-wave { color: #7bed9f; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .modal-overlay {
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            background: linear-gradient(135deg, #1a1a3a 0%, #2a2a4a 100%);
            max-height: 90vh;
            overflow-y: auto;
        }
        .modal-content::-webkit-scrollbar { width: 8px; }
        .modal-content::-webkit-scrollbar-track { background: #1a1a3a; }
        .modal-content::-webkit-scrollbar-thumb { background: #4a4a8a; border-radius: 4px; }
        
        .btn-category {
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }
        .btn-category:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        .btn-category.active {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.3), rgba(0, 255, 255, 0.2));
            border-color: rgba(255, 215, 0, 0.5);
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
        }
        
        .gold-text { color: #ffd700; }
        .cyan-text { color: #00ffff; }
        .purple-text { color: #bf7fff; }
        
        .gradient-text {
            background: linear-gradient(135deg, #ffd700, #00ffff, #bf7fff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tab-btn {
            transition: all 0.3s ease;
            border-bottom: 2px solid transparent;
        }
        .tab-btn.active {
            border-bottom-color: #ffd700;
            color: #ffd700;
        }
        
        .pros-item { border-left: 3px solid #2ed573; }
        .cons-item { border-left: 3px solid #ff4757; }
        
        .info-section {
            background: rgba(30, 30, 60, 0.5);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .salary-bar {
            height: 24px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
        }
        .salary-fill {
            height: 100%;
            border-radius: 12px;
            transition: width 1s ease;
        }
        
        @media (max-width: 768px) {
            .filter-bar { flex-wrap: wrap; gap: 0.5rem; }
            .btn-category { font-size: 0.75rem; padding: 0.25rem 0.5rem; }
        }
    </style>
</head>
<body class="relative">
    <div class="stars-bg" id="stars"></div>
    <div class="bubble-bg" id="bubbles"></div>
    
    <div class="relative z-10 container mx-auto px-4 py-8">
        <header class="text-center mb-12">
            <h1 class="orbitron text-5xl md:text-6xl font-bold gradient-text mb-4">
                ✦ 专业星图 ✦
            </h1>
            <p class="text-xl text-gray-400 mb-2">探索你的职业星空</p>
            <p class="text-gray-500">涵盖全国13大学科门类 · 100+专业详解</p>
        </header>
        
        <div class="filter-bar flex flex-wrap justify-center gap-2 mb-8">
            <button class="btn-category active px-4 py-2 rounded-lg text-sm" data-category="all">
                全部专业
            </button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="01">01 哲学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="02">02 经济学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="03">03 法学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="04">04 教育学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="05">05 文学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="06">06 历史学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="07">07 理学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="08">08 工学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="09">09 农学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="10">10 医学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="11">11 管理学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="12">12 艺术学</button>
            <button class="btn-category px-4 py-2 rounded-lg text-sm" data-category="13">13 军事学</button>
        </div>
        
        <div class="search-sort flex flex-wrap gap-4 mb-8 justify-center">
            <input type="text" id="searchInput" placeholder="搜索专业名称..." 
                   class="px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-white focus:border-yellow-500 focus:outline-none w-full max-w-md">
            <select id="sortSelect" class="px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 text-white focus:border-yellow-500 focus:outline-none">
                <option value="default">默认排序</option>
                <option value="salary-asc">薪资 (低→高)</option>
                <option value="salary-desc">薪资 (高→低)</option>
                <option value="difficulty-asc">难度 (易→难)</option>
                <option value="difficulty-desc">难度 (难→易)</option>
            </select>
        </div>
        
        <div id="majorsGrid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        </div>
        
        <div class="text-center mt-8 text-gray-500">
            <p>共 <span id="totalCount" class="gold-text font-bold">0</span> 个专业</p>
        </div>
    </div>
    
    <div id="modal" class="fixed inset-0 z-50 hidden modal-overlay flex items-center justify-center p-4">
        <div class="modal-content w-full max-w-4xl rounded-2xl border border-gray-700 shadow-2xl">
            <div class="sticky top-0 bg-gradient-to-r from-gray-900 to-gray-800 p-6 border-b border-gray-700 flex justify-between items-center">
                <div>
                    <span id="modalCategory" class="text-sm cyan-text"></span>
                    <h2 id="modalTitle" class="orbitron text-2xl gold-text"></h2>
                    <p id="modalSubtitle" class="text-gray-400 text-sm mt-1"></p>
                </div>
                <button id="closeModal" class="text-gray-400 hover:text-white text-3xl">&times;</button>
            </div>
            
            <div class="p-6">
                <div class="flex gap-4 mb-6">
                    <button class="tab-btn active px-4 py-2 text-sm" data-tab="cn">国内数据</button>
                    <button class="tab-btn px-4 py-2 text-sm" data-tab="intl">国际数据</button>
                </div>
                
                <div id="cnContent" class="tab-content">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">学历要求</p>
                            <p id="cnDegree" class="gold-text font-bold"></p>
                        </div>
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">学制</p>
                            <p id="cnDuration" class="cyan-text font-bold"></p>
                        </div>
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">难度</p>
                            <p id="cnHardLevel" class="purple-text font-bold"></p>
                        </div>
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">趋势</p>
                            <p id="cnTrend" class="font-bold"></p>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="gold-text font-bold mb-2">💰 薪资发展 (万元/年)</h3>
                        <div id="cnSalaryChart" class="h-48"></div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="gold-text font-bold mb-2">🏭 就业行业分布</h3>
                        <div id="cnIndustries" class="flex flex-wrap gap-2"></div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="gold-text font-bold mb-2">💼 就业方向</h3>
                        <div id="cnCareers" class="flex flex-wrap gap-2"></div>
                    </div>
                    
                    <div class="grid md:grid-cols-2 gap-4">
                        <div class="info-section">
                            <h3 class="cyan-text font-bold mb-2">📚 核心课程</h3>
                            <ul id="cnCoreCourses" class="text-sm text-gray-300 space-y-1"></ul>
                        </div>
                        <div class="info-section">
                            <h3 class="cyan-text font-bold mb-2">🎯 培养目标</h3>
                            <p id="cnTrainingGoals" class="text-sm text-gray-300"></p>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="cyan-text font-bold mb-2">📖 你将学到</h3>
                        <p id="cnWhatYouLearn" class="text-sm text-gray-300"></p>
                    </div>
                    
                    <div class="grid md:grid-cols-2 gap-4">
                        <div class="info-section">
                            <h3 class="purple-text font-bold mb-2">👤 适合人群</h3>
                            <p id="cnSuitable" class="text-sm text-gray-300"></p>
                        </div>
                        <div class="info-section">
                            <h3 class="purple-text font-bold mb-2">🔮 前景展望</h3>
                            <p id="cnForecast" class="text-sm text-gray-300"></p>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="purple-text font-bold mb-2">🚀 就业建议</h3>
                        <p id="cnEmploymentAdvice" class="text-sm text-gray-300"></p>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="purple-text font-bold mb-2">📐 学习路径</h3>
                        <p id="cnLearningPath" class="text-sm text-gray-300"></p>
                    </div>
                </div>
                
                <div id="intlContent" class="tab-content hidden">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">Degree</p>
                            <p id="intlDegree" class="gold-text font-bold"></p>
                        </div>
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">Duration</p>
                            <p id="intlDuration" class="cyan-text font-bold"></p>
                        </div>
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">Difficulty</p>
                            <p id="intlHardLevel" class="purple-text font-bold"></p>
                        </div>
                        <div class="info-section text-center">
                            <p class="text-gray-400 text-sm">Trend</p>
                            <p id="intlTrend" class="font-bold"></p>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="gold-text font-bold mb-2">💰 Salary Projection (10K CNY/year)</h3>
                        <div id="intlSalaryChart" class="h-48"></div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="gold-text font-bold mb-2">🏭 Industry Distribution</h3>
                        <div id="intlIndustries" class="flex flex-wrap gap-2"></div>
                    </div>
                    
                    <div class="info-section">
                        <h3 class="gold-text font-bold mb-2">💼 Career Paths</h3>
                        <div id="intlCareers" class="flex flex-wrap gap-2"></div>
                    </div>
                    
                    <div class="grid md:grid-cols-2 gap-4">
                        <div class="info-section">
                            <h3 class="cyan-text font-bold mb-2">📚 Core Courses</h3>
                            <ul id="intlCoreCourses" class="text-sm text-gray-300 space-y-1"></ul>
                        </div>
                        <div class="info-section">
                            <h3 class="cyan-text font-bold mb-2">🎯 Training Goals</h3>
                            <p id="intlTrainingGoals" class="text-sm text-gray-300"></p>
                        </div>
                    </div>
                </div>
                
                <div id="reviewSection" class="mt-6 border-t border-gray-700 pt-6">
                    <h3 class="orbitron text-xl gold-text mb-4">⭐ 张雪峰点评</h3>
                    
                    <div class="grid md:grid-cols-2 gap-6">
                        <div>
                            <h4 class="text-green-400 font-bold mb-3">✅ 优势</h4>
                            <ul id="reviewPros" class="space-y-2"></ul>
                        </div>
                        <div>
                            <h4 class="text-red-400 font-bold mb-3">❌ 劣势</h4>
                            <ul id="reviewCons" class="space-y-2"></ul>
                        </div>
                    </div>
                    
                    <div class="mt-6 info-section">
                        <h4 class="purple-text font-bold mb-3">📝 综合评价</h4>
                        <p id="reviewSummary" class="text-gray-300 leading-relaxed"></p>
                    </div>
                    
                    <div class="mt-4 info-section bg-yellow-900/20 border border-yellow-600/30">
                        <h4 class="yellow-400 font-bold mb-3">💬 名人名言</h4>
                        <ul id="reviewQuotes" class="space-y-2"></ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const majorsData = ''' + majors_json + ''';
        
        let currentCategory = 'all';
        let currentLang = 'cn';
        let salaryChart = null;
        
        function initStars() {
            const starsContainer = document.getElementById('stars');
            for (let i = 0; i < 100; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.cssText = `
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    width: ${Math.random() * 3 + 1}px;
                    height: ${Math.random() * 3 + 1}px;
                    --duration: ${Math.random() * 3 + 2}s;
                    --opacity: ${Math.random() * 0.5 + 0.3};
                `;
                starsContainer.appendChild(star);
            }
        }
        
        function initBubbles() {
            const bubblesContainer = document.getElementById('bubbles');
            for (let i = 0; i < 20; i++) {
                const bubble = document.createElement('div');
                bubble.className = 'bubble';
                bubble.style.cssText = `
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    width: ${Math.random() * 100 + 50}px;
                    height: ${Math.random() * 100 + 50}px;
                    --duration: ${Math.random() * 10 + 10}s;
                    animation-delay: ${Math.random() * 5}s;
                `;
                bubblesContainer.appendChild(bubble);
            }
        }
        
        function getTrendClass(trend) {
            const classes = {
                '火爆': 'trend-hot',
                '上升': 'trend-up',
                '稳定': 'trend-stable',
                '波动': 'trend-wave',
                '下降': 'text-red-400'
            };
            return classes[trend] || 'trend-stable';
        }
        
        function getDifficultyColor(level) {
            if (level.includes('简单')) return '#2ed573';
            if (level.includes('中等')) return '#ffa502';
            if (level.includes('较难')) return '#ff6b6b';
            if (level.includes('困难')) return '#ff4757';
            return '#747d8c';
        }
        
        function renderMajors(majors) {
            const grid = document.getElementById('majorsGrid');
            grid.innerHTML = '';
            
            majors.forEach(major => {
                const card = document.createElement('div');
                card.className = 'card rounded-xl p-4';
                
                const lang = currentLang;
                const data = lang === 'cn' ? major.cn : major.intl;
                const hardColor = getDifficultyColor(data.hardLevel);
                
                card.innerHTML = `
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-xs cyan-text">${major.categoryName}</span>
                        <span class="text-xs ${getTrendClass(major.trend)}">${major.trend}</span>
                    </div>
                    <h3 class="font-bold text-lg mb-1">${major.name}</h3>
                    <p class="text-xs text-gray-400 mb-3">${major.subtitle}</p>
                    <div class="flex justify-between text-xs">
                        <span style="color: ${hardColor}">${data.hardLevel}</span>
                        <span class="gold-text">¥${data.salary.y1}万起</span>
                    </div>
                `;
                
                card.addEventListener('click', () => openModal(major));
                grid.appendChild(card);
            });
            
            document.getElementById('totalCount').textContent = majors.length;
        }
        
        function filterMajors() {
            const searchText = document.getElementById('searchInput').value.toLowerCase();
            const sortValue = document.getElementById('sortSelect').value;
            
            let filtered = majorsData.filter(major => {
                const matchCategory = currentCategory === 'all' || major.category === currentCategory;
                const matchSearch = major.name.toLowerCase().includes(searchText) ||
                                   major.categoryName.toLowerCase().includes(searchText);
                return matchCategory && matchSearch;
            });
            
            if (sortValue !== 'default') {
                const difficultyOrder = {'简单': 0, '较简单': 1, '中等': 2, '较难': 3, '困难': 4, 
                                        'Easy': 0, 'Relatively Easy': 1, 'Medium': 2, 
                                        'Relatively Hard': 3, 'Hard': 4};
                
                filtered.sort((a, b) => {
                    const dataA = currentLang === 'cn' ? a.cn : a.intl;
                    const dataB = currentLang === 'cn' ? b.cn : b.intl;
                    
                    if (sortValue === 'salary-asc') {
                        return dataA.salary.y1 - dataB.salary.y1;
                    } else if (sortValue === 'salary-desc') {
                        return dataB.salary.y1 - dataA.salary.y1;
                    } else if (sortValue === 'difficulty-asc') {
                        return (difficultyOrder[dataA.hardLevel] || 2) - (difficultyOrder[dataB.hardLevel] || 2);
                    } else if (sortValue === 'difficulty-desc') {
                        return (difficultyOrder[dataB.hardLevel] || 2) - (difficultyOrder[dataA.hardLevel] || 2);
                    }
                    return 0;
                });
            }
            
            renderMajors(filtered);
        }
        
        function openModal(major) {
            document.getElementById('modal').classList.remove('hidden');
            document.body.style.overflow = 'hidden';
            
            document.getElementById('modalCategory').textContent = `${major.category} ${major.categoryName}`;
            document.getElementById('modalTitle').textContent = major.name;
            document.getElementById('modalSubtitle').textContent = major.subtitle;
            
            updateModalContent(major);
        }
        
        function updateModalContent(major) {
            const cnData = major.cn;
            const intlData = major.intl;
            
            document.getElementById('cnDegree').textContent = cnData.degree;
            document.getElementById('cnDuration').textContent = cnData.duration;
            document.getElementById('cnHardLevel').textContent = cnData.hardLevel;
            document.getElementById('cnTrend').textContent = major.trend;
            document.getElementById('cnTrend').className = getTrendClass(major.trend);
            
            document.getElementById('intlDegree').textContent = intlData.degree;
            document.getElementById('intlDuration').textContent = intlData.duration;
            document.getElementById('intlHardLevel').textContent = intlData.hardLevel;
            document.getElementById('intlTrend').textContent = major.trend;
            document.getElementById('intlTrend').className = getTrendClass(major.trend);
            
            const cnIndustriesEl = document.getElementById('cnIndustries');
            cnIndustriesEl.innerHTML = cnData.industries.map(ind => 
                `<span class="bg-blue-900/50 px-3 py-1 rounded-full text-sm">${ind.name} ${ind.percent}%</span>`
            ).join('');
            
            const intlIndustriesEl = document.getElementById('intlIndustries');
            intlIndustriesEl.innerHTML = intlData.industries.map(ind => 
                `<span class="bg-blue-900/50 px-3 py-1 rounded-full text-sm">${ind.name} ${ind.percent}%</span>`
            ).join('');
            
            const cnCareersEl = document.getElementById('cnCareers');
            cnCareersEl.innerHTML = cnData.careers.map(c => 
                `<span class="bg-purple-900/50 px-3 py-1 rounded-full text-sm">${c}</span>`
            ).join('');
            
            const intlCareersEl = document.getElementById('intlCareers');
            intlCareersEl.innerHTML = intlData.careers.map(c => 
                `<span class="bg-purple-900/50 px-3 py-1 rounded-full text-sm">${c}</span>`
            ).join('');
            
            const cnCoursesEl = document.getElementById('cnCoreCourses');
            cnCoursesEl.innerHTML = cnData.coreCourses.map(c => `<li>• ${c}</li>`).join('');
            
            const intlCoursesEl = document.getElementById('intlCoreCourses');
            intlCoursesEl.innerHTML = intlData.coreCourses.map(c => `<li>• ${c}</li>`).join('');
            
            document.getElementById('cnTrainingGoals').textContent = cnData.trainingGoals;
            document.getElementById('intlTrainingGoals').textContent = intlData.trainingGoals;
            
            document.getElementById('cnWhatYouLearn').textContent = cnData.whatYouLearn;
            
            document.getElementById('cnSuitable').textContent = cnData.suitable;
            document.getElementById('cnForecast').textContent = cnData.forecast;
            document.getElementById('cnEmploymentAdvice').textContent = cnData.employmentAdvice;
            document.getElementById('cnLearningPath').textContent = cnData.learningPath;
            
            const review = major.review;
            document.getElementById('reviewPros').innerHTML = review.pros.map(p => 
                `<li class="pros-item pl-3 text-sm text-gray-300">${p}</li>`
            ).join('');
            
            document.getElementById('reviewCons').innerHTML = review.cons.map(c => 
                `<li class="cons-item pl-3 text-sm text-gray-300">${c}</li>`
            ).join('');
            
            document.getElementById('reviewSummary').textContent = review.summary;
            document.getElementById('reviewQuotes').innerHTML = review.quotes.map(q => 
                `<li class="text-yellow-200 text-sm italic">${q}</li>`
            ).join('');
            
            renderSalaryChart('cn', cnData);
        }
        
        function renderSalaryChart(lang, data) {
            const canvasId = lang === 'cn' ? 'cnSalaryChart' : 'intlSalaryChart';
            const ctx = document.getElementById(canvasId);
            
            if (salaryChart) {
                salaryChart.destroy();
            }
            
            salaryChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['1年', '5年', '10年', '20年', '40年'],
                    datasets: [{
                        label: '薪资 (万元/年)',
                        data: [data.salary.y1, data.salary.y5, data.salary.y10, data.salary.y20, data.salary.y40],
                        borderColor: '#ffd700',
                        backgroundColor: 'rgba(255, 215, 0, 0.1)',
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#00ffff',
                        pointBorderColor: '#fff',
                        pointRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255,255,255,0.1)' },
                            ticks: { color: '#aaa' }
                        },
                        x: {
                            grid: { color: 'rgba(255,255,255,0.1)' },
                            ticks: { color: '#aaa' }
                        }
                    }
                }
            });
        }
        
        function closeModal() {
            document.getElementById('modal').classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
        
        document.querySelectorAll('.btn-category').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.btn-category').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentCategory = btn.dataset.category;
                filterMajors();
            });
        });
        
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentLang = btn.dataset.tab;
                
                document.getElementById('cnContent').classList.toggle('hidden', currentLang !== 'cn');
                document.getElementById('intlContent').classList.toggle('hidden', currentLang !== 'intl');
            });
        });
        
        document.getElementById('searchInput').addEventListener('input', filterMajors);
        document.getElementById('sortSelect').addEventListener('change', filterMajors);
        document.getElementById('closeModal').addEventListener('click', closeModal);
        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target.id === 'modal') closeModal();
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeModal();
        });
        
        initStars();
        initBubbles();
        renderMajors(majorsData);
    </script>
</body>
</html>'''
    
    with open('/workspace/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"成功生成 index.html，共 {len(majors)} 个专业")

if __name__ == '__main__':
    generate()
