// AutoRésumé LinkedIn - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resume-form');
    const generateBtn = document.getElementById('generate-btn');
    const demoBtn = document.getElementById('demo-btn');
    const urlInput = document.getElementById('linkedin-url');
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');

    // Gestion du bouton démo
    if (demoBtn) {
        demoBtn.addEventListener('click', function() {
            generateResume(true);
        });
    }

    // Gestion du formulaire principal
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            generateResume(false);
        });
    }

    function generateResume(useSample = false) {
        // Reset messages
        hideMessages();
        
        // Show loading
        showLoading(true);
        
        const linkedinUrl = urlInput ? urlInput.value.trim() : '';
        
        // Validation
        if (!useSample && !linkedinUrl) {
            showError('Veuillez entrer une URL LinkedIn valide');
            showLoading(false);
            return;
        }

        // Prepare data
        const data = {
            linkedin_url: linkedinUrl,
            use_sample: useSample
        };

        // Make request
        fetch('/api/generate-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                return response.json().then(errorData => {
                    throw new Error(JSON.stringify(errorData));
                });
            }
        })
        .then(blob => {
            // Download PDF
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = useSample ? 'CV_Exemple.pdf' : 'CV_LinkedIn.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showSuccess(useSample ? 'CV d\'exemple généré avec succès !' : 'CV généré avec succès !');
        })
        .catch(error => {
            try {
                const errorData = JSON.parse(error.message);
                if (errorData.use_sample_available) {
                    showError(`${errorData.error}<br><br><strong>Suggestion :</strong> ${errorData.suggestion}`, true);
                } else {
                    showError(errorData.error || 'Erreur lors de la génération du CV');
                }
            } catch {
                showError('Erreur lors de la génération du CV');
            }
        })
        .finally(() => {
            showLoading(false);
        });
    }

    function showLoading(show) {
        if (show) {
            if (generateBtn) {
                generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Génération en cours...';
                generateBtn.disabled = true;
            }
            if (demoBtn) {
                demoBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Génération en cours...';
                demoBtn.disabled = true;
            }
        } else {
            if (generateBtn) {
                generateBtn.innerHTML = '<i class="fas fa-file-pdf mr-2"></i>Générer mon CV';
                generateBtn.disabled = false;
            }
            if (demoBtn) {
                demoBtn.innerHTML = '<i class="fas fa-play mr-2"></i>Mode Démo';
                demoBtn.disabled = false;
            }
        }
    }

    function showError(message, isHtml = false) {
        if (errorDiv) {
            errorDiv.innerHTML = isHtml ? message : `<i class="fas fa-exclamation-triangle mr-2"></i>${message}`;
            errorDiv.classList.remove('hidden');
            errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    function showSuccess(message) {
        if (successDiv) {
            successDiv.innerHTML = `<i class="fas fa-check-circle mr-2"></i>${message}`;
            successDiv.classList.remove('hidden');
            successDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    function hideMessages() {
        if (errorDiv) errorDiv.classList.add('hidden');
        if (successDiv) successDiv.classList.add('hidden');
    }

    // Auto-hide messages after 5 seconds
    setInterval(() => {
        if (errorDiv && !errorDiv.classList.contains('hidden')) {
            errorDiv.classList.add('hidden');
        }
        if (successDiv && !successDiv.classList.contains('hidden')) {
            successDiv.classList.add('hidden');
        }
    }, 5000);

    // Initialize animations
    initAnimations();
    
    // Initialize tooltips
    initTooltips();
});

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