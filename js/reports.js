
async function getReports(category = null, search = null) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  let query = sb
    .from('reports')
    .select('id, major_code, major_name, category, preview_content, pdf_url, download_count, status')
    .eq('status', 'published');
  
  if (category) {
    query = query.eq('category', category);
  }
  
  if (search) {
    query = query.or(`major_name.ilike.%${search}%,major_code.ilike.%${search}%,category.ilike.%${search}%`);
  }
  
  const { data, error } = await query.order('major_name');
  
  if (error) throw error;
  return data;
}

async function getReport(reportId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  const { data, error } = await sb
    .from('reports')
    .select('*')
    .eq('id', reportId)
    .single();
  
  if (error) throw error;
  return data;
}

async function downloadReport(reportId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');
  
  const profile = await window.auth.getUserProfile();
  if (!profile || profile.points_balance < 1) {
    throw new Error('点数不足，请先充值');
  }
  
  const { data: report } = await sb
    .from('reports')
    .select('*')
    .eq('id', reportId)
    .single();
  
  if (!report) throw new Error('Report not found');
  
  const { data: existingRecord } = await sb
    .from('download_records')
    .select('*')
    .eq('user_id', user.id)
    .eq('report_id', reportId)
    .maybeSingle();
  
  if (existingRecord) {
    return {
      text: report.full_content || report.preview_content || '',
      pdfUrl: report.pdf_url ? await generateSignedUrl(report.pdf_url) : null,
      alreadyDownloaded: true
    };
  }
  
  await sb
    .from('user_profiles')
    .update({
      points_balance: profile.points_balance - 1
    })
    .eq('id', user.id);
  
  await sb
    .from('download_records')
    .insert({
      user_id: user.id,
      report_id: reportId,
      points_spent: 1
    });
  
  await sb
    .from('reports')
    .update({
      download_count: (report.download_count || 0) + 1
    })
    .eq('id', reportId);
  
  const pdfSignedUrl = report.pdf_url ? await generateSignedUrl(report.pdf_url) : null;
  
  return {
    text: report.full_content || report.preview_content || '',
    pdfUrl: pdfSignedUrl,
    alreadyDownloaded: false
  };
}

async function generateSignedUrl(fileName) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) return null;
  
  try {
    const { data, error } = await sb.storage
      .from('reports-pdf')
      .createSignedUrl(fileName, 3600);
    
    if (error) {
      console.error('生成签名URL失败:', error.message);
      return null;
    }
    
    return data.signedUrl;
  } catch (err) {
    console.error('生成签名URL出错:', err.message);
    return null;
  }
}

function downloadPdfFromUrl(signedUrl, fileName) {
  if (!signedUrl) {
    throw new Error('PDF文件不存在');
  }
  
  const link = document.createElement('a');
  link.href = signedUrl;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

async function checkDownloaded(reportId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) return false;
  
  const user = await window.auth.getCurrentUser();
  if (!user) return false;
  
  const { data } = await sb
    .from('download_records')
    .select('id')
    .eq('user_id', user.id)
    .eq('report_id', reportId)
    .maybeSingle();
  
  return !!data;
}

if (typeof window) {
  window.reports = {
    getReports,
    getReport,
    downloadReport,
    downloadPdfFromUrl,
    checkDownloaded
  };
}
