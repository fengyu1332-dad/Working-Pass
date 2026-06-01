// ============================================================
// 专业星图 - 创建支付宝支付订单 Edge Function
// 部署: supabase functions deploy create-alipay-order
// ============================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { corsHeaders } from "../_shared/cors.ts";
import { signAlipayParams } from "../_shared/alipay-sdk.ts";

interface RequestBody {
  package_id: number;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "仅支持 POST 请求" }), {
      status: 405,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  try {
    // 1. JWT 认证
    const authHeader = req.headers.get("Authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return new Response(JSON.stringify({ error: "请先登录" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const jwt = authHeader.replace("Bearer ", "");
    const supabaseUrl = Deno.env.get("PROJECT_URL") || "https://djteatwxjlnbjylynvjh.supabase.co";
    const supabaseAnonKey = Deno.env.get("PROJECT_ANON_KEY") || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRqdGVhdHd4amxuYmp5bHludmpoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwODUwOTMsImV4cCI6MjA5NDY2MTA5M30.P6IJW2noTImzeNXtfKsmjJBMp9AJBTw1LamYTdtyd_4";
    const supabase = createClient(supabaseUrl, supabaseAnonKey, {
      global: { headers: { Authorization: `Bearer ${jwt}` } },
    });

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return new Response(JSON.stringify({ error: "登录已过期，请重新登录" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 2. 解析请求
    const body: RequestBody = await req.json();
    if (!body.package_id || typeof body.package_id !== "number") {
      return new Response(JSON.stringify({ error: "请选择套餐" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 3. 查询套餐
    const { data: pkg, error: pkgError } = await supabase
      .from("point_packages")
      .select("id, name, points, price")
      .eq("id", body.package_id)
      .eq("is_active", true)
      .single();

    if (pkgError || !pkg) {
      return new Response(JSON.stringify({ error: "套餐不存在或已下架" }), {
        status: 404,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 4. 创建订单
    const { data: order, error: orderError } = await supabase
      .from("orders")
      .insert({
        user_id: user.id,
        package_id: pkg.id,
        amount: pkg.price,
        points: pkg.points,
        status: "pending",
        payment_method: "alipay",
        expires_at: new Date(Date.now() + 15 * 60 * 1000).toISOString(),
      })
      .select("id, amount, points, status, created_at")
      .single();

    if (orderError || !order) {
      console.error("Order creation failed:", orderError);
      return new Response(JSON.stringify({ error: "订单创建失败，请重试" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 5. 构建支付宝请求参数
    const alipayAppId = Deno.env.get("ALIPAY_APP_ID") || "";
    const alipayPrivateKey = Deno.env.get("ALIPAY_PRIVATE_KEY") || "";

    if (!alipayPrivateKey) {
      return new Response(JSON.stringify({
        error: "ALIPAY_PRIVATE_KEY 未配置，请在 Supabase Dashboard → Settings → Edge Functions → Secrets 中添加"
      }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const keyFormat = alipayPrivateKey.includes("BEGIN RSA PRIVATE KEY") ? "PKCS1" :
                      alipayPrivateKey.includes("BEGIN PRIVATE KEY") ? "PKCS8" : "UNKNOWN";

    const alipayGateway = Deno.env.get("ALIPAY_GATEWAY") || "https://openapi-sandbox.dl.alipaydev.com/gateway.do";
    const frontendUrl = Deno.env.get("FRONTEND_URL") || "http://localhost:5173";
    const notifyUrl = Deno.env.get("ALIPAY_NOTIFY_URL") ||
      `${supabaseUrl}/functions/v1/alipay-notify`;

    const bizContent = JSON.stringify({
      out_trade_no: order.id,
      product_code: "FAST_INSTANT_TRADE_PAY",
      total_amount: Number(pkg.price).toFixed(2),
      subject: `专业星图 - ${pkg.name}`,
      body: `${pkg.points} 点数充值`,
    });

    const alipayParams: Record<string, string> = {
      app_id: alipayAppId,
      method: "alipay.trade.page.pay",
      charset: "utf-8",
      sign_type: "RSA2",
      timestamp: new Date().toISOString().replace("T", " ").replace(/\.\d{3}Z$/, ""),
      version: "1.0",
      notify_url: notifyUrl,
      return_url: `${frontendUrl}/user/payment-callback.html`,
      biz_content: bizContent,
    };

    try {
      var signedQuery = await signAlipayParams(alipayParams, alipayPrivateKey);
    } catch (signErr: unknown) {
      const msg = signErr instanceof Error ? signErr.message : String(signErr);
      return new Response(JSON.stringify({
        error: `签名失败: ${msg}`
      }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
    const paymentUrl = `${alipayGateway}?${signedQuery}`;

    return new Response(JSON.stringify({
      success: true,
      payment_url: paymentUrl,
      order: {
        id: order.id,
        amount: order.amount,
        points: order.points,
        status: order.status,
      },
    }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });

  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    const stack = err instanceof Error ? err.stack : '';
    console.error("create-alipay-order error:", message, stack);
    return new Response(JSON.stringify({ error: `服务器错误: ${message}` }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
