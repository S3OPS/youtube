/**
 * Site Enhancements
 * - Live product search/filter
 * - Dark mode toggle with localStorage persistence
 */

(function () {
    'use strict';

    // ── Dark Mode ────────────────────────────────────────────────────────────

    var DARK_MODE_KEY = 'darkMode';
    var darkModeToggle = document.getElementById('darkModeToggle');

    function applyDarkMode(enabled) {
        document.body.classList.toggle('dark-mode', enabled);
        if (darkModeToggle) {
            darkModeToggle.textContent = enabled ? '☀️' : '🌙';
            darkModeToggle.title = enabled ? 'Switch to light mode' : 'Switch to dark mode';
        }
    }

    // Restore saved preference (default: light)
    var savedDark = localStorage.getItem(DARK_MODE_KEY) === 'true';
    applyDarkMode(savedDark);

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function () {
            var isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem(DARK_MODE_KEY, isDark);
            darkModeToggle.textContent = isDark ? '☀️' : '🌙';
            darkModeToggle.title = isDark ? 'Switch to light mode' : 'Switch to dark mode';
        });
    }

    // ── Live Search / Filter ─────────────────────────────────────────────────

    var searchInput = document.getElementById('productSearch');
    var resultCount = document.getElementById('searchResultCount');

    if (!searchInput) return;

    searchInput.addEventListener('input', function () {
        var query = this.value.trim().toLowerCase();
        var cards = document.querySelectorAll('.product-card');
        var categories = document.querySelectorAll('.category');
        var visible = 0;

        cards.forEach(function (card) {
            var title = (card.querySelector('.product-content h4') || {}).textContent || '';
            var desc = (card.querySelector('.product-content > p') || {}).textContent || '';
            var match = !query || title.toLowerCase().includes(query) || desc.toLowerCase().includes(query);
            card.classList.toggle('hidden', !match);
            if (match) visible++;
        });

        // Hide categories that have no visible products
        categories.forEach(function (cat) {
            var visibleCards = cat.querySelectorAll('.product-card:not(.hidden)');
            cat.classList.toggle('hidden', visibleCards.length === 0);
        });

        // Show result count when searching
        if (resultCount) {
            if (query) {
                resultCount.textContent = visible + (visible === 1 ? ' product found' : ' products found');
            } else {
                resultCount.textContent = '';
            }
        }
    });

})();
