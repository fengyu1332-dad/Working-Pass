function formatPrice(price) {
    if (typeof price !== 'number') {
        price = parseFloat(price) || 0;
    }
    return '¥' + price.toFixed(2);
}

function formatDate(dateString) {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return '';
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}`;
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 5px;
        background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
        color: white;
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

function validatePhone(phone) {
    const phoneRegex = /^1[3-9]\d{9}$/;
    return phoneRegex.test(phone);
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    if (!password || password.length < 8) {
        return false;
    }
    const hasNumber = /\d/.test(password);
    const hasLetter = /[a-zA-Z]/.test(password);
    return hasNumber && hasLetter;
}

async function checkAuth() {
    const { data: { session }, error } = await window.supabaseClient.auth.getSession();
    if (error) {
        console.error('Auth check error:', error);
        return null;
    }
    return session;
}

async function requireAuth() {
    const session = await checkAuth();
    if (!session) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

async function requireAdmin() {
    const session = await checkAuth();
    if (!session) {
        window.location.href = '/login.html';
        return false;
    }
    
    const { data: { user }, error } = await window.supabaseClient.auth.getUser();
    if (error || !user) {
        window.location.href = '/login.html';
        return false;
    }
    
    const { data: profile, error: profileError } = await window.supabaseClient
        .from('profiles')
        .select('role')
        .eq('id', user.id)
        .single();
    
    if (profileError || profile.role !== 'admin') {
        window.location.href = '/';
        return false;
    }
    
    return true;
}

function getRedirectUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('redirect') || '/';
}
