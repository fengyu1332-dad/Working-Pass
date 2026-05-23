# 专业星图 - 报告文件存储与调用指南

## 文件存储结构

### 目录布局

```
/workspace/
└── data/
    └── reports/                          # 主报告目录
        ├── report_<专业代码>_<专业名称>.txt   # TXT原始报告
        ├── report_<专业代码>_<专业名称>.pdf   # PDF生成报告
        ├── backup/                          # 旧版本备份
        ├── backup_before_clean/           # 清理前的备份
        ├── backup_before_clean_v2/        # v2清理前的备份
        └── test_summary.json              # 测试摘要（可选）
```

### 文件命名规范

**命名格式：**
```
report_<专业代码>_<专业名称>.<扩展名>
```

**示例：**
- TXT: `report_080901_计算机科学与技术.txt`
- PDF: `report_080901_计算机科学与技术.pdf`

---

## 当前存储的报告文件

| 专业代码 | 专业名称 | TXT | PDF |
|---------|---------|-----|-----|
| 020301 | 金融学 | ✅ | ✅ |
| 020401 | 新闻学 | ✅ | ✅ |
| 030101 | 法学 | ✅ | ✅ |
| 050301 | 新闻学 | ✅ | ✅ |
| 080901 | 计算机科学与技术 | ✅ | ✅ |
| 100201 | 临床医学 | ✅ | ✅ |

---

## 文件调用方式

### 1. 直接文件访问

#### Python代码调用示例

```python
import os

REPORTS_DIR = "/workspace/data/reports"

# 获取所有TXT报告
txt_reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.txt')]

# 获取所有PDF报告
pdf_reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.pdf')]

# 按专业代码查找
def get_report_by_code(major_code):
    """根据专业代码获取报告文件"""
    for f in os.listdir(REPORTS_DIR):
        if f.startswith(f'report_{major_code}_'):
            return os.path.join(REPORTS_DIR, f)
    return None

# 示例：获取计算机科学与技术的PDF
pdf_path = get_report_by_code("080901")
if pdf_path:
    print(f"PDF路径: {pdf_path}")
```

### 2. 使用管理工具

我们提供了 `report_manager.py` 管理工具（详见下文），可以方便地查询和调用文件。

---

## 文件管理工具

### report_manager.py - 报告管理工具

主要功能：
- 列出所有报告
- 按专业代码查询
- 按专业名称搜索
- 统计报告信息
- 检查文件完整性

使用示例：
```bash
cd /workspace
python report_manager.py --list          # 列出所有报告
python report_manager.py --search 法学    # 搜索专业
python report_manager.py --check        # 检查完整性
```

---

## Web API调用方式（可选）

如果需要通过Web接口访问，可以使用以下方式：

```python
# Flask示例（需要自行实现）
from flask import Flask, send_file, jsonify
import os

app = Flask(__name__)
REPORTS_DIR = "/workspace/data/reports"

@app.route('/api/reports')
def list_reports():
    """获取所有报告列表"""
    reports = []
    for f in os.listdir(REPORTS_DIR):
        if f.endswith('.pdf'):
            reports.append({
                'name': f.replace('.pdf', '').replace('report_', ''),
                'pdf_path': f,
                'txt_path': f.replace('.pdf', '.txt')
            })
    return jsonify(reports)

@app.route('/api/report/<major_code>/pdf')
def get_pdf(major_code):
    """获取指定专业的PDF"""
    for f in os.listdir(REPORTS_DIR):
        if f.startswith(f'report_{major_code}_') and f.endswith('.pdf'):
            return send_file(os.path.join(REPORTS_DIR, f), as_attachment=True)
    return "Not found", 404
```

---

## 与数据库集成（可选）

如果需要将报告文件与Supabase数据库关联：

```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REPORTS_DIR = "/workspace/data/reports"

def link_reports_to_database():
    """将报告文件与数据库关联"""
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    # 这里可以实现将报告文件路径存入数据库的逻辑
    pass
```

---

## 文件完整性检查

使用管理工具可以检查：
- TXT文件是否存在
- PDF文件是否存在
- 成对完整性（TXT和PDF是否都有）
- 文件大小合理性检查

---

## 备份策略

### 自动备份
每次运行 `clean_reports_v2.py` 或 `batch_generate_all.py` 时：
- 清理前备份到 `backup_before_clean/`
- 再次清理时备份到 `backup_before_clean_v2/`

### 手动备份
```bash
cd /workspace/data/reports
mkdir -p backup_$(date +%Y%m%d)
cp *.txt *.pdf backup_$(date +%Y%m%d)/
```

---

## 最佳实践

### 1. 命名一致性
- 严格遵循 `report_<专业代码>_<专业名称>` 格式
- 使用中文专业名称，便于识别

### 2. 文件组织
- 保持所有报告在同一目录
- 使用子目录存放备份
- 定期清理旧备份

### 3. 版本控制
- 重要报告变更前先备份
- 使用版本号或日期标记不同版本

### 4. 存储优化
- TXT文件保留（便于重新生成PDF）
- PDF文件用于分发和展示
- 定期检查磁盘空间

---

## 常见问题

### Q: 如何添加新报告？
A: 将新的TXT文件放入 `data/reports/` 目录，运行 `batch_generate_all.py` 即可。

### Q: 如何批量重新生成PDF？
A: 删除旧PDF，运行 `python batch_generate_all.py`。

### Q: 报告文件太大怎么办？
A: 检查内容是否合理，考虑压缩或分章节处理。

### Q: 如何分享报告？
A: 使用PDF文件即可，TXT保留用于编辑和重新生成。

---

## 附录

### A. 文件路径常量
```python
REPORTS_DIR = "/workspace/data/reports"
REPORTS_TXT = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.txt')]
REPORTS_PDF = [f for f in os.listdir(REPORTS_DIR) if f.endswith('.pdf')]
```

### B. 专业代码映射（示例）
```python
MAJOR_CODES = {
    "080901": "计算机科学与技术",
    "100201": "临床医学",
    "030101": "法学",
    "020301": "金融学",
    "020401": "新闻学",
    "050301": "新闻学"
}
```
