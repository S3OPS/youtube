// Amazon Affiliate Configuration
// Replace 'YOUR-AFFILIATE-ID-20' with your actual Amazon Associates tracking ID
// Example: 'mystore-20' or 'johndoe-21'

const AFFILIATE_CONFIG = {
    // Your Amazon Associates Tracking ID (also known as Associate Tag)
    // You can find this in your Amazon Associates account
    affiliateId: 'pablochakone-20',
    
    // Optional: Amazon store domain (for different countries)
    // Examples: 'amazon.com', 'amazon.co.uk', 'amazon.de', 'amazon.ca', etc.
    amazonDomain: 'amazon.com',
    
    // Optional: Add additional parameters if needed
    // These will be appended to the URL
    additionalParams: {
        // Example: 'ref': 'as_li_ss_tl'
    }
};

// Make config available globally
window.AFFILIATE_CONFIG = AFFILIATE_CONFIG;
