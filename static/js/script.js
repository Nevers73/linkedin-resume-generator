// AutoRésumé LinkedIn - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
});

function initApp() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize form handling
    initFormHandling();
    
    // Initialize animations
    initAnimations();
    
    // Initialize tooltips
    initTooltips();
}

function initFormHandling() {
    const form = document.getElementById('resume-form');
    const urlInput = document.getElementById('linkedin-url');
    const generateBtn = document.getElementById('generate-btn');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('error-message');

    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }

    if (urlInput) {
        urlInput.addEventListener('input', validateUrl);
        urlInput.addEventListener('blur', validateUrl);
    }

    function validateUrl() {
        const url = urlInput.value.trim();
        const isValid = url.includes('linkedin.com/in/');
        
        if (url && !isValid) {
            urlInput.classList.add('input-error');
            urlInput.classList.remove('input-success');
            showError('Veuillez entrer une URL LinkedIn valide (ex: https://www.linkedin.com/in/votre-profil)');
        } else if (url && isValid) {
            urlInput.classList.remove('input-error');
            urlInput.classList.add('input-success');
            hideError();
        } else {
            urlInput.classList.remove('input-error', 'input-success');
            hideError();
        }
    }

    async function handleFormSubmit(e) {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        
        if (!url) {
            showError('Veuillez entrer une URL LinkedIn');
            return;
        }
        
        if (!url.includes('linkedin.com/in/')) {
            showError('Veuillez entrer une URL LinkedIn valide');
            return;
        }

        // Show loading state
        setLoadingState(true);
        
        try {
            const response = await fetch('/api/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    linkedin_url: url
                })
            });

            if (response.ok) {
                // Handle PDF download
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = `resume_${Date.now()}.pdf`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(downloadUrl);
                
                // Show success message
                showSuccess('CV généré avec succès ! Téléchargement en cours...');
                
                // Reset form
                form.reset();
                urlInput.classList.remove('input-success');
                
                // Track conversion (for analytics)
                trackConversion();
                
            } else {
                const errorData = await response.json();
                showError(errorData.error || 'Erreur lors de la génération du CV');
            }
            
        } catch (error) {
            console.error('Error:', error);
            showError('Erreur de connexion. Veuillez réessayer.');
        } finally {
            setLoadingState(false);
        }
    }

    function setLoadingState(isLoading) {
        if (isLoading) {
            generateBtn.disabled = true;
            generateBtn.classList.add('btn-loading');
            generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Génération en cours...';
            loadingDiv.classList.remove('hidden');
            hideError();
        } else {
            generateBtn.disabled = false;
            generateBtn.classList.remove('btn-loading');
            generateBtn.innerHTML = '<i class="fas fa-magic mr-2"></i>Générer mon CV';
            loadingDiv.classList.add('hidden');
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorDiv.classList.remove('hidden');
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function hideError() {
        errorDiv.classList.add('hidden');
    }

    function showSuccess(message) {
        showNotification(message, 'success');
    }
}

function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .testimonial-card, .pricing-card').forEach(el => {
        observer.observe(el);
    });

    // Add hover animations
    document.querySelectorAll('.card-hover').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

function initTooltips() {
    // Initialize tooltips for elements with data-tooltip attribute
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = this.querySelector('.tooltiptext');
            if (tooltip) {
                tooltip.style.visibility = 'visible';
                tooltip.style.opacity = '1';
            }
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltiptext');
            if (tooltip) {
                tooltip.style.visibility = 'hidden';
                tooltip.style.opacity = '0';
            }
        });
    });
}

function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());

    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} mr-2"></i>
            <span>${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    // Hide notification after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function scrollToForm() {
    const formSection = document.getElementById('form-section');
    if (formSection) {
        formSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function trackConversion() {
    // Track conversion for analytics
    if (typeof gtag !== 'undefined') {
        gtag('event', 'conversion', {
            'send_to': 'AW-CONVERSION_ID/CONVERSION_LABEL'
        });
    }
    
    // Track with Facebook Pixel
    if (typeof fbq !== 'undefined') {
        fbq('track', 'Purchase', {
            value: 0.00,
            currency: 'EUR'
        });
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Add smooth scrolling for all internal links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Add loading animation for images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });
    });
});

// Add mobile menu functionality
function initMobileMenu() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// Initialize mobile menu
initMobileMenu();

// Add form validation feedback
function addFormValidationFeedback() {
    const inputs = document.querySelectorAll('input[required], textarea[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.classList.add('input-error');
            } else {
                this.classList.remove('input-error');
                this.classList.add('input-success');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.classList.remove('input-error');
            }
        });
    });
}

// Initialize form validation feedback
addFormValidationFeedback();

// Add scroll-based animations
function initScrollAnimations() {
    const scrollElements = document.querySelectorAll('.scroll-animate');
    
    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <=
            (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };
    
    const displayScrollElement = (element) => {
        element.classList.add('scrolled');
    };
    
    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.25)) {
                displayScrollElement(el);
            }
        });
    };
    
    window.addEventListener('scroll', throttle(handleScrollAnimation, 100));
}

// Initialize scroll animations
initScrollAnimations(); 