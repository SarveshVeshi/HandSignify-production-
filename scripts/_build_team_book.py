import os

TEMPLATE = os.path.join(os.path.dirname(__file__), '..', 'templates', 'about.html')

with open(TEMPLATE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the endblock line index.
endblock_idx = -1
for i, line in enumerate(lines):
    if '{% endblock %}' in line:
        endblock_idx = i
        break

if endblock_idx == -1:
    print('Error: Could not find endblock')
else:
    # Keep header (up to line 130) and final endblock
    before = lines[:130]
    after  = lines[endblock_idx:]

    LI_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>'
    GH_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>'

    MEMBERS = [
        {
            'initials':'SV',
            'name':'Sarvesh Veshi',
            'role':'Backend Architect & API Lead',
            'grad':'linear-gradient(135deg,#10b981,#059669)',
            'ac':'#10b981',
            'email':'sarvesh@handsignify.com',
            'desc':'Built the Flask server, RESTful APIs, and the database architecture that powers HandSignify from the ground up.',
            'bio':'Sarvesh is the technical backbone of HandSignify. He architected the entire backend infrastructure and designed real-time data pipelines.',
            'skills': ['Python', 'Flask', 'PostgreSQL', 'Redis', 'REST APIs']
        },
        {
            'initials':'JG',
            'name':'Janhavi Godase',
            'role':'Systems Analyst & Documentation',
            'grad':'linear-gradient(135deg,#6366f1,#4f46e5)',
            'ac':'#6366f1',
            'email':'janhavi@handsignify.com',
            'desc':'Conducted in-depth requirements analysis and user research to shape every feature of HandSignify.',
            'bio':'Janhavi bridges the gap between users and tech. She ensures every feature is intuitive and aligned with real-world accessibility needs.',
            'skills': ['UX Research', 'System Design', 'Agile', 'Jira', 'Docs']
        },
        {
            'initials':'VK',
            'name':'Vedant Kondvilkar',
            'role':'UI/UX Designer & Frontend Engineer',
            'grad':'linear-gradient(135deg,#f97316,#ea580c)',
            'ac':'#f97316',
            'email':'vedant@handsignify.com',
            'desc':'Designed and built every visual interface — pixel-perfect layouts and smooth micro-interactions that make AI feel human.',
            'bio':'Vedant crafts the face of HandSignify. He engineers performant frontend interactions where every pixel communicates intent.',
            'skills': ['Figma', 'React', 'GSAP', 'CSS3', 'Motion Design']
        },
        {
            'initials':'AG',
            'name':'Atharv Ghadigaonkar',
            'role':'UX Researcher & Asset Manager',
            'grad':'linear-gradient(135deg,#06b6d4,#0891b2)',
            'ac':'#06b6d4',
            'email':'atharv@handsignify.com',
            'desc':'Performed user research and curated all media assets. Ensures design decisions are rooted in real data and empathy.',
            'bio':'Atharv grounds designs in evidence. His insights ensure that HandSignify is not just functional but deeply human and empathetic.',
            'skills': ['User Testing', 'Asset Mgmt', 'Market Analysis', 'Insights']
        },
    ]

    def card(m):
        skills_html = ''.join(f'<span class="tm-skill-tag">{s}</span>' for s in m['skills'])
        return f'''
        <div class="tm-book-wrap">
            <div class="tm-book">
                <!-- BACK CONTENT (inside revealed) -->
                <div class="tm-book-content" style="--ac:{m['ac']};">
                    <div class="tm-book-inner">
                        <div class="tm-av-s" style="background:{m['grad']};">{m['initials']}</div>
                        <h3 class="tm-b-name">{m['name']}</h3>
                        <p class="tm-b-bio">{m['bio']}</p>
                        
                        <div class="tm-skills-box">
                            <p class="tm-skills-label">Key Expertise</p>
                            <div class="tm-skills-list">
                                {skills_html}
                            </div>
                        </div>

                        <div class="tm-b-socials">
                            <a href="#" class="tm-b-social" aria-label="LinkedIn">{LI_SVG}</a>
                            <a href="#" class="tm-b-social" aria-label="GitHub">{GH_SVG}</a>
                        </div>
                        <a href="mailto:{m['email']}" class="tm-b-contact" style="background:var(--ac);">Contact</a>
                    </div>
                </div>
                <!-- SIDE PAGES (depth) -->
                <div class="tm-book-pages"></div>
                <!-- COVER -->
                <div class="tm-book-cover" style="--ac:{m['ac']};">
                    <div class="tm-av" style="background:{m['grad']};">{m['initials']}</div>
                    <h3 class="tm-name">{m['name']}</h3>
                    <p class="tm-role" style="color:var(--ac);">{m['role']}</p>
                    <p class="tm-desc">{m['desc']}</p>
                </div>
            </div>
        </div>'''

    cards_html = ''.join(card(m) for m in MEMBERS)

    new_section = f'''<!-- ── Team Section (3D Book) ── -->
<section id="team-section" class="tm-section" data-animate="section">
    <div class="tm-header">
        <p class="hs-eyebrow" style="display:inline-flex;">Team</p>
        <h2 class="tm-title">Meet the makers.</h2>
        <p class="tm-subtitle">A diverse team united by the mission to break communication barriers.<br>
            <small style="font-size:0.78rem;opacity:0.5;">Open the book to read their story &#10022;</small>
        </p>
    </div>
    <div class="tm-grid">{cards_html}
    </div><!-- /.tm-grid -->
</section>

<!-- ── 3D Book Styles ── -->
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
        gap: 3rem;
        max-width: 1200px;
        margin-inline: auto;
    }}

    /* ── 3D Book Layout ── */
    .tm-book-wrap {{
        perspective: 1500px;
        height: 480px;
        width: 100%;
        display: flex;
        justify-content: center;
    }}

    .tm-book {{
        position: relative;
        width: 290px;
        height: 450px;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
        cursor: pointer;
    }}

    /* Book Hover State */
    .tm-book-wrap:hover .tm-book {{
        transform: rotateY(35deg) translateX(15%);
    }}

    .tm-book-wrap:hover .tm-book-cover {{
        transform: rotateY(-135deg);
    }}

    /* Cover Styling */
    .tm-book-cover {{
        position: absolute;
        inset: 0;
        z-index: 10; /* Highest */
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 4px 28px 28px 4px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transform-origin: left;
        transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2.5rem 1.5rem;
        box-shadow: 10px 10px 40px rgba(0,0,0,0.25);
        backface-visibility: hidden;
    }}

    /* Spine effect on the cover */
    .tm-book-cover::before {{
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 14px;
        background: rgba(255,255,255,0.15);
        border-right: 1px solid rgba(255,255,255,0.1);
        border-radius: 4px 0 0 4px;
    }}

    /* Pages depth effect */
    .tm-book-pages {{
        position: absolute;
        inset: 4px 0 4px 8px;
        z-index: 2;
        background: #f8fafc;
        border-radius: 2px 24px 24px 2px;
        box-shadow: 
            2px 0 0 #e2e8f0,
            4px 0 0 #cbd5e1,
            6px 0 0 #f8fafc,
            12px 10px 30px rgba(0,0,0,0.1);
    }}

    /* Inside Content */
    .tm-book-content {{
        position: absolute;
        inset: 0;
        z-index: 5; /* Above pages (2) but below cover (10) when closed */
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 4px 28px 28px 4px;
        padding: 2.2rem 1.5rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: inset 8px 0 15px rgba(0,0,0,0.03);
    }}

    .tm-book-inner {{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    /* Typography & Elements */
    .tm-av {{
        width: 95px; height: 95px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: #fff; font-size: 2rem; font-weight: 800;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
    }}
    .tm-av-s {{
        width: 55px; height: 55px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: #fff; font-size: 1.2rem; font-weight: 800;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
    }}

    .tm-name {{ font-size: 1.3rem; font-weight: 800; color: #0f172a; margin-bottom: 0.3rem; }}
    .tm-role {{ font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1.2rem; }}
    .tm-desc {{ font-size: 0.9rem; line-height: 1.6; color: #475569; font-weight: 500; }}

    .tm-b-name {{ font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-bottom: 0.6rem; }}
    .tm-b-bio {{ font-size: 0.85rem; line-height: 1.65; color: #64748b; margin-bottom: 1.5rem; font-weight: 500; }}

    /* Skills */
    .tm-skills-box {{ width: 100%; margin-bottom: 1.5rem; text-align: left; }}
    .tm-skills-label {{ font-size: 0.65rem; font-weight: 800; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.05em; margin-bottom: 0.5rem; padding-left: 2px; }}
    .tm-skills-list {{ display: flex; flex-wrap: wrap; gap: 0.4rem; }}
    .tm-skill-tag {{
        font-size: 0.7rem; font-weight: 600; padding: 0.25rem 0.6rem;
        background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 6px;
    }}

    /* Socials */
    .tm-b-socials {{ display: flex; gap: 0.6rem; margin-top: auto; margin-bottom: 1.2rem; }}
    .tm-b-social {{
        width: 36px; height: 36px; border-radius: 50%;
        background: #f8fafc; border: 1px solid #e2e8f0;
        display: flex; align-items: center; justify-content: center; color: #64748b;
        transition: all 0.3s ease;
    }}
    .tm-b-social:hover {{ background: #f1f5f9; color: #0f172a; transform: translateY(-2px); }}

    .tm-b-contact {{
        width: 100%; padding: 0.6rem; border-radius: 12px; color: #fff;
        font-size: 0.8rem; font-weight: 700; text-decoration: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    .tm-b-contact:hover {{ transform: scale(1.02); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }}

    /* Responsive */
    @media (max-width: 1260px) {{
        .tm-grid {{ grid-template-columns: repeat(2, 1fr); gap: 4rem 2rem; max-width: 700px; }}
        .tm-book-wrap {{ height: 500px; }}
    }}
    @media (max-width: 650px) {{
        .tm-grid {{ grid-template-columns: 1fr; gap: 3rem; }}
        .tm-book {{ width: 280px; height: 480px; }}
        .tm-book-wrap {{ height: 520px; }}
        .tm-section {{ padding: 4rem 1.5rem 6rem; }}
    }}
</style>
'''

    with open(TEMPLATE, 'w', encoding='utf-8') as f:
        f.writelines(before)
        f.write(new_section)
        f.writelines(after)

    print('Successfully built Rich 3D Book Team Section')
