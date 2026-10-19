#!/usr/bin/env python3
"""Resume as SVGs in assets/resume/; run by hand after editing, line breaks are manual: python3 scripts/resume.py"""
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'assets' / 'resume'

GREENS = ['#9be9a8', '#9be9a8', '#40c463', '#40c463', '#30a14e', '#216e39']

EXPERIENCE = [  # (start, colour, dates, role lines, company, bullets as card lines; the wide row joins each list)
    (2024 + 2 / 12, '#6e7695', 'Mar 2024 – Present', ['Senior Full-Stack Developer &', 'Architect'], 'Beauty Luxury',
     [['Full-stack $4M e-commerce:', '6-layer event-driven cache', '(-93% DB load), PHPStan L8'],
      ['Conversion funnel, GA4/FB CAPI analytics,', 'live chat & AI agent context loader']]),
    (2022 + 10 / 12, '#bc776f', 'Nov 2022 – Jan 2024', ['Lead Web Development Instructor'], 'Rolling Code',
     [['Taught full-stack JS & algorithms to 80+', 'devs · high 12-month placement rate'],
      ['Technical lead mentoring junior devs', '& designing bilingual curricula']]),
    (2018.0, '#bca354', 'Jan 2018 – Oct 2022', ['Senior Software Engineer'], 'Mobillers',
     [['Scaled international B2B/B2C SaaS', 'platforms (React, Node, Python, PHP)'],
      ['AWS auto-scaling, Redis caching', '& CloudFormation IaC (-70% origin traffic)']]),
    (2016 + 2 / 12, '#6e93bc', 'Mar 2016 – Dec 2017', ['Legal Tech Developer & Mediator'], 'Mediaciones.ar',
     [['Architected automated mediation platform', '(processed 10,000+ dispute cases)'],
      ['Established cross-functional', 'conflict-resolution protocols', '& codebase reviews']]),
    (2009.0, '#bcb57b', 'Jan 2009 – Dec 2015', ['Co-Founder & CTO'], '365 Carilo',
     [['Built publishing platform for luxury media', '(polo, real estate, luxury auto)'],
      ["Reached 100% of Cariló's 7,000", 'residences & 20,000 affluent subscribers']]),
    (2005 + 8 / 12, '#6788a5', 'Sep 2005 – Dec 2008', ['Product Owner'], 'Consejo de la Magistratura C.A.B.A.',
     [['Paperless judiciary case-management', 'platform (~400,000 legal cases)'],
      ['Led cross-functional team on', 'mission-critical system with 10,000+ users']]),
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

CARD_W, RIGHT, TEXT_X = 400, 384, 26  # mobile: one 400-wide column, stretched to the page; content flush left
WIDE_W = 784                           # desktop: two 384 columns and a 16px gutter

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
  </style>'''


def e(text):
    return escape(text, quote=False)


def svg(width, height, label, body):
    return f'''<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(label)}">
{STYLE}
  <g class="rise">{body}
  </g>
</svg>
'''


def experience_heading():
    """Heading and tenure bar: desktop with year ticks, mobile without (the cards carry the dates)"""
    years = int(NOW - EXPERIENCE[-1][0])
    chrono = list(reversed(EXPERIENCE))
    first, span = chrono[0][0], NOW - chrono[0][0]
    heading = f'\n    <text class="sans muted" x="0" y="30" font-size="24"><tspan class="primary">{years}</tspan> Years of Experience</text>'

    def bar(width):
        px = width / span
        segs = ''
        for i, (start, color, *_) in enumerate(chrono):
            end = chrono[i + 1][0] if i + 1 < len(chrono) else NOW
            segs += f'\n      <rect x="{(start - first) * px:.1f}" y="46" width="{(end - start) * px:.1f}" height="24" fill="{color}"/>'
        return (f'\n    <clipPath id="bar"><rect x="0" y="46" width="{width}" height="24" rx="12"/></clipPath>'
                f'\n    <g clip-path="url(#bar)">{segs}\n    </g>')

    px = WIDE_W / span
    ticks = ''.join(f'\n    <text class="sans muted" x="{(start - first) * px:.1f}" y="92" font-size="13">{int(start)}</text>'
                    for start, *_ in chrono)
    ticks += f'\n    <text class="sans muted" x="{WIDE_W}" y="92" font-size="13" text-anchor="end">now</text>'
    label = f'{years} Years of Experience'
    return {'experience-wide.svg': svg(WIDE_W, 104, label, heading + bar(WIDE_W) + ticks),
            'experience.svg': svg(CARD_W, 86, label, heading + bar(RIGHT))}


def heading(name, text):
    body = f'\n    <text class="sans muted" x="0" y="30" font-size="24">{e(text)}</text>'
    return {f'{name}-wide.svg': svg(WIDE_W, 44, text, body), f'{name}.svg': svg(CARD_W, 44, text, body)}


def job_row(job):
    """Desktop: one full-width row, role · company with dates on the right, one line per bullet"""
    _, color, dates, role, company, bullets = job
    body = (f'\n    <circle cx="8" cy="16" r="8" fill="{color}"/>'
            f'\n    <text class="sans primary" x="{TEXT_X}" y="22" font-size="18"><tspan font-weight="600">{e(" ".join(role))}</tspan> · {e(company)}</text>'
            f'\n    <text class="sans muted" x="{WIDE_W}" y="22" font-size="15" text-anchor="end">{e(dates)}</text>')
    body += ''.join(f'\n    <text class="sans muted" x="{TEXT_X}" y="{48 + 22 * i}" font-size="16">{e(" ".join(lines))}</text>'
                    for i, lines in enumerate(bullets))
    return svg(WIDE_W, 48 + 22 * (len(bullets) - 1) + 30, f'{" ".join(role)} · {company} · {dates}', body)


def job_card(job):
    """Mobile: dates, role, company, then the bullets wrapped to the card"""
    _, color, dates, role, company, bullets = job
    body = f'\n    <text class="sans muted" x="{TEXT_X}" y="16" font-size="14">{e(dates)}</text>'
    y = 42
    body += f'\n    <circle cx="8" cy="{y - 6}" r="8" fill="{color}"/>'
    for line in role:
        body += f'\n    <text class="sans primary" x="{TEXT_X}" y="{y}" font-size="18" font-weight="600">{e(line)}</text>'
        y += 24
    body += f'\n    <text class="sans primary" x="{TEXT_X}" y="{y}" font-size="16">{e(company)}</text>'
    y += 6
    for lines in bullets:
        y += 8
        for line in lines:
            y += 22
            body += f'\n    <text class="sans muted" x="{TEXT_X}" y="{y}" font-size="16">{e(line)}</text>'
    return svg(CARD_W, y + 26, f'{" ".join(role)} · {company} · {dates}', body)


def skill_block(skill):
    """(body, height) of one skill group at the origin"""
    name, color, items = skill
    body = (f'\n    <circle cx="8" cy="12" r="8" fill="{color}"/>'
            f'\n    <text class="sans primary" x="{TEXT_X}" y="18" font-size="15" font-weight="600">{e(name)}</text>')
    body += ''.join(f'\n    <text class="sans muted" x="{TEXT_X}" y="{44 + 22 * i}" font-size="16">{e(line)}</text>'
                    for i, line in enumerate(items))
    return body, 44 + 22 * (len(items) - 1) + 24


def education_block():
    body = '\n    <text class="sans muted" x="0" y="30" font-size="24">Education &amp; Certifications</text>'
    for i, (year, title, school) in enumerate(EDUCATION):
        y = 70 + i * 46
        body += (f'\n    <text class="sans muted" x="0" y="{y}" font-size="15">{year}</text>'
                 f'\n    <text class="sans primary" x="48" y="{y}" font-size="17">{e(title)}</text>'
                 f'\n    <text class="sans muted" x="48" y="{y + 20}" font-size="15">{e(school)}</text>')
    return body, 70 + (len(EDUCATION) - 1) * 46 + 20 + 20


def languages_block():
    body = '\n    <text class="sans muted" x="0" y="30" font-size="24">Spoken Languages</text>'
    seg_gap, seg_h, step = 6, 12, 64
    seg_w = (RIGHT - 5 * seg_gap) / 6
    for i, (name, level, label) in enumerate(LANGUAGES):
        y = 70 + i * step
        body += (f'\n    <text class="sans primary" x="0" y="{y}" font-size="17">{name}</text>'
                 f'\n    <text class="sans muted" x="{RIGHT}" y="{y}" font-size="15" text-anchor="end">{e(label)}</text>')
        for k in range(6):
            paint = f'fill="{GREENS[k]}"' if k < level else 'class="empty"'
            body += f'\n    <rect {paint} x="{k * (seg_w + seg_gap):.1f}" y="{y + 12}" width="{seg_w:.1f}" height="{seg_h}" rx="3"/>'
    return body, 70 + (len(LANGUAGES) - 1) * step + 12 + seg_h + 20


def place(blocks, cols):
    """Lay (body, height) blocks out in `cols` columns of CARD_W + gutter; returns (body, height)"""
    out, y = '', 0
    for i in range(0, len(blocks), cols):
        row = blocks[i:i + cols]
        for j, (body, _) in enumerate(row):
            out += f'\n    <g transform="translate({j * (WIDE_W - CARD_W + 16)} {y})">{body}\n    </g>'
        y += max(h for _, h in row)
    return out, y


def section(name, blocks, label):
    """Desktop: two columns 784 wide; mobile: one column 400 wide, stretched like the job cards"""
    wide, wide_h = place(blocks, 2)
    stack, stack_h = place(blocks, 1)
    return {f'{name}-wide.svg': svg(WIDE_W, wide_h, label, wide), f'{name}.svg': svg(CARD_W, stack_h, label, stack)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob('*.svg'):
        stale.unlink()
    files = {**experience_heading(), **heading('skills-heading', 'Skills')}

    for i, job in enumerate(EXPERIENCE, 1):
        files[f'job-{i}-wide.svg'] = job_row(job)
        files[f'job-{i}.svg'] = job_card(job)

    files.update(section('skills', [skill_block(s) for s in SKILLS],
                         'Skills: ' + '; '.join(f'{n}: {" · ".join(items)}' for n, _, items in SKILLS)))
    files.update(section('education', [education_block(), languages_block()],
                         'Education & Certifications; Spoken Languages: ' + ', '.join(f'{n} {l}' for n, _, l in LANGUAGES)))

    for name, content in files.items():
        (OUT / name).write_text(content, encoding='utf-8')
    print(f'{len(files)} files in {OUT}')


if __name__ == '__main__':
    main()
