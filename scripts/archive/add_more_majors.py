
import urllib.request
import urllib.error
import json
import ssl

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def import_major(major):
    url = f"{SUPABASE_URL}/rest/v1/majors"
    data = json.dumps(major).encode('utf-8')
    
    req = urllib.request.Request(url, data=data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Prefer', 'return=representation')
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            print(f"✅ 成功导入: {major['name']}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print(f"⚠️  已存在: {major['name']}")
            return False
        else:
            print(f"❌ 导入失败 {major['name']}: {e.code}")
            return False
    except Exception as e:
        print(f"❌ 导入失败 {major['name']}")
        return False

majors_to_add = [
    # 文学 - 更多小语种
    {
        'code': '050238',
        'name': '荷兰语',
        'category': '05 文学',
        'hot': 3,
        'overview': '荷兰语专业培养掌握荷兰语语言文学的复合型人才。',
        'study_content': '荷兰语语音、语法、口语、阅读、写作、文学、文化等。',
        'suitable_people': '对荷兰及北欧语言文化有兴趣的学生。',
        'employment': '外事、经贸、教育、文化、旅游等领域。',
        'xuefeng_comment': '荷兰语虽是小语种，但在国际贸易和文化交流中很实用。',
        'courses': '荷兰语语音、语法、口语、阅读、写作、文学、文化',
        'top_universities': '北京外国语大学、上海外国语大学'
    },
    {
        'code': '050240',
        'name': '瑞典语',
        'category': '05 文学',
        'hot': 3,
        'overview': '瑞典语专业培养掌握瑞典语语言文学的专门人才。',
        'study_content': '瑞典语语音、语法、口语、阅读、写作、文学、文化等。',
        'suitable_people': '对瑞典及北欧语言文化有兴趣的学生。',
        'employment': '外事、经贸、教育、文化、旅游等领域。',
        'xuefeng_comment': '瑞典是创新强国，瑞典语人才在相关领域很有价值。',
        'courses': '瑞典语语音、语法、口语、阅读、写作、文学、文化',
        'top_universities': '北京外国语大学、上海外国语大学'
    },
    {
        'code': '050241',
        'name': '丹麦语',
        'category': '05 文学',
        'hot': 3,
        'overview': '丹麦语专业培养掌握丹麦语语言文学的专门人才。',
        'study_content': '丹麦语语音、语法、口语、阅读、写作、文学、文化等。',
        'suitable_people': '对丹麦及北欧语言文化有兴趣的学生。',
        'employment': '外事、经贸、教育、文化、旅游等领域。',
        'xuefeng_comment': '丹麦设计闻名世界，丹麦语人才在相关领域有独特优势。',
        'courses': '丹麦语语音、语法、口语、阅读、写作、文学、文化',
        'top_universities': '北京外国语大学、上海外国语大学'
    },
    {
        'code': '050242',
        'name': '芬兰语',
        'category': '05 文学',
        'hot': 3,
        'overview': '芬兰语专业培养掌握芬兰语语言文学的专门人才。',
        'study_content': '芬兰语语音、语法、口语、阅读、写作、文学、文化等。',
        'suitable_people': '对芬兰语言文化有兴趣的学生。',
        'employment': '外事、经贸、教育、文化、旅游等领域。',
        'xuefeng_comment': '芬兰教育世界领先，芬兰语人才在教育交流领域很重要。',
        'courses': '芬兰语语音、语法、口语、阅读、写作、文学、文化',
        'top_universities': '北京外国语大学、上海外国语大学'
    },
    {
        'code': '050243',
        'name': '挪威语',
        'category': '05 文学',
        'hot': 3,
        'overview': '挪威语专业培养掌握挪威语语言文学的专门人才。',
        'study_content': '挪威语语音、语法、口语、阅读、写作、文学、文化等。',
        'suitable_people': '对挪威及北欧语言文化有兴趣的学生。',
        'employment': '外事、经贸、教育、文化、旅游等领域。',
        'xuefeng_comment': '挪威在海洋工程等领域领先，挪威语人才有独特就业机会。',
        'courses': '挪威语语音、语法、口语、阅读、写作、文学、文化',
        'top_universities': '北京外国语大学、上海外国语大学'
    },
    {
        'code': '050244',
        'name': '希腊语',
        'category': '05 文学',
        'hot': 2,
        'overview': '希腊语专业培养掌握希腊语语言文学的专门人才。',
        'study_content': '希腊语语音、语法、口语、阅读、写作、文学、文化等。',
        'suitable_people': '对希腊语言文化有兴趣的学生。',
        'employment': '外事、教育、文化、科研、旅游等领域。',
        'xuefeng_comment': '希腊是西方文明发源地，学习希腊语对研究西方文化很有帮助。',
        'courses': '希腊语语音、语法、口语、阅读、写作、文学、文化',
        'top_universities': '北京外国语大学、上海外国语大学'
    },
    # 理学补充
    {
        'code': '070603',
        'name': '应用气象学',
        'category': '07 理学',
        'hot': 4,
        'overview': '应用气象学专业培养掌握气象学理论和应用技能的人才。',
        'study_content': '大气科学、气象学、气候学、大气探测等。',
        'suitable_people': '对气象科学有兴趣，有志于气象事业的学生。',
        'employment': '气象部门、环保、民航、农业等领域。',
        'xuefeng_comment': '应用气象学专业实用性强，就业领域广，工作稳定。',
        'courses': '大气科学、气象学、气候学、大气探测、天气学',
        'top_universities': '南京信息工程大学、成都信息工程大学、南京大学'
    },
    {
        'code': '070401',
        'name': '天文学',
        'category': '07 理学',
        'hot': 3,
        'overview': '天文学专业培养掌握天文学理论和观测技能的人才。',
        'study_content': '天体物理学、天体力学、天文观测等。',
        'suitable_people': '对宇宙星空有浓厚兴趣，有志于天文研究的学生。',
        'employment': '科研院所、天文台、高校、科普机构等。',
        'xuefeng_comment': '天文学是基础前沿学科，适合热爱科学研究的学生。',
        'courses': '天体物理学、天体力学、天文观测、宇宙学',
        'top_universities': '南京大学、北京大学、中国科学技术大学'
    },
    {
        'code': '070702',
        'name': '海洋技术',
        'category': '07 理学',
        'hot': 4,
        'overview': '海洋技术专业培养掌握海洋技术理论和实践技能的人才。',
        'study_content': '海洋学、海洋探测、海洋技术装备等。',
        'suitable_people': '对海洋科学有兴趣，有志于海洋事业的学生。',
        'employment': '海洋部门、科研院所、涉海企业等。',
        'xuefeng_comment': '海洋战略是国家战略，海洋技术人才需求持续增长。',
        'courses': '海洋学、海洋探测、海洋技术装备、海洋环境保护',
        'top_universities': '中国海洋大学、厦门大学、上海海洋大学'
    },
    # 法学补充 - 更多公安学类
    {
        'code': '030603TK',
        'name': '边防管理',
        'category': '03 法学',
        'hot': 4,
        'overview': '边防管理专业培养从事边防管理工作的专门人才。',
        'study_content': '边防管理、边防检查、边境管理等。',
        'suitable_people': '有志于公安边防事业的学生。',
        'employment': '公安边防部门。',
        'xuefeng_comment': '边防管理专业就业定向明确，工作稳定，待遇好。',
        'courses': '边防管理、边防检查、边境管理、边防法学',
        'top_universities': '中国人民公安大学、中国人民警察大学'
    },
    {
        'code': '030605TK',
        'name': '警犬技术',
        'category': '03 法学',
        'hot': 3,
        'overview': '警犬技术专业培养掌握警犬训练和使用技能的专门人才。',
        'study_content': '警犬学、警犬训练、警犬使用等。',
        'suitable_people': '热爱动物，有志于公安事业的学生。',
        'employment': '公安部门。',
        'xuefeng_comment': '警犬技术专业特色鲜明，在刑事侦查、治安等领域作用重要。',
        'courses': '警犬学、警犬训练、警犬使用、刑事侦查学',
        'top_universities': '中国刑事警察学院'
    },
    {
        'code': '030606TK',
        'name': '经济犯罪侦查',
        'category': '03 法学',
        'hot': 4,
        'overview': '经济犯罪侦查专业培养从事经济犯罪侦查工作的专门人才。',
        'study_content': '经济犯罪侦查、司法会计、经济法学等。',
        'suitable_people': '有志于公安经侦事业的学生。',
        'employment': '公安经济犯罪侦查部门。',
        'xuefeng_comment': '经济犯罪侦查专业实用性强，在打击经济犯罪中发挥重要作用。',
        'courses': '经济犯罪侦查、司法会计、经济法学、刑事侦查学',
        'top_universities': '中国人民公安大学、中国刑事警察学院'
    },
    {
        'code': '030607TK',
        'name': '边防指挥',
        'category': '03 法学',
        'hot': 3,
        'overview': '边防指挥专业培养从事边防指挥工作的专门人才。',
        'study_content': '边防指挥、边防管理、军事法学等。',
        'suitable_people': '有志于公安边防指挥事业的学生。',
        'employment': '公安边防部门。',
        'xuefeng_comment': '边防指挥专业培养指挥人才，责任重大，使命光荣。',
        'courses': '边防指挥、边防管理、军事法学、战术学',
        'top_universities': '中国人民警察大学'
    },
    {
        'code': '030608TK',
        'name': '消防指挥',
        'category': '03 法学',
        'hot': 4,
        'overview': '消防指挥专业培养从事消防指挥工作的专门人才。',
        'study_content': '消防指挥、灭火战术、消防技术装备等。',
        'suitable_people': '有志于消防事业的学生。',
        'employment': '消防救援部门。',
        'xuefeng_comment': '消防指挥专业培养消防指挥员，职业光荣，责任重大。',
        'courses': '消防指挥、灭火战术、消防技术装备、消防工程',
        'top_universities': '中国人民警察大学'
    },
    # 工学补充
    {
        'code': '080206',
        'name': '过程装备与控制工程',
        'category': '08 工学',
        'hot': 4,
        'overview': '过程装备与控制工程专业培养装备设计制造和控制的工程人才。',
        'study_content': '过程装备设计、控制工程、机械设计等。',
        'suitable_people': '对机械和化工装备有兴趣的学生。',
        'employment': '化工、石油、能源、机械等行业。',
        'xuefeng_comment': '过控专业是传统优势专业，就业稳定，适用领域广。',
        'courses': '过程装备设计、控制工程、机械设计、工程力学',
        'top_universities': '浙江大学、西安交通大学、华东理工大学'
    },
    {
        'code': '080601',
        'name': '电气工程及其自动化',
        'category': '08 工学',
        'hot': 5,
        'overview': '电气工程及其自动化专业培养电气系统设计运行的工程人才。',
        'study_content': '电路、电机学、电力系统、自动化等。',
        'suitable_people': '对电气技术有兴趣的学生。',
        'employment': '电力、电气、制造等行业。',
        'xuefeng_comment': '电气专业是工科王牌专业，就业面广，待遇好。',
        'courses': '电路、电机学、电力系统、自动控制原理',
        'top_universities': '清华大学、西安交通大学、华中科技大学'
    },
    {
        'code': '081201',
        'name': '测绘工程',
        'category': '08 工学',
        'hot': 4,
        'overview': '测绘工程专业培养测绘数据采集处理的工程技术人才。',
        'study_content': '测量学、大地测量、工程测量、遥感等。',
        'suitable_people': '对地理信息技术有兴趣的学生。',
        'employment': '测绘、国土、建筑、交通等行业。',
        'xuefeng_comment': '测绘工程专业应用领域广，现代测绘技术发展快。',
        'courses': '测量学、大地测量、工程测量、遥感原理与应用',
        'top_universities': '武汉大学、解放军信息工程大学、中国矿业大学'
    },
    # 医学补充
    {
        'code': '100802',
        'name': '中药资源与开发',
        'category': '10 医学',
        'hot': 3,
        'overview': '中药资源与开发专业培养中药资源保护开发的专门人才。',
        'study_content': '中药学、药用植物学、中药资源学等。',
        'suitable_people': '对中医药有兴趣的学生。',
        'employment': '中药企业、药检所、科研院所等。',
        'xuefeng_comment': '中医药复兴，中药资源专业前景好。',
        'courses': '中药学、药用植物学、中药资源学、中药鉴定学',
        'top_universities': '南京中医药大学、中国药科大学、北京中医药大学'
    },
    {
        'code': '101002',
        'name': '医学实验技术',
        'category': '10 医学',
        'hot': 3,
        'overview': '医学实验技术专业培养医学实验技术专门人才。',
        'study_content': '基础医学、医学实验技术、医学检验等。',
        'suitable_people': '对医学实验技术有兴趣的学生。',
        'employment': '医院、科研院所、生物公司等。',
        'xuefeng_comment': '医学实验技术专业实用性强，是医学研究的重要支撑。',
        'courses': '基础医学、医学实验技术、医学检验、分子生物学',
        'top_universities': '北京大学医学部、北京协和医学院、复旦大学上海医学院'
    },
    {
        'code': '101004',
        'name': '眼视光学',
        'category': '10 医学',
        'hot': 4,
        'overview': '眼视光学专业培养眼视光医疗保健专门人才。',
        'study_content': '眼科学、视光学、眼镜学、角膜接触镜学等。',
        'suitable_people': '对眼视光有兴趣的学生。',
        'employment': '医院眼科、视光中心、眼镜企业等。',
        'xuefeng_comment': '眼视光学专业就业好，创业机会多。',
        'courses': '眼科学、视光学、眼镜学、角膜接触镜学',
        'top_universities': '温州医科大学、天津医科大学、南京医科大学'
    },
    # 管理学补充
    {
        'code': '120104',
        'name': '房地产开发与管理',
        'category': '12 管理学',
        'hot': 4,
        'overview': '房地产开发与管理专业培养房地产行业管理人才。',
        'study_content': '房地产开发、房地产经营、工程管理等。',
        'suitable_people': '对房地产行业有兴趣的学生。',
        'employment': '房地产企业、建筑企业、中介机构等。',
        'xuefeng_comment': '房地产专业适应市场需求，就业机会多。',
        'courses': '房地产开发、房地产经营、工程管理、工程估价',
        'top_universities': '重庆大学、同济大学、东南大学'
    },
    {
        'code': '120214',
        'name': '文化产业管理',
        'category': '12 管理学',
        'hot': 4,
        'overview': '文化产业管理专业培养文化产业经营管理人才。',
        'study_content': '文化产业管理、文化经济学、文化市场营销等。',
        'suitable_people': '对文化产业有兴趣的学生。',
        'employment': '文化企业、媒体、文化场馆等。',
        'xuefeng_comment': '文化产业蓬勃发展，文管专业前景好。',
        'courses': '文化产业管理、文化经济学、文化市场营销、文化创意',
        'top_universities': '中国传媒大学、中央财经大学、山东大学'
    },
    {
        'code': '120603',
        'name': '采购管理',
        'category': '12 管理学',
        'hot': 4,
        'overview': '采购管理专业培养采购与供应链管理人才。',
        'study_content': '采购管理、供应链管理、物流管理等。',
        'suitable_people': '对采购供应链有兴趣的学生。',
        'employment': '工商企业、物流企业、政府采购部门等。',
        'xuefeng_comment': '采购与供应链管理日益重要，专才需求大。',
        'courses': '采购管理、供应链管理、物流管理、谈判学',
        'top_universities': '北京物资学院、浙江工商大学、上海海事大学'
    },
    # 农学补充
    {
        'code': '090103',
        'name': '植物保护',
        'category': '09 农学',
        'hot': 4,
        'overview': '植物保护专业培养植物病虫害防治技术人才。',
        'study_content': '植物病理学、昆虫学、农药学等。',
        'suitable_people': '对农业和植物保护有兴趣的学生。',
        'employment': '农业部门、农技推广、农药企业等。',
        'xuefeng_comment': '植物保护是农业生产的重要保障，专业性强。',
        'courses': '植物病理学、昆虫学、农药学、植物化学保护',
        'top_universities': '中国农业大学、南京农业大学、西北农林科技大学'
    },
    {
        'code': '090106',
        'name': '种子科学与工程',
        'category': '09 农学',
        'hot': 4,
        'overview': '种子科学与工程专业培养种子研发生产技术人才。',
        'study_content': '种子学、作物育种学、种子生产技术等。',
        'suitable_people': '对种业有兴趣的学生。',
        'employment': '种子企业、农业科研、农技推广等。',
        'xuefeng_comment': '种业是农业的芯片，种子专业非常重要。',
        'courses': '种子学、作物育种学、种子生产技术、种子检验',
        'top_universities': '中国农业大学、南京农业大学、华中农业大学'
    },
    {
        'code': '090202',
        'name': '茶学',
        'category': '09 农学',
        'hot': 3,
        'overview': '茶学专业培养茶叶生产加工和茶文化专业人才。',
        'study_content': '茶树栽培学、茶叶加工学、茶叶审评、茶文化等。',
        'suitable_people': '对茶文化和茶产业有兴趣的学生。',
        'employment': '茶企业、茶场、茶叶研究所等。',
        'xuefeng_comment': '茶学专业特色鲜明，中国茶文化底蕴深厚。',
        'courses': '茶树栽培学、茶叶加工学、茶叶审评、茶文化',
        'top_universities': '安徽农业大学、浙江大学、湖南农业大学'
    },
    {
        'code': '090502',
        'name': '野生动物与自然保护区管理',
        'category': '09 农学',
        'hot': 3,
        'overview': '野保专业培养野生动物保护和自然保护区管理人才。',
        'study_content': '野生动物学、保护生物学、自然保护区管理等。',
        'suitable_people': '热爱自然和野生动物的学生。',
        'employment': '自然保护区、林业部门、动物园等。',
        'xuefeng_comment': '生态保护日益重要，野保专业意义重大。',
        'courses': '野生动物学、保护生物学、自然保护区管理',
        'top_universities': '东北林业大学、北京林业大学、西南林业大学'
    },
    # 经济学补充
    {
        'code': '020102',
        'name': '经济统计学',
        'category': '02 经济学',
        'hot': 4,
        'overview': '经济统计学专业培养经济统计分析人才。',
        'study_content': '统计学、经济学、计量经济学、抽样调查等。',
        'suitable_people': '对数据和经济分析有兴趣的学生。',
        'employment': '政府统计部门、金融机构、企业市场研究等。',
        'xuefeng_comment': '大数据时代，统计学专业就业好，发展前景广阔。',
        'courses': '统计学、经济学、计量经济学、抽样调查、数据分析',
        'top_universities': '中国人民大学、厦门大学、中央财经大学'
    }
]

print(f"准备导入 {len(majors_to_add)} 个专业...\n")
success_count = 0
for major in majors_to_add:
    if import_major(major):
        success_count += 1

print(f"\n✅ 成功导入 {success_count} 个专业")
