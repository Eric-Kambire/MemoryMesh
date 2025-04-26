// Authentication related functions
const API_URL = 'http://localhost:5000/api';

async function login(username, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }

        // Store token and user data
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Redirect to index page
        window.location.href = 'index.html';
        
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

async function signup(username, email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Signup failed');
        }

        // Store token and user data
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Redirect to index page
        window.location.href = 'index.html';
        
        return data;
    } catch (error) {
        console.error('Signup error:', error);
        throw error;
    }
}

async function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        return false;
    }

    try {
        const response = await fetch(`${API_URL}/auth/check-auth`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        const data = await response.json();
        return data.authenticated;
    } catch (error) {
        console.error('Auth check error:', error);
        return false;
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// Form handling
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const errorMessage = document.createElement('div');
    errorMessage.className = 'text-red-500 text-sm mt-2 hidden';
    
    if (loginForm) {
        loginForm.appendChild(errorMessage.cloneNode(true));
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = loginForm.querySelector('input[type="text"]').value;
            const password = loginForm.querySelector('input[type="password"]').value;
            
            try {
                await login(username, password);
            } catch (error) {
                const errorDiv = loginForm.querySelector('.text-red-500');
                errorDiv.textContent = error.message;
                errorDiv.classList.remove('hidden');
            }
        });
    }
    
    if (signupForm) {
        signupForm.appendChild(errorMessage.cloneNode(true));
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = signupForm.querySelector('input[placeholder="Username"]').value;
            const email = signupForm.querySelector('input[type="email"]').value;
            const password = signupForm.querySelector('input[type="password"]').value;
            
            try {
                await signup(username, email, password);
            } catch (error) {
                const errorDiv = signupForm.querySelector('.text-red-500');
                errorDiv.textContent = error.message;
                errorDiv.classList.remove('hidden');
            }
        });
    }

    // Check authentication status on protected pages
    if (!window.location.pathname.includes('login.html')) {
        checkAuth().then(isAuthenticated => {
            if (!isAuthenticated) {
                window.location.href = 'login.html';
            }
        });
    }
});
