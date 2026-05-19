"""
系统性补充教育部2024年专业清单中的缺失专业
第三批：文学（小语种）、艺术学
"""
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
    # ========== 05文学-小语种 ==========
    {
        "code": "050202",
        "name": "俄语",
        "category": "05 文学",
        "category_icon": "🇷🇺",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "俄语专业培养掌握俄语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事俄语工作。",
        "what_you_learn": "基础俄语、高级俄语、俄语语法、俄语阅读、俄语听力、俄语口语、俄罗斯文学",
        "suitable_for": "对俄语和俄罗斯文化感兴趣的学生。",
        "career_outlook": "外事外贸企业、俄语地区驻华机构、教育机构、媒体等。",
        "xuefeng_comment": "俄语专业就业稳定，随着中俄贸易发展，需求增长！",
        "yearly_courses": {"大一": ["基础俄语", "俄语语法"], "大二": ["高级俄语", "俄语听力", "俄语口语"], "大三": ["俄语阅读", "俄罗斯文学", "俄语写作"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "黑龙江大学", "南京大学"], "international": ["莫斯科国立大学"]}
    },
    {
        "code": "050203",
        "name": "德语",
        "category": "05 文学",
        "category_icon": "🇩🇪",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "德语专业培养掌握德语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事德语工作。",
        "what_you_learn": "基础德语、高级德语、德语语法、德语听力、德语口语、德国文学",
        "suitable_for": "对德语和德国文化感兴趣的学生。",
        "career_outlook": "德资企业、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "德语专业就业好，德资企业多，需求大！",
        "yearly_courses": {"大一": ["基础德语", "德语语法"], "大二": ["高级德语", "德语听力", "德语口语"], "大三": ["德语阅读", "德国文学", "德语写作"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "同济大学", "南京大学"], "international": ["慕尼黑大学", "柏林自由大学"]}
    },
    {
        "code": "050204",
        "name": "法语",
        "category": "05 文学",
        "category_icon": "🇫🇷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "法语专业培养掌握法语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事法语工作。",
        "what_you_learn": "基础法语、高级法语、法语语法、法语听力、法语口语、法国文学",
        "suitable_for": "对法语和法国文化感兴趣的学生。",
        "career_outlook": "法资企业、外事外贸企业、教育机构、媒体、非洲法语区等。",
        "xuefeng_comment": "法语专业就业好，法国和非洲法语区需求大！",
        "yearly_courses": {"大一": ["基础法语", "法语语法"], "大二": ["高级法语", "法语听力", "法语口语"], "大三": ["法语阅读", "法国文学", "法语写作"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "武汉大学", "南京大学"], "international": ["巴黎高等师范学院", "索邦大学"]}
    },
    {
        "code": "050205",
        "name": "西班牙语",
        "category": "05 文学",
        "category_icon": "🇪🇸",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-22k",
        "overview": "西班牙语专业培养掌握西班牙语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事西班牙语工作。",
        "what_you_learn": "基础西班牙语、高级西班牙语、西班牙语语法、西班牙语听力、西班牙语口语、西班牙文学",
        "suitable_for": "对西班牙语和拉丁美洲文化感兴趣的学生。",
        "career_outlook": "西班牙语国家驻华机构、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "西班牙语专业就业非常好，西班牙语是世界第二大语言，需求大！",
        "yearly_courses": {"大一": ["基础西班牙语", "西班牙语语法"], "大二": ["高级西班牙语", "西班牙语听力", "西班牙语口语"], "大三": ["西班牙语阅读", "西班牙文学", "拉丁美洲文学"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "对外经济贸易大学", "南京大学"], "international": ["马德里康普顿斯大学"]}
    },
    {
        "code": "050206",
        "name": "阿拉伯语",
        "category": "05 文学",
        "category_icon": "🇸🇦",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "阿拉伯语专业培养掌握阿拉伯语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事阿拉伯语工作。",
        "what_you_learn": "基础阿拉伯语、高级阿拉伯语、阿拉伯语语法、阿拉伯语听力、阿拉伯语口语、阿拉伯文学",
        "suitable_for": "对阿拉伯语和阿拉伯文化感兴趣的学生。",
        "career_outlook": "阿拉伯国家驻华机构、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "阿拉伯语专业就业非常好，小语种稀缺人才！",
        "yearly_courses": {"大一": ["基础阿拉伯语", "阿拉伯语语法"], "大二": ["高级阿拉伯语", "阿拉伯语听力", "阿拉伯语口语"], "大三": ["阿拉伯语阅读", "阿拉伯文学", "阿拉伯国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "对外经济贸易大学", "北京大学"], "international": ["开罗大学", "爱资哈尔大学"]}
    },
    {
        "code": "050207",
        "name": "日语",
        "category": "05 文学",
        "category_icon": "🇯🇵",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "日语专业培养掌握日语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事日语工作。",
        "what_you_learn": "基础日语、高级日语、日语语法、日语听力、日语口语、日本文学",
        "suitable_for": "对日语和日本文化感兴趣的学生。",
        "career_outlook": "日资企业、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "日语专业就业好，日资企业多，需求大！",
        "yearly_courses": {"大一": ["基础日语", "日语语法"], "大二": ["高级日语", "日语听力", "日语口语"], "大三": ["日语阅读", "日本文学", "日语写作"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京外国语大学", "上海外国语大学", "北京大学", "南京大学"], "international": ["东京大学", "早稻田大学"]}
    },
    {
        "code": "050208",
        "name": "波斯语",
        "category": "05 文学",
        "category_icon": "🇮🇷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "波斯语专业培养掌握波斯语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事波斯语工作。",
        "what_you_learn": "基础波斯语、高级波斯语、波斯语语法、波斯语听力、波斯语口语、波斯文学",
        "suitable_for": "对波斯语和伊朗文化感兴趣的学生。",
        "career_outlook": "伊朗驻华机构、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "波斯语专业就业非常好，小语种稀缺人才！",
        "yearly_courses": {"大一": ["基础波斯语", "波斯语语法"], "大二": ["高级波斯语", "波斯语听力", "波斯语口语"], "大三": ["波斯语阅读", "波斯文学", "伊朗国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学", "上海外国语大学"], "international": ["德黑兰大学"]}
    },
    {
        "code": "050209",
        "name": "朝鲜语",
        "category": "05 文学",
        "category_icon": "🇰🇷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "朝鲜语专业培养掌握朝鲜语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事朝鲜语工作。",
        "what_you_learn": "基础朝鲜语、高级朝鲜语、朝鲜语语法、朝鲜语听力、朝鲜语口语、韩国文学",
        "suitable_for": "对朝鲜语和韩国文化感兴趣的学生。",
        "career_outlook": "韩资企业、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "朝鲜语专业就业好，韩资企业多！",
        "yearly_courses": {"大一": ["基础朝鲜语", "朝鲜语语法"], "大二": ["高级朝鲜语", "朝鲜语听力", "朝鲜语口语"], "大三": ["朝鲜语阅读", "韩国文学", "朝鲜半岛概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学", "上海外国语大学", "对外经济贸易大学"], "international": ["首尔大学", "延世大学"]}
    },
    {
        "code": "050210",
        "name": "菲律宾语",
        "category": "05 文学",
        "category_icon": "🇵🇭",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "菲律宾语专业培养掌握菲律宾语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事菲律宾语工作。",
        "what_you_learn": "基础菲律宾语、菲律宾语语法、菲律宾语听力、菲律宾语口语、菲律宾文学",
        "suitable_for": "对菲律宾语和菲律宾文化感兴趣的学生。",
        "career_outlook": "菲律宾驻华机构、外事外贸企业、教育机构等。",
        "xuefeng_comment": "菲律宾语专业是小语种，就业面相对较窄但人才稀缺。",
        "yearly_courses": {"大一": ["基础菲律宾语", "菲律宾语语法"], "大二": ["高级菲律宾语", "菲律宾语听力", "菲律宾语口语"], "大三": ["菲律宾语阅读", "菲律宾文学", "菲律宾国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学", "上海外国语大学"], "international": []}
    },
    {
        "code": "050211",
        "name": "梵语巴利语",
        "category": "05 文学",
        "category_icon": "🕉️",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "梵语巴利语专业培养掌握梵语和巴利语语言的高级专门人才，能在学术研究机构、教育部门从事相关研究工作。",
        "what_you_learn": "梵语基础、巴利语基础、梵语语法、梵语文学、印度佛教文献学",
        "suitable_for": "对梵语和印度佛教文化感兴趣，有学术志向的学生。",
        "career_outlook": "高校、科研机构、佛教研究机构等。",
        "xuefeng_comment": "梵语巴利语是超冷门专业，学术性很强，主要在研究领域就业。建议继续深造。",
        "yearly_courses": {"大一": ["梵语基础"], "大二": ["梵语语法", "巴利语基础"], "大三": ["梵语文学", "印度佛教文献学"], "大四": ["研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "中国社会科学院"], "international": ["哈佛大学", "牛津大学"]}
    },
    {
        "code": "050213",
        "name": "印地语",
        "category": "05 文学",
        "category_icon": "🇮🇳",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "印地语专业培养掌握印地语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事印地语工作。",
        "what_you_learn": "基础印地语、高级印地语、印地语语法、印地语听力、印地语口语、印度文学",
        "suitable_for": "对印地语和印度文化感兴趣的学生。",
        "career_outlook": "印度驻华机构、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "印地语专业就业好，小语种稀缺人才！",
        "yearly_courses": {"大一": ["基础印地语", "印地语语法"], "大二": ["高级印地语", "印地语听力", "印地语口语"], "大三": ["印地语阅读", "印度文学", "印度国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学", "上海外国语大学"], "international": ["德里大学"]}
    },
    {
        "code": "050215",
        "name": "老挝语",
        "category": "05 文学",
        "category_icon": "🇱🇦",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "老挝语专业培养掌握老挝语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事老挝语工作。",
        "what_you_learn": "基础老挝语、老挝语语法、老挝语听力、老挝语口语、老挝文学",
        "suitable_for": "对老挝语和老挝文化感兴趣的学生。",
        "career_outlook": "老挝驻华机构、外事外贸企业、教育机构等。",
        "xuefeng_comment": "老挝语专业是小语种稀缺人才！",
        "yearly_courses": {"大一": ["基础老挝语", "老挝语语法"], "大二": ["高级老挝语", "老挝语听力", "老挝语口语"], "大三": ["老挝语阅读", "老挝文学", "老挝国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "云南民族大学"], "international": []}
    },
    {
        "code": "050216",
        "name": "缅甸语",
        "category": "05 文学",
        "category_icon": "🇲🇲",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "缅甸语专业培养掌握缅甸语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事缅甸语工作。",
        "what_you_learn": "基础缅甸语、缅甸语语法、缅甸语听力、缅甸语口语、缅甸文学",
        "suitable_for": "对缅甸语和缅甸文化感兴趣的学生。",
        "career_outlook": "缅甸驻华机构、外事外贸企业、教育机构等。",
        "xuefeng_comment": "缅甸语专业是小语种稀缺人才！",
        "yearly_courses": {"大一": ["基础缅甸语", "缅甸语语法"], "大二": ["高级缅甸语", "缅甸语听力", "缅甸语口语"], "大三": ["缅甸语阅读", "缅甸文学", "缅甸国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "云南民族大学"], "international": []}
    },
    {
        "code": "050218",
        "name": "蒙古语",
        "category": "05 文学",
        "category_icon": "🇲🇳",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-15k",
        "overview": "蒙古语专业培养掌握蒙古语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事蒙古语工作。",
        "what_you_learn": "基础蒙古语、蒙古语语法、蒙古语听力、蒙古语口语、蒙古文学",
        "suitable_for": "对蒙古语和蒙古文化感兴趣的学生。",
        "career_outlook": "蒙古驻华机构、外事外贸企业、教育机构等。",
        "xuefeng_comment": "蒙古语专业是小语种，就业面相对较窄。",
        "yearly_courses": {"大一": ["基础蒙古语", "蒙古语语法"], "大二": ["高级蒙古语", "蒙古语听力", "蒙古语口语"], "大三": ["蒙古语阅读", "蒙古文学", "蒙古国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "内蒙古大学", "黑龙江大学"], "international": []}
    },
    {
        "code": "050220",
        "name": "泰语",
        "category": "05 文学",
        "category_icon": "🇹🇭",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "泰语专业培养掌握泰语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事泰语工作。",
        "what_you_learn": "基础泰语、泰语语法、泰语听力、泰语口语、泰国文学",
        "suitable_for": "对泰语和泰国文化感兴趣的学生。",
        "career_outlook": "泰国驻华机构、外事外贸企业、教育机构、媒体等。",
        "xuefeng_comment": "泰语专业就业好，泰国旅游业发达！",
        "yearly_courses": {"大一": ["基础泰语", "泰语语法"], "大二": ["高级泰语", "泰语听力", "泰语口语"], "大三": ["泰语阅读", "泰国文学", "泰国国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学", "云南民族大学"], "international": ["朱拉隆功大学"]}
    },
    {
        "code": "050221",
        "name": "乌尔都语",
        "category": "05 文学",
        "category_icon": "🇵🇰",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "乌尔都语专业培养掌握乌尔都语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事乌尔都语工作。",
        "what_you_learn": "基础乌尔都语、乌尔都语语法、乌尔都语听力、乌尔都语口语、乌尔都文学",
        "suitable_for": "对乌尔都语和巴基斯坦文化感兴趣的学生。",
        "career_outlook": "巴基斯坦驻华机构、外事外贸企业、教育机构等。",
        "xuefeng_comment": "乌尔都语专业是小语种稀缺人才！",
        "yearly_courses": {"大一": ["基础乌尔都语", "乌尔都语语法"], "大二": ["高级乌尔都语", "乌尔都语听力", "乌尔都语口语"], "大三": ["乌尔都语阅读", "乌尔都文学", "巴基斯坦国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学"], "international": []}
    },
    {
        "code": "050222",
        "name": "希伯来语",
        "category": "05 文学",
        "category_icon": "🇮🇱",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "希伯来语专业培养掌握希伯来语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事希伯来语工作。",
        "what_you_learn": "基础希伯来语、高级希伯来语、希伯来语语法、希伯来语听力、希伯来语口语",
        "suitable_for": "对希伯来语和以色列文化感兴趣的学生。",
        "career_outlook": "以色列驻华机构、外事外贸企业、教育机构等。",
        "xuefeng_comment": "希伯来语专业是稀缺小语种！",
        "yearly_courses": {"大一": ["基础希伯来语", "希伯来语语法"], "大二": ["高级希伯来语", "希伯来语听力", "希伯来语口语"], "大三": ["希伯来语阅读", "以色列概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "北京外国语大学", "上海外国语大学"], "international": ["希伯来大学"]}
    },
    {
        "code": "050223",
        "name": "越南语",
        "category": "05 文学",
        "category_icon": "🇻🇳",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "越南语专业培养掌握越南语语言文学和文化的高级专门人才，能在外事、外贸、教育等部门从事越南语工作。",
        "what_you_learn": "基础越南语、越南语语法、越南语听力、越南语口语、越南文学",
        "suitable_for": "对越南语和越南文化感兴趣的学生。",
        "career_outlook": "越南驻华机构、外事外贸企业、教育机构等。",
        "xuefeng_comment": "越南语专业就业好，随着中越贸易发展，需求增长！",
        "yearly_courses": {"大一": ["基础越南语", "越南语语法"], "大二": ["高级越南语", "越南语听力", "越南语口语"], "大三": ["越南语阅读", "越南文学", "越南国家概况"], "大四": ["翻译实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "云南民族大学", "广西民族大学"], "international": ["河内大学"]}
    },
    {
        "code": "050103T",
        "name": "古典文献学",
        "category": "05 文学",
        "category_icon": "📜",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥5k-12k",
        "overview": "古典文献学专业培养掌握中国古典文献整理和研究能力的专门人才，能在图书馆、博物馆、出版社等机构从事古籍整理和研究工作。",
        "what_you_learn": "古典文献学概论、古籍版本学、古籍整理学、目录学、考据学、中国古代文学",
        "suitable_for": "对古典文献和古籍整理感兴趣，有耐心的学生。",
        "career_outlook": "图书馆、博物馆、出版社古籍部、高校古籍研究所等。",
        "xuefeng_comment": "古典文献学是冷门专业，需要长期积累，建议继续深造。",
        "yearly_courses": {"大一": ["古典文献学概论", "古代汉语", "中国古代文学"], "大二": ["古籍版本学", "目录学", "考据学"], "大三": ["古籍整理学", "古籍保护技术"], "大四": ["图书馆/博物馆实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京大学", "复旦大学", "南京大学", "浙江大学"], "international": []}
    },
    
    # ========== 05文学-艺术学 - 音乐舞蹈 ==========
    {
        "code": "050401",
        "name": "音乐表演",
        "category": "05 文学",
        "category_icon": "🎵",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-20k",
        "overview": "音乐表演专业培养掌握音乐表演技能的艺术人才，能在文艺团体、音乐教育机构从事表演和教学工作。",
        "what_you_learn": "声乐/器乐主科、视唱练耳、乐理、和声、曲式分析、中外音乐史",
        "suitable_for": "有音乐特长，专业技能强的学生。",
        "career_outlook": "文艺团体、音乐院校、艺术培训机构、影视传媒公司等。",
        "xuefeng_comment": "音乐表演专业就业主要在文艺团体和培训机构，需要有真才实学！",
        "yearly_courses": {"大一": ["声乐/器乐主科", "视唱练耳", "乐理", "中外国音乐史"], "大二": ["和声", "曲式分析", "专业主科"], "大三": ["专业主科", "室内乐/合唱", "艺术实践"], "大四": ["毕业音乐会", "毕业论文"]},
        "top_universities": {"domestic": ["中央音乐学院", "上海音乐学院", "中国音乐学院", "武汉音乐学院"], "international": ["茱莉亚音乐学院", "柯蒂斯音乐学院"]}
    },
    {
        "code": "050402",
        "name": "音乐学",
        "category": "05 文学",
        "category_icon": "🎼",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-15k",
        "overview": "音乐学专业培养掌握音乐理论研究和教学能力的专门人才，能在音乐院校、研究机构从事音乐研究和教学工作。",
        "what_you_learn": "音乐学概论、中外音乐史、音乐美学、音乐分析、音乐文献学",
        "suitable_for": "对音乐研究感兴趣，有一定音乐基础的学生。",
        "career_outlook": "音乐院校、研究机构、音乐媒体、出版社等。",
        "xuefeng_comment": "音乐学专业偏理论研究，就业主要在教育和研究领域！",
        "yearly_courses": {"大一": ["音乐学概论", "中外国音乐史", "乐理"], "大二": ["音乐美学", "音乐分析", "音乐文献学"], "大三": ["音乐专题研究", "音乐民族学"], "大四": ["研究机构/学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["中央音乐学院", "上海音乐学院", "中国音乐学院", "南京艺术学院"], "international": ["茱莉亚音乐学院", "柯蒂斯音乐学院"]}
    },
    {
        "code": "050403",
        "name": "作曲与作曲技术理论",
        "category": "05 文学",
        "category_icon": "🎹",
        "difficulty": "⭐⭐⭐⭐",
        "salary_range": "¥7k-22k",
        "overview": "作曲与作曲技术理论专业培养掌握作曲和作曲技术理论的专门人才，能在音乐院校、文艺团体从事作曲和教学工作。",
        "what_you_learn": "作曲主科、和声学、复调音乐、曲式学、配器法、作品分析",
        "suitable_for": "有很强音乐天赋和创作能力的学生。",
        "career_outlook": "音乐院校、文艺团体、影视传媒公司等。",
        "xuefeng_comment": "作曲专业是音乐类最难的专业之一，需要极高的音乐天赋！",
        "yearly_courses": {"大一": ["作曲主科", "和声学", "乐理"], "大二": ["复调音乐", "曲式学", "配器法"], "大三": ["作品分析", "作曲主科"], "大四": ["毕业作品音乐会", "毕业论文"]},
        "top_universities": {"domestic": ["中央音乐学院", "上海音乐学院", "中国音乐学院"], "international": ["茱莉亚音乐学院", "柯蒂斯音乐学院"]}
    },
    {
        "code": "050404",
        "name": "舞蹈表演",
        "category": "05 文学",
        "category_icon": "💃",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-20k",
        "overview": "舞蹈表演专业培养掌握舞蹈表演技能的艺术人才，能在文艺团体从事舞蹈表演工作。",
        "what_you_learn": "芭蕾基训、中国舞基训、舞蹈剧目、舞蹈编导、舞蹈概论",
        "suitable_for": "有舞蹈特长，身体条件好的学生。",
        "career_outlook": "文艺团体、舞蹈院校、艺术培训机构、影视传媒公司等。",
        "xuefeng_comment": "舞蹈表演专业需要扎实的基本功，就业主要在文艺团体！",
        "yearly_courses": {"大一": ["芭蕾基训", "中国舞基训", "舞蹈概论"], "大二": ["舞蹈剧目", "舞蹈编导基础"], "大三": ["舞蹈剧目", "舞蹈技术技巧"], "大四": ["毕业舞蹈演出", "毕业论文"]},
        "top_universities": {"domestic": ["北京舞蹈学院", "上海戏剧学院", "中央民族大学"], "international": ["纽约大学 Tisch 艺术学院"]}
    },
    {
        "code": "050405",
        "name": "舞蹈学",
        "category": "05 文学",
        "category_icon": "🩰",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-15k",
        "overview": "舞蹈学专业培养掌握舞蹈理论和教学能力的专门人才，能在舞蹈院校、研究机构从事舞蹈研究和教学工作。",
        "what_you_learn": "舞蹈概论、中外舞蹈史、舞蹈教育学、舞蹈编导理论、舞蹈美学",
        "suitable_for": "对舞蹈研究感兴趣，有一定舞蹈基础的学生。",
        "career_outlook": "舞蹈院校、研究机构、舞蹈媒体等。",
        "xuefeng_comment": "舞蹈学专业偏理论研究，就业主要在教育和研究领域！",
        "yearly_courses": {"大一": ["舞蹈概论", "中外舞蹈史", "舞蹈基训"], "大二": ["舞蹈教育学", "舞蹈编导理论"], "大三": ["舞蹈美学", "舞蹈专题研究"], "大四": ["学校/研究机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京舞蹈学院", "上海戏剧学院", "中央民族大学", "南京艺术学院"], "international": []}
    },
    {
        "code": "050406",
        "name": "舞蹈编导",
        "category": "05 文学",
        "category_icon": "🎭",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "舞蹈编导专业培养掌握舞蹈编导理论和技能的艺术人才，能在文艺团体从事舞蹈创作和导演工作。",
        "what_you_learn": "舞蹈编导理论、舞蹈创作、舞蹈结构分析、舞台导演基础、舞蹈作品分析",
        "suitable_for": "有舞蹈基础，有创作能力的学生。",
        "career_outlook": "文艺团体、影视传媒公司、舞蹈院校等。",
        "xuefeng_comment": "舞蹈编导专业需要有创作能力，就业主要在文艺团体！",
        "yearly_courses": {"大一": ["舞蹈概论", "舞蹈基训", "舞蹈编导理论"], "大二": ["舞蹈创作", "舞蹈结构分析"], "大三": ["舞台导演基础", "舞蹈作品分析"], "大四": ["毕业作品创作", "毕业论文"]},
        "top_universities": {"domestic": ["北京舞蹈学院", "上海戏剧学院", "中央民族大学"], "international": []}
    },
    {
        "code": "050407T",
        "name": "舞蹈教育",
        "category": "05 文学",
        "category_icon": "🏫",
        "difficulty": "⭐⭐",
        "salary_range": "¥5k-14k",
        "overview": "舞蹈教育专业培养掌握舞蹈教育理论和方法的专门人才，能在舞蹈院校、艺术培训机构从事舞蹈教学工作。",
        "what_you_learn": "舞蹈教育学、舞蹈教学法、舞蹈基训、中国舞教学、芭蕾舞教学",
        "suitable_for": "对舞蹈教育感兴趣，有舞蹈基础的学生。",
        "career_outlook": "舞蹈院校、艺术培训机构、社区文化中心等。",
        "xuefeng_comment": "舞蹈教育专业就业稳定，舞蹈培训市场需求大！",
        "yearly_courses": {"大一": ["舞蹈概论", "舞蹈基训", "舞蹈教育学"], "大二": ["舞蹈教学法", "中国舞教学"], "大三": ["芭蕾舞教学", "舞蹈教学实践"], "大四": ["学校/培训机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["北京舞蹈学院", "四川师范大学", "云南艺术学院"], "international": []}
    },
    
    # ========== 05文学-艺术学 - 戏剧影视 ==========
    {
        "code": "050501",
        "name": "戏剧影视文学",
        "category": "05 文学",
        "category_icon": "🎬",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "戏剧影视文学专业培养掌握戏剧影视文学创作和研究的专门人才，能在影视制作机构、剧院等从事剧本创作和编辑工作。",
        "what_you_learn": "戏剧概论、影视概论、剧本写作、中外戏剧史、中外电影史、影视评论",
        "suitable_for": "对戏剧影视创作感兴趣，有文学功底的学生。",
        "career_outlook": "影视制作公司、剧院、电视台、出版社等。",
        "xuefeng_comment": "戏剧影视文学专业就业需要作品和才华！",
        "yearly_courses": {"大一": ["戏剧概论", "影视概论", "文学概论"], "大二": ["剧本写作", "中外戏剧史"], "大三": ["中外电影史", "影视评论"], "大四": ["影视机构实习", "毕业论文"]},
        "top_universities": {"domestic": ["中央戏剧学院", "北京电影学院", "上海戏剧学院", "中国戏曲学院"], "international": ["纽约大学 Tisch 艺术学院"]}
    },
    {
        "code": "050502",
        "name": "广播电视编导",
        "category": "05 文学",
        "category_icon": "📺",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "广播电视编导专业培养掌握广播电视节目策划和编导能力的专门人才，能在广播电视机构从事节目策划和导演工作。",
        "what_you_learn": "广播电视概论、节目策划、导演基础、摄像技术、剪辑艺术、广播电视文稿写作",
        "suitable_for": "对广播电视节目制作感兴趣，有创意能力的学生。",
        "career_outlook": "电视台、网络视听平台、影视制作公司等。",
        "xuefeng_comment": "广播电视编导专业就业好，新媒体行业发展迅速！",
        "yearly_courses": {"大一": ["广播电视概论", "摄像基础", "导演基础"], "大二": ["节目策划", "广播电视文稿写作"], "大三": ["剪辑艺术", "节目制作实践"], "大四": ["电视台/影视公司实习", "毕业作品"]},
        "top_universities": {"domestic": ["中国传媒大学", "浙江传媒学院", "上海戏剧学院", "北京电影学院"], "international": []}
    },
    {
        "code": "050503",
        "name": "戏剧影视导演",
        "category": "05 文学",
        "category_icon": "🎭",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "戏剧影视导演专业培养掌握戏剧和影视导演理论和技能的专门人才，能在剧院、影视制作机构从事导演工作。",
        "what_you_learn": "导演基础、戏剧导演、影视导演、表演基础、舞台美术、剧本分析",
        "suitable_for": "对导演工作感兴趣，有艺术天赋和创意能力的学生。",
        "career_outlook": "剧院、影视制作公司、电视台、网络视听平台等。",
        "xuefeng_comment": "戏剧影视导演是艺术类核心专业，需要很强的综合素质！",
        "yearly_courses": {"大一": ["导演基础", "表演基础", "戏剧概论"], "大二": ["戏剧导演", "剧本分析"], "大三": ["影视导演", "舞台美术"], "大四": ["毕业导演作品", "毕业论文"]},
        "top_universities": {"domestic": ["中央戏剧学院", "北京电影学院", "上海戏剧学院"], "international": ["纽约大学 Tisch 艺术学院"]}
    },
    {
        "code": "050504",
        "name": "戏剧影视美术设计",
        "category": "05 文学",
        "category_icon": "🎨",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "戏剧影视美术设计专业培养掌握舞台和影视美术设计理论和技能的专门人才，能在剧院、影视制作机构从事美术设计工作。",
        "what_you_learn": "舞台美术设计、影视美术设计、灯光设计、服装设计、化妆造型、道具设计",
        "suitable_for": "对美术设计感兴趣，有艺术功底的学生。",
        "career_outlook": "剧院、影视制作公司、电视台、演出公司等。",
        "xuefeng_comment": "戏剧影视美术设计是技术性强的艺术专业！",
        "yearly_courses": {"大一": ["舞台美术设计基础", "绘画基础"], "大二": ["影视美术设计", "灯光设计"], "大三": ["服装设计", "化妆造型"], "大四": ["毕业设计", "实习"]},
        "top_universities": {"domestic": ["中央戏剧学院", "北京电影学院", "上海戏剧学院"], "international": []}
    },
    {
        "code": "050505",
        "name": "录音艺术",
        "category": "05 文学",
        "category_icon": "🎙️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-22k",
        "overview": "录音艺术专业培养掌握录音艺术和技术理论的专门人才，能在广播影视机构从事录音和音响工程工作。",
        "what_you_learn": "录音艺术概论、录音技术、音响工程、声音设计、音频编辑、音乐录音",
        "suitable_for": "对录音艺术感兴趣，有音乐基础的学生。",
        "career_outlook": "广播电视台、影视制作公司、音乐制作公司、演出公司等。",
        "xuefeng_comment": "录音艺术专业是技术性强的艺术专业，人才稀缺！",
        "yearly_courses": {"大一": ["录音艺术概论", "音乐基础", "声学基础"], "大二": ["录音技术", "音频编辑"], "大三": ["音响工程", "声音设计"], "大四": ["录音棚/影视公司实习", "毕业作品"]},
        "top_universities": {"domestic": ["中国传媒大学", "北京电影学院", "上海戏剧学院"], "international": []}
    },
    {
        "code": "050506",
        "name": "播音与主持艺术",
        "category": "05 文学",
        "category_icon": "🎤",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-22k",
        "overview": "播音与主持艺术专业培养掌握播音和主持理论和技能的专门人才，能在广播电视机构从事播音和主持工作。",
        "what_you_learn": "播音主持概论、播音基础、主持艺术、语言表达、形体训练、广播电视节目策划",
        "suitable_for": "对播音主持感兴趣，语言表达能力强，形象气质好的学生。",
        "career_outlook": "广播电视台、网络视听平台、婚庆公司、会议活动主持等。",
        "xuefeng_comment": "播音与主持艺术专业就业好，需要好的形象气质和语言表达能力！",
        "yearly_courses": {"大一": ["播音主持概论", "播音基础", "语言表达"], "大二": ["主持艺术", "形体训练"], "大三": ["广播电视节目策划", "播音主持实践"], "大四": ["广播电视台实习", "毕业作品"]},
        "top_universities": {"domestic": ["中国传媒大学", "浙江传媒学院", "上海戏剧学院", "华东师范大学"], "international": []}
    },
    {
        "code": "050507",
        "name": "动画",
        "category": "05 文学",
        "category_icon": "🎬",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "动画专业培养掌握动画创作和制作技能的专门人才，能在动画制作机构、游戏公司等从事动画创作和制作工作。",
        "what_you_learn": "动画概论、动画美术设计、二维动画制作、三维动画制作、动画分镜头设计、动画运动规律",
        "suitable_for": "对动画创作感兴趣，有绘画基础的学生。",
        "career_outlook": "动画制作公司、游戏公司、影视制作公司、广告公司等。",
        "xuefeng_comment": "动画专业就业好，游戏动漫行业发展迅速！",
        "yearly_courses": {"大一": ["动画概论", "绘画基础", "动画美术设计"], "大二": ["二维动画制作", "动画分镜头设计"], "大三": ["三维动画制作", "动画运动规律"], "大四": ["动画公司实习", "毕业作品"]},
        "top_universities": {"domestic": ["北京电影学院", "中国传媒大学", "四川美术学院", "广州美术学院"], "international": ["加州艺术学院", "萨凡纳艺术与设计学院"]}
    },
    {
        "code": "050508",
        "name": "影视摄影与制作",
        "category": "05 文学",
        "category_icon": "📷",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥8k-25k",
        "overview": "影视摄影与制作专业培养掌握影视摄影和制作技能的专门人才，能在影视制作机构从事摄影和后期制作工作。",
        "what_you_learn": "摄影基础、摄像技术、影视剪辑、影视特效、影视调色、影视照明",
        "suitable_for": "对影视摄影制作感兴趣，有审美能力的学生。",
        "career_outlook": "影视制作公司、电视台、广告公司、网络视听平台等。",
        "xuefeng_comment": "影视摄影与制作专业就业好，需要好的审美和技术！",
        "yearly_courses": {"大一": ["摄影基础", "摄像技术基础"], "大二": ["影视剪辑", "影视照明"], "大三": ["影视特效", "影视调色"], "大四": ["影视公司实习", "毕业作品"]},
        "top_universities": {"domestic": ["北京电影学院", "中国传媒大学", "浙江传媒学院"], "international": []}
    },
    
    # ========== 05文学-艺术学 - 美术设计 ==========
    {
        "code": "050701",
        "name": "艺术设计学",
        "category": "05 文学",
        "category_icon": "🖌️",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "艺术设计学专业培养掌握艺术设计理论和历史的专门人才，能在设计研究机构、高等院校从事设计研究和教学工作。",
        "what_you_learn": "设计概论、中外设计史、设计美学、设计批评、设计管理",
        "suitable_for": "对设计理论和历史感兴趣的学生。",
        "career_outlook": "设计研究机构、高等院校、设计媒体等。",
        "xuefeng_comment": "艺术设计学专业偏理论研究，适合继续深造！",
        "yearly_courses": {"大一": ["设计概论", "艺术概论", "绘画基础"], "大二": ["中外设计史", "设计美学"], "大三": ["设计批评", "设计管理"], "大四": ["研究机构/学校实习", "毕业论文"]},
        "top_universities": {"domestic": ["清华大学美术学院", "中央美术学院", "中国美术学院"], "international": ["皇家艺术学院", "帕森斯设计学院"]}
    },
    {
        "code": "050704",
        "name": "产品设计",
        "category": "05 文学",
        "category_icon": "💎",
        "difficulty": "⭐⭐",
        "salary_range": "¥7k-20k",
        "overview": "产品设计专业培养掌握产品设计理论和技能的专门人才，能在设计机构、企业设计部门从事产品设计工作。",
        "what_you_learn": "产品设计概论、产品造型设计、产品材料与工艺、人机工程学、产品模型制作",
        "suitable_for": "对产品设计感兴趣，有创新思维的学生。",
        "career_outlook": "设计机构、企业设计部门、制造业等。",
        "xuefeng_comment": "产品设计专业就业好，制造业转型升级需要大量设计人才！",
        "yearly_courses": {"大一": ["设计概论", "绘画基础", "产品设计概论"], "大二": ["产品造型设计", "人机工程学"], "大三": ["产品材料与工艺", "产品模型制作"], "大四": ["设计机构/企业实习", "毕业设计"]},
        "top_universities": {"domestic": ["清华大学美术学院", "中央美术学院", "中国美术学院", "江南大学"], "international": ["皇家艺术学院", "帕森斯设计学院"]}
    },
    {
        "code": "050706",
        "name": "公共艺术",
        "category": "05 文学",
        "category_icon": "🏛️",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥7k-18k",
        "overview": "公共艺术专业培养掌握公共艺术设计和创作技能的专门人才，能在城市设计、景观设计等领域从事公共艺术创作工作。",
        "what_you_learn": "公共艺术概论、公共艺术设计、环境雕塑、公共设施设计、公共艺术创作",
        "suitable_for": "对公共艺术感兴趣，有空间想象力学生。",
        "career_outlook": "规划设计院、景观设计公司、城市建设部门等。",
        "xuefeng_comment": "公共艺术专业就业好，城市美化需求增长！",
        "yearly_courses": {"大一": ["公共艺术概论", "绘画基础", "雕塑基础"], "大二": ["公共艺术设计", "环境雕塑"], "大三": ["公共设施设计", "公共艺术创作"], "大四": ["设计机构实习", "毕业设计"]},
        "top_universities": {"domestic": ["中央美术学院", "中国美术学院", "广州美术学院"], "international": []}
    },
    {
        "code": "050707",
        "name": "工艺美术",
        "category": "05 文学",
        "category_icon": "🏺",
        "difficulty": "⭐⭐",
        "salary_range": "¥6k-18k",
        "overview": "工艺美术专业培养掌握传统工艺美术设计和制作技能的专门人才，能在工艺美术行业从事传统工艺传承和创新工作。",
        "what_you_learn": "工艺美术概论、中国传统工艺、陶瓷艺术、漆画艺术、金属工艺、纤维艺术",
        "suitable_for": "对传统工艺美术感兴趣，有动手能力的学生。",
        "career_outlook": "工艺美术企业、博物馆、文创产业、艺术品市场等。",
        "xuefeng_comment": "工艺美术专业就业稳定，非遗传承受国家重视！",
        "yearly_courses": {"大一": ["工艺美术概论", "中国传统工艺"], "大二": ["陶瓷艺术", "漆画艺术"], "大三": ["金属工艺", "纤维艺术"], "大四": ["工艺美术企业实习", "毕业作品"]},
        "top_universities": {"domestic": ["中央美术学院", "中国美术学院", "清华大学美术学院", "广州美术学院"], "international": []}
    },
    {
        "code": "050708T",
        "name": "数字媒体艺术",
        "category": "05 文学",
        "category_icon": "💻",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "数字媒体艺术专业培养掌握数字媒体艺术设计和创作技能的专门人才，能在互联网、游戏、影视等领域从事数字媒体艺术创作工作。",
        "what_you_learn": "数字媒体艺术概论、数字绘画、界面设计、交互设计、三维动画、影视特效",
        "suitable_for": "对数字媒体艺术感兴趣，有创意和技术能力的学生。",
        "career_outlook": "互联网公司、游戏公司、影视制作公司、广告公司等。",
        "xuefeng_comment": "数字媒体艺术专业就业非常好，互联网游戏行业需求大！强烈推荐！",
        "yearly_courses": {"大一": ["数字媒体艺术概论", "数字绘画", "设计基础"], "大二": ["界面设计", "交互设计基础"], "大三": ["三维动画", "影视特效"], "大四": ["互联网/游戏公司实习", "毕业作品"]},
        "top_universities": {"domestic": ["中国传媒大学", "北京电影学院", "清华大学美术学院", "浙江大学"], "international": ["加州艺术学院"]}
    },
    {
        "code": "050709T",
        "name": "艺术与科技",
        "category": "05 文学",
        "category_icon": "🚀",
        "difficulty": "⭐⭐⭐",
        "salary_range": "¥9k-25k",
        "overview": "艺术与科技专业培养掌握艺术与科技交叉领域设计和创作技能的专门人才，能在文化创意产业从事跨领域创作工作。",
        "what_you_learn": "艺术与科技概论、交互设计、媒体艺术、虚拟现实技术、数字娱乐设计",
        "suitable_for": "对艺术与科技交叉领域感兴趣，有创新思维的学生。",
        "career_outlook": "互联网公司、游戏公司、VR/AR企业、展览展示公司等。",
        "xuefeng_comment": "艺术与科技专业是新兴交叉学科，就业前景好！",
        "yearly_courses": {"大一": ["艺术与科技概论", "交互设计基础", "数字艺术基础"], "大二": ["媒体艺术", "虚拟现实技术"], "大三": ["数字娱乐设计", "跨媒体创作"], "大四": ["科技/文化企业实习", "毕业作品"]},
        "top_universities": {"domestic": ["中国传媒大学", "中央美术学院", "上海戏剧学院"], "international": []}
    }
]

count = 0
skipped = 0

print("开始补充文学、艺术学类专业（小语种、戏剧影视、美术设计）...")
print("="*60)

for major in majors:
    ok, code = import_major(major)
    if ok:
        print(f"✅ {major['code']} - {major['name']}")
        count += 1
    elif code == 409:
        print(f"⏭️ {major['code']} - {major['name']} (已存在)")
        skipped += 1
    else:
        print(f"❌ {major['code']} - {major['name']}")
    time.sleep(0.3)

print("="*60)
print(f"✅ 成功添加 {count} 个专业")
print(f"⏭️ 跳过 {skipped} 个(已存在)")
