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


# Normal-sized text and control combinations that appear repeatedly in the shell.
PAIRS = [
    ('primary button', '#ffffff', '#172033'),
    ('muted on card', '#526077', '#ffffff'),
    ('muted on page', '#526077', '#f4f7fb'),
    ('secondary muted on card', '#59697f', '#ffffff'),
    ('upcoming route label', '#59697f', '#f4f7fa'),
    ('visited route label', '#355f56', '#edf6f4'),
    ('story prose', '#27384a', '#ffffff'),
    ('story term', '#0e6174', '#ffffff'),
    ('orientation copy', '#46566a', '#eef5f8'),
    ('journey banner copy', '#dbe9f3', '#1c5364'),
    ('journey banner eyebrow', '#9bd8e8', '#173a54'),
    ('guide metadata', '#bad0df', '#173a54'),
    ('hint secondary text', '#5b4a28', '#fff4df'),
    ('error text', '#7c1d16', '#fff1f0'),
]

problems = []
results = []
for label, fg, bg in PAIRS:
    # Keep the audit coupled to the current stylesheet so a future palette change
    # cannot leave a stale numerical report passing silently.
    if fg not in CSS or bg not in CSS:
        problems.append(f'{label}: audited color pair is no longer present in CSS ({fg} on {bg})')
        continue
    value = ratio(fg, bg)
    results.append((label, fg, bg, value))
    if value < 4.5:
        problems.append(f'{label}: contrast {value:.2f}:1 is below 4.5:1')

if problems:
    print('SITE UX1 CONTRAST QA FAIL')
    for item in problems:
        print(f'- {item}')
    raise SystemExit(1)

minimum = min(results, key=lambda x: x[3])
print('SITE UX1 CONTRAST QA PASS')
print(f'Minimum audited normal-text contrast: {minimum[3]:.2f}:1 ({minimum[0]})')
for label, fg, bg, value in results:
    print(f'- {label}: {value:.2f}:1 ({fg} on {bg})')
