
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

majors = [
    {
        "code": "082101T",
        "name": "农业工程",
        "category": "08 工学",
        "category_icon": "🚜",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "农业工程专业培养掌握农业工程知识的工程师，从事农业工程设计和技术工作。",
        "what_you_learn": "农业机械化、农业电气化、农业水土工程、农业生物环境工程",
        "suitable_for": "对农业工程有兴趣的学生。",
        "career_outlook": "农业企业、农机企业等对农业工程人才有需求。",
        "xuefeng_comment": "农业工程是农业工程类专业，就业稳定。建议对农业工程有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["理论力学", "材料力学", "机械设计基础", "农业机械化"], "大三": ["农业电气化", "农业水土工程"], "大四": ["农业企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "浙江大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082102T",
        "name": "农业机械化及其自动化",
        "category": "08 工学",
        "category_icon": "🚜",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "农业机械化及其自动化专业培养掌握农业机械化知识的工程师，从事农业机械设计和生产工作。",
        "what_you_learn": "农业机械学、机械设计、机械制造、自动化技术",
        "suitable_for": "对农业机械化有兴趣的学生。",
        "career_outlook": "农机企业等对农业机械化人才有需求。",
        "xuefeng_comment": "农业机械化及其自动化是农业工程类专业，就业稳定。建议对农业机械有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["理论力学", "材料力学", "机械设计基础"], "大三": ["农业机械学", "机械制造", "自动化技术"], "大四": ["农机企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学", "吉林大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082103T",
        "name": "农业电气化",
        "category": "08 工学",
        "category_icon": "⚡",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "农业电气化专业培养掌握农业电气化知识的工程师，从事农业电气化工作。",
        "what_you_learn": "电工电子学、电力系统、农业电气化、自动控制",
        "suitable_for": "对农业电气化有兴趣的学生。",
        "career_outlook": "农业企业、电力企业等对农业电气化人才有需求。",
        "xuefeng_comment": "农业电气化是农业工程类专业，就业稳定。建议对农业电气化有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "电工电子学"], "大二": ["电路分析", "电机学", "电力系统"], "大三": ["农业电气化", "自动控制"], "大四": ["农业企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082104T",
        "name": "农业建筑环境与能源工程",
        "category": "08 工学",
        "category_icon": "🏡",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "农业建筑环境与能源工程专业培养掌握相关知识的工程师，从事农业建筑和能源工程工作。",
        "what_you_learn": "农业建筑、农业生物环境、新能源工程、能源与环境工程",
        "suitable_for": "对农业建筑环境与能源工程有兴趣的学生。",
        "career_outlook": "农业企业、能源企业等对相关人才有需求。",
        "xuefeng_comment": "农业建筑环境与能源工程是农业工程类专业，就业稳定。建议对相关领域有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["理论力学", "材料力学", "工程热力学"], "大三": ["农业建筑", "农业生物环境", "新能源工程"], "大四": ["农业企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "南京农业大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082105T",
        "name": "农业水利工程",
        "category": "08 工学",
        "category_icon": "💧",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "农业水利工程专业培养掌握农业水利工程知识的工程师，从事农业水利工程工作。",
        "what_you_learn": "水力学、土力学、农田水利工程、水利工程施工",
        "suitable_for": "对农业水利工程有兴趣的学生。",
        "career_outlook": "水利部门、农业企业等对农业水利工程人才有需求。",
        "xuefeng_comment": "农业水利工程是农业工程类专业，就业稳定。建议对农业水利有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["水力学", "土力学", "测量学"], "大三": ["农田水利工程", "水利工程施工"], "大四": ["水利企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "河海大学", "西北农林科技大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082201T",
        "name": "森林工程",
        "category": "08 工学",
        "category_icon": "🌲",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "森林工程专业培养掌握森林工程知识的工程师，从事森林工程和林业机械工作。",
        "what_you_learn": "森林工程机械、林区道路工程、木材生产技术、林业工程",
        "suitable_for": "对森林工程有兴趣的学生。",
        "career_outlook": "林业企业等对森林工程人才有需求。",
        "xuefeng_comment": "森林工程是林业工程类专业，就业稳定。建议对林业有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["理论力学", "材料力学", "机械设计基础"], "大三": ["森林工程机械", "林区道路工程", "木材生产技术"], "大四": ["林业企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["东北林业大学", "南京林业大学", "北京林业大学"], "international": []}
    },
    {
        "code": "082202T",
        "name": "木材科学与工程",
        "category": "08 工学",
        "category_icon": "🪵",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "木材科学与工程专业培养掌握木材科学与工程知识的工程师，从事木材加工和利用工作。",
        "what_you_learn": "木材学、木材加工工艺、木材干燥、人造板工艺",
        "suitable_for": "对木材科学与工程有兴趣的学生。",
        "career_outlook": "木材加工企业等对木材科学与工程人才有需求。",
        "xuefeng_comment": "木材科学与工程是林业工程类专业，就业稳定。建议对木材加工有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "木材学"], "大二": ["物理化学、木材加工工艺"], "大三": ["木材干燥", "人造板工艺"], "大四": ["木材企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京林业大学", "东北林业大学", "北京林业大学"], "international": []}
    },
    {
        "code": "082203T",
        "name": "林产化工",
        "category": "08 工学",
        "category_icon": "🌲",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "林产化工专业培养掌握林产化工知识的工程师，从事林产化工生产工作。",
        "what_you_learn": "林产化工工艺、林产化学品、植物纤维化学、化工原理",
        "suitable_for": "对林产化工有兴趣的学生。",
        "career_outlook": "林业化工企业等对林产化工人才有需求。",
        "xuefeng_comment": "林产化工是林业工程类专业，就业稳定。建议对林产化工有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "工程制图"], "大二": ["物理化学", "化工原理", "植物纤维化学"], "大三": ["林产化工工艺", "林产化学品"], "大四": ["林业化工企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京林业大学", "东北林业大学", "北京林业大学"], "international": []}
    },
    {
        "code": "082204T",
        "name": "林业工程类",
        "category": "08 工学",
        "category_icon": "🌲",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "林业工程类专业培养掌握林业工程知识的人才，从事林业工程相关工作。",
        "what_you_learn": "森林工程机械、木材加工工艺、林产化工等",
        "suitable_for": "对林业工程有兴趣的学生。",
        "career_outlook": "林业企业等对林业工程人才有需求。",
        "xuefeng_comment": "林业工程类是大类招生，后期分专业。建议对林业有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["理论力学", "材料力学", "机械设计基础"], "大三": ["专业课程"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京林业大学", "东北林业大学", "北京林业大学"], "international": []}
    },
    {
        "code": "082301T",
        "name": "环境科学与工程",
        "category": "08 工学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-22k",
        "overview": "环境科学与工程专业培养掌握环境科学与工程知识的工程师，从事环境保护工作。",
        "what_you_learn": "环境科学、环境工程学、环境监测、环境影响评价、水污染控制工程",
        "suitable_for": "对环境保护有兴趣的学生。",
        "career_outlook": "环保部门、环保企业等对环境科学与工程人才有需求。",
        "xuefeng_comment": "环境科学与工程是环境科学与工程类专业，就业稳定。建议对环保有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "环境科学导论"], "大二": ["物理化学", "环境化学", "环境监测"], "大三": ["环境工程学", "水污染控制工程", "环境影响评价"], "大四": ["环保企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "浙江大学", "南京大学"], "international": ["加州大学伯克利分校", "斯坦福大学"]}
    },
    {
        "code": "082302T",
        "name": "环境工程",
        "category": "08 工学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-22k",
        "overview": "环境工程专业培养掌握环境工程知识的工程师，从事环境工程设计和建设工作。",
        "what_you_learn": "水污染控制工程、大气污染控制工程、固体废物处理工程、环境监测",
        "suitable_for": "对环境工程有兴趣的学生。",
        "career_outlook": "环保企业、市政部门等对环境工程人才有需求。",
        "xuefeng_comment": "环境工程是环境科学与工程类专业，就业稳定。建议对环境工程有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "工程制图"], "大二": ["物理化学", "水力学", "环境监测"], "大三": ["水污染控制工程", "大气污染控制工程", "固体废物处理工程"], "大四": ["环保企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "同济大学", "浙江大学", "哈尔滨工业大学"], "international": ["加州大学伯克利分校", "斯坦福大学"]}
    },
    {
        "code": "082303T",
        "name": "环境科学",
        "category": "08 工学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "环境科学专业培养掌握环境科学知识的人才，从事环境科学研究和管理工作。",
        "what_you_learn": "环境化学、环境生物学、环境监测、环境影响评价、环境规划",
        "suitable_for": "对环境科学有兴趣的学生。",
        "career_outlook": "环保部门、科研机构等对环境科学人才有需求。",
        "xuefeng_comment": "环境科学是环境科学与工程类专业，就业稳定。建议对环境科学有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "环境科学导论"], "大二": ["物理化学", "环境化学", "环境生物学"], "大三": ["环境监测", "环境影响评价", "环境规划"], "大四": ["环保部门实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "浙江大学", "清华大学"], "international": ["加州大学伯克利分校", "斯坦福大学"]}
    },
    {
        "code": "082304T",
        "name": "环境生态工程",
        "category": "08 工学",
        "category_icon": "🌿",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "环境生态工程专业培养掌握环境生态工程知识的工程师，从事生态修复和生态工程工作。",
        "what_you_learn": "生态学、生态工程学、环境生物学、生态监测、生态修复技术",
        "suitable_for": "对环境生态工程有兴趣的学生。",
        "career_outlook": "环保企业、生态修复企业等对环境生态工程人才有需求。",
        "xuefeng_comment": "环境生态工程是环境科学与工程类专业，就业稳定。建议对生态工程有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "植物学"], "大二": ["生态学", "环境生物学", "生态监测"], "大三": ["生态工程学", "生态修复技术"], "大四": ["生态企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "南京大学", "浙江大学", "北京师范大学"], "international": ["加州大学伯克利分校", "斯坦福大学"]}
    },
    {
        "code": "082305T",
        "name": "环保设备工程",
        "category": "08 工学",
        "category_icon": "🛠️",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "环保设备工程专业培养掌握环保设备知识的工程师，从事环保设备设计和生产工作。",
        "what_you_learn": "环保设备原理、环保设备设计、机械设计、环境工程学",
        "suitable_for": "对环保设备工程有兴趣的学生。",
        "career_outlook": "环保设备企业等对环保设备工程人才有需求。",
        "xuefeng_comment": "环保设备工程是环境科学与工程类专业，就业稳定。建议对环保设备有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "工程制图", "工程力学"], "大二": ["理论力学", "材料力学", "机械设计基础"], "大三": ["环保设备原理", "环保设备设计"], "大四": ["环保设备企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["华中科技大学", "湖南大学", "同济大学"], "international": []}
    },
    {
        "code": "082306T",
        "name": "资源环境科学",
        "category": "08 工学",
        "category_icon": "🌍",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "资源环境科学专业培养掌握资源环境科学知识的人才，从事资源利用和环境保护工作。",
        "what_you_learn": "资源科学、环境科学、环境监测、资源利用技术",
        "suitable_for": "对资源环境科学有兴趣的学生。",
        "career_outlook": "环保部门、资源企业等对资源环境科学人才有需求。",
        "xuefeng_comment": "资源环境科学是环境科学与工程类专业，就业稳定。建议对资源环境有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "植物学"], "大二": ["资源科学", "环境科学", "环境监测"], "大三": ["资源利用技术"], "大四": ["资源企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["南京农业大学", "浙江大学", "中国农业大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082307T",
        "name": "水质科学与技术",
        "category": "08 工学",
        "category_icon": "💧",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "水质科学与技术专业培养掌握水质科学与技术知识的人才，从事水处理和水质监测工作。",
        "what_you_learn": "水处理工程、水质监测、水分析化学、水力学",
        "suitable_for": "对水质科学与技术有兴趣的学生。",
        "career_outlook": "水厂、水处理企业等对水质科学与技术人才有需求。",
        "xuefeng_comment": "水质科学与技术是环境科学与工程类专业，就业稳定。建议对水质有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "分析化学"], "大二": ["水分析化学", "水力学", "环境化学"], "大三": ["水处理工程", "水质监测"], "大四": ["水厂实习", "毕业论文"]},
        "top_universities": {"domestic": ["哈尔滨工业大学", "同济大学", "重庆大学"], "international": []}
    },
    {
        "code": "082401T",
        "name": "生物医学工程",
        "category": "08 工学",
        "category_icon": "🏥",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-28k",
        "overview": "生物医学工程专业培养掌握生物医学工程知识的工程师，从事医疗设备研发和医疗技术工作。",
        "what_you_learn": "生物医学传感器、医学成像、生物信号处理、医疗仪器",
        "suitable_for": "对生物医学工程有兴趣的学生。",
        "career_outlook": "医疗企业、医院等对生物医学工程人才有需求。",
        "xuefeng_comment": "生物医学工程是生物医学工程类专业，就业非常好。建议对医疗设备有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "人体解剖学"], "大二": ["生理学", "电路分析", "电子技术", "信号与系统"], "大三": ["生物医学传感器", "医学成像", "生物信号处理"], "大四": ["医疗企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "东南大学", "上海交通大学", "浙江大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "082402T",
        "name": "假肢矫形工程",
        "category": "08 工学",
        "category_icon": "🦾",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-24k",
        "overview": "假肢矫形工程专业培养掌握假肢矫形工程知识的人才，从事假肢和矫形器设计工作。",
        "what_you_learn": "人体解剖学、生物力学、假肢学、矫形器学",
        "suitable_for": "对假肢矫形工程有兴趣的学生。",
        "career_outlook": "康复医院、假肢企业等对假肢矫形工程人才有需求。",
        "xuefeng_comment": "假肢矫形工程是生物医学工程类专业，就业稳定。建议对康复工程有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "人体解剖学"], "大二": ["生理学", "生物力学", "材料力学"], "大三": ["假肢学", "矫形器学"], "大四": ["康复医院实习", "毕业论文"]},
        "top_universities": {"domestic": ["首都医科大学", "上海理工大学"], "international": []}
    },
    {
        "code": "082403T",
        "name": "临床工程技术",
        "category": "08 工学",
        "category_icon": "🏥",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-24k",
        "overview": "临床工程技术专业培养掌握临床工程技术知识的人才，从事医疗设备管理和维护工作。",
        "what_you_learn": "医疗设备、医院设备管理、生物医学传感器、电子技术",
        "suitable_for": "对临床工程技术有兴趣的学生。",
        "career_outlook": "医院、医疗企业等对临床工程技术人才有需求。",
        "xuefeng_comment": "临床工程技术是生物医学工程类专业，就业稳定。建议对医疗设备管理有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "人体解剖学"], "大二": ["生理学", "电路分析", "电子技术"], "大三": ["医疗设备", "医院设备管理"], "大四": ["医院实习", "毕业论文"]},
        "top_universities": {"domestic": ["首都医科大学"], "international": []}
    },
    {
        "code": "082501T",
        "name": "食品科学与工程",
        "category": "08 工学",
        "category_icon": "🍎",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-22k",
        "overview": "食品科学与工程专业培养掌握食品科学与工程知识的工程师，从事食品生产和研发工作。",
        "what_you_learn": "食品化学、食品微生物学、食品工程原理、食品工艺学",
        "suitable_for": "对食品科学与工程有兴趣的学生。",
        "career_outlook": "食品企业等对食品科学与工程人才有需求。",
        "xuefeng_comment": "食品科学与工程是食品科学与工程类专业，就业稳定。建议对食品有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "分析化学"], "大二": ["物理化学", "食品化学", "食品微生物学"], "大三": ["食品工程原理", "食品工艺学"], "大四": ["食品企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "江南大学", "华南理工大学", "浙江大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082502T",
        "name": "食品质量与安全",
        "category": "08 工学",
        "category_icon": "🥗",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "食品质量与安全专业培养掌握食品质量与安全知识的人才，从事食品质量控制和安全检测工作。",
        "what_you_learn": "食品分析、食品微生物检验、食品质量管理、食品安全法规",
        "suitable_for": "对食品质量与安全有兴趣的学生。",
        "career_outlook": "食品企业、质量监督部门等对食品质量与安全人才有需求。",
        "xuefeng_comment": "食品质量与安全是食品科学与工程类专业，就业稳定。建议对食品安全有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "分析化学"], "大二": ["食品化学", "食品微生物学", "食品分析"], "大三": ["食品微生物检验", "食品质量管理", "食品安全法规"], "大四": ["食品企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国农业大学", "江南大学", "华南理工大学"], "international": ["康奈尔大学"]}
    },
    {
        "code": "082503T",
        "name": "粮食工程",
        "category": "08 工学",
        "category_icon": "🌾",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "粮食工程专业培养掌握粮食工程知识的工程师，从事粮食加工和贮藏工作。",
        "what_you_learn": "粮食加工工艺、粮食贮藏、粮食化学、食品工程原理",
        "suitable_for": "对粮食工程有兴趣的学生。",
        "career_outlook": "粮食企业等对粮食工程人才有需求。",
        "xuefeng_comment": "粮食工程是食品科学与工程类专业，就业稳定。建议对粮食有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "分析化学"], "大二": ["物理化学", "粮食化学"], "大三": ["粮食加工工艺", "粮食贮藏"], "大四": ["粮食企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["江南大学", "河南工业大学"], "international": []}
    },
    {
        "code": "082504T",
        "name": "乳品工程",
        "category": "08 工学",
        "category_icon": "🥛",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "乳品工程专业培养掌握乳品工程知识的工程师，从事乳品加工和生产工作。",
        "what_you_learn": "乳品工艺学、乳品化学、乳品微生物学、食品工程原理",
        "suitable_for": "对乳品工程有兴趣的学生。",
        "career_outlook": "乳品企业等对乳品工程人才有需求。",
        "xuefeng_comment": "乳品工程是食品科学与工程类专业，就业稳定。建议对乳品有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "分析化学"], "大二": ["物理化学", "乳品化学", "乳品微生物学"], "大三": ["乳品工艺学"], "大四": ["乳品企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["东北农业大学", "江南大学"], "international": []}
    },
    {
        "code": "082505T",
        "name": "酿酒工程",
        "category": "08 工学",
        "category_icon": "🍷",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "酿酒工程专业培养掌握酿酒工程知识的工程师，从事酿酒生产和研发工作。",
        "what_you_learn": "酿酒工艺学、酿酒微生物学、酿酒分析、食品工程原理",
        "suitable_for": "对酿酒工程有兴趣的学生。",
        "career_outlook": "酿酒企业等对酿酒工程人才有需求。",
        "xuefeng_comment": "酿酒工程是食品科学与工程类专业，就业稳定。建议对酿酒有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "分析化学"], "大二": ["物理化学", "酿酒微生物学"], "大三": ["酿酒工艺学", "酿酒分析"], "大四": ["酿酒企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["江南大学", "西北农林科技大学"], "international": ["加州大学戴维斯分校"]}
    },
    {
        "code": "082506T",
        "name": "葡萄与葡萄酒工程",
        "category": "08 工学",
        "category_icon": "🍷",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "葡萄与葡萄酒工程专业培养掌握葡萄与葡萄酒工程知识的人才，从事葡萄种植和葡萄酒酿造工作。",
        "what_you_learn": "葡萄栽培学、葡萄酒工艺学、葡萄酒分析、葡萄酒品鉴",
        "suitable_for": "对葡萄与葡萄酒工程有兴趣的学生。",
        "career_outlook": "葡萄酒企业等对相关人才有需求。",
        "xuefeng_comment": "葡萄与葡萄酒工程是食品科学与工程类特色专业，就业稳定。建议对葡萄酒有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "植物学"], "大二": ["物理化学", "葡萄栽培学"], "大三": ["葡萄酒工艺学", "葡萄酒分析"], "大四": ["葡萄酒企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["西北农林科技大学", "中国农业大学"], "international": ["加州大学戴维斯分校"]}
    },
    {
        "code": "082507T",
        "name": "食品营养与检验教育",
        "category": "08 工学",
        "category_icon": "🥗",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "食品营养与检验教育专业培养掌握相关知识的教师，从事食品营养与检验教育工作。",
        "what_you_learn": "食品营养学、食品检验、教育学、心理学",
        "suitable_for": "对食品营养与检验教育有兴趣的学生。",
        "career_outlook": "职业学校等对相关人才有需求。",
        "xuefeng_comment": "食品营养与检验教育是食品科学与工程类教育专业，就业稳定。建议对食品教育有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "食品营养学"], "大二": ["食品检验", "教育学", "心理学"], "大三": ["教育实习准备"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["江南大学"], "international": []}
    },
    {
        "code": "082508T",
        "name": "烹饪与营养教育",
        "category": "08 工学",
        "category_icon": "🍳",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "烹饪与营养教育专业培养掌握烹饪与营养知识的教师，从事烹饪教育工作。",
        "what_you_learn": "烹饪工艺学、食品营养学、教育学、心理学",
        "suitable_for": "对烹饪与营养教育有兴趣的学生。",
        "career_outlook": "职业学校等对相关人才有需求。",
        "xuefeng_comment": "烹饪与营养教育是食品科学与工程类教育专业，就业稳定。建议对烹饪教育有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "食品营养学"], "大二": ["烹饪工艺学", "教育学", "心理学"], "大三": ["教育实习准备"], "大四": ["学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["扬州大学", "四川旅游学院"], "international": []}
    },
    {
        "code": "082601T",
        "name": "建筑学",
        "category": "08 工学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-28k",
        "overview": "建筑学专业培养掌握建筑学知识的建筑师，从事建筑设计和规划工作。",
        "what_you_learn": "建筑设计、建筑史、建筑美术、建筑构造、建筑物理",
        "suitable_for": "对建筑学有兴趣的学生。",
        "career_outlook": "建筑设计企业等对建筑学人才有需求。",
        "xuefeng_comment": "建筑学是建筑类核心专业，就业非常好。建议对建筑设计有兴趣的同学报考。",
        "yearly_courses": {"大一": ["建筑设计基础", "建筑美术", "工程制图"], "大二": ["建筑史", "建筑构造", "建筑设计"], "大三": ["建筑物理", "建筑设计", "城市规划"], "大四": ["建筑设计", "设计院实习"], "大五": ["设计院实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学", "东南大学", "同济大学", "天津大学"], "international": ["麻省理工学院", "哈佛大学"]}
    },
    {
        "code": "082602T",
        "name": "城乡规划",
        "category": "08 工学",
        "category_icon": "🏙️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-26k",
        "overview": "城乡规划专业培养掌握城乡规划知识的人才，从事城乡规划和设计工作。",
        "what_you_learn": "城市规划原理、城市设计、城市规划管理、城市经济学",
        "suitable_for": "对城乡规划有兴趣的学生。",
        "career_outlook": "规划设计企业、规划部门等对城乡规划人才有需求。",
        "xuefeng_comment": "城乡规划是建筑类专业，就业好。建议对城市规划有兴趣的同学报考。",
        "yearly_courses": {"大一": ["建筑设计基础", "城市规划导论", "工程制图"], "大二": ["城市规划原理", "城市设计"], "大三": ["城市规划管理", "城市经济学"], "大四": ["规划院实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学", "东南大学", "同济大学", "天津大学"], "international": ["哈佛大学", "麻省理工学院"]}
    },
    {
        "code": "082603T",
        "name": "风景园林",
        "category": "08 工学",
        "category_icon": "🌳",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-26k",
        "overview": "风景园林专业培养掌握风景园林知识的人才，从事园林设计和景观规划工作。",
        "what_you_learn": "园林史、园林植物学、园林设计、景观规划",
        "suitable_for": "对风景园林有兴趣的学生。",
        "career_outlook": "园林设计企业等对风景园林人才有需求。",
        "xuefeng_comment": "风景园林是建筑类专业，就业好。建议对园林设计有兴趣的同学报考。",
        "yearly_courses": {"大一": ["园林美术", "植物学", "工程制图"], "大二": ["园林史", "园林植物学", "园林设计"], "大三": ["景观规划", "园林设计"], "大四": ["园林院实习", "毕业设计"]},
        "top_universities": {"domestic": ["北京林业大学", "清华大学", "东南大学", "同济大学"], "international": ["哈佛大学"]}
    },
    {
        "code": "082604T",
        "name": "建筑类",
        "category": "08 工学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-28k",
        "overview": "建筑类专业培养掌握建筑知识的人才，从事建筑、规划和园林相关工作。",
        "what_you_learn": "建筑设计、城市规划、园林设计等",
        "suitable_for": "对建筑类有兴趣的学生。",
        "career_outlook": "建筑设计企业等对建筑类人才有需求。",
        "xuefeng_comment": "建筑类是大类招生，后期分专业。建议对建筑有兴趣的同学报考。",
        "yearly_courses": {"大一": ["建筑设计基础", "建筑美术", "工程制图"], "大二": ["专业基础课程"], "大三": ["专业课程"], "大四": ["设计院实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学", "东南大学", "同济大学", "天津大学"], "international": ["麻省理工学院", "哈佛大学"]}
    },
    {
        "code": "082701T",
        "name": "安全工程",
        "category": "08 工学",
        "category_icon": "🛡️",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-24k",
        "overview": "安全工程专业培养掌握安全工程知识的工程师，从事安全生产管理和安全技术工作。",
        "what_you_learn": "安全系统工程、安全管理学、安全评价、安全技术",
        "suitable_for": "对安全工程有兴趣的学生。",
        "career_outlook": "企业安全部门、安全监督部门等对安全工程人才有需求。",
        "xuefeng_comment": "安全工程是安全科学与工程类专业，就业稳定。建议对安全有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "工程力学"], "大二": ["理论力学", "材料力学", "安全系统工程"], "大三": ["安全管理学", "安全评价", "安全技术"], "大四": ["企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国矿业大学", "中南大学", "重庆大学", "西安科技大学"], "international": []}
    },
    {
        "code": "082702T",
        "name": "安全防范工程",
        "category": "08 工学",
        "category_icon": "📹",
        "difficulty": "⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "安全防范工程专业培养掌握安全防范工程知识的工程师，从事安全防范系统设计和安装工作。",
        "what_you_learn": "安全防范技术、安全系统工程、视频监控、入侵检测",
        "suitable_for": "对安全防范工程有兴趣的学生。",
        "career_outlook": "安防企业、安全部门等对安全防范工程人才有需求。",
        "xuefeng_comment": "安全防范工程是安全科学与工程类专业，就业稳定。建议对安全防范有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "大学物理", "工程制图", "电工电子学"], "大二": ["电路分析", "安全系统工程"], "大三": ["安全防范技术", "视频监控", "入侵检测"], "大四": ["安防企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国人民公安大学", "北京理工大学"], "international": []}
    },
    {
        "code": "082801T",
        "name": "生物工程",
        "category": "08 工学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-26k",
        "overview": "生物工程专业培养掌握生物工程知识的工程师，从事生物技术研发和生产工作。",
        "what_you_learn": "微生物学、生物化学、分子生物学、生物反应工程、发酵工程",
        "suitable_for": "对生物工程有兴趣的学生。",
        "career_outlook": "生物技术企业、制药企业等对生物工程人才有需求。",
        "xuefeng_comment": "生物工程是生物工程类专业，就业好。建议对生物工程有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "生物化学"], "大二": ["微生物学", "分子生物学", "化工原理"], "大三": ["生物反应工程", "发酵工程"], "大四": ["生物企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["华东理工大学", "天津大学", "上海交通大学", "清华大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "082802T",
        "name": "生物技术",
        "category": "08 工学",
        "category_icon": "🧬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-26k",
        "overview": "生物技术专业培养掌握生物技术知识的人才，从事生物技术研发和应用工作。",
        "what_you_learn": "分子生物学、细胞生物学、生物化学、基因工程、蛋白质工程",
        "suitable_for": "对生物技术有兴趣的学生。",
        "career_outlook": "生物技术企业、科研机构等对生物技术人才有需求。",
        "xuefeng_comment": "生物技术是生物工程类专业，就业好。建议对生物技术有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "生物化学"], "大二": ["微生物学", "分子生物学", "细胞生物学"], "大三": ["基因工程", "蛋白质工程"], "大四": ["生物企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "上海交通大学", "复旦大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "082803T",
        "name": "生物信息学",
        "category": "08 工学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥10k-28k",
        "overview": "生物信息学专业培养掌握生物信息学知识的人才，从事生物信息分析工作。",
        "what_you_learn": "生物信息学、分子生物学、计算机程序设计、生物统计学",
        "suitable_for": "对生物信息学有兴趣的学生。",
        "career_outlook": "生物技术企业、科研机构等对生物信息学人才有需求。",
        "xuefeng_comment": "生物信息学是生物工程类新兴专业，前景好。建议对生物信息有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "程序设计"], "大二": ["生物化学", "分子生物学", "生物统计学"], "大三": ["生物信息学"], "大四": ["生物企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学", "北京大学", "上海交通大学", "复旦大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    },
    {
        "code": "082804T",
        "name": "生态学",
        "category": "08 工学",
        "category_icon": "🌿",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "生态学专业培养掌握生态学知识的人才，从事生态研究和保护工作。",
        "what_you_learn": "生态学、植物学、动物学、环境科学、生态监测",
        "suitable_for": "对生态学有兴趣的学生。",
        "career_outlook": "科研机构、环保企业等对生态学人才有需求。",
        "xuefeng_comment": "生态学是生物工程类专业，就业稳定。建议对生态学有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "植物学", "动物学"], "大二": ["生态学", "环境科学"], "大三": ["生态监测"], "大四": ["科研机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京师范大学", "北京大学", "兰州大学", "华东师范大学"], "international": ["斯坦福大学"]}
    },
    {
        "code": "082901T",
        "name": "生物制药",
        "category": "08 工学",
        "category_icon": "💊",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-28k",
        "overview": "生物制药专业培养掌握生物制药知识的人才，从事生物制药研发和生产工作。",
        "what_you_learn": "生物制药工艺、微生物学、生物化学、分子生物学、发酵工程",
        "suitable_for": "对生物制药有兴趣的学生。",
        "career_outlook": "制药企业、生物科技企业等对生物制药人才有需求。",
        "xuefeng_comment": "生物制药是生物工程类专业，就业好。建议对生物制药有兴趣的同学报考。",
        "yearly_courses": {"大一": ["高等数学", "无机化学", "有机化学", "生物化学"], "大二": ["微生物学", "分子生物学", "化工原理"], "大三": ["生物制药工艺", "发酵工程"], "大四": ["制药企业实习", "毕业论文"]},
        "top_universities": {"domestic": ["中国药科大学", "沈阳药科大学", "华东理工大学"], "international": ["麻省理工学院", "斯坦福大学"]}
    }
]

count = 0
skipped = 0

for major in majors:
    ok, code = import_major(major)
    if ok:
        print(f"✅ {major['code']} - {major['name']} 成功")
        count += 1
    elif code == 409:
        print(f"⏭️ {major['code']} - {major['name']} 已存在")
        skipped += 1
    else:
        print(f"❌ {major['code']} - {major['name']} 失败")
    time.sleep(0.5)

print(f"\n导入完成！成功 {count}，跳过 {skipped}")
