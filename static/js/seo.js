// SEO Optimization Script
(function() {
    'use strict';
    
    // Ajout de métadonnées JSON-LD dynamiques
    function addStructuredData() {
        const structuredData = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "AutoRésumé LinkedIn PDF",
            "description": "Transformez votre profil LinkedIn en CV PDF professionnel en 30 secondes",
            "url": window.location.origin,
            "applicationCategory": "ProductivityApplication",
            "operatingSystem": "Web Browser",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "EUR",
                "description": "Version gratuite disponible"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "ratingCount": "1250",
                "bestRating": "5",
                "worstRating": "1"
            },
            "author": {
                "@type": "Organization",
                "name": "AutoRésumé LinkedIn"
            },
            "datePublished": "2024-01-15",
            "dateModified": new Date().toISOString().split('T')[0]
        };
        
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(structuredData);
        document.head.appendChild(script);
    }
    
    // Ajout de métadonnées pour les FAQ
    function addFAQStructuredData() {
        const faqData = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Comment fonctionne AutoRésumé LinkedIn ?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Il suffit de coller l'URL de votre profil LinkedIn public et notre outil extrait automatiquement vos informations pour générer un CV PDF professionnel en 30 secondes."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Est-ce que c'est gratuit ?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Oui, la version de base est entièrement gratuite. Vous pouvez générer votre CV sans aucune limitation."
                    }
                },
                {
                    "@type": "Question",
                    "name": "Mes données sont-elles sécurisées ?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Absolument. Nous ne stockons aucune de vos données. Tout est traité en temps réel et supprimé immédiatement après la génération du PDF."
                    }
                }
            ]
        };
        
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(faqData);
        document.head.appendChild(script);
    }
    
    // Optimisation des images pour le SEO
    function optimizeImages() {
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (!img.hasAttribute('alt')) {
                img.setAttribute('alt', 'AutoRésumé LinkedIn - Générateur de CV');
            }
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }
        });
    }
    
    // Ajout de métadonnées pour les réseaux sociaux
    function addSocialMetaTags() {
        const metaTags = [
            { property: 'og:type', content: 'website' },
            { property: 'og:url', content: window.location.href },
            { property: 'og:title', content: 'AutoRésumé LinkedIn PDF - Générateur de CV Professionnel Gratuit' },
            { property: 'og:description', content: 'Transformez votre profil LinkedIn en CV PDF professionnel en 30 secondes. Outil gratuit et automatique.' },
            { property: 'og:image', content: window.location.origin + '/static/images/og-image.jpg' },
            { property: 'og:image:width', content: '1200' },
            { property: 'og:image:height', content: '630' },
            { property: 'og:locale', content: 'fr_FR' },
            { property: 'og:site_name', content: 'AutoRésumé LinkedIn' },
            { name: 'twitter:card', content: 'summary_large_image' },
            { name: 'twitter:title', content: 'AutoRésumé LinkedIn PDF - Générateur de CV Professionnel Gratuit' },
            { name: 'twitter:description', content: 'Transformez votre profil LinkedIn en CV PDF professionnel en 30 secondes. Outil gratuit et automatique.' },
            { name: 'twitter:image', content: window.location.origin + '/static/images/twitter-image.jpg' }
        ];
        
        metaTags.forEach(tag => {
            const meta = document.createElement('meta');
            if (tag.property) {
                meta.setAttribute('property', tag.property);
            }
            if (tag.name) {
                meta.setAttribute('name', tag.name);
            }
            meta.setAttribute('content', tag.content);
            document.head.appendChild(meta);
        });
    }
    
    // Initialisation
    document.addEventListener('DOMContentLoaded', function() {
        addStructuredData();
        addFAQStructuredData();
        optimizeImages();
        addSocialMetaTags();
        
        // Tracking des événements pour l'analytics
        if (typeof gtag !== 'undefined') {
            // Track page view
            gtag('event', 'page_view', {
                page_title: document.title,
                page_location: window.location.href
            });
            
            // Track form interactions
            const form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', function() {
                    gtag('event', 'form_submit', {
                        form_name: 'linkedin_resume_generator'
                    });
                });
            }
        }
    });
    
})(); 