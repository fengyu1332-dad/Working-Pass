const packages = {
    async list() {
        try {
            const { data, error } = await window.supabaseClient
                .from('packages')
                .select('*')
                .eq('status', 'active')
                .order('price', { ascending: true });
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('List packages error:', error);
            return { success: false, error };
        }
    },
    
    async create(pkg) {
        try {
            const { data, error } = await window.supabaseClient
                .from('packages')
                .insert(pkg)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Create package error:', error);
            return { success: false, error };
        }
    },
    
    async update(id, updates) {
        try {
            const { data, error } = await window.supabaseClient
                .from('packages')
                .update(updates)
                .eq('id', id)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Update package error:', error);
            return { success: false, error };
        }
    }
};

const orders = {
    async list(userId, isAdmin = false) {
        try {
            let query = window.supabaseClient
                .from('orders')
                .select(`
                    *,
                    packages (*),
                    profiles!orders_user_id_fkey (*)
                `)
                .order('created_at', { ascending: false });
            
            if (!isAdmin && userId) {
                query = query.eq('user_id', userId);
            }
            
            const { data, error } = await query;
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('List orders error:', error);
            return { success: false, error };
        }
    },
    
    async create(order) {
        try {
            const { data, error } = await window.supabaseClient
                .from('orders')
                .insert(order)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Create order error:', error);
            return { success: false, error };
        }
    },
    
    async pay(orderId) {
        try {
            const { data, error } = await window.supabaseClient
                .from('orders')
                .update({ 
                    status: 'paid',
                    paid_at: new Date().toISOString()
                })
                .eq('id', orderId)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Pay order error:', error);
            return { success: false, error };
        }
    },
    
    async cancel(orderId) {
        try {
            const { data, error } = await window.supabaseClient
                .from('orders')
                .update({ 
                    status: 'cancelled',
                    cancelled_at: new Date().toISOString()
                })
                .eq('id', orderId)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Cancel order error:', error);
            return { success: false, error };
        }
    }
};

const reports = {
    async list(isAdmin = false) {
        try {
            let query = window.supabaseClient
                .from('reports')
                .select(`
                    *,
                    profiles!reports_user_id_fkey (*)
                `)
                .order('created_at', { ascending: false });
            
            if (!isAdmin) {
                const { data: { user } } = await window.supabaseClient.auth.getUser();
                if (user) {
                    query = query.eq('user_id', user.id);
                }
            }
            
            const { data, error } = await query;
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('List reports error:', error);
            return { success: false, error };
        }
    },
    
    async get(id) {
        try {
            const { data, error } = await window.supabaseClient
                .from('reports')
                .select(`
                    *,
                    profiles!reports_user_id_fkey (*)
                `)
                .eq('id', id)
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Get report error:', error);
            return { success: false, error };
        }
    },
    
    async create(report) {
        try {
            const { data, error } = await window.supabaseClient
                .from('reports')
                .insert(report)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Create report error:', error);
            return { success: false, error };
        }
    },
    
    async update(id, updates) {
        try {
            const { data, error } = await window.supabaseClient
                .from('reports')
                .update(updates)
                .eq('id', id)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Update report error:', error);
            return { success: false, error };
        }
    },
    
    async delete(id) {
        try {
            const { error } = await window.supabaseClient
                .from('reports')
                .delete()
                .eq('id', id);
            
            if (error) throw error;
            return { success: true };
        } catch (error) {
            console.error('Delete report error:', error);
            return { success: false, error };
        }
    }
};

const downloads = {
    async list(userId) {
        try {
            let query = window.supabaseClient
                .from('downloads')
                .select(`
                    *,
                    reports (*)
                `)
                .order('created_at', { ascending: false });
            
            if (userId) {
                query = query.eq('user_id', userId);
            }
            
            const { data, error } = await query;
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('List downloads error:', error);
            return { success: false, error };
        }
    },
    
    async create(userId, reportId) {
        try {
            const { data, error } = await window.supabaseClient
                .from('downloads')
                .insert({
                    user_id: userId,
                    report_id: reportId,
                    created_at: new Date().toISOString()
                })
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Create download record error:', error);
            return { success: false, error };
        }
    }
};

const users = {
    async list() {
        try {
            const { data, error } = await window.supabaseClient
                .from('profiles')
                .select('*')
                .order('created_at', { ascending: false });
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('List users error:', error);
            return { success: false, error };
        }
    },
    
    async get(id) {
        try {
            const { data, error } = await window.supabaseClient
                .from('profiles')
                .select('*')
                .eq('id', id)
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Get user error:', error);
            return { success: false, error };
        }
    },
    
    async updatePoints(userId, pointsDelta) {
        try {
            const { data: user, error: getError } = await window.supabaseClient
                .from('profiles')
                .select('points')
                .eq('id', userId)
                .single();
            
            if (getError) throw getError;
            
            const newPoints = (user.points || 0) + pointsDelta;
            
            const { data, error } = await window.supabaseClient
                .from('profiles')
                .update({ points: newPoints })
                .eq('id', userId)
                .select()
                .single();
            
            if (error) throw error;
            return { success: true, data };
        } catch (error) {
            console.error('Update user points error:', error);
            return { success: false, error };
        }
    }
};
