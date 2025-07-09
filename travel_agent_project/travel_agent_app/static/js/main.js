document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        });
    }
    
    // Login modal for protected pages
    const loginModal = document.getElementById('loginModal');
    const closeModal = document.querySelector('.close-modal');
    
    if (loginModal) {
        // Show modal if user tries to access protected page without login
        if (window.location.href.includes('error=login_required')) {
            loginModal.style.display = 'flex';
        }
        
        // Close modal
        if (closeModal) {
            closeModal.addEventListener('click', function() {
                loginModal.style.display = 'none';
            });
        }
        
        // Close when clicking outside
        window.addEventListener('click', function(e) {
            if (e.target === loginModal) {
                loginModal.style.display = 'none';
            }
        });
    }
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            let valid = true;
            
            this.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderColor = 'var(--danger-color)';
                    valid = false;
                    
                    // Add error message if not exists
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-message')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.className = 'error-message';
                        errorMsg.textContent = 'This field is required';
                        errorMsg.style.color = 'var(--danger-color)';
                        errorMsg.style.fontSize = '0.875rem';
                        errorMsg.style.marginTop = '0.25rem';
                        input.insertAdjacentElement('afterend', errorMsg);
                    }
                } else {
                    input.style.borderColor = '';
                    if (input.nextElementSibling && input.nextElementSibling.classList.contains('error-message')) {
                        input.nextElementSibling.remove();
                    }
                }
            });
            
            if (!valid) {
                e.preventDefault();
                
                // Scroll to first error
                const firstError = this.querySelector('[required]:invalid');
                if (firstError) {
                    firstError.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                    firstError.focus();
                }
            }
        });
    });
    
    // Price formatting
    document.querySelectorAll('input[type="number"][name*="price"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
});