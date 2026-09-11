from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'frontend/css/base.css').read_text(encoding='utf-8') + '\n' + (ROOT / 'frontend/css/app.css').read_text(encoding='utf-8')


def rgb(hex_value: str):
    h = hex_value.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))


def linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_value: str) -> float:
    r, g, b = rgb(hex_value)
    return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# Moon Notes uses color as a structural highlighter behind dark text.
# Normal-sized text must remain at least 4.5:1, and utility controls stay neutral.
PAIRS = [
    ('paper text', '#111111', '#ffffff'),
    ('page text', '#111111', '#fbfbfa'),
    ('muted text on paper', '#575757', '#ffffff'),
    ('muted text on page', '#575757', '#fbfbfa'),
    ('primary button', '#ffffff', '#111111'),
    ('yellow highlighter text', '#111111', '#fff36d'),
    ('green highlighter text', '#111111', '#8cff8a'),
    ('turquoise highlighter text', '#111111', '#72e6e3'),
    ('pink highlighter text', '#111111', '#ff8fd3'),
    ('soft yellow note text', '#111111', '#fffbd1'),
    ('soft green note text', '#111111', '#eaffea'),
    ('soft turquoise note text', '#111111', '#e8fbfb'),
    ('soft pink note text', '#111111', '#fff0f8'),
    ('error text', '#4b1834', '#fff0f8'),
]

problems = []
results = []
for label, fg, bg in PAIRS:
    if fg not in CSS or bg not in CSS:
        problems.append(f'{label}: audited Moon Notes color pair is missing from CSS ({fg} on {bg})')
        continue
    value = ratio(fg, bg)
    results.append((label, fg, bg, value))
    if value < 4.5:
        problems.append(f'{label}: contrast {value:.2f}:1 is below 4.5:1')

# Structural design contracts. These stop future changes from quietly returning
# the site to the previous rounded-dashboard visual language.
for required in [
    'font-family:"Times New Roman", Times, serif',
    '--moon-yellow:#fff36d',
    '--moon-green:#8cff8a',
    '--moon-turquoise:#72e6e3',
    '--moon-pink:#ff8fd3',
    'border-radius:5px',
    'box-shadow:none',
]:
    if required not in CSS:
        problems.append(f'Moon Notes structural contract missing: {required}')

if problems:
    print('MOON NOTES CONTRAST QA FAIL')
    for item in problems:
        print(f'- {item}')
    raise SystemExit(1)

minimum = min(results, key=lambda x: x[3])
print('MOON NOTES CONTRAST QA PASS')
print(f'Minimum audited normal-text contrast: {minimum[3]:.2f}:1 ({minimum[0]})')
for label, fg, bg, value in results:
    print(f'- {label}: {value:.2f}:1 ({fg} on {bg})')
