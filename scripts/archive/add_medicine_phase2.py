
import urllib.request
import urllib.error
import json
import ssl
import time

SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def import_major(major):
    url = f'{SUPABASE_URL}/rest/v1/majors'
    data = json.dumps(major).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('apikey', SUPABASE_KEY)
    req.add_header('Authorization', f'Bearer {SUPABASE_KEY}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Prefer', 'return=minimal')
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return True, response.status
    except urllib.error.HTTPError as e:
        return False, e.code if e.code != 409 else 409

majors_to_add = [
    {
        'code': '100202TK',
        'name': '麻醉学',
        'category': '10 医学',
        'category_icon': '💊',
        'difficulty': '⭐⭐⭐⭐',
        'salary_range': '¥10k-30k',
        'overview': '麻醉学专业培养掌握麻醉学知识的专业人才，从事临床麻醉、急救复苏等工作。',
        'what_you_learn': '麻醉学、药理学、生理学、外科学、内科学、急救医学、疼痛诊疗学',
        'suitable_for': '对医学和麻醉有兴趣的学生。',
        'career_outlook': '医院麻醉科、手术室、ICU等对麻醉学人才有需求。',
        'xuefeng_comment': '麻醉学是医学热门专业，待遇好，工作强度较大但成就感强。建议对医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '组织胚胎学'], '大二': ['药理学', '病理学', '病理生理学', '诊断学'], '大三': ['麻醉学', '外科学', '内科学', '疼痛诊疗学'], '大四': ['临床麻醉学', '急救医学', '危重病医学', '医院实习'], '大五': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['北京协和医学院', '北京大学', '复旦大学', '上海交通大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '斯坦福大学']}
    },
    {
        'code': '100203TK',
        'name': '医学影像学',
        'category': '10 医学',
        'category_icon': '📷',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥10k-25k',
        'overview': '医学影像学专业培养掌握医学影像技术的专业人才，从事医学影像诊断和介入治疗工作。',
        'what_you_learn': '医学影像诊断学、医学影像检查技术、放射治疗学、超声诊断学、核医学',
        'suitable_for': '对医学和影像技术有兴趣的学生。',
        'career_outlook': '医院影像科、放疗科等对医学影像学人才有需求。',
        'xuefeng_comment': '医学影像学是医学热门专业，工作环境相对干净，待遇不错。建议对医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '物理学'], '大二': ['医学物理学', '病理学', '诊断学', '医学影像设备学'], '大三': ['医学影像诊断学', '超声诊断学', '核医学', '放射治疗学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['复旦大学', '上海交通大学', '华中科技大学', '中山大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '斯坦福大学']}
    },
    {
        'code': '100204TK',
        'name': '眼视光医学',
        'category': '10 医学',
        'category_icon': '👁️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥10k-28k',
        'overview': '眼视光医学专业培养掌握眼视光知识的专业人才，从事眼部疾病诊断和视力矫正工作。',
        'what_you_learn': '眼科学、视光学、眼视光器械学、眼镜学、双眼视觉学、斜弱视学',
        'suitable_for': '对眼科学和视光学有兴趣的学生。',
        'career_outlook': '医院眼科、视光中心等对眼视光医学人才有需求。',
        'xuefeng_comment': '眼视光医学是医学热门专业，待遇不错，市场需求持续增长。建议对眼科学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '组织胚胎学'], '大二': ['眼科学基础', '视光学基础', '病理学', '诊断学'], '大三': ['眼科学', '视光学', '眼镜学', '双眼视觉学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['温州医科大学', '天津医科大学', '上海交通大学', '中山大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '伦敦帝国学院']}
    },
    {
        'code': '100205TK',
        'name': '精神医学',
        'category': '10 医学',
        'category_icon': '🧠',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥10k-26k',
        'overview': '精神医学专业培养掌握精神医学知识的专业人才，从事精神疾病诊断和心理治疗工作。',
        'what_you_learn': '精神病学、心理学、心理治疗学、精神药理学、社会精神病学',
        'suitable_for': '对精神医学和心理学有兴趣的学生。',
        'career_outlook': '医院精神科、心理卫生中心等对精神医学人才有需求。',
        'xuefeng_comment': '精神医学是医学重要专业，随着社会发展对心理健康的重视，需求在增长。建议对精神医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '心理学'], '大二': ['精神病学基础', '病理学', '诊断学', '心理学'], '大三': ['精神病学', '心理治疗学', '精神药理学', '社会精神病学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['中南大学', '上海交通大学', '北京大学', '首都医科大学'], 'international': ['哈佛大学', '斯坦福大学', '伦敦国王学院']}
    },
    {
        'code': '100206TK',
        'name': '放射医学',
        'category': '10 医学',
        'category_icon': '☢️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥10k-27k',
        'overview': '放射医学专业培养掌握放射医学知识的专业人才，从事放射治疗、影像诊断和核医学工作。',
        'what_you_learn': '放射物理学、放射生物学、放射治疗学、医学影像诊断学、核医学',
        'suitable_for': '对放射医学和影像技术有兴趣的学生。',
        'career_outlook': '医院放疗科、影像科等对放射医学人才有需求。',
        'xuefeng_comment': '放射医学是医学重要专业，随着肿瘤治疗的发展，需求在增长。建议对放射医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '物理学'], '大二': ['放射物理学', '放射生物学', '病理学', '诊断学'], '大三': ['放射治疗学', '医学影像诊断学', '核医学', '肿瘤学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['苏州大学', '复旦大学', '上海交通大学', '华中科技大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '斯坦福大学']}
    },
    {
        'code': '100403TK',
        'name': '针灸推拿学',
        'category': '10 医学',
        'category_icon': '💉',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥8k-22k',
        'overview': '针灸推拿学专业培养掌握针灸推拿知识的专业人才，从事针灸治疗和推拿康复工作。',
        'what_you_learn': '针灸学、推拿学、经络腧穴学、针法灸法学、推拿手法学',
        'suitable_for': '对针灸推拿和中医有兴趣的学生。',
        'career_outlook': '中医院、针灸推拿科等对针灸推拿学人才有需求。',
        'xuefeng_comment': '针灸推拿学是中医特色专业，随着中医国际化，前景不错。建议对中医有兴趣的同学报考。',
        'yearly_courses': {'大一': ['中医基础理论', '中医诊断学', '中药学', '方剂学'], '大二': ['经络腧穴学', '针法灸法学', '推拿手法学', '针灸医籍选'], '大三': ['针灸治疗学', '推拿治疗学', '中医内科学', '中医骨伤科学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['北京中医药大学', '上海中医药大学', '天津中医药大学', '南京中医药大学'], 'international': []}
    },
    {
        'code': '100404TK',
        'name': '藏医学',
        'category': '10 医学',
        'category_icon': '🏔️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '藏医学专业培养掌握藏医学知识的专业人才，从事藏医诊疗和藏药研究工作。',
        'what_you_learn': '藏医学基础、藏药药理学、藏医诊断学、藏医治疗学、藏药方剂学',
        'suitable_for': '对藏医学和民族医学有兴趣的学生。',
        'career_outlook': '藏医院、民族医院等对藏医学人才有需求。',
        'xuefeng_comment': '藏医学是民族医学特色专业，适合对藏医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['藏医学基础', '藏语基础', '藏药基础'], '大二': ['藏医诊断学', '藏药药理学', '藏药方剂学'], '大三': ['藏医治疗学', '藏医内科学', '藏医外科学'], '大四': ['藏医院实习', '毕业论文']},
        'top_universities': {'domestic': ['西藏藏医药大学', '青海大学', '甘肃中医药大学'], 'international': []}
    },
    {
        'code': '100405TK',
        'name': '蒙医学',
        'category': '10 医学',
        'category_icon': '🐴',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '蒙医学专业培养掌握蒙医学知识的专业人才，从事蒙医诊疗和蒙药研究工作。',
        'what_you_learn': '蒙医学基础、蒙药药理学、蒙医诊断学、蒙医治疗学、蒙药方剂学',
        'suitable_for': '对蒙医学和民族医学有兴趣的学生。',
        'career_outlook': '蒙医院、民族医院等对蒙医学人才有需求。',
        'xuefeng_comment': '蒙医学是民族医学特色专业，适合对蒙医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['蒙医学基础', '蒙语基础', '蒙药基础'], '大二': ['蒙医诊断学', '蒙药药理学', '蒙药方剂学'], '大三': ['蒙医治疗学', '蒙医内科学', '蒙医外科学'], '大四': ['蒙医院实习', '毕业论文']},
        'top_universities': {'domestic': ['内蒙古医科大学', '内蒙古民族大学'], 'international': []}
    },
    {
        'code': '100406TK',
        'name': '维医学',
        'category': '10 医学',
        'category_icon': '🏜️',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '维医学专业培养掌握维医学知识的专业人才，从事维医诊疗和维药研究工作。',
        'what_you_learn': '维医学基础、维药药理学、维医诊断学、维医治疗学、维药方剂学',
        'suitable_for': '对维医学和民族医学有兴趣的学生。',
        'career_outlook': '维医院、民族医院等对维医学人才有需求。',
        'xuefeng_comment': '维医学是民族医学特色专业，适合对维医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['维医学基础', '维语基础', '维药基础'], '大二': ['维医诊断学', '维药药理学', '维药方剂学'], '大三': ['维医治疗学', '维医内科学', '维医外科学'], '大四': ['维医院实习', '毕业论文']},
        'top_universities': {'domestic': ['新疆医科大学'], 'international': []}
    },
    {
        'code': '100407TK',
        'name': '壮医学',
        'category': '10 医学',
        'category_icon': '🌴',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '壮医学专业培养掌握壮医学知识的专业人才，从事壮医诊疗和壮药研究工作。',
        'what_you_learn': '壮医学基础、壮药药理学、壮医诊断学、壮医治疗学、壮药方剂学',
        'suitable_for': '对壮医学和民族医学有兴趣的学生。',
        'career_outlook': '壮医院、民族医院等对壮医学人才有需求。',
        'xuefeng_comment': '壮医学是民族医学特色专业，适合对壮医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['壮医学基础', '壮语基础', '壮药基础'], '大二': ['壮医诊断学', '壮药药理学', '壮药方剂学'], '大三': ['壮医治疗学', '壮医内科学', '壮医外科学'], '大四': ['壮医院实习', '毕业论文']},
        'top_universities': {'domestic': ['广西中医药大学'], 'international': []}
    },
    {
        'code': '100408TK',
        'name': '哈萨克医学',
        'category': '10 医学',
        'category_icon': '🐪',
        'difficulty': '⭐⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '哈萨克医学专业培养掌握哈萨克医学知识的专业人才，从事哈医诊疗和哈药研究工作。',
        'what_you_learn': '哈萨克医学基础、哈药药理学、哈医诊断学、哈医治疗学、哈药方剂学',
        'suitable_for': '对哈萨克医学和民族医学有兴趣的学生。',
        'career_outlook': '哈萨克医院、民族医院等对哈萨克医学人才有需求。',
        'xuefeng_comment': '哈萨克医学是民族医学特色专业，适合对哈萨克医学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['哈萨克医学基础', '哈语基础', '哈药基础'], '大二': ['哈医诊断学', '哈药药理学', '哈药方剂学'], '大三': ['哈医治疗学', '哈医内科学', '哈医外科学'], '大四': ['哈医院实习', '毕业论文']},
        'top_universities': {'domestic': ['新疆医科大学'], 'international': []}
    },
    {
        'code': '101001T',
        'name': '医学检验技术',
        'category': '10 医学',
        'category_icon': '🔬',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '医学检验技术专业培养掌握医学检验技术的专业人才，从事临床检验和实验室检查工作。',
        'what_you_learn': '临床检验基础、生物化学检验、微生物检验、免疫学检验、血液学检验',
        'suitable_for': '对医学检验和实验技术有兴趣的学生。',
        'career_outlook': '医院检验科、体检中心等对医学检验技术人才有需求。',
        'xuefeng_comment': '医学检验技术是医学重要辅助专业，工作稳定，需求大。建议对医学检验有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '有机化学'], '大二': ['微生物学', '免疫学', '病理学', '临床检验基础'], '大三': ['生物化学检验', '微生物检验', '免疫学检验', '血液学检验'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['重庆医科大学', '首都医科大学', '天津医科大学', '南京医科大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '伦敦帝国学院']}
    },
    {
        'code': '101003T',
        'name': '医学影像技术',
        'category': '10 医学',
        'category_icon': '📷',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '医学影像技术专业培养掌握医学影像技术的专业人才，从事医学影像检查和设备操作工作。',
        'what_you_learn': '医学影像检查技术、医学影像设备学、医学影像诊断学、放射治疗技术学',
        'suitable_for': '对医学影像和设备操作有兴趣的学生。',
        'career_outlook': '医院影像科、放疗科等对医学影像技术人才有需求。',
        'xuefeng_comment': '医学影像技术是医学重要辅助专业，工作稳定，需求大。建议对医学影像有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '物理学', '生物化学'], '大二': ['医学影像设备学', '病理学', '医学影像物理学'], '大三': ['医学影像检查技术', '放射治疗技术学', '医学影像诊断学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['上海健康医学院', '重庆医科大学', '天津医科大学', '南京医科大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '伦敦帝国学院']}
    },
    {
        'code': '101006T',
        'name': '口腔医学技术',
        'category': '10 医学',
        'category_icon': '🦷',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '口腔医学技术专业培养掌握口腔医学技术的专业人才，从事义齿制作和口腔修复技术工作。',
        'what_you_learn': '口腔解剖学、口腔材料学、口腔修复学、牙体解剖学、义齿工艺技术',
        'suitable_for': '对口腔医学和工艺技术有兴趣的学生。',
        'career_outlook': '口腔医院、义齿加工企业等对口腔医学技术人才有需求。',
        'xuefeng_comment': '口腔医学技术是口腔医学重要辅助专业，就业前景好。建议对口腔医学技术有兴趣的同学报考。',
        'yearly_courses': {'大一': ['口腔解剖学', '口腔生理学', '牙体解剖学'], '大二': ['口腔材料学', '口腔修复学基础', '义齿工艺技术'], '大三': ['固定义齿工艺技术', '可摘义齿工艺技术', '全口义齿工艺技术'], '大四': ['企业实习', '毕业论文']},
        'top_universities': {'domestic': ['四川大学', '上海交通大学', '北京大学', '武汉大学'], 'international': ['哈佛大学', '伦敦国王学院', '东京医科齿科大学']}
    },
    {
        'code': '101007T',
        'name': '卫生检验与检疫',
        'category': '10 医学',
        'category_icon': '🧪',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-18k',
        'overview': '卫生检验与检疫专业培养掌握卫生检验技术的专业人才，从事卫生检验和检疫工作。',
        'what_you_learn': '卫生微生物学、卫生检验学、空气理化检验、水质理化检验、食品理化检验',
        'suitable_for': '对卫生检验和检疫有兴趣的学生。',
        'career_outlook': '疾控中心、卫生监督所等对卫生检验与检疫人才有需求。',
        'xuefeng_comment': '卫生检验与检疫是公共卫生重要专业，工作稳定。建议对卫生检验有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '微生物学'], '大二': ['卫生微生物学', '卫生化学', '毒理学基础'], '大三': ['空气理化检验', '水质理化检验', '食品理化检验', '卫生检验学'], '大四': ['疾控中心实习', '毕业论文']},
        'top_universities': {'domestic': ['四川大学', '南京医科大学', '天津医科大学', '重庆医科大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '伦敦帝国学院']}
    },
    {
        'code': '101101',
        'name': '护理学',
        'category': '10 医学',
        'category_icon': '👩⚕️',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '护理学专业培养掌握护理学知识的专业人才，从事临床护理和护理管理工作。',
        'what_you_learn': '护理学基础、内科护理学、外科护理学、妇产科护理学、儿科护理学',
        'suitable_for': '对护理和医疗服务有兴趣的学生。',
        'career_outlook': '医院、社区卫生服务中心等对护理学人才有大量需求。',
        'xuefeng_comment': '护理学是医学重要专业，就业非常好，但工作较辛苦。建议对护理有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '护理学基础'], '大二': ['内科护理学', '外科护理学', '健康评估', '病理学'], '大三': ['妇产科护理学', '儿科护理学', '急危重症护理学', '护理心理学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['北京协和医学院', '北京大学', '复旦大学', '上海交通大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '伦敦国王学院']}
    },
    {
        'code': '101102T',
        'name': '助产学',
        'category': '10 医学',
        'category_icon': '🤰',
        'difficulty': '⭐⭐',
        'salary_range': '¥7k-20k',
        'overview': '助产学专业培养掌握助产学知识的专业人才，从事助产和妇幼保健工作。',
        'what_you_learn': '助产学、妇产科护理学、儿科护理学、母婴保健学、分娩心理学',
        'suitable_for': '对助产学和妇幼保健有兴趣的学生。',
        'career_outlook': '医院妇产科、妇幼保健院等对助产学人才有需求。',
        'xuefeng_comment': '助产学是妇产科重要专业，随着生育政策，需求在增长。建议对助产学有兴趣的同学报考。',
        'yearly_courses': {'大一': ['系统解剖学', '生理学', '生物化学', '护理学基础'], '大二': ['助产学基础', '妇产科护理学', '健康评估', '病理学'], '大三': ['助产学、妇科护理学、儿科护理学、母婴保健学'], '大四': ['医院实习', '毕业论文']},
        'top_universities': {'domestic': ['首都医科大学', '天津医科大学', '南京医科大学', '重庆医科大学'], 'international': ['哈佛大学', '约翰霍普金斯大学', '伦敦国王学院']}
    }
]

def main():
    print('=' * 70)
    print('🏥 医学类专业补充（第二阶段）')
    print('=' * 70)
    
    success = failed = skipped = 0
    
    for major in majors_to_add:
        print(f'\n正在导入: {major["code"]} - {major["name"]}')
        ok, code = import_major(major)
        if ok or code in [200, 201]:
            success += 1
            print(f'✅ 成功')
        elif code == 409:
            skipped += 1
            print(f'⏭️ 已存在')
        else:
            failed += 1
            print(f'❌ 失败 (HTTP {code})')
        time.sleep(0.2)
    
    print(f'\n导入完成！成功: {success}, 跳过: {skipped}, 失败: {failed}')

if __name__ == '__main__':
    main()

