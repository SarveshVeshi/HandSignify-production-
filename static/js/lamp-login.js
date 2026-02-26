/* ============================================================
   HandSignify — Cinematic Lamp Login: Interaction Engine
   State Machine + GSAP Animations + Physics
   ============================================================ */

(function () {
    'use strict';

    // ─── STATE MACHINE ──────────────────────────────────────────
    const STATES = {
        OFF_IDLE: 'OFF_IDLE',
        TURNING_ON: 'TURNING_ON',
        ON_IDLE: 'ON_IDLE',
        TURNING_OFF: 'TURNING_OFF',
    };

    let currentState = STATES.OFF_IDLE;
    let isTransitioning = false;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ─── DOM REFERENCES ─────────────────────────────────────────
    const lampCharacter = document.getElementById('lampCharacter');
    const loginCard = document.getElementById('lampLoginCard');
    const pullString = document.getElementById('pullString');
    const pullStringPath = document.getElementById('pullStringPath');
    const pullStringBead = document.getElementById('pullStringBead');
    const lampShade = document.getElementById('lampShade');
    const particlesContainer = document.getElementById('lampParticles');

    if (!lampCharacter || !loginCard || !pullString) return;

    // ─── PARTICLES ──────────────────────────────────────────────
    function createParticles() {
        if (prefersReducedMotion) return;
        const count = 20;
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.classList.add('lamp-particle');
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = (60 + Math.random() * 40) + '%';
            particle.style.animationDuration = (8 + Math.random() * 12) + 's';
            particle.style.animationDelay = (Math.random() * 10) + 's';
            particle.style.width = (1 + Math.random() * 2) + 'px';
            particle.style.height = particle.style.width;
            if (particlesContainer) particlesContainer.appendChild(particle);
        }
    }

    // ─── PULL STRING INTERACTION ────────────────────────────────
    function animatePull() {
        if (isTransitioning) return;

        // Hide hint permanently after first interaction
        const hint = document.getElementById('pullHint');
        if (hint) {
            hint.style.opacity = '0';
            hint.style.animation = 'none';
            setTimeout(() => hint.remove(), 500);
        }

        // Determine target state
        if (currentState === STATES.OFF_IDLE) {
            turnOn();
        } else if (currentState === STATES.ON_IDLE) {
            turnOff();
        }
    }

    // ─── TURN ON ────────────────────────────────────────────────
    function turnOn() {
        isTransitioning = true;
        currentState = STATES.TURNING_ON;

        const dur = prefersReducedMotion ? 0.15 : 1;

        // 1. Pull string stretch (200ms spring)
        if (!prefersReducedMotion && pullStringBead) {
            gsap.to(pullStringBead, {
                y: 12,
                duration: 0.15,
                ease: 'power2.out',
                yoyo: true,
                repeat: 1,
            });
        }

        // 2. Lamp state class change (triggers CSS transitions for eyes/mouth/shade)
        setTimeout(() => {
            lampCharacter.classList.remove('lamp-state-off');
            lampCharacter.classList.add('lamp-state-on');

            // Shade color via GSAP for smooth morph
            if (lampShade) {
                gsap.to(lampShade, {
                    attr: { fill: '#5C8B65' },
                    duration: 0.4 * dur,
                    ease: 'power2.out',
                });
            }
        }, prefersReducedMotion ? 0 : 200);

        // 3. Show login card (600ms, 150ms delay after lamp)
        setTimeout(() => {
            loginCard.classList.add('card-visible');
        }, prefersReducedMotion ? 50 : 350);

        // 4. Overshoot bounce on card
        if (!prefersReducedMotion) {
            setTimeout(() => {
                gsap.fromTo(loginCard,
                    { scale: 1 },
                    {
                        scale: 1.02,
                        duration: 0.15,
                        ease: 'power2.out',
                        yoyo: true,
                        repeat: 1,
                        onComplete: () => {
                            gsap.set(loginCard, { scale: 1 });
                        }
                    }
                );
            }, 650);
        }

        // Transition complete
        setTimeout(() => {
            currentState = STATES.ON_IDLE;
            isTransitioning = false;
        }, prefersReducedMotion ? 200 : 1000);
    }

    // ─── TURN OFF ───────────────────────────────────────────────
    function turnOff() {
        isTransitioning = true;
        currentState = STATES.TURNING_OFF;

        const dur = prefersReducedMotion ? 0.15 : 1;

        // 1. Pull string stretch
        if (!prefersReducedMotion && pullStringBead) {
            gsap.to(pullStringBead, {
                y: 12,
                duration: 0.15,
                ease: 'power2.out',
                yoyo: true,
                repeat: 1,
            });
        }

        // 2. Hide card (500ms slide out)
        loginCard.classList.remove('card-visible');

        // 3. Lamp expression fades
        setTimeout(() => {
            lampCharacter.classList.remove('lamp-state-on');
            lampCharacter.classList.add('lamp-state-off');

            // Shade color back to dark
            if (lampShade) {
                gsap.to(lampShade, {
                    attr: { fill: '#3A4A48' },
                    duration: 0.35 * dur,
                    ease: 'power2.inOut',
                });
            }
        }, prefersReducedMotion ? 0 : 250);

        // Transition complete
        setTimeout(() => {
            currentState = STATES.OFF_IDLE;
            isTransitioning = false;
        }, prefersReducedMotion ? 200 : 800);
    }

    // ─── EVENT BINDINGS ─────────────────────────────────────────

    // Click on pull string
    pullString.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        animatePull();
    });

    // Keyboard accessibility
    pullString.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            animatePull();
        }
    });

    // Touch support
    let touchStartY = 0;
    pullString.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    pullString.addEventListener('touchend', (e) => {
        const touchEndY = e.changedTouches[0].clientY;
        const diff = touchEndY - touchStartY;
        // If dragged down (pull), trigger
        if (diff > 5) {
            animatePull();
        }
    }, { passive: true });

    // ─── EYE BLINK (IDLE) ──────────────────────────────────────
    function startIdleBlink() {
        if (prefersReducedMotion) return;

        const sleepyEyes = document.querySelectorAll('.lamp-eye-sleepy');

        function doBlink() {
            sleepyEyes.forEach(eye => {
                gsap.to(eye, {
                    scaleY: 0.1,
                    duration: 0.1,
                    transformOrigin: 'center center',
                    yoyo: true,
                    repeat: 1,
                    ease: 'power2.inOut',
                });
            });
            // Random interval between blinks (2-6 seconds)
            setTimeout(doBlink, 2000 + Math.random() * 4000);
        }

        setTimeout(doBlink, 3000);
    }

    // ─── INITIALIZATION ─────────────────────────────────────────
    function init() {
        // Set initial state
        lampCharacter.classList.add('lamp-state-off');

        // Add body class for dark theme override
        document.body.classList.add('lamp-login-body');

        // Create particles
        createParticles();

        // Start idle blink
        startIdleBlink();
    }

    // Wait for DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
