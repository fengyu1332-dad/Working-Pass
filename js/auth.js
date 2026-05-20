async function register(phone, password, email) {
    try {
        const { data, error } = await window.supabaseClient.auth.signUp({
            phone: phone,
            password: password,
            options: {
                data: {
                    email: email
                }
            }
        });
        
        if (error) {
            throw error;
        }
        
        if (data.user) {
            const { error: profileError } = await window.supabaseClient
                .from('profiles')
                .insert({
                    id: data.user.id,
                    phone: phone,
                    email: email,
                    role: 'user',
                    points: 0,
                    created_at: new Date().toISOString()
                });
            
            if (profileError) {
                console.error('Profile creation error:', profileError);
            }
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, error };
    }
}

async function loginWithPhone(phone, password) {
    try {
        const { data, error } = await window.supabaseClient.auth.signInWithPassword({
            phone: phone,
            password: password
        });
        
        if (error) {
            throw error;
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('Phone login error:', error);
        return { success: false, error };
    }
}

async function loginWithEmail(email, password) {
    try {
        const { data, error } = await window.supabaseClient.auth.signInWithPassword({
            email: email,
            password: password
        });
        
        if (error) {
            throw error;
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('Email login error:', error);
        return { success: false, error };
    }
}

async function logout() {
    try {
        const { error } = await window.supabaseClient.auth.signOut();
        
        if (error) {
            throw error;
        }
        
        window.location.href = '/login.html';
        return { success: true };
    } catch (error) {
        console.error('Logout error:', error);
        return { success: false, error };
    }
}

async function getCurrentUser() {
    try {
        const { data: { user }, error } = await window.supabaseClient.auth.getUser();
        
        if (error) {
            throw error;
        }
        
        if (!user) {
            return { success: false, user: null };
        }
        
        const { data: profile, error: profileError } = await window.supabaseClient
            .from('profiles')
            .select('*')
            .eq('id', user.id)
            .single();
        
        if (profileError) {
            console.error('Profile fetch error:', profileError);
        }
        
        return { success: true, user, profile };
    } catch (error) {
        console.error('Get current user error:', error);
        return { success: false, error };
    }
}

async function updateProfile(updates) {
    try {
        const { data: { user }, error: userError } = await window.supabaseClient.auth.getUser();
        
        if (userError || !user) {
            throw userError || new Error('User not found');
        }
        
        const { data, error } = await window.supabaseClient
            .from('profiles')
            .update(updates)
            .eq('id', user.id)
            .select()
            .single();
        
        if (error) {
            throw error;
        }
        
        return { success: true, data };
    } catch (error) {
        console.error('Update profile error:', error);
        return { success: false, error };
    }
}
