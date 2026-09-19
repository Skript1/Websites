# Photography

Every image on the site now comes from Pepe's own Instagram,
[@pepereillybox](https://www.instagram.com/pepereillybox/) — his posts, his
gym, his class. The stock placeholders are gone.

| File | What it is | Source post |
|---|---|---|
| `coach.jpg` | Pepe, arms crossed, Wild Card banner behind him | cropped from his 7AM class flyer, 10 May 2026 |
| `hero.jpg` | The 7am class lined up in the ring | 20 Mar 2026 |
| `bag.jpg` | Same class, full frame | 20 Mar 2026 |
| `ring.jpg` | Sparring on the Wild Card floor | 5 Aug 2026 |
| `canvas.jpg` | Pepe in the corner at a show | 7 Oct 2024 |
| `og.jpg` | Social share card, same corner shot | 7 Oct 2024 |

## Two things to settle before this goes anywhere public

**Permission.** These were taken from a public profile without asking. That's
fine for showing Pepe what his own site could look like — they're his
pictures and it's his site. It is not fine for a live site on a real domain
until he says yes. Ask him for the originals at the same time; what's here
was pulled at Instagram's preview resolution, 360–640px on the long edge,
upscaled. It survives the dark treatment but it is not print quality and
never will be.

**Other people's faces.** The class photos show his clients. He posted them
himself, so they're already public, but a website hero is a different thing
from a story post. Worth a sentence to him.

Posts credited to other photographers on his grid — egor dëmin, Michael
Citrone, Freddie Roach, Wild Card Boxing — were deliberately left alone.
Those are somebody else's copyright, and there was no need for them.

## If the real files arrive

Keep the filenames and the ratios and nothing else has to change:
`coach.jpg` 4:5 · `hero.jpg` 3:2, subject right of centre (the headline sits
on the left) · `og.jpg` 1200×630 · the rest 4:3.

The site grades photos toward the dark palette in `assets/css/style.css`
(`.photo img`, `.ribbon__item img`, `.hero__photo`). The hero currently
carries a 1.5px blur specifically to hide the upscaling — drop it once a
real photograph is in place.
