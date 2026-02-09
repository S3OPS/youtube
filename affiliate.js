/**
 * Amazon Affiliate Link Manager
 * Automatically adds affiliate tracking to Amazon links
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
            console.error('Affiliate configuration not loaded');
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
    }

})();
