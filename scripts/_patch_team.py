"""Patch about.html: replace old team section (1-indexed lines 128-664) with 3D flip cards."""
TARGET = r'c:\Users\kondv\Downloads\Ronaldo_07\Ronaldo_07\templates\about.html'

NEW_SECTION = r"""<!-- ── Team Section — Premium 3D Flip Cards ──────────────────── -->
<section id="team-section" class="hs-flip-section" data-animate="section">

    <!-- Section header -->
    <div class="hs-flip-header">
        <p class="hs-eyebrow" style="display:inline-flex;">Team</p>
        <h2 class="hs-flip-title">Meet the makers.</h2>
        <p class="hs-flip-subtitle">A diverse team united by the mission to break communication barriers.<br>
            <small style="font-size:0.78rem;opacity:0.5;">Hover over a card to learn more &#10022;</small>
        </p>
    </div>

    <!-- Cards grid -->
    <div class="hs-flip-grid">

        <!-- Card 1: Sarvesh -->
        <div class="hs-flip-scene">
            <div class="hs-flip-card" id="fc0">
                <div class="hs-flip-face hs-flip-front" style="--glow:rgba(16,185,129,0.22);--border:rgba(16,185,129,0.25);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(16,185,129,0.30) 0%,transparent 70%);"></div>
                    <div class="hs-flip-avatar" style="background:linear-gradient(135deg,#10b981,#059669);box-shadow:0 0 32px rgba(16,185,129,0.5);">
                        <span>SV</span>
                        <div class="hs-flip-ring" style="border-color:rgba(16,185,129,0.45);"></div>
                    </div>
                    <h3 class="hs-flip-name">Sarvesh Veshi</h3>
                    <div class="hs-flip-tags">
                        <span class="hs-flip-tag" style="background:rgba(16,185,129,0.15);color:#10b981;">Backend Architect</span>
                        <span class="hs-flip-tag" style="background:rgba(59,111,239,0.15);color:#3b6fef;">API Design</span>
                    </div>
                    <p class="hs-flip-desc">Architected the server logic and built scalable APIs. Passionate about clean, efficient backend systems.</p>
                    <div class="hs-flip-hint">&#8645; Hover to flip</div>
                </div>
                <div class="hs-flip-face hs-flip-back" style="--glow:rgba(16,185,129,0.18);--border:rgba(16,185,129,0.3);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(16,185,129,0.22) 0%,transparent 65%);"></div>
                    <div class="hs-back-avatar-sm" style="background:linear-gradient(135deg,#10b981,#059669);">SV</div>
                    <h3 class="hs-back-name">Sarvesh Veshi</h3>
                    <p class="hs-back-role" style="color:#10b981;">Backend Architect &amp; API Lead</p>
                    <p class="hs-back-bio">Built the Flask server, RESTful APIs, WebSocket real-time pipeline, and database architecture that powers HandSignify. Loves clean code and system design patterns.</p>
                    <div class="hs-back-socials">
                        <a href="#" class="hs-social-btn" aria-label="LinkedIn" style="--sc:#0a66c2;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                        </a>
                        <a href="#" class="hs-social-btn" aria-label="GitHub" style="--sc:#e5e7eb;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                        </a>
                    </div>
                    <a href="mailto:sarvesh@handsignify.com" class="hs-back-contact" style="--cc:#10b981;">Contact</a>
                </div>
            </div>
        </div>

        <!-- Card 2: Janhavi -->
        <div class="hs-flip-scene">
            <div class="hs-flip-card" id="fc1">
                <div class="hs-flip-face hs-flip-front" style="--glow:rgba(236,72,153,0.20);--border:rgba(236,72,153,0.25);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(236,72,153,0.26) 0%,transparent 70%);"></div>
                    <div class="hs-flip-avatar" style="background:linear-gradient(135deg,#ec4899,#db2777);box-shadow:0 0 32px rgba(236,72,153,0.5);">
                        <span>JG</span>
                        <div class="hs-flip-ring" style="border-color:rgba(236,72,153,0.45);"></div>
                    </div>
                    <h3 class="hs-flip-name">Janhavi Godase</h3>
                    <div class="hs-flip-tags">
                        <span class="hs-flip-tag" style="background:rgba(236,72,153,0.15);color:#ec4899;">Analysis</span>
                        <span class="hs-flip-tag" style="background:rgba(168,85,247,0.15);color:#a855f7;">Documentation</span>
                    </div>
                    <p class="hs-flip-desc">Led requirements gathering and systems analysis. Ensures every feature aligns with real user needs and accessibility standards.</p>
                    <div class="hs-flip-hint">&#8645; Hover to flip</div>
                </div>
                <div class="hs-flip-face hs-flip-back" style="--glow:rgba(236,72,153,0.16);--border:rgba(236,72,153,0.3);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(236,72,153,0.20) 0%,transparent 65%);"></div>
                    <div class="hs-back-avatar-sm" style="background:linear-gradient(135deg,#ec4899,#db2777);">JG</div>
                    <h3 class="hs-back-name">Janhavi Godase</h3>
                    <p class="hs-back-role" style="color:#ec4899;">Systems Analyst &amp; Documentation</p>
                    <p class="hs-back-bio">Conducted thorough requirements analysis and user research. Created detailed documentation and ensured every feature is accessible, aligned with real-world needs of the community.</p>
                    <div class="hs-back-socials">
                        <a href="#" class="hs-social-btn" aria-label="LinkedIn" style="--sc:#0a66c2;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                        </a>
                        <a href="#" class="hs-social-btn" aria-label="GitHub" style="--sc:#e5e7eb;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                        </a>
                    </div>
                    <a href="mailto:janhavi@handsignify.com" class="hs-back-contact" style="--cc:#ec4899;">Contact</a>
                </div>
            </div>
        </div>

        <!-- Card 3: Vedant -->
        <div class="hs-flip-scene">
            <div class="hs-flip-card" id="fc2">
                <div class="hs-flip-face hs-flip-front" style="--glow:rgba(249,115,22,0.20);--border:rgba(249,115,22,0.25);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(249,115,22,0.26) 0%,transparent 70%);"></div>
                    <div class="hs-flip-avatar" style="background:linear-gradient(135deg,#f97316,#ea580c);box-shadow:0 0 32px rgba(249,115,22,0.5);">
                        <span>VK</span>
                        <div class="hs-flip-ring" style="border-color:rgba(249,115,22,0.45);"></div>
                    </div>
                    <h3 class="hs-flip-name">Vedant Kondvilkar</h3>
                    <div class="hs-flip-tags">
                        <span class="hs-flip-tag" style="background:rgba(249,115,22,0.15);color:#f97316;">UI/UX Design</span>
                        <span class="hs-flip-tag" style="background:rgba(59,111,239,0.15);color:#3b6fef;">Frontend</span>
                    </div>
                    <p class="hs-flip-desc">Crafted the intuitive user interface and seamless experience. Believes great design makes complex tech feel simple and accessible.</p>
                    <div class="hs-flip-hint">&#8645; Hover to flip</div>
                </div>
                <div class="hs-flip-face hs-flip-back" style="--glow:rgba(249,115,22,0.16);--border:rgba(249,115,22,0.3);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(249,115,22,0.20) 0%,transparent 65%);"></div>
                    <div class="hs-back-avatar-sm" style="background:linear-gradient(135deg,#f97316,#ea580c);">VK</div>
                    <h3 class="hs-back-name">Vedant Kondvilkar</h3>
                    <p class="hs-back-role" style="color:#f97316;">UI/UX Designer &amp; Frontend Engineer</p>
                    <p class="hs-back-bio">Designed and built every visual interface of HandSignify — from pixel-perfect layouts to smooth micro-interactions. Bridges engineering and design to make AI feel human and approachable.</p>
                    <div class="hs-back-socials">
                        <a href="#" class="hs-social-btn" aria-label="LinkedIn" style="--sc:#0a66c2;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                        </a>
                        <a href="#" class="hs-social-btn" aria-label="GitHub" style="--sc:#e5e7eb;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                        </a>
                    </div>
                    <a href="mailto:vedant@handsignify.com" class="hs-back-contact" style="--cc:#f97316;">Contact</a>
                </div>
            </div>
        </div>

        <!-- Card 4: Atharv -->
        <div class="hs-flip-scene">
            <div class="hs-flip-card" id="fc3">
                <div class="hs-flip-face hs-flip-front" style="--glow:rgba(6,182,212,0.20);--border:rgba(6,182,212,0.25);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(6,182,212,0.26) 0%,transparent 70%);"></div>
                    <div class="hs-flip-avatar" style="background:linear-gradient(135deg,#06b6d4,#0891b2);box-shadow:0 0 32px rgba(6,182,212,0.5);">
                        <span>AG</span>
                        <div class="hs-flip-ring" style="border-color:rgba(6,182,212,0.45);"></div>
                    </div>
                    <h3 class="hs-flip-name">Atharv Ghadigaonkar</h3>
                    <div class="hs-flip-tags">
                        <span class="hs-flip-tag" style="background:rgba(6,182,212,0.15);color:#06b6d4;">Research</span>
                        <span class="hs-flip-tag" style="background:rgba(168,85,247,0.15);color:#a855f7;">Asset Mgmt</span>
                    </div>
                    <p class="hs-flip-desc">Conducted user research and curated design assets. Bridges user insights and implementation with meticulous attention to detail.</p>
                    <div class="hs-flip-hint">&#8645; Hover to flip</div>
                </div>
                <div class="hs-flip-face hs-flip-back" style="--glow:rgba(6,182,212,0.16);--border:rgba(6,182,212,0.3);">
                    <div class="hs-flip-glow" style="background:radial-gradient(circle,rgba(6,182,212,0.20) 0%,transparent 65%);"></div>
                    <div class="hs-back-avatar-sm" style="background:linear-gradient(135deg,#06b6d4,#0891b2);">AG</div>
                    <h3 class="hs-back-name">Atharv Ghadigaonkar</h3>
                    <p class="hs-back-role" style="color:#06b6d4;">UX Researcher &amp; Asset Manager</p>
                    <p class="hs-back-bio">Performed in-depth user research, competitive analysis, and curated all media assets. Ensures HandSignify's design decisions are rooted in real data and genuine user empathy.</p>
                    <div class="hs-back-socials">
                        <a href="#" class="hs-social-btn" aria-label="LinkedIn" style="--sc:#0a66c2;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                        </a>
                        <a href="#" class="hs-social-btn" aria-label="GitHub" style="--sc:#e5e7eb;">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                        </a>
                    </div>
                    <a href="mailto:atharv@handsignify.com" class="hs-back-contact" style="--cc:#06b6d4;">Contact</a>
                </div>
            </div>
        </div>

    </div><!-- /.hs-flip-grid -->
</section>

<!-- 3D Flip Card Styles -->
<style>
.hs-flip-section { padding:6rem 2rem 8rem; text-align:center; position:relative; }
.hs-flip-header  { margin-bottom:3.5rem; }
.hs-flip-title {
    font-size:clamp(1.8rem,4vw,2.8rem); font-weight:800; letter-spacing:-0.03em; margin-block:.5rem;
    background:linear-gradient(135deg,var(--hs-text-main) 0%,rgba(255,255,255,.55) 100%);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.hs-flip-subtitle { color:var(--hs-text-soft); font-size:1rem; line-height:1.75; max-width:520px; margin-inline:auto; }
.hs-flip-grid {
    display:grid; grid-template-columns:repeat(4,1fr); gap:1.5rem;
    max-width:1200px; margin-inline:auto;
}
.hs-flip-scene { perspective:1000px; height:420px; }
.hs-flip-card {
    position:relative; width:100%; height:100%;
    transform-style:preserve-3d;
    transition: transform .65s cubic-bezier(.4,.2,.2,1), box-shadow .3s ease;
    will-change:transform; border-radius:24px; cursor:pointer;
}
.hs-flip-scene:hover .hs-flip-card,
.hs-flip-card.is-flipped {
    transform:rotateY(180deg) scale(1.03);
    box-shadow:0 28px 70px rgba(0,0,0,.42),0 0 0 1px rgba(255,255,255,.08);
}
.hs-flip-face {
    position:absolute; inset:0; border-radius:24px;
    backface-visibility:hidden; -webkit-backface-visibility:hidden;
    overflow:hidden; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    padding:2rem 1.4rem;
    background:rgba(255,255,255,.04);
    border:1px solid var(--border,rgba(255,255,255,.10));
    backdrop-filter:blur(22px); -webkit-backdrop-filter:blur(22px);
    box-shadow:0 8px 32px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.08);
    transition:box-shadow .35s ease;
}
.hs-flip-scene:hover .hs-flip-face {
    box-shadow:0 8px 32px rgba(0,0,0,.28),
               inset 0 0 50px var(--glow,rgba(255,255,255,.04)),
               inset 0 1px 0 rgba(255,255,255,.12);
}
.hs-flip-back { transform:rotateY(180deg); justify-content:flex-start; padding-top:2.2rem; }
.hs-flip-glow {
    position:absolute; top:-40px; left:50%; transform:translateX(-50%);
    width:220px; height:220px; border-radius:50%;
    pointer-events:none; filter:blur(35px);
    opacity:0; transition:opacity .4s ease;
}
.hs-flip-scene:hover .hs-flip-glow { opacity:1; }
.hs-flip-avatar {
    position:relative; width:88px; height:88px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    color:#fff; font-size:1.55rem; font-weight:800;
    margin-bottom:1.1rem; flex-shrink:0;
}
.hs-flip-ring {
    position:absolute; inset:-7px; border-radius:50%; border:2px solid;
    opacity:.55; animation:fring 6s linear infinite;
}
@keyframes fring { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
.hs-flip-name   { font-size:1.05rem; font-weight:700; color:var(--hs-text-main); margin-bottom:.55rem; }
.hs-flip-tags   { display:flex; gap:.35rem; flex-wrap:wrap; justify-content:center; margin-bottom:.75rem; }
.hs-flip-tag    { font-size:.65rem; padding:.25rem .55rem; border-radius:999px; font-weight:600; }
.hs-flip-desc   { color:var(--hs-text-soft); font-size:.82rem; line-height:1.65; margin:0; }
.hs-flip-hint   { margin-top:1rem; font-size:.7rem; color:rgba(255,255,255,.25); font-weight:500; transition:opacity .3s; }
.hs-flip-scene:hover .hs-flip-hint { opacity:0; }
.hs-back-avatar-sm {
    width:52px; height:52px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    color:#fff; font-size:1rem; font-weight:800; margin-bottom:.7rem; flex-shrink:0;
}
.hs-back-name  { font-size:1rem; font-weight:700; color:var(--hs-text-main); margin-bottom:.2rem; }
.hs-back-role  { font-size:.72rem; font-weight:600; letter-spacing:.03em; margin-bottom:.85rem; text-transform:uppercase; }
.hs-back-bio   { color:var(--hs-text-soft); font-size:.8rem; line-height:1.65; margin-bottom:1.1rem; text-align:center; }
.hs-back-socials { display:flex; gap:.6rem; justify-content:center; margin-bottom:1rem; }
.hs-social-btn {
    width:36px; height:36px; border-radius:50%;
    background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12);
    display:flex; align-items:center; justify-content:center;
    color:var(--sc,#fff); transition:background .2s,transform .2s; text-decoration:none;
}
.hs-social-btn:hover { background:rgba(255,255,255,.14); transform:scale(1.12); }
.hs-back-contact {
    display:inline-flex; align-items:center; justify-content:center;
    padding:.45rem 1.3rem; border-radius:999px;
    background:rgba(255,255,255,.06); border:1px solid var(--cc,rgba(255,255,255,.2));
    color:var(--cc,#fff); font-size:.78rem; font-weight:600; letter-spacing:.04em;
    text-decoration:none; transition:background .2s,transform .2s;
}
.hs-back-contact:hover { background:rgba(255,255,255,.12); transform:scale(1.04); }
@media (max-width:1100px) { .hs-flip-grid{grid-template-columns:repeat(2,1fr);} .hs-flip-scene{height:400px;} }
@media (max-width:640px)  { .hs-flip-grid{grid-template-columns:1fr;gap:1.2rem;} .hs-flip-section{padding:4rem 1.2rem 5rem;} .hs-flip-scene{height:380px;} }
</style>

<!-- Tap-to-flip for touch devices -->
<script>
(function(){
    function initFlip(){
        if(!window.matchMedia('(hover:none)').matches) return;
        document.querySelectorAll('.hs-flip-card').forEach(c=>{
            c.addEventListener('click',()=>c.classList.toggle('is-flipped'));
        });
    }
    document.readyState==='loading'
        ? document.addEventListener('DOMContentLoaded',initFlip)
        : initFlip();
})();
</script>
"""

with open(TARGET, encoding='utf-8') as fh:
    lines = fh.readlines()

# Lines 128-664 (1-indexed) => indices 127-663 (0-indexed), replace inclusive
before = lines[:127]
after  = lines[664:]
result = before + [NEW_SECTION + '\n'] + after

with open(TARGET, 'w', encoding='utf-8') as fh:
    fh.writelines(result)

print(f"Done. File now has {len(result)} lines.")
