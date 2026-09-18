# Spacetime Boxing — website

A fast, single-page static site for Spacetime Boxing (Hollywood, CA).
No build step, no framework, no dependencies. Three files do the work:
`index.html`, `assets/css/style.css`, `assets/js/main.js`.

## Run it locally

```bash
npx http-server . -p 8080
# → http://localhost:8080
```

Any static server works, or just open `index.html`.

## Deploy

Drop the folder on any static host — Netlify, Vercel, Cloudflare Pages,
GitHub Pages, S3. There is nothing to compile.

- **Netlify / Cloudflare Pages:** publish directory = this folder, build command = none.
- **GitHub Pages:** push this folder to the `gh-pages` branch or set Pages to serve `/`.

## Before you launch — checklist

Everything below is a real value that needs confirming or a placeholder to swap.

1. **Photos.** The site currently shows styled placeholder tiles. Drop real images into
   `assets/img/` and replace each `<div class="photo" …>` with an `<img>`, or set a
   background on it:
   ```html
   <div class="photo" style="background-image:url('assets/img/ring.jpg')"></div>
   ```
   Wanted: one portrait of Pepe (`coach.jpg`, portrait crop) and 4–5 gym shots
   (ring, heavy bags, mitt work, wraps, the corner). Also add `assets/img/og.jpg`
   (1200×630) for link previews.

2. **Contact form endpoint.** `index.html` → `<form id="bookForm" action="…">` points at a
   Formspree placeholder. Create a form at [formspree.io](https://formspree.io) (free tier
   is fine) and paste your endpoint in. Until you do, the form politely tells visitors to
   call instead — it never silently drops a message.

3. **Prices.** Deliberately not published. The site says "clear rates and package options,
   no surprises — call for the current rate sheet," which matches how the gym already talks
   about pricing. If you want published rates, add a pricing section and I'll build it.

4. **Hours.** Listed as Mon–Sat, 7:00 AM – 2:00 PM (from the public listing). Correct it in
   two places if it's wrong: the `.contact` list, the footer, and the JSON-LD block at the
   bottom of `index.html`.

5. **Social links.** The JSON-LD `sameAs` array is empty. Add Instagram/YouTube URLs there,
   and add icon links to the footer if you want them visible.

6. **Domain.** The canonical URL, Open Graph URLs, `sitemap.xml` and `robots.txt` all assume
   `https://www.spacetimeboxing.com/`. Change them together if the domain changes.

## The 3D layer

The site has a real 3D layer, built entirely with CSS 3D transforms — no three.js, no
WebGL, no added weight:

- **Hero** is a room in perspective: floor and ceiling grids rotated on X and scrolling
  toward a vanishing line, with the headline, copy, buttons and stats each drifting at a
  different depth as the pointer moves (`data-depth` on the element, eased in `main.js`).
- **Headline** is extruded with eight stacked text-shadow layers rather than a flat shadow.
- **Cards and photo tiles** tilt toward the cursor (`data-tilt`), with their inner content
  raised on `translateZ` so it separates from the surface, plus a glare that tracks the
  pointer.
- **Reveals** rotate in on X and deal in from the side instead of fading up.

It is all transform/opacity, so it runs on the compositor — no layout, no repaint. It also
switches itself off completely for `prefers-reduced-motion` and for coarse pointers
(phones and tablets get the flat, fast version, since tilt needs a cursor).

Tuning: the tilt angle is `MAX` in `main.js`; depth amounts are the `data-depth` values in
`index.html`; the runway speed is the `runway` keyframe duration in `style.css`.

## What's built in

- **SEO:** semantic headings, meta description, canonical, Open Graph + Twitter cards,
  `SportsActivityLocation` JSON-LD with address, phone, hours and coach — so the gym can
  surface properly in Google's local results.
- **Accessibility:** skip link, visible focus rings, labelled form fields with inline errors,
  `aria-live` form status, keyboard-operable menu (Esc closes), and full
  `prefers-reduced-motion` support that disables every animation.
- **Performance:** zero dependencies and zero third-party requests — Anton and Inter are
  self-hosted in `assets/fonts/` (~160 KB total, subset to latin) and preloaded, so nothing
  is fetched from Google. All visuals are CSS/SVG: no hero video, no image payload until
  you add photos.
- **Progressive enhancement:** the page is complete and readable with JavaScript off.
  JS only adds reveals, counters, the mobile menu and async form submit.
- **Responsive:** verified at 1440px and 390px with zero horizontal overflow.

## Structure

```
index.html            # the whole page
404.html              # styled not-found page
robots.txt
sitemap.xml
assets/
  css/style.css       # design tokens at the top of the file
  js/main.js          # progressive enhancement only
  img/favicon.svg
  fonts/             # self-hosted Anton + Inter (woff2)
```

Colours, spacing and the container width are CSS custom properties in `:root` at the top of
`style.css` — change the palette there and the whole site follows.
