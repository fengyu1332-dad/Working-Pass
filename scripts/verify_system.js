#!/usr/bin/env node

const { createClient } = require('@supabase/supabase-js');

const SUPABASE_URL = process.env.SUPABASE_URL || '';
const SUPABASE_KEY = process.env.SUPABASE_KEY || '';

if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('错误: 请设置 SUPABASE_URL 和 SUPABASE_KEY 环境变量');
  console.error('参考 .env.example 文件了解配置方式');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

async function verifySystem() {
  console.log('\n========================================');
  console.log('专业星图 - 系统验证报告');
  console.log('========================================\n');

  let allPassed = true;

  console.log('1. 检查 reports 表...');
  try {
    const { data: reports, error } = await supabase
      .from('reports')
      .select('id, major_name, major_code')
      .limit(5);

    if (error) {
      console.log('   ❌ 错误:', error.message);
      allPassed = false;
    } else {
      console.log(`   ✅ 成功读取 ${reports?.length || 0} 条报告数据`);
    }
  } catch (err) {
    console.log('   ❌ 异常:', err.message);
    allPassed = false;
  }

  console.log('\n2. 检查 user_profiles 表...');
  try {
    const { data: profiles, error } = await supabase
      .from('user_profiles')
      .select('id, phone, points_balance')
      .limit(5);

    if (error) {
      console.log('   ❌ 错误:', error.message);
      allPassed = false;
    } else {
      console.log(`   ✅ 成功读取 ${profiles?.length || 0} 条用户数据`);
    }
  } catch (err) {
    console.log('   ❌ 异常:', err.message);
    allPassed = false;
  }

  console.log('\n3. 检查 Storage (reports-pdf)...');
  try {
    const { data: files, error } = await supabase.storage
      .from('reports-pdf')
      .list();

    if (error) {
      console.log('   ❌ Storage可能未配置:', error.message);
      console.log('   💡 提示: 请在Supabase Dashboard中创建 reports-pdf 存储桶');
      allPassed = false;
    } else {
      console.log(`   ✅ Storage已配置，包含 ${files?.length || 0} 个文件`);
    }
  } catch (err) {
    console.log('   ❌ 异常:', err.message);
    allPassed = false;
  }

  console.log('\n4. 检查 download_records 表...');
  try {
    const { data: records, error } = await supabase
      .from('download_records')
      .select('id')
      .limit(5);

    if (error) {
      console.log('   ❌ 错误:', error.message);
      allPassed = false;
    } else {
      console.log(`   ✅ 表结构正常`);
    }
  } catch (err) {
    console.log('   ❌ 异常:', err.message);
    allPassed = false;
  }

  console.log('\n========================================');
  if (allPassed) {
    console.log('✅ 所有检查通过！系统已准备就绪。');
  } else {
    console.log('⚠️ 部分检查失败，请检查上述问题。');
  }
  console.log('========================================\n');

  console.log('\n下一步操作:');
  console.log('1. 运行 "node upload_reports_to_storage.js" 上传PDF文件');
  console.log('2. 运行 "node import_reports_to_db.js" 导入报告数据');
  console.log('3. 在Supabase Dashboard中配置Storage权限');
  console.log('4. 测试完整下载流程\n');
}

verifySystem().catch(console.error);
