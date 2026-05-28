const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const SUPABASE_URL = process.env.SUPABASE_URL || '';
const SUPABASE_KEY = process.env.SUPABASE_KEY || '';

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('错误: 请设置 SUPABASE_URL 和 SUPABASE_KEY 环境变量');
  console.error('参考 .env.example 文件了解配置方式');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function uploadPDFToStorage(filePath, fileName) {
  try {
    const fileBuffer = fs.readFileSync(filePath);
    
    const { data, error } = await supabase.storage
      .from('reports-pdf')
      .upload(fileName, fileBuffer, {
        contentType: 'application/pdf',
        upsert: true
      });

    if (error) {
      console.error(`上传 ${fileName} 失败:`, error.message);
      return null;
    }

    console.log(`✓ 上传成功: ${fileName}`);
    return data;
  } catch (err) {
    console.error(`上传 ${fileName} 出错:`, err.message);
    return null;
  }
}

async function uploadAllPDFs() {
  const reportsDir = path.join(__dirname, 'data', 'reports');
  const files = fs.readdirSync(reportsDir)
    .filter(f => f.endsWith('.pdf'));

  console.log(`\n找到 ${files.length} 个PDF文件\n`);

  for (const file of files) {
    const filePath = path.join(reportsDir, file);
    await uploadPDFToStorage(filePath, file);
  }

  console.log('\n上传完成！\n');
  await listStorageFiles();
}

async function listStorageFiles() {
  const { data, error } = await supabase.storage
    .from('reports-pdf')
    .list();

  if (error) {
    console.error('列出文件失败:', error.message);
    return;
  }

  console.log('Storage中的文件:');
  if (data && data.length > 0) {
    data.forEach(f => console.log(`  - ${f.name}`));
  } else {
    console.log('  (空)');
  }
}

uploadAllPDFs();
