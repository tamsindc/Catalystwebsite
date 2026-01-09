// Particle Background Animation
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 30;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');

        const size = Math.random() * 20 + 10;
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * window.innerHeight;
        const delay = Math.random() * 15;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${startX}px`;
        particle.style.top = `${startY}px`;
        particle.style.animationDelay = `${delay}s`;

        particlesContainer.appendChild(particle);
    }
}

// Mobile Menu Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Close menu when clicking on a link
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar Background on Scroll
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    }

    lastScroll = currentScroll;
});

// 3D Tilt Effect for Feature Cards
function tiltEffect() {
    const cards = document.querySelectorAll('[data-tilt]');

    cards.forEach(card => {
        card.addEventListener('mousemove', handleTilt);
        card.addEventListener('mouseleave', resetTilt);
    });

    function handleTilt(e) {
        const card = e.currentTarget;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
    }

    function resetTilt(e) {
        const card = e.currentTarget;
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
    }
}

// Intersection Observer for Fade-in Animations
function observeElements() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.feature-card, .workflow-card').forEach(card => {
        observer.observe(card);
    });
}

// Button Click Animations
const downloadBtn = document.getElementById('downloadBtn');
const exploreBtn = document.getElementById('exploreBtn');

downloadBtn.addEventListener('click', () => {
    // Add ripple effect
    createRipple(downloadBtn, event);

    // Simulate download action
    setTimeout(() => {
        alert('🎉 Download starting! Thanks for choosing fshpind.ai');
    }, 300);
});

exploreBtn.addEventListener('click', () => {
    createRipple(exploreBtn, event);
    document.querySelector('#workflows').scrollIntoView({ behavior: 'smooth' });
});

// Ripple Effect Function
function createRipple(button, event) {
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');

    button.appendChild(ripple);

    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Workflow Install Buttons
document.querySelectorAll('.workflow-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        const workflowName = this.parentElement.querySelector('h3').textContent;

        // Add loading state
        const originalText = this.textContent;
        this.textContent = 'Installing...';
        this.style.background = 'var(--cyan)';

        // Simulate installation
        setTimeout(() => {
            this.textContent = '✓ Installed';
            this.style.background = '#4caf50';

            setTimeout(() => {
                this.textContent = originalText;
                this.style.background = '';
            }, 2000);
        }, 1500);
    });
});

// Parallax Effect for Hero Section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroVisual = document.querySelector('.hero-visual');
    const squares = document.querySelectorAll('.square');

    if (heroVisual) {
        heroVisual.style.transform = `translateY(${scrolled * 0.3}px)`;
    }

    squares.forEach((square, index) => {
        square.style.transform = `translateY(${scrolled * (0.1 + index * 0.05)}px)`;
    });
});

// Typing Animation for Hero Title (Alternative)
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// Add cursor animation to CTA buttons
document.querySelectorAll('.btn-primary, .btn-secondary, .download-btn').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
        this.style.cursor = 'pointer';
    });
});

// Animated Counter for Stats (if you want to add stats section)
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);

    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }

    updateCounter();
}

// Easter Egg: Konami Code
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-konamiSequence.length);

    if (konamiCode.join('') === konamiSequence.join('')) {
        activateEasterEgg();
    }
});

function activateEasterEgg() {
    document.body.style.animation = 'rainbow 2s infinite';
    alert('🎮 Konami Code Activated! You found the secret! 🎉');

    setTimeout(() => {
        document.body.style.animation = '';
    }, 5000);
}

// Rainbow animation keyframes (injected dynamically)
const style = document.createElement('style');
style.textContent = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }

    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }

    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Mouse Trail Effect (Optional - can be enabled)
function createMouseTrail() {
    const trail = [];
    const trailLength = 20;

    document.addEventListener('mousemove', (e) => {
        const dot = document.createElement('div');
        dot.style.position = 'fixed';
        dot.style.width = '5px';
        dot.style.height = '5px';
        dot.style.background = 'var(--yellow)';
        dot.style.borderRadius = '50%';
        dot.style.left = e.clientX + 'px';
        dot.style.top = e.clientY + 'px';
        dot.style.pointerEvents = 'none';
        dot.style.opacity = '0.6';
        dot.style.transition = 'opacity 0.5s';

        document.body.appendChild(dot);
        trail.push(dot);

        if (trail.length > trailLength) {
            const oldDot = trail.shift();
            oldDot.style.opacity = '0';
            setTimeout(() => oldDot.remove(), 500);
        }
    });
}

// Uncomment to enable mouse trail
// createMouseTrail();

// Initialize all features when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    tiltEffect();
    observeElements();

    // Add scroll reveal to sections
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(50px)';

        setTimeout(() => {
            section.style.transition = 'all 0.8s ease';
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, index * 100);
    });

    console.log('🐟 Welcome to fshpind.ai - Dive into AI workflows!');
});

// Performance optimization: Debounce scroll events
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

// Apply debouncing to scroll-heavy operations
const debouncedScroll = debounce(() => {
    // Any heavy scroll operations here
}, 10);

window.addEventListener('scroll', debouncedScroll);
