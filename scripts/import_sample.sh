#!/bin/bash

SUPABASE_URL="https://djteatwxjlnbjylynvjh.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4"

echo "========================================="
echo "开始导入工科专业..."
echo "========================================="

# 人工智能
curl -X POST "$SUPABASE_URL/rest/v1/majors" \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "080717T",
    "name": "人工智能",
    "category": "08 工学",
    "category_icon": "🤖",
    "difficulty": "⭐⭐⭐⭐⭐",
    "salary_range": "¥20k-45k",
    "overview": "人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的新兴技术学科。本专业培养掌握人工智能基础理论、机器学习和深度学习算法、智能系统设计与开发的专业人才。",
    "what_you_learn": "机器学习、深度学习、神经网络、计算机视觉、自然语言处理、机器人技术、智能系统设计、Python编程、算法优化、数据结构",
    "suitable_for": "数学基础扎实、逻辑思维强、对新技术充满好奇心、喜欢编程和算法研究的学生。需要具备较强的抽象思维能力和持续学习能力。",
    "career_outlook": "人工智能是国家战略重点发展的领域，就业前景极为广阔。毕业生可在互联网企业、科技公司、研究机构等单位从事AI算法研发、智能产品设计、数据分析等工作。",
    "xuefeng_comment": "人工智能是当下最火爆的专业之一，但报考需要理性看待。这个专业对数学和编程要求极高，不是单纯追热门就能学好的。需要学生真正热爱技术、有较强的逻辑思维能力，并且做好持续学习、不断更新知识的准备。建议选择有人工智能强势学科的高校，同时要有读研的规划，因为本科阶段的学习深度往往不足以支撑直接就业。当然，如果能学好，这个专业的薪资待遇确实非常可观，但前提是你必须真正热爱这个领域，而不是单纯为了高薪。",
    "yearly_courses": {"大一": ["高等数学", "线性代数", "概率论", "计算机导论", "程序设计基础"], "大二": ["数据结构", "算法设计", "机器学习基础", "数据库原理", "操作系统"], "大三": ["深度学习", "计算机视觉", "自然语言处理", "强化学习", "人工智能综合项目"], "大四": ["毕业设计", "企业实习"]},
    "top_universities": {"domestic": ["清华大学", "北京大学", "浙江大学", "上海交通大学", "中国科学技术大学", "哈尔滨工业大学"], "international": ["MIT", "Stanford", "Carnegie Mellon", "UC Berkeley"]}
  }' 2>/dev/null && echo "✅ 080717T - 人工智能" || echo "❌ 人工智能"

sleep 0.2

# 数据科学与大数据技术
curl -X POST "$SUPABASE_URL/rest/v1/majors" \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "080910T",
    "name": "数据科学与大数据技术",
    "category": "08 工学",
    "category_icon": "📊",
    "difficulty": "⭐⭐⭐⭐",
    "salary_range": "¥18k-40k",
    "overview": "数据科学与大数据技术是研究数据采集、存储、处理、分析和可视化的综合性学科。本专业培养掌握大数据技术体系、具有大数据分析和应用能力的高级专门人才。",
    "what_you_learn": "大数据技术概论、Hadoop生态系统、Spark计算框架、NoSQL数据库、数据挖掘与机器学习、Python/R语言、数据可视化、统计学基础",
    "suitable_for": "对数据感兴趣、具备良好数学基础、喜欢分析和处理信息的学生。需要有耐心处理大量数据，并能从数据中发现规律。",
    "career_outlook": "大数据已渗透到各行各业，数据科学家被麦肯锡评为21世纪最具吸引力的职业。毕业生可在互联网、金融、医疗、零售等行业从事数据分析工作。",
    "xuefeng_comment": "数据科学和大数据技术是数字化时代的香饽饽，但我要泼点冷水。这个专业听起来高大上，实际上需要非常扎实的数学和编程基础。建议数学成绩一般的同学慎重考虑，因为概率统计、机器学习这些课程对数学要求很高。就业方向确实不错，但竞争也很激烈，建议读研提升竞争力。",
    "yearly_courses": {"大一": ["高等数学", "线性代数", "概率论", "Python程序设计", "数据科学导论"], "大二": ["数据结构", "数据库原理", "统计学", "机器学习基础"], "大三": ["大数据技术概论", "Hadoop开发", "Spark实战", "数据挖掘"], "大四": ["毕业设计", "企业实习"]},
    "top_universities": {"domestic": ["北京大学", "复旦大学", "中国人民大学", "华东师范大学"], "international": ["MIT", "Stanford", "UC Berkeley"]}
  }' 2>/dev/null && echo "✅ 080910T - 数据科学与大数据技术" || echo "❌ 数据科学与大数据技术"

echo ""
echo "========================================="
echo "导入完成！"
echo "========================================="