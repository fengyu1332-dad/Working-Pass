// ============================================================
// 专业星图 - AI 深度分析报告生成 Edge Function
// 部署: supabase functions deploy generate-report
// 密钥: supabase secrets set DEEPSEEK_API_KEY=sk-...
// ============================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

interface MajorData {
  name: string;
  code: string;
  category: string;
  degree?: string;
  duration?: number;
  difficulty?: string;
  overview?: string;
  what_you_learn?: string;
  yearly_courses?: string | object;
  career_outlook?: string;
  salary_range?: string;
  suitable_for?: string;
  career_directions?: string | object;
  xuefeng_comment?: string;
  top_universities?: string | object;
}

function safeStr(v: unknown, fallback = "暂无数据"): string {
  if (!v) return fallback;
  if (typeof v === "object") return JSON.stringify(v, null, 2);
  return String(v);
}

function buildUserPrompt(m: MajorData): string {
  return `请为以下专业生成完整的13章节深度分析报告。

======= 专业基础信息 =======
专业名称：${m.name || ""}
专业代码：${m.code || ""}
学科门类：${m.category || ""}
学位：${m.degree || "未标注"}
学制：${m.duration || 4}年
难度评级：${m.difficulty || "未标注"}

======= 专业概况 =======
${safeStr(m.overview)}

======= 核心课程与技能 =======
${safeStr(m.what_you_learn)}

======= 课程安排（JSON） =======
${safeStr(m.yearly_courses)}

======= 就业前景描述 =======
${safeStr(m.career_outlook)}

======= 薪资范围 =======
${safeStr(m.salary_range)}

======= 适合人群分析 =======
${safeStr(m.suitable_for)}

======= 就业方向（JSON） =======
${safeStr(m.career_directions)}

======= 雪峰点评参考 =======
${safeStr(m.xuefeng_comment)}

======= 推荐院校（JSON） =======
${safeStr(m.top_universities)}

======= 报告结构要求 =======
严格按以下13章生成（每章<h2>标题须完全一致），总字数≥8000汉字，用具体数字而非模糊描述：

<h2>一、专业概述</h2>
- 1.1 专业定义与学科定位（150-200字）
- 1.2 培养目标（3-5条）
- 1.3 学科特点与核心价值（3-4个特点）

<h2>二、课程安排与学习内容</h2>
- 2.1 分年级课程体系（HTML表格：大一~大四）
- 2.2 核心课程详解（3-5门，每门50-80字）
- 2.3 实践教学环节（5-6项）
- 2.4 核心能力培养（4-5项）

<h2>三、就业前景分析</h2>
- 3.1 就业率数据（总体、对口、满意度，引用来源）
- 3.2 主要就业方向与岗位（7-10个，分"核心技术岗"和"拓展方向"）
- 3.3 行业分布（6个以上行业+大致百分比）
- 3.4 绿牌/红牌标识及解读

<h2>四、薪资水平与职业发展</h2>
- 4.1 薪资数据（应届/3年/5年/10年平均薪资）
- 4.2 高薪比例
- 4.3 城市薪资差异（一线/新一线/二线对比）
- 4.4 职业发展路径（技术线+管理线，入门→资深→专家/管理）
- 4.5 职业天花板评估
- 4.6 长期发展潜力（10年以上）

<h2>五、考研与深造分析</h2>
- 5.1 考研必要性评估
- 5.2 考研数据（报名趋势、录取率）
- 5.3 推荐深造方向（5个细分方向）
- 5.4 院校推荐（A+/A/A-三级）
- 5.5 读博建议

<h2>六、考公考编分析</h2>
- 6.1 对口度评估（可报岗位数、竞争比、上岸难度1-5星）
- 6.2 适合的编制岗位（公务员/事业编/国企）
- 6.3 体制内薪资待遇
- 6.4 考公优劣势对比

<h2>七、行业发展与人才需求</h2>
- 7.1 行业生命周期评估（成长期/成熟期/衰退期，说明理由）
- 7.2 行业规模与增长率（具体数字）
- 7.3 国家政策支持力度
- 7.4 人才缺口数据
- 7.5 未来5年趋势（5个具体判断）

<h2>八、适合人群与适配度</h2>
- 8.1 适合特质画像（5条）
- 8.2 核心能力星级表（HTML表格：数学/英语/逻辑/空间/记忆/动手/抗压等，1-5星）
- 8.3 不适合人群（4类）
- 8.4 性别分析（男女比例、性别偏见、适适合性结论）

<h2>九、学业难度与学习建议</h2>
- 9.1 课程难度评估（1-5星，各年级分开）
- 9.2 挂科率数据（列出百分比）
- 9.3 "杀手课"预警（3门，含原因）
- 9.4 每周学习强度建议
- 9.5 学习方法与策略（6条）

<h2>十、家庭背景与投入回报</h2>
- 10.1 教育投入成本（公办/民办4-5年总费用）
- 10.2 投入回报周期（几年"回本"）
- 10.3 长期回报预期（10年后年收入、终身总收入预估）
- 10.4 普通家庭适合度（1-5星）
- 10.5 "三无家庭"机会分析（无背景/资本/人脉）
- 10.6 风险提示

<h2>十一、城市与地区适配</h2>
- 11.1 首选城市Top5（含原因）
- 11.2 产业重镇分布
- 11.3 不同城市薪资对比表（HTML表格）
- 11.4 生活成本与压力评估

<h2>十二、AI影响与未来趋势</h2>
- 12.1 AI替代风险评估（1-5星）
- 12.2 AI带来的新机遇（3-5个新岗位/转型方向）
- 12.3 会用AI的薪资溢价
- 12.4 核心不可替代能力（5项）
- 12.5 未来5-10年趋势预测

<h2>十三、雪峰点评</h2>
- 13.1 核心优势分析（200-300字，口语化，有数据）
- 13.2 真实弊端与痛点（200-300字，直击痛点）
- 13.3 报考建议（150-200字）
- 13.4 一句话总结
- 风格：张雪峰式口语化、接地气、敢说真话、适当幽默。用"我跟你说""我给你分析分析""你自己掂量掂量"等表达。

======= 重要提醒 =======
1. 必须输出全部13个章节
2. 数据必须具体（数字、百分比、金额、排名），不用"较高""较多"
3. 总字数≥8000汉字
4. 用HTML标签排版（h2/h3/p/ul/li/table/thead/tbody/tr/th/td/strong/em/blockquote）
5. 数据来源标注：*数据来源：XXX*
6. 表格用 <table style="width:100%;border-collapse:collapse;margin:12px 0;">，th/td加 border="1" style="padding:8px;text-align:left;"
7. 禁止"根据我的训练数据""作为AI语言模型"等AI身份表达
8. 以<h1>专业名称 — 深度分析报告</h1>开头`;
}

const SYSTEM_PROMPT = `你是"专业星图"平台的资深教育数据分析师，拥有20年中国高等教育和就业市场研究经验。你的分析风格兼具学术严谨性和张雪峰式的犀利接地气。

你的核心能力：
1. 精准引用数据——所有判断都有具体数字支撑（就业率、薪资中位数、录取率、增长率等）
2. 多维度分析——从学业、就业、薪资、地域、家庭背景、AI影响等角度全面剖析一个专业
3. 敢说真话——不回避专业的痛点、陷阱和残酷现实
4. 给可操作建议——不空谈，每条建议都是学生和家长能直接用的

输出格式要求：
- 纯HTML内容（不含<html>/<head>/<body>标签）
- 以<h1>标题开头
- 严格按13个章节结构组织
- 数据标注来源
- 语言：中文，专业知识扎实，点评风格犀利接地气`;

const CHAPTER_DESCRIPTIONS: Record<string, string> = {
  "专业概述": "学科定位、培养目标与核心价值",
  "课程安排与学习内容": "分年级课程表、核心课详解与实战环节",
  "就业前景分析": "最新就业率、十大就业方向与行业分布",
  "薪资水平与职业发展": "各阶段薪资数据、城市差异与晋升路径",
  "考研与深造分析": "考研必要性评估、录取率与A+/A/A-院校推荐",
  "考公考编分析": "岗位竞争比、编制类型与体制内待遇对比",
  "行业发展与人才需求": "行业生命周期、政策支持与5年趋势预测",
  "适合人群与适配度": "特质画像、能力星级评估与性别分析",
  "学业难度与学习建议": "挂科率数据、杀手课预警与高效学习策略",
  "家庭背景与投入回报": "4年总成本核算、回报周期与三无家庭机会",
  "城市与地区适配": "Top5首选城市、产业集群分布与薪资对比",
  "AI影响与未来趋势": "AI替代风险评估、新机遇与5-10年演变预测",
  "雪峰点评": "核心优势、真实痛点、报考建议与一句话总结",
};

function buildPreview(html: string): string {
  // Extract all h2 titles
  const h2Regex = /<h2>([^<]+)<\/h2>/g;
  const h2Titles: string[] = [];
  let match: RegExpExecArray | null;
  while ((match = h2Regex.exec(html)) !== null) {
    h2Titles.push(match[1].replace(/[一二三四五六七八九十]+、/, "").trim());
  }

  // Calculate approximate pages (Chinese: ~600 chars/page, plus tables add bulk)
  const textOnly = html.replace(/<[^>]+>/g, "").replace(/\s+/g, "");
  const estimatedPages = Math.max(12, Math.ceil(textOnly.length / 550));

  // Find matching chapter descriptions
  const lines: string[] = [];
  for (const title of h2Titles) {
    const desc = CHAPTER_DESCRIPTIONS[title];
    if (desc) {
      lines.push(`<p style="margin:4px 0;"><strong>${title}</strong> — ${desc}</p>`);
    }
  }

  const previewHTML = `
<div style="font-family:system-ui,-apple-system,sans-serif;line-height:1.8;color:#333;">
  <div style="background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:16px 20px;border-radius:12px;margin-bottom:16px;">
    <p style="margin:0 0 6px;font-size:18px;font-weight:700;">深度分析报告</p>
    <p style="margin:0;font-size:14px;opacity:0.9;">预计阅读时间：${Math.round(estimatedPages * 1.8)} 分钟 · 约 ${estimatedPages} 页 · ${textOnly.length.toLocaleString()} 字</p>
  </div>
  <p style="margin:0 0 12px;font-weight:600;color:#555;">本报告由专业星图AI分析引擎生成，涵盖以下 ${h2Titles.length} 个核心章节：</p>
  ${lines.join("\n  ")}
  <div style="margin-top:16px;padding:12px 16px;background:#f5f5f5;border-radius:8px;font-size:13px;color:#666;">
    <p style="margin:0;">数据来源：教育部、麦可思研究院、智联招聘、Boss直聘研究院、各高校就业质量报告</p>
    <p style="margin:4px 0 0;">解锁后可在线阅读完整报告，含详细数据表格、对比分析和雪峰老师专业点评。</p>
  </div>
</div>`.trim();

  return previewHTML;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "仅支持POST请求" }), {
      status: 405,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  try {
    // --- 1. Auth check ---
    const authHeader = req.headers.get("Authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return new Response(JSON.stringify({ error: "请先登录管理员账号" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const jwt = authHeader.replace("Bearer ", "");
    const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
    const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY") || "";

    // --- 2. Optional admin check (verifies JWT is valid) ---
    // Anon key is sufficient for auth.getUser() which validates the JWT
    const supabase = createClient(supabaseUrl, supabaseAnonKey, {
      global: { headers: { Authorization: `Bearer ${jwt}` } },
    });
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return new Response(JSON.stringify({ error: "请先登录管理员账号" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // --- 3. Parse major data from request ---
    const body = await req.json();
    const major: MajorData = body.major;
    if (!major || !major.name) {
      return new Response(JSON.stringify({ error: "缺少专业数据" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // --- 4. Check API key ---
    const apiKey = Deno.env.get("DEEPSEEK_API_KEY");
    if (!apiKey) {
      return new Response(JSON.stringify({ error: "服务端配置错误：未设置DEEPSEEK_API_KEY" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // --- 5. Call DeepSeek API ---
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 95000);

    let responseText = "";
    try {
      const userPrompt = buildUserPrompt(major);
      const res = await fetch("https://api.deepseek.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model: "deepseek-chat",
          max_tokens: 10000,
          temperature: 0.5,
          messages: [
            { role: "system", content: SYSTEM_PROMPT },
            { role: "user", content: userPrompt },
          ],
        }),
        signal: controller.signal,
      });
      clearTimeout(timeoutId);

      if (!res.ok) {
        const errBody = await res.text().catch(() => "");
        console.error(`DeepSeek API ${res.status}: ${errBody}`);

        if (res.status === 401) {
          return new Response(JSON.stringify({ error: "AI服务认证失败，请联系管理员检查API密钥" }), {
            status: 500,
            headers: { ...corsHeaders, "Content-Type": "application/json" },
          });
        }
        if (res.status === 429) {
          return new Response(JSON.stringify({ error: "AI服务暂时繁忙，请等待30秒后重试" }), {
            status: 503,
            headers: { ...corsHeaders, "Content-Type": "application/json" },
          });
        }
        return new Response(JSON.stringify({ error: `AI服务异常(${res.status})，请稍后重试` }), {
          status: 502,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      const data = await res.json();
      responseText = data?.choices?.[0]?.message?.content || "";
    } catch (err: unknown) {
      clearTimeout(timeoutId);
      const message = err instanceof Error ? err.message : String(err);
      if (message.includes("abort") || message.includes("timeout")) {
        return new Response(JSON.stringify({ error: "AI分析耗时较长（超时），请重试或选择其他专业" }), {
          status: 504,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      console.error("Fetch error:", message);
      return new Response(JSON.stringify({ error: "网络异常，请检查网络后重试" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // --- 6. Validate output ---
    if (!responseText || responseText.trim().length < 1000) {
      return new Response(JSON.stringify({ error: "AI返回内容不足，请重试" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // --- 7. Build professional preview ---
    const preview = buildPreview(responseText);

    return new Response(JSON.stringify({
      success: true,
      html: responseText,
      preview,
    }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("Unexpected error:", message);
    return new Response(JSON.stringify({ error: "服务器内部错误，请稍后重试" }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
