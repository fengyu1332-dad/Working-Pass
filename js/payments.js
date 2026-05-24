
async function getPointPackages() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  const { data, error } = await sb
    .from('point_packages')
    .select('*')
    .eq('active', true)
    .order('price', { ascending: true });
  
  if (error) throw error;
  return data;
}

async function createOrder(packageId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');
  
  const { data: pkg } = await sb
    .from('point_packages')
    .select('*')
    .eq('id', packageId)
    .single();
  
  if (!pkg) throw new Error('Package not found');
  
  const { data: order, error } = await sb
    .from('orders')
    .insert({
      user_id: user.id,
      package_id: packageId,
      points: pkg.points,
      amount: pkg.price,
      status: 'pending'
    })
    .select()
    .single();
  
  if (error) throw error;
  return order;
}

async function completeOrder(orderId) {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');
  
  const { data: order } = await sb
    .from('orders')
    .select('*, point_packages(*)')
    .eq('id', orderId)
    .single();
  
  if (!order) throw new Error('Order not found');
  
  const { data: profile } = await sb
    .from('user_profiles')
    .select('points_balance')
    .eq('id', user.id)
    .single();
  
  await sb
    .from('user_profiles')
    .update({
      points_balance: (profile.points_balance || 0) + order.points
    })
    .eq('id', user.id);
  
  await sb
    .from('orders')
    .update({
      status: 'paid',
      paid_at: new Date().toISOString()
    })
    .eq('id', orderId);
  
  return true;
}

async function getOrders() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');
  
  const { data, error } = await sb
    .from('orders')
    .select('*, point_packages(*)')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });
  
  if (error) throw error;
  return data;
}

async function getDownloadRecords() {
  const sb = window.auth ? window.auth.getSupabase() : null;
  if (!sb) throw new Error('Supabase not initialized');
  
  const user = await window.auth.getCurrentUser();
  if (!user) throw new Error('User not logged in');
  
  const { data, error } = await sb
    .from('download_records')
    .select('*, reports(*)')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });
  
  if (error) throw error;
  return data;
}

if (typeof window !== 'undefined') {
  window.payments = {
    getPointPackages,
    createOrder,
    completeOrder,
    getOrders,
    getDownloadRecords
  };
}

