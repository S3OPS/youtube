/**
 * Amazon Affiliate Link Manager
 * Automatically adds affiliate tracking to Amazon links and optimizes image loading
 */

(function() {
    'use strict';

    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAffiliateLinks);
    } else {
        initAffiliateLinks();
    }

    function initAffiliateLinks() {
        // Check if config is loaded
        if (typeof window.AFFILIATE_CONFIG === 'undefined') {
            console.error('Affiliate configuration not loaded. Ensure config.js is included before affiliate.js');
            return;
        }

        const config = window.AFFILIATE_CONFIG;

        // Find all Amazon links
        const amazonLinks = document.querySelectorAll('a[href*="amazon"]');

        // Process each link
        amazonLinks.forEach(link => {
            try {
                const url = new URL(link.href);

                // Only process Amazon links
                if (!url.hostname.includes('amazon')) {
                    return;
                }

                // Add the affiliate tag parameter
                url.searchParams.set('tag', config.affiliateId);

                // Update the link
                link.href = url.toString();
                
                // Open in new tab
                link.target = '_blank';
                link.rel = 'noopener noreferrer';

            } catch (error) {
                console.error('Error processing link:', error);
            }
        });

        // Optimize image loading
        optimizeImageLoading();
    }

    function optimizeImageLoading() {
        const images = document.querySelectorAll('.product-image');
        const maxRetries = 2;
        
        images.forEach(img => {
            // Store retry count as a data attribute for persistence
            img.setAttribute('data-retry-count', '0');
            
            // Add error handler for failed image loads
            img.addEventListener('error', function() {
                const retryCount = parseInt(this.getAttribute('data-retry-count') || '0');
                console.warn('Failed to load image:', this.src, '(attempt ' + (retryCount + 1) + ')');
                
                if (retryCount < maxRetries) {
                    // Increment retry count
                    this.setAttribute('data-retry-count', (retryCount + 1).toString());
                    // Try to reload the image with a cache-busting parameter
                    const originalSrc = this.src.split('?')[0];
                    this.src = originalSrc + '?retry=' + (retryCount + 1);
                } else {
                    // After retries, show placeholder
                    this.style.backgroundColor = '#f0f0f0';
                    this.style.display = 'flex';
                    this.style.alignItems = 'center';
                    this.style.justifyContent = 'center';
                    this.style.minHeight = '200px';
                    this.alt = 'Image unavailable';
                }
            });

            // Add load handler for successful loads
            img.addEventListener('load', function() {
                this.style.opacity = '1';
                this.style.transition = 'opacity 0.3s ease-in';
            });

            // Set initial opacity for fade-in effect
            img.style.opacity = '0.5';
        });
    }

    // Back to Top Button Functionality
    function initBackToTop() {
        const backToTopButton = document.getElementById('backToTop');
        
        if (!backToTopButton) return;

        // Show/hide button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });

        // Scroll to top when clicked
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Initialize back to top functionality
    initBackToTop();

})();
