/**
 * Image Fallback Handler
 * Handles cases where Amazon images are blocked by ad blockers or content blockers
 */

(function() {
    'use strict';

    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initImageFallback);
    } else {
        initImageFallback();
    }

    function initImageFallback() {
        // Find all product images
        const productImages = document.querySelectorAll('.product-image');
        
        console.log(`Setting up fallback for ${productImages.length} product images`);

        // Add error handler to each image
        productImages.forEach(img => {
            // Create a placeholder gradient based on product name
            const productCard = img.closest('.product-card');
            const productName = productCard ? productCard.querySelector('h4')?.textContent : 'Product';
            
            img.addEventListener('error', function() {
                // Replace with a styled placeholder
                this.style.backgroundColor = '#1a0a0a';
                this.style.display = 'flex';
                this.style.alignItems = 'center';
                this.style.justifyContent = 'center';
                this.style.fontSize = '3rem';
                this.style.color = '#ff0040';
                this.style.textShadow = '0 0 10px rgba(255, 0, 64, 0.5)';
                
                // Add an icon based on category
                const icon = getIconForProduct(productName);
                this.alt = icon;
                this.setAttribute('data-placeholder', icon);
                
                // Create a pseudo-element effect using CSS
                this.classList.add('image-placeholder');
            });

            // Also handle successful loads
            img.addEventListener('load', function() {
                this.classList.add('image-loaded');
            });

            // Trigger load check for images that might be already cached
            if (img.complete && img.naturalHeight === 0) {
                img.dispatchEvent(new Event('error'));
            }
        });

        // Add CSS for placeholder styling
        addPlaceholderStyles();
    }

    function getIconForProduct(productName) {
        const name = productName.toLowerCase();
        
        // Electronics
        if (name.includes('phone') || name.includes('iphone') || name.includes('galaxy')) return '📱';
        if (name.includes('laptop') || name.includes('macbook') || name.includes('computer')) return '💻';
        if (name.includes('camera') || name.includes('canon') || name.includes('sony') || name.includes('nikon')) return '📷';
        if (name.includes('tv') || name.includes('television') || name.includes('oled')) return '📺';
        if (name.includes('headphone') || name.includes('airpod') || name.includes('earbuds')) return '🎧';
        if (name.includes('tablet') || name.includes('ipad')) return '📲';
        if (name.includes('watch') || name.includes('smartwatch')) return '⌚';
        if (name.includes('speaker') || name.includes('soundbar') || name.includes('sonos')) return '🔊';
        if (name.includes('drone') || name.includes('mavic')) return '🚁';
        
        // Kitchen & Food
        if (name.includes('coffee') || name.includes('espresso')) return '☕';
        if (name.includes('water') && name.includes('bottle')) return '💧';
        if (name.includes('tea')) return '🍵';
        if (name.includes('snack') || name.includes('granola') || name.includes('bar')) return '🍫';
        if (name.includes('oatmeal')) return '🥣';
        
        // Cleaning & Household
        if (name.includes('vacuum') || name.includes('roomba')) return '🧹';
        if (name.includes('paper') && name.includes('towel')) return '🧻';
        if (name.includes('tissue') || name.includes('kleenex')) return '🧻';
        if (name.includes('toilet') && name.includes('paper')) return '🧻';
        if (name.includes('trash') || name.includes('garbage') || name.includes('bag')) return '🗑️';
        if (name.includes('dish') && (name.includes('soap') || name.includes('detergent'))) return '🧼';
        if (name.includes('sponge') || name.includes('scotch-brite')) return '🧽';
        if (name.includes('clean') || name.includes('lysol') || name.includes('clorox')) return '🧴';
        if (name.includes('wipe') || name.includes('disinfect')) return '🧽';
        if (name.includes('laundry') || name.includes('tide') || name.includes('detergent')) return '🧺';
        if (name.includes('dryer') && name.includes('sheet')) return '🧺';
        if (name.includes('air fresh') || name.includes('febreze') || name.includes('glade')) return '🌸';
        if (name.includes('storage') && name.includes('bag')) return '📦';
        if (name.includes('ziploc') || name.includes('food storage')) return '📦';
        if (name.includes('aluminum') || name.includes('foil')) return '🥘';
        if (name.includes('wrap') || name.includes('saran')) return '📦';
        if (name.includes('container') || name.includes('rubbermaid')) return '📦';
        if (name.includes('mop') || name.includes('swiffer')) return '🧹';
        
        // Personal Care
        if (name.includes('toothpaste') || name.includes('crest')) return '🦷';
        if (name.includes('toothbrush')) return '🪥';
        if (name.includes('shampoo') || name.includes('conditioner')) return '🧴';
        if (name.includes('body wash') || name.includes('soap')) return '🧼';
        if (name.includes('deodorant')) return '🧴';
        if (name.includes('razor') || name.includes('gillette')) return '🪒';
        if (name.includes('lotion') || name.includes('moisturizer')) return '🧴';
        if (name.includes('hand sanitizer')) return '🧴';
        
        // Home & Appliances
        if (name.includes('air') && name.includes('fryer')) return '🍳';
        if (name.includes('blender') || name.includes('vitamix')) return '🥤';
        if (name.includes('refrigerator') || name.includes('fridge')) return '🧊';
        if (name.includes('washer') || name.includes('dryer')) return '🧺';
        if (name.includes('thermostat') || name.includes('nest')) return '🌡️';
        if (name.includes('doorbell') || name.includes('ring')) return '🔔';
        if (name.includes('light') && name.includes('bulb')) return '💡';
        if (name.includes('battery') || name.includes('energizer') || name.includes('duracell')) return '🔋';
        if (name.includes('command') && name.includes('hook')) return '🔧';
        if (name.includes('hanger')) return '👔';
        
        // Gaming & Computing
        if (name.includes('game') || name.includes('playstation') || name.includes('xbox')) return '🎮';
        if (name.includes('monitor') || name.includes('display')) return '🖥️';
        if (name.includes('keyboard')) return '⌨️';
        if (name.includes('mouse')) return '🖱️';
        if (name.includes('router') || name.includes('wifi')) return '📡';
        
        // Office Supplies
        if (name.includes('pen') || name.includes('bic')) return '✒️';
        if (name.includes('post-it') || name.includes('sticky')) return '📋';
        if (name.includes('notebook') || name.includes('paper')) return '📓';
        if (name.includes('marker') || name.includes('sharpie')) return '🖊️';
        if (name.includes('tape') || name.includes('scotch')) return '📎';
        
        // Fitness & Wellness
        if (name.includes('fitness') || name.includes('treadmill') || name.includes('bike')) return '💪';
        if (name.includes('yoga')) return '🧘';
        if (name.includes('dumbbell') || name.includes('weight')) return '🏋️';
        if (name.includes('protein') || name.includes('supplement')) return '🥤';
        if (name.includes('bottle') || name.includes('water')) return '🧴';
        
        return '🛍️'; // Default shopping icon
    }

    function addPlaceholderStyles() {
        if (document.getElementById('image-fallback-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'image-fallback-styles';
        style.textContent = `
            .image-placeholder {
                position: relative;
                background: linear-gradient(135deg, #1a0a0a 0%, #2a0a0a 50%, #1a0a0a 100%) !important;
                border: 2px solid #ff0040 !important;
            }
            
            .image-placeholder::after {
                content: attr(data-placeholder);
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 4rem;
                filter: drop-shadow(0 0 10px rgba(255, 0, 64, 0.5));
            }
            
            .image-loaded {
                animation: imageReveal 0.5s ease-in-out;
            }
            
            @keyframes imageReveal {
                from {
                    opacity: 0;
                    filter: brightness(0.5);
                }
                to {
                    opacity: 1;
                    filter: brightness(0.9);
                }
            }
        `;
        document.head.appendChild(style);
    }

})();
