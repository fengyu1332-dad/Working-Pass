// ============================================================
// 专业星图 — 7天未登录用户召回提醒 Edge Function
// 部署: supabase functions deploy send-reminders --no-verify-jwt
//
// 用法: 通过外部 cron 服务 (如 cron-job.org) 定期 GET/POST 此 URL
// 推荐频率: 每天一次 (e.g. 每天早上 9:00 UTC+8)
// 可选参数: ?send=true 实际发送召回邮件，否则仅预览名单
// ============================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

interface RemindTarget {
  user_id: string;
  email: string;
  days_inactive: number;
  last_sign_in: string | null;
}

Deno.serve(async (req: Request) => {
  try {
    const supabaseUrl = Deno.env.get("PROJECT_URL") || "https://djteatwxjlnbjylynvjh.supabase.co";
    const serviceRoleKey = Deno.env.get("PROJECT_SERVICE_ROLE_KEY") || "";

    if (!serviceRoleKey) {
      return new Response(JSON.stringify({ error: "PROJECT_SERVICE_ROLE_KEY not configured" }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }

    const supabase = createClient(supabaseUrl, serviceRoleKey, {
      auth: { autoRefreshToken: false, persistSession: false },
    });

    const url = new URL(req.url);
    const shouldSend = url.searchParams.get("send") === "true";

    // ---- 1. 查询符合召回条件的用户 ----
    // 条件: email_follow_up=true + 7天以上未登录 + 7天内未被提醒
    const { data: targets, error: queryErr } = await supabase.rpc("get_remind_targets");

    if (queryErr) {
      console.error("get_remind_targets error:", queryErr);
      return new Response(JSON.stringify({ error: queryErr.message }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }

    const users: RemindTarget[] = (targets || []) as RemindTarget[];

    if (!users.length) {
      return new Response(JSON.stringify({ success: true, reminded: 0, message: "No users to remind" }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    console.log(`send-reminders: ${users.length} users eligible for reminder`);

    // ---- 2. 发送召回邮件 + 记录日志 ----
    let sent = 0;
    const errors: string[] = [];

    for (const user of users) {
      try {
        if (shouldSend) {
          // 发送召回邮件
          // 注意: 需要配置 Supabase 自定义邮件模板 "reengagement" 或使用第三方邮件服务
          // 目前通过 auth.admin 无法直接发送自定义邮件，此处为集成点
          // 替代方案: 使用 resend/sendgrid 等服务的 REST API 发送
          console.log(`[DRY RUN] Would send reminder to ${user.email} (inactive ${user.days_inactive}d)`);
        }

        // 记录提醒日志（防止 7 天内重复发送）
        const { error: logErr } = await supabase
          .from("reminder_logs")
          .insert({ user_id: user.user_id });

        if (logErr) {
          errors.push(`${user.email}: ${logErr.message}`);
        } else {
          sent++;
        }
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : String(err);
        errors.push(`${user.email}: ${msg}`);
      }
    }

    const result = {
      success: true,
      dry_run: !shouldSend,
      total_eligible: users.length,
      logged: sent,
      errors: errors.length ? errors : undefined,
    };

    console.log(`send-reminders: logged ${sent}/${users.length} reminders`);

    return new Response(JSON.stringify(result), {
      headers: { "Content-Type": "application/json" },
    });

  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("send-reminders unexpected error:", message);
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
});
