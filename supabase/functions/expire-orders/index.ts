// ============================================================
// 专业星图 - 订单过期清理 Edge Function
// 部署: supabase functions deploy expire-orders --no-verify-jwt
//
// 用法: 通过外部 cron 服务 (如 cron-job.org) 定期 GET/POST 此 URL
// 推荐频率: 每 1-5 分钟一次
// ============================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  try {
    const supabaseUrl = "https://djteatwxjlnbjylynvjh.supabase.co";
    const serviceRoleKey = Deno.env.get("PROJECT_SERVICE_ROLE_KEY") || "";

    if (!serviceRoleKey) {
      return new Response(JSON.stringify({ error: "PROJECT_SERVICE_ROLE_KEY not configured" }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }

    const supabase = createClient(supabaseUrl, serviceRoleKey);

    const { data, error } = await supabase.rpc("expire_pending_orders");

    if (error) {
      console.error("expire-orders error:", error);
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }

    const count = data && data[0]?.cnt || 0;
    console.log(`expire-orders: ${count} orders expired`);

    return new Response(JSON.stringify({ success: true, expired_count: count }), {
      headers: { "Content-Type": "application/json" },
    });

  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("expire-orders unexpected error:", message);
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
});
