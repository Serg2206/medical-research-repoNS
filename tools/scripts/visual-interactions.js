/**
 * Visual Interactions JavaScript
 * Medical Manuscript System
 * Date: November 10, 2025
 * 
 * Provides interactive functionality for:
 * - Image gallery lightbox
 * - Comparison sliders
 * - Keyboard navigation
 * - Accessibility features
 */

(function() {
    'use strict';

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        initLightboxes();
        initComparisonSliders();
        initKeyboardNavigation();
    }

    /**
     * Initialize lightbox functionality for image galleries
     */
    function initLightboxes() {
        const galleries = document.querySelectorAll('.image-gallery');
        
        galleries.forEach(gallery => {
            const galleryId = gallery.id;
            const lightboxId = galleryId + '-lightbox';
            const lightbox = document.getElementById(lightboxId);
            
            if (!lightbox) return;
            
            const items = gallery.querySelectorAll('.gallery-item.lightbox-enabled');
            const lightboxImage = lightbox.querySelector('.lightbox-image');
            const lightboxCaption = lightbox.querySelector('.lightbox-caption');
            const closeBtn = lightbox.querySelector('.lightbox-close');
            const prevBtn = lightbox.querySelector('.lightbox-prev');
            const nextBtn = lightbox.querySelector('.lightbox-next');
            
            let currentIndex = 0;
            
            // Open lightbox
            items.forEach((item, index) => {
                item.addEventListener('click', () => {
                    currentIndex = index;
                    showLightboxImage(currentIndex);
                    lightbox.style.display = 'flex';
                    document.body.style.overflow = 'hidden';
                });
                
                // Keyboard accessibility for gallery items
                item.setAttribute('tabindex', '0');
                item.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        item.click();
                    }
                });
            });
            
            // Close lightbox
            function closeLightbox() {
                lightbox.style.display = 'none';
                document.body.style.overflow = '';
            }
            
            closeBtn.addEventListener('click', closeLightbox);
            
            lightbox.addEventListener('click', (e) => {
                if (e.target === lightbox) {
                    closeLightbox();
                }
            });
            
            // Navigation
            function showLightboxImage(index) {
                const item = items[index];
                const img = item.querySelector('img');
                const caption = item.querySelector('.gallery-caption');
                
                lightboxImage.src = img.src;
                lightboxImage.alt = img.alt;
                
                if (caption) {
                    lightboxCaption.textContent = caption.textContent;
                } else {
                    lightboxCaption.textContent = '';
                }
            }
            
            prevBtn.addEventListener('click', () => {
                currentIndex = (currentIndex - 1 + items.length) % items.length;
                showLightboxImage(currentIndex);
            });
            
            nextBtn.addEventListener('click', () => {
                currentIndex = (currentIndex + 1) % items.length;
                showLightboxImage(currentIndex);
            });
            
            // Keyboard navigation for lightbox
            document.addEventListener('keydown', (e) => {
                if (lightbox.style.display === 'flex') {
                    if (e.key === 'Escape') {
                        closeLightbox();
                    } else if (e.key === 'ArrowLeft') {
                        prevBtn.click();
                    } else if (e.key === 'ArrowRight') {
                        nextBtn.click();
                    }
                }
            });
        });
    }

    /**
     * Initialize comparison slider functionality
     */
    function initComparisonSliders() {
        const sliders = document.querySelectorAll('.comparison-slider-container');
        
        sliders.forEach(container => {
            const wrapper = container.querySelector('.comparison-slider-wrapper');
            const handle = container.querySelector('.comparison-slider-handle');
            const beforeWrapper = container.querySelector('.comparison-before-wrapper');
            
            if (!wrapper || !handle || !beforeWrapper) return;
            
            let isDragging = false;
            
            // Mouse events
            handle.addEventListener('mousedown', startDrag);
            document.addEventListener('mousemove', drag);
            document.addEventListener('mouseup', stopDrag);
            
            // Touch events
            handle.addEventListener('touchstart', startDrag);
            document.addEventListener('touchmove', drag);
            document.addEventListener('touchend', stopDrag);
            
            function startDrag(e) {
                isDragging = true;
                e.preventDefault();
            }
            
            function stopDrag() {
                isDragging = false;
            }
            
            function drag(e) {
                if (!isDragging) return;
                
                e.preventDefault();
                
                const rect = wrapper.getBoundingClientRect();
                let x;
                
                if (e.type === 'touchmove') {
                    x = e.touches[0].clientX - rect.left;
                } else {
                    x = e.clientX - rect.left;
                }
                
                // Constrain x to wrapper bounds
                x = Math.max(0, Math.min(x, rect.width));
                
                const percentage = (x / rect.width) * 100;
                
                handle.style.left = percentage + '%';
                beforeWrapper.style.width = percentage + '%';
            }
            
            // Keyboard navigation for comparison slider
            handle.setAttribute('tabindex', '0');
            handle.setAttribute('role', 'slider');
            handle.setAttribute('aria-label', 'Comparison slider');
            handle.setAttribute('aria-valuemin', '0');
            handle.setAttribute('aria-valuemax', '100');
            
            handle.addEventListener('keydown', (e) => {
                const rect = wrapper.getBoundingClientRect();
                const currentLeft = parseFloat(handle.style.left) || 50;
                let newLeft = currentLeft;
                
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    newLeft = Math.max(0, currentLeft - 5);
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    newLeft = Math.min(100, currentLeft + 5);
                }
                
                if (newLeft !== currentLeft) {
                    handle.style.left = newLeft + '%';
                    beforeWrapper.style.width = newLeft + '%';
                    handle.setAttribute('aria-valuenow', Math.round(newLeft));
                }
            });
            
            // Set initial aria-valuenow
            const initialValue = parseFloat(handle.style.left) || 50;
            handle.setAttribute('aria-valuenow', Math.round(initialValue));
        });
    }

    /**
     * Initialize keyboard navigation for all interactive elements
     */
    function initKeyboardNavigation() {
        // Add keyboard hints for screen readers
        const galleries = document.querySelectorAll('.image-gallery');
        galleries.forEach(gallery => {
            gallery.setAttribute('role', 'list');
            gallery.setAttribute('aria-label', 'Image gallery');
            
            const items = gallery.querySelectorAll('.gallery-item');
            items.forEach(item => {
                item.setAttribute('role', 'listitem');
            });
        });
        
        // Multi-panel figures
        const figures = document.querySelectorAll('.multi-panel-figure');
        figures.forEach(figure => {
            figure.setAttribute('role', 'group');
            figure.setAttribute('aria-label', 'Multi-panel figure');
        });
        
        // Procedure steps
        const procedures = document.querySelectorAll('.procedure-container');
        procedures.forEach(procedure => {
            procedure.setAttribute('role', 'list');
            procedure.setAttribute('aria-label', 'Procedure steps');
            
            const steps = procedure.querySelectorAll('.procedure-step');
            steps.forEach((step, index) => {
                step.setAttribute('role', 'listitem');
                step.setAttribute('aria-label', `Step ${index + 1}`);
            });
        });
    }

    /**
     * Utility: Detect reduced motion preference
     */
    function prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    /**
     * Lazy loading for images (optional enhancement)
     */
    function initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const images = document.querySelectorAll('img[loading="lazy"]');
            
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        }
    }

    // Optional: Initialize lazy loading
    // initLazyLoading();

})();
