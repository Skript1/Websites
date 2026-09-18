# Spacetime Boxing — website

Static site for Spacetime Boxing (Hollywood, CA). No framework, no dependencies,
no third-party requests at runtime.

## The idea

Boxing measures itself in time: three minutes of work, one minute of rest. The gym
is literally named after time. So the site is built as a fight card on a clock —
a rail of round markers down the page edge, a round timer in the hero that actually
runs, a session broken into real timecodes, and monospace type wherever the page
reports a number, the way an instrument would.

That concept decides the details: numbering appears only where the content really is
a sequence (the session breakdown), never as decoration on a list of options.

**Palette** ink `#07080A` · bone `#F1EDE3` · blood `#C81E2D` · steel `#7C8794` ·
corner amber `#E8B44A` (spent once, on the clock's rest state).
**Type** Anton (fight-poster display) · Inter (body) · JetBrains Mono (data).

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home — hero, positioning, training overview, coach, gym |
| `classes.html` | Training formats, how a session runs, what to bring |
| `about.html` | Pepe Reilly, credentials, Wild Card |
| `contact.html` | Booking form, contact details, FAQ (with FAQ schema) |
| `404.html` | Not-found page |

Split into four pages because Google ranks pages, not sections — four pages means
four entry points for local searches like "boxing classes Hollywood".

## Editing

`build/pages.py` generates the four pages from one shared shell, so the header,
footer and metadata cannot drift apart. Change content there and run:

```bash
python3 build/pages.py
```

If you would rather hand-edit the HTML from now on, that is fine — just delete
`build/pages.py` so there is only one source of truth. Don't keep both and edit both.

The design tokens (color, type, spacing, container width) are CSS custom properties
in `:root` at the top of `assets/css/style.css`. Change them there and the whole
site follows.

## Run it locally

```bash
npx http-server . -p 8080
```

## Deploy

Any static host — Netlify, Cloudflare Pages, GitHub Pages, S3. Publish directory is
this folder, build command none.

## Before launch — checklist

1. **Photos.** The styled grey tiles are placeholders. Drop images into `assets/img/`
   and set them as backgrounds:
   ```html
   <div class="photo" style="background-image:url('assets/img/ring.jpg')"></div>
   ```
   Wanted: a portrait of Pepe, plus ring / heavy bags / mitt work / wraps / the corner.
   Also add `assets/img/og.jpg` (1200×630) for link previews.
2. **Form endpoint.** `contact.html` points at a Formspree placeholder. Create a form
   at formspree.io and paste the endpoint in. Until then the form tells people to call
   rather than silently dropping the message.
3. **Prices.** Not published — the site says to call for the current rate sheet, which
   matches how the gym already talks about pricing. Say the word and I'll add a rates
   section.
4. **Hours.** Listed as Mon–Sat 07:00–14:00, taken from the public listing, not from
   Pepe. Confirm, then correct them in `build/pages.py` (`HOURS`) and in the JSON-LD.
5. **Phone.** `(323) 206-2804`, same caveat — confirm it.
6. **Social links.** The JSON-LD `sameAs` array is empty. Add Instagram there and to
   the footer.
7. **Domain.** Everything canonical points at `https://www.spacetimeboxing.com`.
   The live site is currently on Wix, so moving means repointing DNS — and leaving the
   MX records alone if the gym has email on that domain.

## What's built in

- **SEO** — per-page titles, descriptions and canonicals; Open Graph and Twitter cards;
  `SportsActivityLocation` JSON-LD on every page with address, phone, hours and coach;
  `FAQPage` schema on the contact page; a four-URL sitemap.
- **Accessibility** — skip link, visible focus rings, labelled fields with inline errors,
  `aria-live` form status, `aria-current` on the active nav item, keyboard-operable menu,
  and a full `prefers-reduced-motion` path that flattens every animation including the
  round clock.
- **Performance** — zero dependencies and zero third-party requests. Anton, Inter and
  JetBrains Mono are self-hosted (~190 KB total, latin subsets) and preloaded.
- **Progressive enhancement** — every page is complete with JavaScript off. JS adds the
  clock, reveals, the rail indicator, tilt and async form submit.
- **3D layer** — CSS 3D transforms only: a hero in perspective with pointer parallax at
  per-element depths, an extruded headline, and cards that tilt toward the cursor with
  their content raised on `translateZ`. Transform-only, so it runs on the compositor.
  Disabled for coarse pointers and reduced motion.

Verified at 1440px and 390px: no horizontal overflow, no console errors, clock ticking.
