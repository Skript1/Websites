"""Generates placeholder art for the photo slots.

These are deliberately graphic, not photographic: nobody should mistake them
for pictures of the actual gym. They carry the site's palette and its subject
(rounds, ropes, bags, the bell) so the layout reads as finished while the real
photography is still missing.
"""
import os, math

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
INK, INK2, BONE, BLOOD, STEEL, AMBER = "#07080A", "#14171C", "#F1EDE3", "#C81E2D", "#7C8794", "#E8B44A"

def halftone(seed, w, h, color, max_r=3.4, step=17, opacity=.5):
    """A dot field, drawn as a tiled pattern and faded with a gradient mask.

    Drawing every dot as its own <circle> cost ~100KB per tile; one pattern
    plus one mask does the same job in a few hundred bytes.
    """
    uid = f"ht{seed}"
    return f'''<defs>
<pattern id="{uid}p" width="{step}" height="{step}" patternUnits="userSpaceOnUse">
<circle cx="{step/2:.1f}" cy="{step/2:.1f}" r="{max_r:.2f}" fill="{color}"/>
</pattern>
<linearGradient id="{uid}g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/>
</linearGradient>
<mask id="{uid}m"><rect width="{w}" height="{h}" fill="url(#{uid}g)"/></mask>
</defs>
<rect width="{w}" height="{h}" fill="url(#{uid}p)" opacity="{opacity}" mask="url(#{uid}m)"/>'''

def frame(w, h, body, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">
<rect width="{w}" height="{h}" fill="{INK}"/>
{body}
</svg>'''

def ropes(w=1200, h=900):
    ys = [h*.30, h*.46, h*.62, h*.78]
    lines = "".join(
        f'<rect x="0" y="{y-7}" width="{w}" height="14" fill="{BONE}" opacity="{.16+i*.07:.2f}"/>'
        f'<rect x="0" y="{y-7}" width="{w}" height="3" fill="{BONE}" opacity="{.3+i*.1:.2f}"/>'
        for i, y in enumerate(ys))
    posts = "".join(f'<rect x="{x}" y="{h*.18}" width="26" height="{h*.72}" fill="{INK2}"/>'
                    f'<rect x="{x}" y="{h*.18}" width="6" height="{h*.72}" fill="{BLOOD}" opacity=".85"/>'
                    for x in (w*.11, w*.83))
    return frame(w, h, f'''
<rect width="{w}" height="{h}" fill="url(#g)"/>
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{INK2}"/><stop offset="1" stop-color="{INK}"/></linearGradient></defs>
{lines}{posts}
{halftone(1, w, h, BLOOD, 3.0, 19, .30)}''', "Ring ropes")

def bag(w=1200, h=900):
    cx, top, bw, bh = w*.5, h*.10, w*.30, h*.74
    chain = "".join(f'<circle cx="{cx}" cy="{top-16-i*20}" r="8" fill="none" stroke="{STEEL}" stroke-width="4"/>' for i in range(3))
    return frame(w, h, f'''
{chain}
<rect x="{cx-bw/2}" y="{top}" width="{bw}" height="{bh}" rx="{bw*.26}" fill="{BONE}" opacity=".92"/>
<rect x="{cx-bw/2}" y="{top+bh*.26}" width="{bw}" height="{bh*.10}" fill="{BLOOD}"/>
<rect x="{cx-bw/2}" y="{top+bh*.62}" width="{bw}" height="{bh*.10}" fill="{BLOOD}"/>
<rect x="{cx-bw/2}" y="{top}" width="{bw*.26}" height="{bh}" rx="{bw*.13}" fill="{INK}" opacity=".14"/>
{halftone(2, w, h, BLOOD, 3.4, 18, .34)}''', "Heavy bag")

def timer(w=1200, h=900):
    cx, cy, r = w*.5, h*.5, min(w, h)*.31
    ticks = ""
    for i in range(60):
        a = math.radians(i*6 - 90)
        long_ = i % 5 == 0
        r1 = r*(0.86 if long_ else 0.92)
        ticks += (f'<line x1="{cx+math.cos(a)*r1:.1f}" y1="{cy+math.sin(a)*r1:.1f}" '
                  f'x2="{cx+math.cos(a)*r:.1f}" y2="{cy+math.sin(a)*r:.1f}" '
                  f'stroke="{BONE}" stroke-width="{2.6 if long_ else 1.2}" opacity="{.7 if long_ else .32}"/>')
    sweep = 0.75  # three quarters of the round elapsed
    end = math.radians(sweep*360 - 90)
    large = 1 if sweep > .5 else 0
    arc = (f'<path d="M {cx} {cy-r*1.1} A {r*1.1} {r*1.1} 0 {large} 1 '
           f'{cx+math.cos(end)*r*1.1:.1f} {cy+math.sin(end)*r*1.1:.1f}" '
           f'fill="none" stroke="{BLOOD}" stroke-width="7" stroke-linecap="round"/>')
    return frame(w, h, f'''
<ellipse cx="{cx}" cy="{cy}" rx="{w*.40}" ry="{h*.40}" fill="{BLOOD}" opacity=".10"/>
{arc}{ticks}
<circle cx="{cx}" cy="{cy}" r="{r*.55}" fill="none" stroke="{STEEL}" stroke-width="1.4" opacity=".5"/>
<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-r*.62}" stroke="{AMBER}" stroke-width="5" stroke-linecap="round"/>
<circle cx="{cx}" cy="{cy}" r="7" fill="{AMBER}"/>
{halftone(3, w, h, BONE, 2.2, 23, .13)}''', "Round timer")

def wraps(w=1200, h=900):
    bands = ""
    for i in range(-14, 30):
        x = i*64
        c = BONE if i % 3 else BLOOD
        o = .13 if i % 3 else .55
        bands += f'<rect x="{x}" y="-200" width="30" height="{h+400}" fill="{c}" opacity="{o}" transform="rotate(28 {x} {h/2})"/>'
    return frame(w, h, f'<g>{bands}</g>{halftone(4, w, h, INK, 3.6, 16, .5)}', "Hand wraps")

def bell(w=1200, h=900):
    cx, cy = w*.5, h*.5
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{60 + i*62}" fill="none" stroke="{BLOOD}" '
        f'stroke-width="{9 - i:.0f}" opacity="{.95 - i*.12:.2f}"/>' for i in range(7))
    return frame(w, h, f'''
{rings}
<circle cx="{cx}" cy="{cy}" r="44" fill="{AMBER}"/>
{halftone(5, w, h, BONE, 3.0, 20, .16)}''', "Impact")

def canvas(w=1200, h=900):
    g = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{BONE}" stroke-width="1" opacity=".10"/>'
                for x in range(0, w+1, 68))
    g += "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{BONE}" stroke-width="1" opacity=".10"/>'
                 for y in range(0, h+1, 68))
    return frame(w, h, f'''
{g}
<path d="M -50 {h*.78} L {w*.62} -60 L {w*.86} -60 L {w*.14} {h+60} L -50 {h+60} Z" fill="{BLOOD}" opacity=".9"/>
<path d="M {w*.70} {h+60} L {w+60} {h*.30} L {w+60} {h*.56} L {w*.90} {h+60} Z" fill="{BONE}" opacity=".85"/>
{halftone(6, w, h, BONE, 3.2, 19, .18)}''', "Canvas")

def corner(w=1200, h=1500):
    cx = w*.5
    return frame(w, h, f'''
<circle cx="{cx}" cy="{h*.33}" r="{w*.40}" fill="{BLOOD}" opacity=".85"/>
<circle cx="{cx}" cy="{h*.30}" r="{w*.21}" fill="{BONE}" opacity=".95"/>
<path d="M {w*.14} {h+40} Q {w*.16} {h*.60} {cx} {h*.58} Q {w*.84} {h*.60} {w*.86} {h+40} Z"
      fill="{BONE}" opacity=".95"/>
<path d="M {cx} {h*.58} L {cx} {h+40}" stroke="{INK}" stroke-width="3" opacity=".25"/>
{halftone(7, w, h, INK, 3.6, 17, .42)}''', "The corner")

tiles = {
    "ring.svg": ropes(), "bag.svg": bag(), "timer.svg": timer(),
    "wraps.svg": wraps(), "bell.svg": bell(), "canvas.svg": canvas(),
    "coach.svg": corner(),
}
for name, svg in tiles.items():
    open(os.path.join(OUT, name), "w").write(svg)
    print(f"  {name:12} {len(svg):>6} bytes")
