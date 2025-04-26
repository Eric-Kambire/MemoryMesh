// Tailwind Configuration
tailwind.config = {
    theme: {
        extend: {
            fontFamily: {
                'inter': ['Inter', 'sans-serif'],
            },
            colors: {
                'bg-primary': '#F7F9F6',
                'accent-primary': '#C7F0DA',
                'text-primary': '#1F2937',
                'text-secondary': '#6B7280',
                'icon-active': '#4ADE80',
                'border': '#E5E7EB',
            }
        }
    }
};

// Auth Tabs Functionality
function setupAuthTabs() {
    const loginTab = document.getElementById('login-tab');
    const signupTab = document.getElementById('signup-tab');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (loginTab && signupTab) {
        loginTab.addEventListener('click', () => {
            loginTab.classList.add('active');
            signupTab.classList.remove('active');
            loginForm.classList.remove('hidden');
            signupForm.classList.add('hidden');
        });

        signupTab.addEventListener('click', () => {
            signupTab.classList.add('active');
            loginTab.classList.remove('active');
            signupForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
        });
    }
}

// Quiz Input Validation
function setupQuizValidation() {
    const quizInputs = document.querySelectorAll('.quiz-input');
    
    quizInputs.forEach(input => {
        input.addEventListener('input', (e) => {
            const value = e.target.value.trim();
            if (value) {
                input.classList.add('border-icon-active');
            } else {
                input.classList.remove('border-icon-active');
            }
        });
    });
}

// Calendar Event Handling
function setupCalendarEvents() {
    const calendarDays = document.querySelectorAll('.calendar-day');
    
    calendarDays.forEach(day => {
        day.addEventListener('click', () => {
            // Remove previous selection
            document.querySelector('.calendar-day.selected')?.classList.remove('selected');
            // Add new selection
            day.classList.add('selected');
        });
    });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setupAuthTabs();
    setupQuizValidation();
    setupCalendarEvents();
});
