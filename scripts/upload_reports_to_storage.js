const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const SUPABASE_URL = 'https://djteatwxjlnbjylynvjh.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4';

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
