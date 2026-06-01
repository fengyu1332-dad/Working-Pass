// ============================================================
// 专业星图 - 管理员创建用户 Edge Function
// 部署: supabase functions deploy admin-create-user
// ============================================================

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

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
    // 1. Verify caller is admin
    const authHeader = req.headers.get("Authorization");
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return new Response(JSON.stringify({ error: "未登录" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const jwt = authHeader.replace("Bearer ", "");
    const supabaseUrl = Deno.env.get("PROJECT_URL") || "";
    const supabaseAnonKey = Deno.env.get("PROJECT_ANON_KEY") || "";

    const anonClient = createClient(supabaseUrl, supabaseAnonKey, {
      global: { headers: { Authorization: `Bearer ${jwt}` } },
    });

    // Verify JWT and admin role
    const { data: { user }, error: authError } = await anonClient.auth.getUser();
    if (authError || !user) {
      return new Response(JSON.stringify({ error: "登录已过期" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const { data: profile } = await anonClient
      .from("user_profiles")
      .select("role")
      .eq("id", user.id)
      .single();

    if (!profile || profile.role !== "admin") {
      return new Response(JSON.stringify({ error: "仅管理员可创建用户" }), {
        status: 403,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 2. Parse request
    const body = await req.json();
    const { email, password, phone, role } = body;
    if (!email || !password || password.length < 6) {
      return new Response(JSON.stringify({ error: "邮箱和密码（至少6位）为必填项" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 3. Create user via signUp — must use clean client (no admin JWT)
    const cleanClient = createClient(supabaseUrl, supabaseAnonKey);
    const { data: signUpData, error: signUpError } = await cleanClient.auth.signUp({
      email,
      password,
      options: { data: { phone: phone || "" } },
    });

    if (signUpError) {
      if (signUpError.message.includes("already") || signUpError.message.includes("exists")) {
        return new Response(JSON.stringify({ error: "该邮箱已被注册" }), {
          status: 409,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      return new Response(JSON.stringify({ error: `创建失败: ${signUpError.message}` }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 4. Admin sets role/phone via authenticated client (trigger created default profile)
    if (signUpData.user) {
      const { error: updateError } = await anonClient
        .from("user_profiles")
        .update({ role: role || "user", phone: phone || null })
        .eq("id", signUpData.user.id);

      // If trigger hasn't created profile yet, insert it
      if (updateError) {
        await anonClient
          .from("user_profiles")
          .insert({
            id: signUpData.user.id,
            email: email,
            phone: phone || null,
            role: role || "user",
            points_balance: 1,
          });
      }
    }

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });

  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    console.error("admin-create-user error:", message);
    return new Response(JSON.stringify({ error: "服务器内部错误" }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
