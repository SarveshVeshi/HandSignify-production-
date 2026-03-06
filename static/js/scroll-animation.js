const canvas = document.getElementById("hero-canvas");
const context = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const frameCount = 204;
const currentFrame = index =>
    `/static/hologram-sequence/ezgif-frame-${String(index).padStart(3, "0")}.jpg`;

const images = [];
const hero = {
    frame: 1
};

// Preload images
for (let i = 1; i <= frameCount; i++) {
    const img = new Image();
    img.src = currentFrame(i);
    images.push(img);
}

// GSAP Register ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// Initialize Lenis Smooth Scroll
const lenis = new Lenis({
    duration: 1.5,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    orientation: 'vertical',
    gestureOrientation: 'vertical',
    smoothWheel: true,
    wheelMultiplier: 1,
    smoothTouch: false,
    touchMultiplier: 2,
    infinite: false,
})

function raf(time) {
    lenis.raf(time)
    requestAnimationFrame(raf)
}

requestAnimationFrame(raf)

// Sync ScrollTrigger with Lenis
lenis.on('scroll', ScrollTrigger.update)

gsap.ticker.add((time) => {
    lenis.raf(time * 1000)
})

gsap.ticker.lagSmoothing(0)

// Animation Logic
const render = () => {
    const img = images[hero.frame - 1];
    if (img && img.complete) {
        context.clearRect(0, 0, canvas.width, canvas.height);

        // Handle object-fit: cover in canvas
        const imgRatio = img.width / img.height;
        const canvasRatio = canvas.width / canvas.height;
        let drawWidth, drawHeight, offsetX, offsetY;

        if (imgRatio > canvasRatio) {
            drawHeight = canvas.height;
            drawWidth = canvas.height * imgRatio;
            offsetX = -(drawWidth - canvas.width) / 2;
            offsetY = 0;
        } else {
            drawWidth = canvas.width;
            drawHeight = canvas.width / imgRatio;
            offsetX = 0;
            offsetY = -(drawHeight - canvas.height) / 2;
        }

        context.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
    }
};

// Update on resize
window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    render();
});

// Button Visibility Logic (Tied to progress)
const showButton = () => {
    gsap.to("#start-btn", {
        opacity: 1,
        scale: 1,
        duration: 0.8,
        ease: "back.out(1.7)",
        overwrite: "auto"
    });
};

const hideButton = () => {
    gsap.to("#start-btn", {
        opacity: 0,
        scale: 0.8,
        duration: 0.5,
        overwrite: "auto"
    });
};

// Check progress on every render
const originalRender = render;
const enhancedRender = () => {
    originalRender();
    if (hero.frame >= 200) {
        showButton();
        gsap.to(".scroll-indicator", { opacity: 0, scale: 0, pointerEvents: "none", duration: 0.3, overwrite: "auto" });
    } else {
        hideButton();
    }
};

// Primary Scroll Animation
gsap.to(hero, {
    frame: frameCount,
    snap: "frame",
    ease: "none",
    scrollTrigger: {
        trigger: ".scroll-hero",
        start: "top top",
        end: "bottom+=400% top",
        scrub: 2,
        pin: true,
        onUpdate: enhancedRender
    }
});

// Hide scroll indicator on scroll
gsap.to(".scroll-indicator", {
    opacity: 0,
    y: -20,
    scrollTrigger: {
        trigger: ".scroll-hero",
        start: "top top",
        end: "top+=5% top",
        scrub: true
    }
});

// Initial Render on First Load
images[0].onload = render;

// Redirect logic
document.getElementById("start-btn").addEventListener("click", () => {
    window.location.href = "/login";
});
