const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

const SUPABASE_URL = process.env.SUPABASE_URL || '';
const SUPABASE_KEY = process.env.SUPABASE_KEY || '';

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('错误: 请设置 SUPABASE_URL 和 SUPABASE_KEY 环境变量');
  console.error('参考 .env.example 文件了解配置方式');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

const reportsConfig = [
  {
    major_code: '080901',
    major_name: '计算机科学与技术',
    category: '工学',
    preview_content: '本专业培养具备良好数理基础、扎实的计算机科学理论、工程实践能力和创新意识的复合型高级专门人才...',
    pdf_url: 'report_080901_计算机科学与技术.pdf'
  },
  {
    major_code: '020301',
    major_name: '金融学',
    category: '经济学',
    preview_content: '金融学专业培养具有全球视野、系统掌握金融理论知识和业务技能的复合型金融人才...',
    pdf_url: 'report_020301_金融学.pdf'
  },
  {
    major_code: '100201K',
    major_name: '临床医学',
    category: '医学',
    preview_content: '临床医学专业培养掌握基础医学、临床医学的基本理论和医疗预防的基本技能的医学专门人才...',
    pdf_url: 'report_100201_临床医学.pdf'
  },
  {
    major_code: '030101K',
    major_name: '法学',
    category: '法学',
    preview_content: '法学专业培养系统掌握法学知识，熟悉我国法律和党的相关政策的高级专门人才...',
    pdf_url: 'report_030101_法学.pdf'
  },
  {
    major_code: '050301',
    major_name: '新闻学',
    category: '文学',
    preview_content: '新闻学专业培养具有新闻学基本理论与业务技能，熟悉我国新闻政策法规的复合型新闻人才...',
    pdf_url: 'report_050301_新闻学.pdf'
  },
  {
    major_code: '050201',
    major_name: '英语',
    category: '文学',
    preview_content: '英语专业培养具有扎实的英语语言基础和广泛的文化知识的英语专门人才...',
    pdf_url: 'report_050201_英语.pdf'
  },
  {
    major_code: '070101',
    major_name: '数学与应用数学',
    category: '理学',
    preview_content: '数学与应用数学专业培养掌握数学科学的基本理论与基本方法，运用数学知识和计算机解决实际问题的专门人才...',
    pdf_url: 'report_070101_数学与应用数学.pdf'
  },
  {
    major_code: '080202',
    major_name: '机械设计制造及其自动化',
    category: '工学',
    preview_content: '机械设计制造及其自动化专业培养具备机械设计制造基础知识与应用能力的高级工程技术人才...',
    pdf_url: 'report_080202_机械设计制造及其自动化.pdf'
  },
  {
    major_code: '080701',
    major_name: '电子信息工程',
    category: '工学',
    preview_content: '电子信息工程专业培养具备电子技术和信息系统的基础知识与应用能力的高级工程技术人才...',
    pdf_url: 'report_080701_电子信息工程.pdf'
  },
  {
    major_code: '120203K',
    major_name: '会计学',
    category: '管理学',
    preview_content: '会计学专业培养具备管理、经济、法律和会计学等方面的知识和能力的应用型高级专门人才...',
    pdf_url: 'report_120203K_会计学.pdf'
  },
  {
    major_code: '020401',
    major_name: '新闻学（另）',
    category: '文学',
    preview_content: '本专业培养具备系统的新闻理论知识与技能、宽广的文化与科学知识的新闻学专门人才...',
    pdf_url: 'report_020401_新闻学.pdf'
  }
];

async function readReportContent(majorCode, majorName) {
  const reportsDir = path.join(__dirname, 'data', 'reports');
  const fileName = `report_${majorCode}_${majorName}.txt`;
  const filePath = path.join(reportsDir, fileName);
  
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return content;
  } catch (err) {
    console.warn(`  警告: 无法读取 ${filePath}: ${err.message}`);
    return null;
  }
}

async function insertReports() {
  console.log('\n开始导入报告数据到Supabase...\n');

  let successCount = 0;
  let errorCount = 0;

  for (const config of reportsConfig) {
    console.log(`处理: ${config.major_name} (${config.major_code})`);
    
    try {
      const fullContent = await readReportContent(config.major_code, config.major_name);
      
      if (!fullContent) {
        console.log(`  ⚠ 跳过 (文件不存在)\n`);
        continue;
      }

      const reportData = {
        major_code: config.major_code,
        major_name: config.major_name,
        category: config.category,
        preview_content: config.preview_content,
        full_content: fullContent,
        pdf_url: config.pdf_url,
        download_count: 0,
        status: 'published'
      };

      const { data, error } = await supabase
        .from('reports')
        .upsert(reportData, { onConflict: 'major_code' })
        .select()
        .single();

      if (error) {
        console.error(`  ✗ 插入失败: ${error.message}`);
        errorCount++;
      } else {
        console.log(`  ✓ 成功插入/更新 (ID: ${data.id})`);
        successCount++;
      }
    } catch (err) {
      console.error(`  ✗ 出错: ${err.message}`);
      errorCount++;
    }
    console.log('');
  }

  console.log('='.repeat(50));
  console.log(`导入完成: 成功 ${successCount} 个, 失败 ${errorCount} 个`);
  console.log('='.repeat(50));
}

async function verifyReports() {
  console.log('\n验证数据库中的报告...');
  
  const { data, error } = await supabase
    .from('reports')
    .select('id, major_code, major_name, status')
    .order('major_name');

  if (error) {
    console.error('验证失败:', error.message);
    return;
  }

  console.log(`\n数据库中共有 ${data.length} 个报告:\n`);
  data.forEach(r => {
    console.log(`  [${r.id}] ${r.major_name} (${r.major_code}) - ${r.status}`);
  });
}

async function main() {
  await insertReports();
  await verifyReports();
}

main().catch(console.error);
