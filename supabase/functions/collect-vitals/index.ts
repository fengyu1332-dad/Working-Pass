// ============================================================
// 专业星图 - Web Vitals 数据收集 Edge Function
// 部署: supabase functions deploy collect-vitals --no-verify-jwt
//
// 接收前端 sendBeacon POST，写入 web_vitals 表
// ============================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok");

  if (req.method !== "POST") {
    return new Response("fail", { status: 405 });
  }

  try {
    const body = await req.json().catch(() => null);
    if (!body || !body.name || typeof body.value !== "number") {
      return new Response("fail", { status: 400 });
    }

    const supabaseUrl = "https://djteatwxjlnbjylynvjh.supabase.co";
    const serviceRoleKey = Deno.env.get("PROJECT_SERVICE_ROLE_KEY") || "";
    if (!serviceRoleKey) {
      return new Response(JSON.stringify({ error: "not configured" }), { status: 500 });
    }

    const supabase = createClient(supabaseUrl, serviceRoleKey);

    const { error } = await supabase.from("web_vitals").insert({
      name: String(body.name).slice(0, 20),
      value: body.value,
      rating: body.rating || null,
      page: String(body.page || "").slice(0, 255),
      user_agent: req.headers.get("user-agent") || null,
    });

    if (error) {
      console.error("collect-vitals insert error:", error);
      return new Response("fail", { status: 500 });
    }

    return new Response("ok");

  } catch (err: unknown) {
    console.error("collect-vitals error:", err);
    return new Response("fail", { status: 500 });
  }
});
