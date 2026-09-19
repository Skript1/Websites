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

1. **Photography.** Every image is pulled from Pepe's public Instagram
   without asking, at preview resolution. Fine for showing him; not fine for
   a live site. Get his permission and his originals — see
   `PHOTO-CREDITS.md`.
2. **The booking form.** `contact.html` posts to
   `https://formspree.io/f/your-form-id`. Create a Formspree form (or any
   endpoint that accepts a POST) and put its real URL in the `action`
   attribute. Until that's done the form falls back to opening the visitor's
   mail client with the enquiry pre-filled, addressed to
   `hello@spacetimeboxing.com` — change that address in `assets/js/main.js`
   if it's wrong.
3. **Rates.** The site says rates depend on the format and to text and ask,
   rather than printing prices. If Pepe wants numbers on the page, they go in
   the four cards in `classes.html`.

## Facts on the page, worth a second check

Confirmed against his own sources: the phone (323) 206-2804, the address,
and the 7am Mon/Wed/Fri class all come from the flyer on his Instagram, and
the phone also matches his Yelp listing.

Still unverified, from the original draft: pro record 15–4 with 11 KO, 25+
years coaching, cornering Ray Beltran. Confirm with him before publishing.

Note that Spacetime Boxing, the business, has closed. He trains at Wild Card
as an individual. The site says nothing that implies otherwise — keep it
that way.

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
