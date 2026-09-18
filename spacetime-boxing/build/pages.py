# Generates the four static pages from one shared shell so the header,
# footer and metadata cannot drift between them.
import os, html

SITE = "https://www.spacetimeboxing.com"
PHONE_HREF = "+13232062804"
PHONE = "(323) 206&#8209;2804"
ADDR = "1123 Vine St, Los Angeles, CA 90038"
MAPS = "https://maps.google.com/?q=1123+Vine+St,+Los+Angeles,+CA+90038"
HOURS = "Mon–Sat · 07:00 – 14:00"

NAV = [("index.html","Home"),("classes.html","Training"),("about.html","Coach"),("contact.html","Book")]

MARK = ('<svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true">'
        '<circle cx="16" cy="16" r="14" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<path d="M16 4v12l8 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')

def brand(size=26):
    m = MARK.replace('width="26" height="26"', f'width="{size}" height="{size}"')
    return (f'<a class="brand" href="index.html" aria-label="Spacetime Boxing home">'
            f'<span class="brand__mark">{m}</span>'
            f'<span class="brand__text">Spacetime<span>Boxing</span></span></a>')

def nav(current):
    CUR = ' aria-current="page"'
    links = "".join(
        '<a href="%s"%s>%s</a>' % (h, CUR if h == current else "", t)
        for h, t in NAV)
    mob = links
    return f"""<header class="nav" id="nav">
  <div class="wrap nav__inner">
    {brand()}
    <nav class="nav__links" aria-label="Main">{links}</nav>
    <a class="btn btn--sm nav__cta" href="contact.html">Book a session</a>
    <button class="nav__toggle" id="navToggle" aria-expanded="false" aria-controls="mobileMenu" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="nav__mobile" id="mobileMenu" hidden>{mob}<a class="btn" href="contact.html">Book a session</a></div>
</header>"""

def rail(items):
    if not items: return ""
    links = "".join(f'<a href="#{i}">{t}</a>' for i,t in items)
    return f'<nav class="rail" aria-label="Sections">{links}</nav>'

FOOTER = f"""<footer class="footer">
  <div class="wrap footer__inner">
    <div>
      {brand(22)}
      <p class="footer__blurb">Boxing classes and private training in Hollywood, California. Beginners to professionals.</p>
    </div>
    <nav aria-label="Footer">
      <h3>Site</h3>
      {"".join(f'<a href="{h}">{t}</a>' for h,t in NAV)}
    </nav>
    <div>
      <h3>Find us</h3>
      <p><a href="tel:{PHONE_HREF}">{PHONE}</a></p>
      <p><a href="{MAPS}" target="_blank" rel="noopener">1123 Vine St<br>Los Angeles, CA 90038</a></p>
      <p class="muted">{HOURS}</p>
    </div>
  </div>
  <div class="wrap footer__bottom">
    <p>© <span data-year>2026</span> Spacetime Boxing</p>
    <p><a href="#top">Back to top ↑</a></p>
  </div>
</footer>"""

LD_BASE = """{
  "@context": "https://schema.org",
  "@type": "SportsActivityLocation",
  "name": "Spacetime Boxing",
  "description": "Boxing classes and private boxing training with 1992 U.S. Olympian and National Golden Gloves champion Pepe Reilly, in Hollywood, California.",
  "url": "%s/",
  "telephone": "+1-323-206-2804",
  "address": {"@type":"PostalAddress","streetAddress":"1123 Vine St","addressLocality":"Los Angeles","addressRegion":"CA","postalCode":"90038","addressCountry":"US"},
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"07:00","closes":"14:00"}],
  "employee":{"@type":"Person","name":"Pepe Reilly","jobTitle":"Head Boxing Coach"},
  "sameAs": []
}""" % SITE

def page(fname, title, desc, body, rails=(), extra_ld=None):
    ld = f'<script type="application/ld+json">\n{LD_BASE}\n</script>'
    if extra_ld:
        ld += f'\n<script type="application/ld+json">\n{extra_ld}\n</script>'
    canon = f"{SITE}/" if fname == "index.html" else f"{SITE}/{fname}"
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Spacetime Boxing">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07080A">

<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/anton-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body id="top">
<a class="skip-link" href="#main">Skip to content</a>
<div class="grain" aria-hidden="true"></div>
{rail(rails)}
{nav(fname)}
<div class="page">
<main id="main">
{body}
</main>
{FOOTER}
</div>
{ld}
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    open(os.path.join(OUT, fname), "w").write(doc)
    print(f"  {fname:14} {len(doc):>6} bytes")

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ══════════════════════════════════════════════════════════════════ HOME
HOME = f"""  <section class="hero">
    <div class="hero__bg" aria-hidden="true">
      <div class="hero__glow hero__glow--a"></div>
      <div class="hero__glow hero__glow--b"></div>
      <div class="hero__space">
        <div class="hero__plane hero__plane--floor"></div>
        <div class="hero__plane hero__plane--ceil"></div>
      </div>
      <div class="hero__horizon"></div>
    </div>

    <div class="wrap hero__inner" data-stage>
      <div class="clock" id="roundClock" data-depth="12" role="img" aria-label="A boxing round timer, counting down three minutes of work and one minute of rest">
        <span class="clock__face" data-face>3:00</span>
        <span class="clock__meta"><b data-phase>Round</b>Wild Card · Hollywood</span>
      </div>

      <h1 class="hero__title" data-depth="44">
        <span class="line">Real boxing.</span>
        <span class="line accent" data-text="Taught right.">Taught right.</span>
      </h1>

      <p class="hero__lede" data-depth="26">
        Private training and small classes with <strong>Pepe Reilly</strong> — 1992 U.S. Olympian,
        National Golden Gloves champion, and the trainer behind world champions.
        Total beginners welcome.
      </p>

      <div class="hero__cta" data-depth="32">
        <a class="btn btn--lg" href="contact.html">Book your first session</a>
        <a class="btn btn--ghost btn--lg" href="classes.html">See training options</a>
      </div>

      <dl class="stats data" data-depth="14">
        <div class="stat"><dt>Olympic team</dt><dd><span data-plain>1992</span></dd></div>
        <div class="stat"><dt>Pro record</dt><dd><span data-count="15">0</span>–4 <em>11 KO</em></dd></div>
        <div class="stat"><dt>Years coaching</dt><dd><span data-count="25">0</span>+</dd></div>
        <div class="stat"><dt>Beginners</dt><dd>Welcome</dd></div>
      </dl>
    </div>
  </section>

  <div class="marquee" aria-hidden="true">
    <div class="marquee__track">
      <span>Footwork</span><i>◆</i><span>Defense</span><i>◆</i><span>Timing</span><i>◆</i><span>Conditioning</span><i>◆</i><span>Confidence</span><i>◆</i>
      <span>Footwork</span><i>◆</i><span>Defense</span><i>◆</i><span>Timing</span><i>◆</i><span>Conditioning</span><i>◆</i><span>Confidence</span><i>◆</i>
    </div>
  </div>

  <section class="section" id="why">
    <div class="wrap grid2">
      <div class="reveal">
        <p class="eyebrow">What this is</p>
        <h2 class="h2">Not a fitness class<br>that borrows the gloves</h2>
      </div>
      <div class="reveal">
        <p class="lede">Most "boxing workouts" hand you mitts and count reps. We teach you to box — stance, balance, distance, defense — then build the conditioning around it.</p>
        <p>The result is a full-body workout that happens to make you genuinely capable: endurance, coordination, reflexes, and the confidence that only comes from knowing what you're doing. Clear cues, instant corrections, no wasted rounds.</p>
        <p><a class="btn btn--ghost" href="classes.html">How the training works</a></p>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="training">
    <div class="wrap">
      <div class="sec-head reveal reveal--3d">
        <p class="eyebrow">Training</p>
        <h2 class="h2">Pick your round</h2>
        <p class="lede">Every option starts with fundamentals. Where you take them is up to you.</p>
      </div>
      <div class="cards">
        <article class="card reveal" data-tilt>
          <span class="card__tag">Private</span>
          <h3 class="h3">One on one</h3>
          <p>Undivided attention on the mitts. The fastest way to build clean technique, whether it's your first day or your fifteenth fight.</p>
        </article>
        <article class="card reveal" data-tilt>
          <span class="card__tag">Partner</span>
          <h3 class="h3">Two at a time</h3>
          <p>Bring a friend. Real coaching, real drills, enough eyes on you that nothing slips.</p>
        </article>
        <article class="card reveal" data-tilt>
          <span class="card__tag">Group</span>
          <h3 class="h3">Boxing class</h3>
          <p>Fundamentals for beginners, technical work for experienced athletes, conditioning that leaves nothing on the floor.</p>
        </article>
        <article class="card reveal" data-tilt>
          <span class="card__tag">Optional</span>
          <h3 class="h3">Sparring</h3>
          <p>Light and controlled for anyone who wants it, moderate when you're genuinely ready. Supervised every round, never required.</p>
        </article>
      </div>
      <div class="note reveal">
        <p><strong>Rates &amp; packages:</strong> clear pricing, package options, no surprises. Call <a href="tel:{PHONE_HREF}">{PHONE}</a> or <a href="contact.html">send a note</a> and we'll send the current rate sheet.</p>
      </div>
    </div>
  </section>

  <section class="section" id="coach">
    <div class="wrap grid-coach">
      <div class="coach__media reveal" style="position:relative">
        <div class="photo photo--portrait" data-tilt data-label="Coach portrait"></div>
        <div class="badge"><strong>1992</strong><span>Barcelona<br>Team USA</span></div>
      </div>
      <div class="reveal">
        <p class="eyebrow">The coach</p>
        <h2 class="h2">Pepe Reilly</h2>
        <p class="lede">Los Angeles native. 1992 National Golden Gloves champion and a member of the United States Olympic boxing team in Barcelona. Fifteen wins as a professional, eleven by knockout.</p>
        <p>Since hanging up the gloves he's spent more than two decades in the corner — out of Wild Card in Hollywood, cornering world champion Ray Beltran, coaching everyone from first-timers to title contenders.</p>
        <p><a class="btn btn--ghost" href="about.html">More about Pepe and the gym</a></p>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="gym">
    <div class="wrap">
      <div class="sec-head reveal reveal--3d">
        <p class="eyebrow">The room</p>
        <h2 class="h2">You'll be training at Wild Card</h2>
        <p class="lede">1123 Vine Street, Hollywood. Freddie Roach's gym — the most famous boxing gym in the world, and still a working one.</p>
      </div>
      <div class="gallery">
        <div class="photo reveal" data-tilt data-label="Ring"></div>
        <div class="photo reveal" data-tilt data-label="Heavy bags"></div>
        <div class="photo reveal" data-tilt data-label="Mitt work"></div>
        <div class="photo reveal" data-tilt data-label="Wraps"></div>
        <div class="photo reveal" data-tilt data-label="The corner"></div>
      </div>
    </div>
  </section>

  <section class="pull">
    <div class="wrap reveal">
      <blockquote>
        <p>“Fundamentals first. Everything else is just a punch you haven't earned yet.”</p>
        <footer>— Coach Pepe Reilly</footer>
      </blockquote>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap reveal">
      <h2>First round's the hardest.<br><span>Make the call.</span></h2>
      <div class="cta-band__btns">
        <a class="btn btn--lg" href="tel:{PHONE_HREF}">{PHONE}</a>
        <a class="btn btn--ghost btn--lg" href="contact.html">Send a message</a>
      </div>
    </div>
  </section>"""

page("index.html",
     "Spacetime Boxing — Boxing Classes &amp; Private Training in Hollywood",
     "Boxing classes and private training with Pepe Reilly — 1992 Olympian and National Golden Gloves champion — at Wild Card in Hollywood. Total beginners welcome.",
     HOME,
     rails=[("why","01"),("training","02"),("coach","03"),("gym","04")])

# ═══════════════════════════════════════════════════════════════ CLASSES
CLASSES = f"""  <section class="section" id="head" style="padding-top:clamp(120px,14vw,190px)">
    <div class="wrap">
      <p class="eyebrow reveal">Training</p>
      <h1 class="h1 reveal">Every session<br>is rounds</h1>
      <p class="lede reveal" style="margin-top:1.4rem">Three minutes of work, one minute of rest — the same clock a fight runs on. What changes is what you do inside them.</p>
    </div>
  </section>

  <section class="section" id="formats" style="padding-top:0">
    <div class="wrap">
      <div class="cards">
        <article class="card reveal" data-tilt>
          <span class="card__tag">Private</span>
          <h3 class="h3">One on one</h3>
          <p>Undivided attention on the mitts. The fastest way to build clean technique, whether it's your first day or your fifteenth fight.</p>
          <ul class="ticks">
            <li>Stance, footwork &amp; punch mechanics</li>
            <li>Mitt work with live corrections</li>
            <li>Conditioning built to your level</li>
          </ul>
          <p class="card__meta">Best for: fast progress<br>camera-ready prep, fight camps</p>
        </article>
        <article class="card reveal" data-tilt>
          <span class="card__tag">Partner</span>
          <h3 class="h3">Two at a time</h3>
          <p>Bring a friend or join a handful of people. Real coaching, real drills, enough eyes on you that nothing slips.</p>
          <ul class="ticks">
            <li>Technical drills at your pace</li>
            <li>Shared rounds, individual feedback</li>
            <li>Friendly, zero-ego room</li>
          </ul>
          <p class="card__meta">Best for: training with a partner<br>staying accountable</p>
        </article>
        <article class="card reveal" data-tilt>
          <span class="card__tag">Group</span>
          <h3 class="h3">Boxing class</h3>
          <p>Fundamentals for beginners, technical work for experienced athletes, and high-intensity conditioning that leaves nothing on the floor.</p>
          <ul class="ticks">
            <li>Warm-up, rounds, core &amp; cardio</li>
            <li>Bag work and pad rotations</li>
            <li>All levels in the same room</li>
          </ul>
          <p class="card__meta">Best for: fitness and structure<br>meeting people</p>
        </article>
        <article class="card reveal" data-tilt>
          <span class="card__tag">Optional</span>
          <h3 class="h3">Sparring</h3>
          <p>Light, controlled sparring for anyone who wants it — and moderate sparring when you're genuinely ready. Supervised every round.</p>
          <ul class="ticks">
            <li>Optional, never required</li>
            <li>Matched by level, not ego</li>
            <li>Coach in the ring with you</li>
          </ul>
          <p class="card__meta">Best for: applying what you've<br>learned, safely</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="session">
    <div class="wrap">
      <div class="sec-head reveal reveal--3d">
        <p class="eyebrow">Inside an hour</p>
        <h2 class="h2">What a session<br>actually looks like</h2>
        <p class="lede">A real sequence, not a menu — this is the order it happens in.</p>
      </div>
      <ol class="rounds">
        <li class="reveal">
          <span class="rounds__n">00:00 — 10:00</span>
          <div><h3 class="h3">Warm-up &amp; wraps</h3><p>Rope, shadow, mobility. Your hands get wrapped properly — and you get shown how, so eventually you do it yourself.</p></div>
        </li>
        <li class="reveal">
          <span class="rounds__n">10:00 — 25:00</span>
          <div><h3 class="h3">Technique</h3><p>Stance, guard, footwork, and whichever punch or defense you're building. Slow and correct before fast and sloppy.</p></div>
        </li>
        <li class="reveal">
          <span class="rounds__n">25:00 — 45:00</span>
          <div><h3 class="h3">Mitts &amp; bag</h3><p>Rounds on the pads with live corrections, then the heavy bag to put weight behind it. This is where the work gets loud.</p></div>
        </li>
        <li class="reveal">
          <span class="rounds__n">45:00 — 60:00</span>
          <div><h3 class="h3">Conditioning &amp; core</h3><p>Built to your level, not somebody else's. You'll finish tired — that part is the point.</p></div>
        </li>
      </ol>
      <div class="note reveal">
        <p>Timings are the shape of a typical hour, not a rulebook. A fight camp, a first lesson and a role-prep session all run differently.</p>
      </div>
    </div>
  </section>

  <section class="section" id="bring">
    <div class="wrap grid2">
      <div class="reveal">
        <p class="eyebrow">Practical</p>
        <h2 class="h2">What to bring</h2>
      </div>
      <div class="reveal">
        <ul class="ticks" style="font-size:1rem">
          <li>Athletic clothes you can sweat through</li>
          <li>Training shoes with a flat, grippy sole</li>
          <li>Water — more than you think</li>
          <li>Hand wraps and gloves can be sorted at the gym</li>
        </ul>
        <p style="margin-top:1.4rem">Don't buy expensive gloves before your first session. Come in, train, and we'll tell you what actually suits your hands and what you'll be doing.</p>
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap reveal">
      <h2>Book your<br><span>first round</span></h2>
      <div class="cta-band__btns">
        <a class="btn btn--lg" href="contact.html">Get in touch</a>
        <a class="btn btn--ghost btn--lg" href="tel:{PHONE_HREF}">{PHONE}</a>
      </div>
    </div>
  </section>"""

page("classes.html",
     "Boxing Classes &amp; Private Training — Spacetime Boxing, Hollywood",
     "Private one-on-one boxing, partner sessions, group classes and optional supervised sparring in Hollywood. See exactly how a session runs and what to bring.",
     CLASSES,
     rails=[("formats","01"),("session","02"),("bring","03")])

# ═════════════════════════════════════════════════════════════════ ABOUT
ABOUT = f"""  <section class="section" id="head" style="padding-top:clamp(120px,14vw,190px)">
    <div class="wrap">
      <p class="eyebrow reveal">The coach</p>
      <h1 class="h1 reveal">Pepe Reilly</h1>
      <p class="lede reveal" style="margin-top:1.4rem">Olympian, Golden Gloves champion, and more than twenty years in the corner at the most famous boxing gym in the world.</p>
    </div>
  </section>

  <section class="section" id="story" style="padding-top:0">
    <div class="wrap grid-coach">
      <div class="coach__media reveal" style="position:relative">
        <div class="photo photo--portrait" data-tilt data-label="Coach portrait"></div>
        <div class="badge"><strong>1992</strong><span>Barcelona<br>Team USA</span></div>
      </div>
      <div class="reveal">
        <p>Los Angeles native. In 1992 he won the National Golden Gloves and made the United States Olympic boxing team that went to Barcelona.</p>
        <p>He turned professional in the spring of 1993 and went 11–1 across his first year and a half, finishing with a record of fifteen wins and eleven knockouts over seven years in the sport.</p>
        <p>Since retiring from competition he has worked out of Wild Card in Hollywood, cornering world champion Ray Beltran and coaching everyone from people who have never thrown a punch to Hollywood talent preparing for a role to fighters heading into a title camp.</p>
        <p>The teaching is the same either way: clear fundamentals, honest feedback, and the patience to make them stick. Nobody gets thrown in the deep end, and nobody gets bored.</p>
        <ul class="creds">
          <li><span>1992</span> National Golden Gloves Champion</li>
          <li><span>1992</span> U.S. Olympic Team — Barcelona</li>
          <li><span>15–4</span> Professional record, 11 KOs</li>
          <li><span>25+</span> Years coaching at Wild Card</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="gym">
    <div class="wrap">
      <div class="sec-head reveal reveal--3d">
        <p class="eyebrow">The room</p>
        <h2 class="h2">Wild Card,<br>1123 Vine Street</h2>
        <p class="lede">Freddie Roach's gym in Hollywood — the most famous boxing gym in the world, and still very much a working one. Heavy bags, a real ring, and the sound of people who mean it.</p>
      </div>
      <div class="gallery">
        <div class="photo reveal" data-tilt data-label="Ring"></div>
        <div class="photo reveal" data-tilt data-label="Heavy bags"></div>
        <div class="photo reveal" data-tilt data-label="Mitt work"></div>
        <div class="photo reveal" data-tilt data-label="Wraps"></div>
        <div class="photo reveal" data-tilt data-label="The corner"></div>
      </div>
    </div>
  </section>

  <section class="pull">
    <div class="wrap reveal">
      <blockquote>
        <p>“Fundamentals first. Everything else is just a punch you haven't earned yet.”</p>
        <footer>— Coach Pepe Reilly</footer>
      </blockquote>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap reveal">
      <h2>Train with<br><span>the corner</span></h2>
      <div class="cta-band__btns">
        <a class="btn btn--lg" href="contact.html">Book a session</a>
        <a class="btn btn--ghost btn--lg" href="classes.html">See training options</a>
      </div>
    </div>
  </section>"""

page("about.html",
     "Pepe Reilly — Olympian, Golden Gloves Champion, Coach at Wild Card",
     "Pepe Reilly: 1992 U.S. Olympian and National Golden Gloves champion, 15-4 as a professional, and over two decades coaching at Wild Card Boxing Club in Hollywood.",
     ABOUT,
     rails=[("story","01"),("gym","02")])

# ═══════════════════════════════════════════════════════════════ CONTACT
FAQ_LD = """{
  "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":"I've never boxed. Is that a problem?","acceptedAnswer":{"@type":"Answer","text":"No — it is the most common way people start here. Day one is stance, guard and the jab. You will be taught, not tested."}},
  {"@type":"Question","name":"Do I have to spar?","acceptedAnswer":{"@type":"Answer","text":"Never. Sparring is optional and supervised. Light controlled work is available to anyone who wants it; moderate sparring only when you are genuinely ready."}},
  {"@type":"Question","name":"What do I need to bring?","acceptedAnswer":{"@type":"Answer","text":"Athletic clothes, training shoes and water. Hand wraps and gloves can be handled at the gym — ask before buying anything expensive."}},
  {"@type":"Question","name":"Am I too out of shape for this?","acceptedAnswer":{"@type":"Answer","text":"The conditioning is built to your level, not someone else's. Boxing is one of the best ways to get fit precisely because the skill work carries the workout."}},
  {"@type":"Question","name":"What does it cost?","acceptedAnswer":{"@type":"Answer","text":"Clear rates and package options, no surprises. Call or send the form and we will send the current rate sheet for privates, partner sessions and classes."}},
  {"@type":"Question","name":"Do you train fighters and film work?","acceptedAnswer":{"@type":"Answer","text":"Yes. Fight camps, amateur prep and role preparation for actors are all part of the regular week."}}]
}"""

CONTACT = f"""  <section class="section" id="head" style="padding-top:clamp(120px,14vw,190px)">
    <div class="wrap">
      <p class="eyebrow reveal">Book</p>
      <h1 class="h1 reveal">Let's get you<br>in the gym</h1>
      <p class="lede reveal" style="margin-top:1.4rem">Fastest way in is a phone call. Prefer to write? The form goes straight to us.</p>
    </div>
  </section>

  <section class="section" id="book" style="padding-top:0">
    <div class="wrap grid-book">
      <div class="reveal">
        <ul class="contact">
          <li><span class="contact__k">Phone</span><a class="contact__v data" href="tel:{PHONE_HREF}">{PHONE}</a></li>
          <li><span class="contact__k">Location</span><a class="contact__v" href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a></li>
          <li><span class="contact__k">Hours</span><span class="contact__v data">{HOURS}</span></li>
          <li><span class="contact__k">Gym</span><span class="contact__v">Wild Card Boxing Club</span></li>
        </ul>
        <a class="btn btn--lg" href="tel:{PHONE_HREF}">Call {PHONE}</a>
        <p style="margin-top:2rem;color:var(--steel);font-size:.92rem">Parking on Vine and the surrounding streets. Nearest Metro is Hollywood/Vine, a short walk north.</p>
      </div>

      <div class="reveal">
        <form class="form" id="bookForm" action="https://formspree.io/f/your-form-id" method="POST" novalidate>
          <div class="field">
            <label for="f-name">Name</label>
            <input id="f-name" name="name" type="text" autocomplete="name" required>
            <p class="err" data-for="f-name"></p>
          </div>
          <div class="field">
            <label for="f-contact">Phone or email</label>
            <input id="f-contact" name="contact" type="text" autocomplete="tel" required>
            <p class="err" data-for="f-contact"></p>
          </div>
          <div class="field">
            <label for="f-level">Experience</label>
            <select id="f-level" name="level">
              <option>Total beginner</option>
              <option>Some experience</option>
              <option>Trained before, getting back into it</option>
              <option>Competitive / pro</option>
            </select>
          </div>
          <div class="field">
            <label for="f-goal">What are you after?</label>
            <textarea id="f-goal" name="goal" rows="4" placeholder="Fitness, learning to box, fight prep, role prep…"></textarea>
          </div>
          <button class="btn btn--lg btn--full" type="submit">Send it</button>
          <p class="form__status" id="formStatus" role="status" aria-live="polite"></p>
        </form>
      </div>
    </div>
  </section>

  <section class="section section--alt" id="faq">
    <div class="wrap">
      <div class="sec-head reveal reveal--3d">
        <p class="eyebrow">Questions</p>
        <h2 class="h2">Before you<br>come in</h2>
      </div>
      <div class="faq">
        <details class="reveal"><summary>I've never boxed. Is that a problem?</summary><p>No — it's the most common way people start here. Day one is stance, guard, and the jab. You'll be taught, not tested.</p></details>
        <details class="reveal"><summary>Do I have to spar?</summary><p>Never. Sparring is optional and supervised. Light, controlled work is available to anyone who wants it; moderate sparring only when you're genuinely ready.</p></details>
        <details class="reveal"><summary>What do I need to bring?</summary><p>Athletic clothes, training shoes, and water. Hand wraps and gloves can be handled at the gym — ask before you buy anything expensive.</p></details>
        <details class="reveal"><summary>Am I too out of shape for this?</summary><p>The conditioning is built to your level, not someone else's. Boxing is one of the best ways to get fit precisely because the skill work carries the workout.</p></details>
        <details class="reveal"><summary>What does it cost?</summary><p>Clear rates and package options, no surprises. Call or send the form and we'll send you the current rate sheet for privates, partner sessions, and classes.</p></details>
        <details class="reveal"><summary>Do you train fighters and film work?</summary><p>Yes. Fight camps, amateur prep, and role preparation for actors are all part of the regular week. Tell us your timeline when you get in touch.</p></details>
      </div>
    </div>
  </section>"""

page("contact.html",
     "Book a Session — Spacetime Boxing, 1123 Vine St, Hollywood",
     "Book boxing training at Wild Card in Hollywood. Call (323) 206-2804 or send a message. Hours Mon-Sat 7am-2pm. Total beginners welcome.",
     CONTACT,
     rails=[("book","01"),("faq","02")],
     extra_ld=FAQ_LD)

# ═══════════════════════════════════════════════════════════════ SITEMAP
pages = ["", "classes.html", "about.html", "contact.html"]
urls = "\n".join(
    f"  <url>\n    <loc>{SITE}/{p}</loc>\n    <changefreq>monthly</changefreq>\n"
    f"    <priority>{'1.0' if p=='' else '0.8'}</priority>\n  </url>" for p in pages)
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n'
    f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
print("  sitemap.xml    4 urls")
