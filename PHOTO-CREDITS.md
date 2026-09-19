# Photography — placeholder set

All images in `assets/img/*.jpg` are **temporary stock**, sourced from Pexels
(Pexels License: free for commercial use, no attribution required, no model
release implied). They are there so the site can be shown and reviewed as a
finished piece — **they are not Wild Card, and none of the people pictured are
Pepe Reilly.** Replace every one of them with real photography of the gym and
the coach before the site goes live.

| File | Used for | Source |
|---|---|---|
| `hero.jpg` | Home hero background | pexels.com/photo/8612501 |
| `og.jpg` | Social share card (1200×630) | pexels.com/photo/8612501 |
| `coach.jpg` | Coach portrait, home + about (4:5) | pexels.com/photo/30323314 |
| `ring.jpg` | "Ring" | pexels.com/photo/9944634 |
| `bag.jpg` | "Heavy bags" | pexels.com/photo/9944893 |
| `wraps.jpg` | "Wraps" | pexels.com/photo/29884889 |
| `timer.jpg` | "Rounds" | pexels.com/photo/5563414 |
| `bell.jpg` | "Speed bag" | pexels.com/photo/4753922 |
| `canvas.jpg` | "The floor" | pexels.com/photo/5549509 |

## Swapping in the real photos

Keep the filenames and the aspect ratios and nothing else has to change:

- `coach.jpg` — 1200×1500 (4:5), portrait
- `hero.jpg` — 1800×1200, the subject sitting right of centre (the headline
  covers the left half)
- `og.jpg` — 1200×630
- everything else — 1200×900 (4:3)

The site grades photos toward the dark palette in CSS
(`.photo img` and `.ribbon__item img` in `assets/css/style.css`); if the real
photos are already dark and moody, dial those filters back.
