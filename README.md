# Spacetime Boxing — website

Static site (no build step). Four pages, one stylesheet, one script,
self-hosted fonts. Open `index.html` through any web server and it runs.

```
index.html      Home
about.html      The coach / the gym
classes.html    Training options, how an hour runs, what to bring
contact.html    Booking form + details
assets/css/style.css
assets/js/main.js
assets/img/      photos (placeholder stock — see PHOTO-CREDITS.md)
assets/fonts/    Anton, Inter, JetBrains Mono (latin subsets)
```

## Preview locally

```bash
python -m http.server 7811 --directory .
```

Then open http://localhost:7811. (Opening `index.html` as a `file://` URL
mostly works but the fonts won't load.)

## Before it goes live — three things

1. **Photography.** Every image is placeholder stock. See `PHOTO-CREDITS.md`
   for the list, the sizes, and how to swap them.
2. **The booking form.** `contact.html` posts to
   `https://formspree.io/f/your-form-id`. Create a Formspree form (or any
   endpoint that accepts a POST) and put its real URL in the `action`
   attribute. Until that's done the form falls back to opening the visitor's
   mail client with the enquiry pre-filled, addressed to
   `hello@spacetimeboxing.com` — change that address in `assets/js/main.js`
   if it's wrong.
3. **Rates.** The site deliberately says "call for the current rate sheet"
   rather than printing prices. If Pepe wants numbers on the page, they go in
   the four cards in `classes.html`.

## Facts on the page, worth a second check

Pulled from the original draft, not independently verified:
1992 U.S. Olympic team / National Golden Gloves champion; pro record 15–4,
11 KO; 25+ years coaching; cornering Ray Beltran; Wild Card, 1123 Vine Street;
phone (323) 206-2804; hours Mon–Sat 07:00–14:00. Confirm each with Pepe
before publishing — the record and the hours especially.

## `build/` is stale — don't run it

`build/pages.py` and `build/tiles.py` generated the first draft (the SVG
placeholder tiles, and the HTML around them). The pages have moved on since:
the generator still emits empty `.photo` divs with no images at all, so
re-running it would throw away the photography and the fixes. The HTML files
are the source of truth now; `build/` is kept only for the tile generator,
which is still the thing to look at if the graphic tiles are ever wanted back.

## Deploying

Drag the folder onto Netlify, or push it to a repo and point Netlify/Pages at
it. There's nothing to build. The canonical URL in every page's `<head>` is
`https://www.spacetimeboxing.com/` — change it if the domain changes.
