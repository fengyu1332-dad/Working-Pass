import os
import sys
import json

# 安装supabase库
try:
    from supabase import create_client, Client
except ImportError:
    print("安装supabase库...")
    os.system(f"{sys.executable} -m pip install supabase")
    from supabase import create_client, Client

# Supabase配置
SUPABASE_URL = "https://djteatwxjlnbjylynvjh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4"

# 初始化Supabase客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables():
    """创建数据库表结构"""
    print("正在创建数据库表...")
    
    # 创建majors表
    try:
        result = supabase.rpc('create_table', {
            'name': 'majors',
            'columns': [
                {'name': 'code', 'type': 'varchar(20)', 'constraints': 'unique not null'},
                {'name': 'name', 'type': 'varchar(100)', 'constraints': 'not null'},
                {'name': 'category', 'type': 'varchar(50)', 'constraints': 'not null'},
                {'name': 'category_icon', 'type': 'varchar(10)'},
                {'name': 'difficulty', 'type': 'varchar(20)'},
                {'name': 'salary_range', 'type': 'varchar(50)'},
                {'name': 'overview', 'type': 'text'},
                {'name': 'what_you_learn', 'type': 'text'},
                {'name': 'suitable_for', 'type': 'text'},
                {'name': 'career_outlook', 'type': 'text'},
                {'name': 'xuefeng_comment', 'type': 'text'},
                {'name': 'yearly_courses', 'type': 'jsonb'},
                {'name': 'top_universities', 'type': 'jsonb'},
                {'name': 'view_count', 'type': 'int', 'default': '0'},
                {'name': 'status', 'type': 'varchar(20)', 'default': "'active'"},
                {'name': 'created_at', 'type': 'timestamp', 'default': 'now()'},
                {'name': 'updated_at', 'type': 'timestamp', 'default': 'now()'}
            ]
        }).execute()
        print("majors表创建成功")
    except Exception as e:
        print(f"创建majors表时出错: {e}")
    
    # 创建subscribers表
    try:
        result = supabase.rpc('create_table', {
            'name': 'subscribers',
            'columns': [
                {'name': 'email', 'type': 'varchar(255)', 'constraints': 'unique not null'},
                {'name': 'major_code', 'type': 'varchar(20)'},
                {'name': 'subscribed_at', 'type': 'timestamp', 'default': 'now()'},
                {'name': 'source', 'type': 'varchar(50)', 'default': "'website'"}
            ]
        }).execute()
        print("subscribers表创建成功")
    except Exception as e:
        print(f"创建subscribers表时出错: {e}")
    
    # 创建reports表
    try:
        result = supabase.rpc('create_table', {
            'name': 'reports',
            'columns': [
                {'name': 'major_code', 'type': 'varchar(20)'},
                {'name': 'executive_summary', 'type': 'text'},
                {'name': 'employment_data', 'type': 'jsonb'},
                {'name': 'learning_difficulty', 'type': 'jsonb'},
                {'name': 'career_path', 'type': 'jsonb'},
                {'name': 'industry_trends', 'type': 'text'},
                {'name': 'suitable_profiles', 'type': 'text'},
                {'name': 'warnings', 'type': 'text'},
                {'name': 'advice', 'type': 'text'},
                {'name': 'status', 'type': 'varchar(20)', 'default': "'draft'"},
                {'name': 'view_count', 'type': 'int', 'default': '0'},
                {'name': 'purchase_count', 'type': 'int', 'default': '0'},
                {'name': 'created_at', 'type': 'timestamp', 'default': 'now()'},
                {'name': 'updated_at', 'type': 'timestamp', 'default': 'now()'}
            ]
        }).execute()
        print("reports表创建成功")
    except Exception as e:
        print(f"创建reports表时出错: {e}")

def create_tables_manual():
    """手动创建表结构（使用SQL）"""
    print("正在手动创建数据库表...")
    
    # 需要在Supabase控制台中执行SQL：
    sql_commands = [
        """
        CREATE TABLE majors (
            id SERIAL PRIMARY KEY,
            code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            category_icon VARCHAR(10),
            difficulty VARCHAR(20),
            salary_range VARCHAR(50),
            overview TEXT,
            what_you_learn TEXT,
            suitable_for TEXT,
            career_outlook TEXT,
            xuefeng_comment TEXT,
            yearly_courses JSONB,
            top_universities JSONB,
            view_count INT DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """,
        """
        CREATE TABLE subscribers (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            major_code VARCHAR(20),
            subscribed_at TIMESTAMP DEFAULT NOW(),
            source VARCHAR(50) DEFAULT 'website'
        );
        """,
        """
        CREATE TABLE reports (
            id SERIAL PRIMARY KEY,
            major_code VARCHAR(20),
            executive_summary TEXT,
            employment_data JSONB,
            learning_difficulty JSONB,
            career_path JSONB,
            industry_trends TEXT,
            suitable_profiles TEXT,
            warnings TEXT,
            advice TEXT,
            status VARCHAR(20) DEFAULT 'draft',
            view_count INT DEFAULT 0,
            purchase_count INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """
    ]
    
    print("\n请在Supabase控制台执行以下SQL命令：")
    print("=" * 60)
    for i, sql in enumerate(sql_commands, 1):
        print(f"-- 命令 {i}")
        print(sql)
        print()
    print("=" * 60)
    print("\n步骤：")
    print("1. 登录 Supabase 控制台")
    print("2. 进入您的项目")
    print("3. 点击左侧菜单 'SQL Editor'")
    print("4. 新建查询，粘贴以上SQL")
    print("5. 点击 'Run' 执行")

def import_sample_data():
    """导入示例专业数据"""
    print("\n正在准备专业数据...")
    
    sample_major = {
        "code": "010101",
        "name": "哲学",
        "category": "01 哲学",
        "category_icon": "🎓",
        "difficulty": "★★★☆☆",
        "salary_range": "¥5000-12000",
        "overview": "哲学是一门关于智慧的学问，研究存在、知识、价值、理性、心灵等根本问题。",
        "what_you_learn": "哲学史、逻辑学、伦理学、美学、宗教学、马克思主义哲学等。",
        "suitable_for": "喜欢思考、有好奇心、善于抽象思维、热爱读书的学生。",
        "career_outlook": "可从事教育、科研、公务员、编辑出版、企业管理等工作。",
        "xuefeng_comment": "哲学不是无用之学，它培养的是批判性思维和深度思考能力。",
        "yearly_courses": {
            "year1": ["中国哲学史", "西方哲学史", "马克思主义哲学", "逻辑学"],
            "year2": ["伦理学", "宗教学", "美学原理", "哲学导论"],
            "year3": ["现代西方哲学", "中国现代哲学", "哲学方法论", "专业英语"],
            "year4": ["毕业论文", "实习", "哲学前沿讲座"]
        },
        "top_universities": {
            "domestic": ["北京大学", "中国人民大学", "复旦大学"],
            "international": ["哈佛大学", "牛津大学", "剑桥大学"]
        }
    }
    
    try:
        result = supabase.table('majors').insert(sample_major).execute()
        print("示例数据导入成功！")
    except Exception as e:
        print(f"导入数据时出错: {e}")
        print("\n请先在Supabase控制台创建表结构，然后再运行此脚本")

if __name__ == "__main__":
    print("=" * 60)
    print("  Supabase 数据库配置脚本")
    print("=" * 60)
    print()
    
    # 尝试创建表（如果失败，显示手动创建的SQL）
    try:
        create_tables()
    except Exception as e:
        print(f"自动创建表失败: {e}")
        print("\n请手动在Supabase控制台创建表结构：")
        create_tables_manual()
    
    print("\n" + "=" * 60)
    print("配置完成！请继续下一步操作")
    print("=" * 60)