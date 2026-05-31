// ============================================================
// 专业星图 - 支付宝异步通知接收 Edge Function
// 部署: supabase functions deploy alipay-notify
//
// 支付宝 POST form 到此 URL，此函数:
//   1. 验签（防伪造）
//   2. 调用 complete_alipay_order() 原子化入账
//   3. 返回 "success" 或 "fail"（支付宝据此判断是否重试）
// ============================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { verifyAlipaySignature } from "../_shared/alipay-sdk.ts";

Deno.serve(async (req: Request) => {
  // 支付宝通知是 POST，但用 OPTIONS 做健康检查
  if (req.method === "OPTIONS") {
    return new Response("ok");
  }

  if (req.method !== "POST") {
    return new Response("fail", { status: 405 });
  }

  try {
    // 1. 解析支付宝 POST 的 form 参数
    let formText: string;
    try {
      formText = await req.text();
    } catch {
      return new Response("fail");
    }

    const params: Record<string, string> = {};
    for (const [key, value] of new URLSearchParams(formText)) {
      params[key] = value;
    }

    // 2. 验签
    const alipayPublicKey = Deno.env.get("ALIPAY_PUBLIC_KEY") || "";
    const isValid = await verifyAlipaySignature(params, alipayPublicKey);
    if (!isValid) {
      console.error("Alipay notify: signature verification failed");
      return new Response("fail");
    }

    // 3. 只处理交易成功
    const tradeStatus = params["trade_status"];
    if (tradeStatus !== "TRADE_SUCCESS" && tradeStatus !== "TRADE_FINISHED") {
      console.log(`Alipay notify: trade_status=${tradeStatus}, skipping`);
      return new Response("success");
    }

    // 4. 提取关键字段
    const outTradeNo = params["out_trade_no"];  // 我们的订单 UUID
    const tradeNo = params["trade_no"];          // 支付宝交易号
    const totalAmount = parseFloat(params["total_amount"] || "0");
    const appId = params["app_id"];

    if (!outTradeNo || !tradeNo) {
      console.error("Alipay notify: missing out_trade_no or trade_no");
      return new Response("fail");
    }

    // 验证 app_id 匹配
    const expectedAppId = Deno.env.get("ALIPAY_APP_ID") || "";
    if (appId && expectedAppId && appId !== expectedAppId) {
      console.error(`Alipay notify: app_id mismatch (got ${appId}, expected ${expectedAppId})`);
      return new Response("fail");
    }

    // 5. 调用原子化入账函数（使用 service_role 绕过 RLS）
    const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
    const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
    const supabase = createClient(supabaseUrl, serviceRoleKey);

    const { data, error } = await supabase.rpc("complete_alipay_order", {
      p_order_id: outTradeNo,
      p_alipay_trade_no: tradeNo,
      p_payment_amount: totalAmount,
    });

    if (error) {
      console.error("Alipay notify: complete_alipay_order error:", error);
      return new Response("fail");
    }

    if (data && typeof data === "object" && !data.success) {
      console.error("Alipay notify: complete_alipay_order returned fail:", data);
      // 业务失败（如订单已过期、金额不匹配）不重试
      return new Response("success");
    }

    console.log(`Alipay notify: order ${outTradeNo} completed, trade_no=${tradeNo}`);
    return new Response("success");

  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("Alipay notify unexpected error:", message);
    return new Response("fail");
  }
});
