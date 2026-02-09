/**
 * Category Preview Manager
 * Replaces emoji icons with product preview thumbnails and makes images clickable
 */

(function() {
    'use strict';

    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCategoryPreviews);
    } else {
        initCategoryPreviews();
    }

    function initCategoryPreviews() {
        console.log('Initializing category previews...');
        
        // Replace emoji icons with preview thumbnails
        replaceCategoryEmojisWithPreviews();
        
        // Make product images clickable
        makeProductImagesClickable();
        
        console.log('✅ Category previews initialized successfully');
    }

    function replaceCategoryEmojisWithPreviews() {
        const categories = document.querySelectorAll('.category');
        
        categories.forEach(category => {
            const heading = category.querySelector('h3');
            const firstProductCard = category.querySelector('.product-card');
            
            if (!heading || !firstProductCard) return;
            
            // Get the first product image as preview
            const firstImage = firstProductCard.querySelector('.product-image');
            const firstLink = firstProductCard.querySelector('.amazon-link');
            
            if (!firstImage || !firstLink) return;
            
            // Get category name without emoji
            const categoryText = heading.textContent.trim().replace(/[^\w\s-]/g, '').trim();
            
            // Create preview thumbnail
            const preview = document.createElement('img');
            preview.src = firstImage.src;
            preview.alt = categoryText + ' Preview';
            preview.className = 'category-preview-thumb';
            
            // Create link wrapper for the thumbnail
            const previewLink = document.createElement('a');
            previewLink.href = firstLink.href;
            previewLink.className = 'category-preview-link';
            previewLink.appendChild(preview);
            
            // Replace heading content
            heading.innerHTML = '';
            heading.appendChild(previewLink);
            
            // Add text after the preview
            const textSpan = document.createElement('span');
            textSpan.textContent = categoryText;
            textSpan.className = 'category-title-text';
            heading.appendChild(textSpan);
        });
        
        console.log(`Processed ${categories.length} category headers`);
    }

    function makeProductImagesClickable() {
        const productCards = document.querySelectorAll('.product-card');
        let processedCount = 0;
        
        productCards.forEach(card => {
            const image = card.querySelector('.product-image');
            const amazonLink = card.querySelector('.amazon-link');
            
            if (!image || !amazonLink) return;
            
            // Skip if image is already wrapped in a link
            if (image.parentElement.tagName === 'A') return;
            
            // Create wrapper link for the image
            const imageLink = document.createElement('a');
            imageLink.href = amazonLink.href;
            imageLink.className = 'product-image-link amazon-link';
            imageLink.setAttribute('data-product', amazonLink.getAttribute('data-product'));
            imageLink.setAttribute('aria-label', 'View ' + amazonLink.getAttribute('data-product') + ' on Amazon');
            
            // Wrap the image
            image.parentNode.insertBefore(imageLink, image);
            imageLink.appendChild(image);
            
            processedCount++;
        });
        
        console.log(`Made ${processedCount} product images clickable`);
    }

})();
