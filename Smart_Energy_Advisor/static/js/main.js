// Smart Energy Advisor Core JavaScript Operations

// 1. Password Visibility Toggle
function togglePasswordVisibility(inputId, button) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    const icon = button.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// 2. Alert message for Forgot Password (UI only)
function showForgotPasswordAlert() {
    alert("ℹ️ Forgot Password reset features are currently simulating in sandbox. In production systems, a secure SMTP authentication token would be sent to your inbox to reset credentials.");
}

// 3. Client-Side Register Password Validation
function validateRegisterForm() {
    const pwd = document.getElementById('password').value;
    const confirmPwd = document.getElementById('confirm_password').value;
    const errorCard = document.getElementById('form-error-card');
    const errorText = document.getElementById('form-error-text');
    
    if (pwd !== confirmPwd) {
        errorText.innerText = "Confirm password does not match password.";
        errorCard.classList.remove('hidden');
        return false;
    }
    
    // Check length
    if (pwd.length < 8) {
        errorText.innerText = "Password must be at least 8 characters.";
        errorCard.classList.remove('hidden');
        return false;
    }
    
    // Check uppercase
    if (!/[A-Z]/.test(pwd)) {
        errorText.innerText = "Password must contain at least one uppercase letter.";
        errorCard.classList.remove('hidden');
        return false;
    }
    
    // Check special character
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) {
        errorText.innerText = "Password must contain at least one special character.";
        errorCard.classList.remove('hidden');
        return false;
    }
    
    errorCard.classList.add('hidden');
    return true;
}

// 4. Change Password Form Validations
function validateChangePasswordForm() {
    const newPwd = document.getElementById('new_password').value;
    const confirmPwd = document.getElementById('confirm_password').value;
    const errorCard = document.getElementById('change-pwd-error-card');
    const errorText = document.getElementById('change-pwd-error-text');
    
    if (newPwd !== confirmPwd) {
        errorText.innerText = "Confirm password does not match new password.";
        errorCard.classList.remove('hidden');
        return false;
    }
    
    if (newPwd.length < 8 || !/[A-Z]/.test(newPwd) || !/[!@#$%^&*(),.?":{}|<>]/.test(newPwd)) {
        errorText.innerText = "New password must meet complexity rules (8+ chars, uppercase, symbol).";
        errorCard.classList.remove('hidden');
        return false;
    }
    
    errorCard.classList.add('hidden');
    return true;
}

// 5. Auto Fade Out Flash Notification Toasts
document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll("#toast-container > div");
    toasts.forEach(toast => {
        // Automatically hide and delete toast after 4.5 seconds
        setTimeout(() => {
            toast.style.transform = "translateX(150%)";
            toast.style.opacity = "0";
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 4500);
    });
});
