#!/usr/bin/env python3
"""Resume as 400-wide SVG cards in assets/resume/; run by hand after editing, line breaks are manual: python3 scripts/resume.py"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'assets' / 'resume'

GREENS = ['#9be9a8', '#9be9a8', '#40c463', '#40c463', '#30a14e', '#216e39']

EXPERIENCE = [  # (start, colour, dates, role lines, company, description lines with '' between bullets)
    (2024 + 2 / 12, '#6e7695', 'Mar 2024 – Present', ['Senior Full-Stack Developer &', 'Architect'], 'Beauty Luxury',
     ['Full-stack $4M e-commerce:', '6-layer event-driven cache', '(-93% DB load), PHPStan L8', '',
      'Conversion funnel, GA4/FB CAPI analytics,', 'live chat & AI agent context loader']),
    (2022 + 10 / 12, '#bc776f', 'Nov 2022 – Jan 2024', ['Lead Web Development', 'Instructor'], 'Rolling Code',
     ['Taught full-stack JS & algorithms to 80+', 'devs · high 12-month placement rate', '',
      'Technical lead mentoring junior devs', '& designing bilingual curricula']),
    (2018.0, '#bca354', 'Jan 2018 – Oct 2022', ['Senior Software Engineer'], 'Mobillers',
     ['Scaled international B2B/B2C SaaS', 'platforms (React, Node, Python, PHP)', '',
      'AWS auto-scaling, Redis caching', '& CloudFormation IaC (-70% origin traffic)']),
    (2016 + 2 / 12, '#6e93bc', 'Mar 2016 – Dec 2017', ['Legal Tech Developer & Mediator'], 'Mediaciones.ar',
     ['Architected automated mediation platform', '(processed 10,000+ dispute cases)', '',
      'Established cross-functional', 'conflict-resolution protocols', '& codebase reviews']),
    (2009.0, '#bcb57b', 'Jan 2009 – Dec 2015', ['Co-Founder & CTO'], '365 Carilo',
     ['Built publishing platform for luxury media', '(polo, real estate, luxury auto)', '',
      "Reached 100% of Cariló's 7,000", 'residences & 20,000 affluent subscribers']),
    (2005 + 8 / 12, '#6788a5', 'Sep 2005 – Dec 2008', ['Product Owner'], 'Consejo de la Magistratura C.A.B.A.',
     ['Paperless judiciary case-management', 'platform (~400,000 legal cases)', '',
      'Led cross-functional team on', 'mission-critical system', 'with 10,000+ users']),
]
NOW = 2026 + 10 / 12

SKILLS = [
    ('Engineering', '#6e7695', ['System Design · Software Architecture', 'Domain-Driven Design · Event-Driven', 'Scalability']),
    ('Frontend', '#6e93bc', ['HTML · CSS · Tailwind · JS · TS · React', 'Vue · Vite · Inertia · Web Components']),
    ('Backend', '#bc776f', ['PHP · Laravel · Node.js · Composer · Blade', 'REST API · WebSockets · Microservices']),
    ('Data', '#6788a5', ['MySQL · PostgreSQL · MongoDB · Redis', 'Eloquent ORM · Python · Pandas']),
    ('DevOps', '#bca354', ['Docker · AWS · CI/CD · Actions · Git', 'PHPStan · Pest · Playwright · Tests']),
    ('E-commerce', '#bc7766', ['WooCommerce · Stripe · PayPal · GTM', 'Events · Analytics · GDPR · Security', 'Caching']),
    ('Workflows', '#bcb57b', ['Agile · Scrum · Kanban · CLI & Scripting', 'Remote Work']),
]

EDUCATION = [
    ('2022', 'M.Sc. Data Science', 'U.B.A.'),
    ('2014', 'LL.M. Law & Economics', 'U.B.A.'),
    ('2009', 'Certified Mediator', 'CPACF'),
    ('2009', 'Dip. Ed.', 'U.B.A.'),
    ('2004', 'Attorney-at-Law (6-yr degree)', 'U.B.A.'),
    ('1999', 'Higher Tech. Systems Analysis', 'I.P.S.R.'),
    ('1997', 'Tech. Dip. Computing & Bookkeeping', 'I.P.S.R.'),
]

LANGUAGES = [  # (name, CEFR level 1-6, label)
    ('Spanish', 6, 'Native'),
    ('English', 6, 'C2 · Proficient'),
    ('Italian', 4, 'B2 · Upper Intermediate'),
]

CARD_W, LEFT, RIGHT, TEXT_X = 400, 16, 384, 42
STRIP_W = 784  # two cards side by side; narrower means mobile

STYLE = '''  <style>
    .sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", "DejaVu Sans", Helvetica, Arial, sans-serif; }
    .primary { fill: #1f2328; }
    .muted   { fill: #57544e; }
    .empty   { fill: #ebedf0; }
    @media (prefers-color-scheme: dark) {
      .primary { fill: #f0f6fc; }
      .muted   { fill: #b1aea7; }
      .empty   { fill: #2d333b; }
    }

    .rise { opacity: 0; animation: rise .7s cubic-bezier(.2,.7,.2,1) forwards; }
    @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
    @media (prefers-reduced-motion: reduce) { .rise { animation: none; opacity: 1; } }
%s  </style>'''

STRIP_CSS = f'''    .narrow {{ display: none; }}
    @media (max-width: {STRIP_W - 1}px) {{ .wide {{ display: none; }} .narrow {{ display: inline; }} }}
'''


def e(text):
    return escape(text, quote=False)


def svg(width, height, label, body, css=''):
    return f'''<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(label)}">
{STYLE % css}
  <g class="rise">{body}
  </g>
</svg>
'''


def experience_strip():
    """Heading and tenure bar; on mobile a larger heading and a thicker bar without ticks"""
    years = int(NOW - EXPERIENCE[-1][0])
    chrono = list(reversed(EXPERIENCE))
    first, span = chrono[0][0], NOW - chrono[0][0]

    def bar(y, h, clip):
        px = (STRIP_W - 2 * LEFT) / span
        segs = ''
        for i, (start, color, *_) in enumerate(chrono):
            end = chrono[i + 1][0] if i + 1 < len(chrono) else NOW
            segs += f'\n      <rect x="{LEFT + (start - first) * px:.1f}" y="{y}" width="{(end - start) * px:.1f}" height="{h}" fill="{color}"/>'
        return (f'\n    <clipPath id="{clip}"><rect x="{LEFT}" y="{y}" width="{STRIP_W - 2 * LEFT}" height="{h}" rx="{h // 2}"/></clipPath>'
                f'\n    <g clip-path="url(#{clip})">{segs}\n    </g>')

    px = (STRIP_W - 2 * LEFT) / span
    ticks = ''.join(f'\n    <text class="sans muted" x="{LEFT + (start - first) * px:.1f}" y="106" font-size="13">{int(start)}</text>'
                    for start, *_ in chrono)
    ticks += f'\n    <text class="sans muted" x="{STRIP_W - LEFT}" y="106" font-size="13" text-anchor="end">now</text>'
    heading = f'<tspan class="primary">{years}</tspan> Years of Experience'
    body = f'''
    <g class="wide">
    <text class="sans muted" x="{LEFT}" y="38" font-size="24">{heading}</text>{bar(60, 24, 'bar-wide')}{ticks}
    </g>
    <g class="narrow">
    <text class="sans muted" x="{LEFT}" y="50" font-size="44">{heading}</text>{bar(72, 32, 'bar-narrow')}
    </g>'''
    return svg(STRIP_W, 120, f'{years} Years of Experience', body, STRIP_CSS)


def heading_strip(text):
    body = f'''
    <text class="sans muted wide" x="{LEFT}" y="38" font-size="24">{e(text)}</text>
    <text class="sans muted narrow" x="{LEFT}" y="46" font-size="44">{e(text)}</text>'''
    return svg(STRIP_W, 56, text, body, STRIP_CSS)


def job_card(job, height):
    _, color, dates, role, company, desc = job
    y, body = 24, f'\n    <text class="sans muted" x="{TEXT_X}" y="24" font-size="14">{e(dates)}</text>'
    y += 26
    body += f'\n    <circle cx="{LEFT + 8}" cy="{y - 6}" r="8" fill="{color}"/>'
    for line in role:
        body += f'\n    <text class="sans primary" x="{TEXT_X}" y="{y}" font-size="18" font-weight="600">{e(line)}</text>'
        y += 24
    body += f'\n    <text class="sans primary" x="{TEXT_X}" y="{y}" font-size="16">{e(company)}</text>'
    y += 28
    for line in desc:
        if not line:
            y += 8
            continue
        body += f'\n    <text class="sans muted" x="{TEXT_X}" y="{y}" font-size="16">{e(line)}</text>'
        y += 22
    return svg(CARD_W, height, f'{" ".join(role)} · {company} · {dates}', body)


def job_bottom(job):
    _, _, _, role, _, desc = job
    return 50 + 24 * len(role) + 28 + 22 * sum(1 for d in desc if d) + 8 * desc.count('') - 22


def skill_card(skill, height):
    name, color, items = skill
    body = (f'\n    <circle cx="{LEFT + 8}" cy="18" r="8" fill="{color}"/>'
            f'\n    <text class="sans primary" x="{TEXT_X}" y="24" font-size="15" font-weight="600">{e(name)}</text>')
    body += ''.join(f'\n    <text class="sans muted" x="{TEXT_X}" y="{50 + 22 * i}" font-size="16">{e(line)}</text>'
                    for i, line in enumerate(items))
    return svg(CARD_W, height, f'{name}: {" · ".join(items)}', body)


def education_card(height):
    body = f'\n    <text class="sans muted" x="{LEFT}" y="38" font-size="24">Education &amp; Certifications</text>'
    for i, (year, title, school) in enumerate(EDUCATION):
        y = 80 + i * 46
        body += (f'\n    <text class="sans muted" x="{LEFT}" y="{y}" font-size="15">{year}</text>'
                 f'\n    <text class="sans primary" x="64" y="{y}" font-size="17">{e(title)}</text>'
                 f'\n    <text class="sans muted" x="64" y="{y + 20}" font-size="15">{e(school)}</text>')
    return svg(CARD_W, height, 'Education & Certifications', body)


def languages_card():
    body = f'\n    <text class="sans muted" x="{LEFT}" y="38" font-size="24">Spoken Languages</text>'
    seg_gap, seg_h, step = 6, 12, 64
    seg_w = (RIGHT - LEFT - 5 * seg_gap) / 6
    height = 80 + (len(LANGUAGES) - 1) * step + 12 + seg_h + 20
    for i, (name, level, label) in enumerate(LANGUAGES):
        y = 80 + i * step
        body += (f'\n    <text class="sans primary" x="{LEFT}" y="{y}" font-size="17">{name}</text>'
                 f'\n    <text class="sans muted" x="{RIGHT}" y="{y}" font-size="15" text-anchor="end">{e(label)}</text>')
        for k in range(6):
            paint = f'fill="{GREENS[k]}"' if k < level else 'class="empty"'
            body += f'\n    <rect {paint} x="{LEFT + k * (seg_w + seg_gap):.1f}" y="{y + 12}" width="{seg_w:.1f}" height="{seg_h}" rx="3"/>'
    return svg(CARD_W, round(height), 'Spoken Languages: ' + ', '.join(f'{n} {l}' for n, _, l in LANGUAGES), body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob('*.svg'):
        stale.unlink()
    files = {'experience.svg': experience_strip(), 'skills.svg': heading_strip('Skills')}

    job_h = max(job_bottom(job) for job in EXPERIENCE) + 20
    for i, job in enumerate(EXPERIENCE, 1):
        files[f'job-{i}.svg'] = job_card(job, job_h)

    skill_h = 50 + 22 * (max(len(s[2]) for s in SKILLS) - 1) + 20
    for i, skill in enumerate(SKILLS, 1):
        files[f'skill-{i}.svg'] = skill_card(skill, skill_h)
    # 1px tall, fills the empty half of an odd last row so its card sits left instead of centred
    files['spacer.svg'] = f'<svg viewBox="0 0 {CARD_W} 1" width="{CARD_W}" height="1" xmlns="http://www.w3.org/2000/svg"/>\n'

    files['education.svg'] = education_card(80 + (len(EDUCATION) - 1) * 46 + 20 + 20)
    files['languages.svg'] = languages_card()

    for name, content in files.items():
        (OUT / name).write_text(content, encoding='utf-8')
    print(f'{len(files)} files in {OUT}')


if __name__ == '__main__':
    main()
