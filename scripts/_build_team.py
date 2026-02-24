import os, sys

TEMPLATE = os.path.join(os.path.dirname(__file__), '..', 'templates', 'about.html')

with open(TEMPLATE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep header (0-129) and final endblock (591+)
before = lines[:130]
after  = lines[591:]   # {% endblock %}

# ── SVG helpers ──────────────────────────────────────────────
LI_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>'
GH_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>'

MEMBERS = [
    {
        'initials':'SV',
        'name':'Sarvesh Veshi',
        'role':'Backend Architect &amp; API Lead',
        'grad':'linear-gradient(135deg,#10b981,#059669)',
        'tint':'rgba(16,185,129,0.06)',
        'ac':'#10b981',
        'email':'sarvesh@handsignify.com',
        'desc':'Built the Flask server, RESTful APIs, and the database architecture that powers HandSignify from the ground up.',
        'bio':'Sarvesh is the technical backbone of HandSignify. He architected the entire backend infrastructure, designed clean RESTful APIs, and optimised database schemas for real-time data throughput.',
    },
    {
        'initials':'JG',
        'name':'Janhavi Godase',
        'role':'Systems Analyst &amp; Documentation',
        'grad':'linear-gradient(135deg,#6366f1,#4f46e5)',
        'tint':'rgba(99,102,241,0.06)',
        'ac':'#6366f1',
        'email':'janhavi@handsignify.com',
        'desc':'Conducted in-depth requirements analysis and user research to shape every feature of HandSignify.',
        'bio':'Janhavi bridges the gap between users and the tech team. Through thorough research and documentation, she ensures every feature is accessible, intuitive, and aligned with real-world communication needs.',
    },
    {
        'initials':'VK',
        'name':'Vedant Kondvilkar',
        'role':'UI/UX Designer &amp; Frontend Engineer',
        'grad':'linear-gradient(135deg,#f97316,#ea580c)',
        'tint':'rgba(249,115,22,0.06)',
        'ac':'#f97316',
        'email':'vedant@handsignify.com',
        'desc':'Designed and built every visual interface — pixel-perfect layouts and smooth micro-interactions that make AI feel human.',
        'bio':'Vedant crafts the face of HandSignify. From designing the visual identity to engineering performant frontend interactions, he ensures every pixel communicates intent and every animation serves a purpose.',
    },
    {
        'initials':'AG',
        'name':'Atharv Ghadigaonkar',
        'role':'UX Researcher &amp; Asset Manager',
        'grad':'linear-gradient(135deg,#06b6d4,#0891b2)',
        'tint':'rgba(6,182,212,0.06)',
        'ac':'#06b6d4',
        'email':'atharv@handsignify.com',
        'desc':'Performed user research and curated all media assets. Ensures design decisions are rooted in real data and empathy.',
        'bio':'Atharv grounds every design decision in real evidence. His user research insights, combined with careful curation of visual assets, ensure that HandSignify is not just functional but deeply human.',
    },
]

def card(m):
    return f'''
        <div class="tm-scene">
            <div class="tm-card">
                <!-- FRONT -->
                <div class="tm-face tm-front" style="--tint:{m['tint']};">
                    <div class="tm-av" style="background:{m['grad']};">{m['initials']}</div>
                    <h3 class="tm-name">{m['name']}</h3>
                    <p class="tm-role" style="color:{m['ac']};">{m['role']}</p>
                    <p class="tm-desc">{m['desc']}</p>
                </div>
                <!-- BACK -->
                <div class="tm-face tm-back" style="--tint:{m['tint']};--ac:{m['ac']};">
                    <div class="tm-av" style="background:{m['grad']};">{m['initials']}</div>
                    <h3 class="tm-name">{m['name']}</h3>
                    <p class="tm-bio">{m['bio']}</p>
                    <div class="tm-socials">
                        <a href="#" class="tm-social" aria-label="LinkedIn">{LI_SVG}</a>
                        <a href="#" class="tm-social" aria-label="GitHub">{GH_SVG}</a>
                    </div>
                    <a href="mailto:{m['email']}" class="tm-contact" style="background:var(--ac);">Contact</a>
                </div>
            </div>
        </div>'''

cards_html = ''.join(card(m) for m in MEMBERS)

new_section = f'''<!-- ── Team Section ── -->
<section id="team-section" class="tm-section" data-animate="section">

    <div class="tm-header">
        <p class="hs-eyebrow" style="display:inline-flex;">Team</p>
        <h2 class="tm-title">Meet the makers.</h2>
        <p class="tm-subtitle">A diverse team united by the mission to break communication barriers.<br>
            <small style="font-size:0.78rem;opacity:0.5;">Hover a card to learn more &#10022;</small>
        </p>
    </div>

    <div class="tm-grid">{cards_html}
    </div><!-- /.tm-grid -->
</section>

<!-- ── Team Card Styles ── -->
<style>
    .tm-section {{
        padding: 6rem 2rem 8rem;
        text-align: center;
        position: relative;
    }}
    .tm-header {{ margin-bottom: 3.5rem; }}
    .tm-title {{
        font-size: clamp(1.8rem, 4vw, 2.8rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-block: .5rem;
        background: linear-gradient(135deg, var(--hs-text-main, #e2e8f0) 0%, rgba(255,255,255,.5) 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .tm-subtitle {{
        color: var(--hs-text-soft, #94a3b8);
        font-size: 1rem;
        line-height: 1.75;
        max-width: 520px;
        margin-inline: auto;
    }}

    /* Grid */
    .tm-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        max-width: 1140px;
        margin-inline: auto;
    }}

    /* 3D Scene */
    .tm-scene {{
        perspective: 1100px;
        height: 380px;
    }}

    /* Flip card */
    .tm-card {{
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.45, 0.05, 0.55, 0.95),
                    box-shadow 0.4s ease;
        cursor: pointer;
        border-radius: 28px;
        box-shadow:
            0 4px 24px rgba(0,0,0,0.18),
            0 1px 6px rgba(0,0,0,0.1);
        will-change: transform;
    }}
    .tm-scene:hover .tm-card {{
        transform: rotateY(180deg) scale(1.03);
        box-shadow:
            0 16px 48px rgba(0,0,0,0.28),
            0 4px 16px rgba(0,0,0,0.16);
    }}

    /* Shared face */
    .tm-face {{
        position: absolute;
        inset: 0;
        border-radius: 28px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem 1.5rem;
        box-sizing: border-box;
        background: linear-gradient(
            160deg,
            rgba(255,255,255,0.09) 0%,
            rgba(255,255,255,0.05) 55%,
            var(--tint, rgba(255,255,255,0.03)) 100%
        );
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }}
    .tm-back {{
        transform: rotateY(180deg);
        justify-content: flex-start;
        padding-top: 1.8rem;
    }}

    /* Avatar */
    .tm-av {{
        width: 80px; height: 80px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: #fff; font-size: 1.6rem; font-weight: 800;
        flex-shrink: 0;
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
        margin-bottom: 0.9rem;
    }}

    .tm-name {{
        font-size: 1.05rem; font-weight: 700;
        color: var(--hs-text-main, #e2e8f0);
        margin-bottom: 0.2rem; text-align: center;
    }}
    .tm-role {{
        font-size: 0.65rem; font-weight: 700;
        letter-spacing: 0.07em; text-transform: uppercase;
        text-align: center; margin-bottom: 0.75rem;
    }}
    .tm-desc {{
        font-size: 0.8rem; line-height: 1.65;
        color: var(--hs-text-soft, #94a3b8);
        text-align: center;
    }}
    .tm-bio {{
        font-size: 0.77rem; line-height: 1.7;
        color: var(--hs-text-soft, #94a3b8);
        text-align: center;
        margin-top: 0.25rem; flex-grow: 1;
    }}

    .tm-socials {{
        display: flex; gap: 0.5rem;
        justify-content: center;
        margin-top: 0.7rem; margin-bottom: 0.6rem;
    }}
    .tm-social {{
        width: 32px; height: 32px; border-radius: 50%;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        display: flex; align-items: center; justify-content: center;
        color: var(--hs-text-soft, #94a3b8);
        text-decoration: none;
        transition: background 0.2s ease, color 0.2s ease;
    }}
    .tm-social:hover {{
        background: rgba(255,255,255,0.16);
        color: #fff;
    }}

    .tm-contact {{
        display: inline-flex; align-items: center; justify-content: center;
        padding: 0.4rem 1.4rem; border-radius: 999px;
        color: #fff; font-size: 0.72rem; font-weight: 600;
        letter-spacing: 0.05em; text-decoration: none;
        box-shadow: 0 2px 14px rgba(0,0,0,0.22);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .tm-contact:hover {{
        transform: scale(1.05);
        box-shadow: 0 4px 22px rgba(0,0,0,0.34);
    }}

    /* Responsive */
    @media (max-width: 1024px) {{
        .tm-grid {{ grid-template-columns: repeat(2, 1fr); }}
        .tm-scene {{ height: 360px; }}
    }}
    @media (max-width: 600px) {{
        .tm-grid {{ grid-template-columns: 1fr; }}
        .tm-scene {{ height: 340px; }}
        .tm-section {{ padding: 4rem 1.2rem 5rem; }}
    }}
</style>

'''

with open(TEMPLATE, 'w', encoding='utf-8') as f:
    f.writelines(before)
    f.write(new_section)
    f.writelines(after)

with open(TEMPLATE, 'r', encoding='utf-8') as f:
    total = len(f.readlines())
print(f'Done. Total lines: {total}')
