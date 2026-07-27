/* Earthnode Ecoworks - Interactive JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            // Animate hamburger to X
            const spans = this.querySelectorAll('span');
            spans.forEach(span => span.classList.toggle('active'));
        });
    }

    // Close mobile menu when clicking a link
    const mobileLinks = document.querySelectorAll('.mobile-menu .nav-link');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
            const spans = mobileMenuBtn.querySelectorAll('span');
            spans.forEach(span => span.classList.remove('active'));
        });
    });

    // Header scroll effect
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll <= 0) {
            header.classList.remove('scrolled');
            return;
        }

        if (currentScroll > lastScroll && !header.classList.contains('scrolled')) {
            // Scrolling down
            header.classList.add('scrolled');
        } else if (currentScroll < lastScroll && header.classList.contains('scrolled')) {
            // Scrolling up
            header.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    });

    // Tab functionality for Focus Areas
    const tabBtns = document.querySelectorAll('.tab-btn');
    const focusPanels = document.querySelectorAll('.focus-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons and panels
            tabBtns.forEach(b => b.classList.remove('active'));
            focusPanels.forEach(panel => panel.classList.remove('active'));

            // Add active class to clicked button
            btn.classList.add('active');

            // Show corresponding panel
            const tabId = btn.getAttribute('data-tab');
            const targetPanel = document.getElementById(`${tabId}-content`);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                // Uncomment if you want to observe once only
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe sections for animation
    const sectionsToAnimate = document.querySelectorAll('[data-animate]');
    sectionsToAnimate.forEach(section => {
        observer.observe(section);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                e.preventDefault();

                // Close mobile menu if open
                if (mobileMenu.classList.contains('active')) {
                    mobileMenu.classList.remove('active');
                    const spans = mobileMenuBtn.querySelectorAll('span');
                    spans.forEach(span => span.classList.remove('active'));
                }

                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Floating Leaves Animation
    function createFloatingLeaves() {
        const leavesContainer = document.getElementById('floatingLeaves');
        if (!leavesContainer) return;

        const leafTypes = ['🍃', '🌿', '🌱', '🍂', '🌾'];
        const numberOfLeaves = 15;

        for (let i = 0; i < numberOfLeaves; i++) {
            const leaf = document.createElement('div');
            leaf.className = 'leaf';
            leaf.textContent = leafTypes[Math.floor(Math.random() * leafTypes.length)];

            // Random position
            leaf.style.left = `${Math.random() * 100}%`;
            leaf.style.top = `${Math.random() * 100}%`;

            // Random size
            const size = Math.random() * 20 + 10;
            leaf.style.fontSize = `${size}px`;

            // Random animation duration and delay
            const duration = Math.random() * 15 + 10;
            const delay = Math.random() * 5;
            leaf.style.animation = `floatLeaf ${duration}s ease-in-out ${delay}s infinite`;

            // Random rotation
            leaf.style.transform = `rotate(${Math.random() * 360}deg)`;

            leavesContainer.appendChild(leaf);
        }
    }

    // Add CSS for leaf animation if not present
    if (!document.getElementById('leaf-animation-style')) {
        const style = document.createElement('style');
        style.id = 'leaf-animation-style';
        style.textContent = `
            @keyframes floatLeaf {
                0% {
                    transform: translateY(0) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 0.6;
                }
                90% {
                    opacity: 0.6;
                }
                100% {
                    transform: translateY(-100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Initialize floating leaves
    createFloatingLeaves();

    // Custom Cursor
    const cursorDot = document.getElementById('cursor-dot');
    const cursorOutline = document.getElementById('cursor-outline');

    if (cursorDot && cursorOutline) {
        document.addEventListener('mousemove', (e) => {
            cursorDot.style.left = `${e.clientX}px`;
            cursorDot.style.top = `${e.clientY}px`;

            cursorOutline.style.left = `${e.clientX}px`;
            cursorOutline.style.top = `${e.clientY}px`;
        });

        // Expand cursor on hoverable elements
        const hoverableElements = document.querySelectorAll('a, button, .btn-primary, .btn-secondary, .tab-btn, .focus-link, .social-links a, .nav-link');

        hoverableElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursorDot.style.width = '12px';
                cursorDot.style.height = '12px';
                cursorOutline.style.width = '40px';
                cursorOutline.style.height = '40px';
                cursorDot.style.background = 'rgba(16, 185, 129, 0.8)';
                cursorOutline.style.borderColor = 'rgba(16, 185, 129, 0.5)';
            });

            el.addEventListener('mouseleave', () => {
                cursorDot.style.width = '8px';
                cursorDot.style.height = '8px';
                cursorOutline.style.width = '36px';
                cursorOutline.style.height = '36px';
                cursorDot.style.background = '#10b981';
                cursorOutline.style.borderColor = '#10b981';
            });
        });
    }

    // Form handling (if any forms exist in the future)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Prevent actual submission for demo
            e.preventDefault();

            // Show success message (would be replaced with actual form handling)
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitText.textContent = 'Sending...';
                submitBtn.disabled = true;

                setTimeout(() => {
                    submitBtn.textContent = 'Sent!';
                    setTimeout(() => {
                        submitBtn.textContent = originalText;
                        submitBtn.disabled = false;
                    }, 2000);
                }, 1500);
            }

            // Reset form
            form.reset();
        });
    });

    // Lazy loading for images (if we add actual images later)
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Add animation classes to sections as they enter viewport
    const animateSections = document.querySelectorAll('section, .hero, .footer');
    animateSections.forEach(section => {
        section.setAttribute('data-animate', '');
    });

    // Re-observe elements after DOM changes (for dynamic content)
    function observeNewElements() {
        const newAnimatedElements = document.querySelectorAll('[data-animate]:not(.animate-in)');
        newAnimatedElements.forEach(el => {
            observer.observe(el);
        });
    }

    // Periodically check for new elements (useful if we add content dynamically)
    setInterval(observeNewElements, 1000);

    // Add active class to nav links based on scroll position
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link, .mobile-menu .nav-link');

    function updateActiveNav() {
        let scrollPosition = window.scrollY + 100; // Account for header height

        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (
                scrollPosition >= sectionTop &&
                scrollPosition < sectionTop + sectionHeight
            ) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav);
    // Also call on load in case we start mid-page
    window.addEventListener('load', updateActiveNav);

    // Prevent accidental form submissions via Enter key in certain contexts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.matches('input[type="text"], input[type="email"], textarea')) {
            // Allow form submission only if there's a submit button nearby
            const form = e.target.closest('form');
            if (form && form.querySelector('button[type="submit"]')) {
                // Allow submission
                return;
            }
            // Prevent form submission for non-form inputs
            e.preventDefault();
        }
    });

    // Add touch support for mobile menus
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', e => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', e => {
        touchEndX = e.changedTouches[0].screenX;
        handleGesture();
    }, { passive: true });

    function handleGesture() {
        const swipeThreshold = 50;
        const diff = touchStartX - touchEndX;

        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0 && mobileMenu.classList.contains('active')) {
                // Swipe left - close menu
                mobileMenu.classList.remove('active');
                const spans = mobileMenuBtn.querySelectorAll('span');
                spans.forEach(span => span.classList.remove('active'));
            } else if (diff < 0 && !mobileMenu.classList.contains('active')) {
                // Swipe right - open menu
                mobileMenu.classList.add('active');
                const spans = mobileMenuBtn.querySelectorAll('span');
                spans.forEach(span => span.classList.add('active'));
            }
        }
    }

    // Print optimization
    window.addEventListener('beforeprint', function() {
        // Hide interactive elements when printing
        document.querySelectorAll('.mobile-menu-btn, .floating-leaves, #cursor-dot, #cursor-outline').forEach(el => {
            el.style.display = 'none';
        });
    });

    window.addEventListener('afterprint', function() {
        // Show interactive elements after printing
        document.querySelectorAll('.mobile-menu-btn, .floating-leaves, #cursor-dot, #cursor-outline').forEach(el => {
            el.style.display = '';
        });
    });

    // Initialize AOS-like animations for elements that should animate on scroll
    function initScrollAnimations() {
        const animatedElements = document.querySelectorAll('[data-animate]');

        animatedElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            const windowHeight = window.innerHeight;

            if (elementTop < windowHeight * 0.8 && elementBottom > 0) {
                element.classList.add('animate-in');
            }
        });
    }

    // Run on load and scroll
    window.addEventListener('load', initScrollAnimations);
    window.addEventListener('scroll', () => {
        requestAnimationFrame(initScrollAnimations);
    });

    // Add hover effects to cards for enhanced interactivity
    const cards = document.querySelectorAll('.mission-card, .value-card, .why-card, .stat-item, .skeleton-item');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.1)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });

    // Performance optimization: throttle resize events
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            // Recalculate positions for floating elements if needed
            // Update any size-dependent calculations
        }, 250);
    });

    // Console message for developers (optional)
    if (console && console.info) {
        console.info('%c Earthnode Ecoworks Website %c', 'background: #10b981; color: white; padding: 2px 4px; border-radius: 2px;', 'background: #042b1d; color: #dcfce7; padding: 2px 4px; border-radius: 2px;', 'Building a movement for environmental action through community, technology, and collaboration.');
    }
});

// Helper function for debouncing (for performance optimization)
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