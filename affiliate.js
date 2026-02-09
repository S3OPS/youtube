/**
 * Amazon Affiliate Link Manager
 * Automatically adds affiliate tracking parameters to all Amazon links
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
            console.error('Affiliate configuration not loaded. Make sure config.js is included before affiliate.js');
            return;
        }

        const config = window.AFFILIATE_CONFIG;
        
        // Validate affiliate ID
        if (!config.affiliateId || config.affiliateId === 'YOUR-AFFILIATE-ID-20') {
            console.warn('⚠️  Please set your Amazon Affiliate ID in config.js');
            showWarningBanner();
        }

        // Find all Amazon links
        const amazonLinks = document.querySelectorAll('a[href*="amazon"]');
        
        console.log(`Found ${amazonLinks.length} Amazon links`);

        // Process each link
        amazonLinks.forEach(link => {
            processAffiliateLink(link, config);
        });

        // Add click tracking for analytics (optional)
        addClickTracking(amazonLinks);

        console.log('✅ Affiliate links initialized successfully');
    }

    function processAffiliateLink(link, config) {
        try {
            const originalHref = link.getAttribute('href');
            const url = new URL(originalHref);

            // Only process Amazon links
            if (!url.hostname.includes('amazon')) {
                return;
            }

            // Update domain if specified
            if (config.amazonDomain && url.hostname !== `www.${config.amazonDomain}`) {
                url.hostname = `www.${config.amazonDomain}`;
            }

            // Add or update the tag parameter (affiliate ID)
            url.searchParams.set('tag', config.affiliateId);

            // Add additional parameters if specified
            if (config.additionalParams) {
                for (const [key, value] of Object.entries(config.additionalParams)) {
                    url.searchParams.set(key, value);
                }
            }

            // Update the link
            link.setAttribute('href', url.toString());
            
            // Add target="_blank" to open in new tab
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');

            // Add a visual indicator class
            link.classList.add('affiliate-link-processed');

        } catch (error) {
            console.error('Error processing link:', link.href, error);
        }
    }

    function addClickTracking(links) {
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const productName = this.getAttribute('data-product') || 'Unknown Product';
                
                // Log click (you can integrate with Google Analytics or other tracking)
                console.log('Affiliate link clicked:', productName, this.href);
                
                // Optional: Send to analytics
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'click', {
                        'event_category': 'Affiliate Link',
                        'event_label': productName,
                        'value': 1
                    });
                }
            });
        });
    }

    function showWarningBanner() {
        // Create warning banner for missing affiliate ID
        const banner = document.createElement('div');
        banner.className = 'affiliate-warning-banner';
        banner.innerHTML = `
            <strong>⚠️ Setup Required:</strong> 
            Please configure your Amazon Affiliate ID in <code>config.js</code> to start earning commissions.
            <button onclick="this.parentElement.remove()">✕</button>
        `;
        banner.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #ff9800;
            color: white;
            padding: 15px;
            text-align: center;
            z-index: 9999;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        `;
        banner.querySelector('button').style.cssText = `
            background: white;
            color: #ff9800;
            border: none;
            padding: 5px 10px;
            margin-left: 15px;
            cursor: pointer;
            border-radius: 3px;
            font-weight: bold;
        `;
        document.body.insertBefore(banner, document.body.firstChild);
    }

    // Add a utility function to manually process dynamically added links
    window.processNewAmazonLinks = function(container) {
        const links = container.querySelectorAll('a[href*="amazon"]');
        links.forEach(link => {
            processAffiliateLink(link, window.AFFILIATE_CONFIG);
        });
    };

})();
