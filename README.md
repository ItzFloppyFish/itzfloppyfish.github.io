# itzfloppyfish.com

Static site, no build step required to deploy. GitHub Pages serves it as-is.

## Adding a new system

Everything about a product lives in one place: the `PRODUCTS` list in `_gen.py`.

1. Drop the Lua files into `scripts/<slug>/<Name>.lua`.
2. Add a block to `PRODUCTS` in `_gen.py` (copy an existing one).
3. Run `python3 _gen.py`. This writes `systems/<slug>/index.html` and the
   `systems/<slug>.html` redirect stub.
4. Add the same product to the `SYSTEMS` array in `systems/index.html` and the
   `FEATURED` array in `index.html`.

`_gen.py` is a local tool. It is never fetched by the browser.

## Where things live

| File | Purpose |
|---|---|
| `css/main.css` | Site-wide tokens, nav, footer, cards, buttons |
| `css/product.css` | Everything specific to a product detail page |
| `js/main.js` | Nav, particles, mobile menu, fade-ins |
| `js/product.js` | Carousel, buy panel, script vault, mobile sticky bar |
| `scripts/<slug>/*.lua` | The real script source, fetched and cached at page load |

Product pages contain **no styling and no logic** — only a `PRODUCT`, `MEDIA`
and `SCRIPTS` config object. Never paste CSS or JS into a product page; it
belongs in the two shared files or it will drift between products.

## Colour rules

Two accents only: neutral glass for free/secondary, the blue→cyan gradient for
premium/primary. Green appears in exactly one place (the "Copied" flash) and red
in one (contact form errors). Amber survives only on the testimonial stars,
where it reads as an icon rather than an accent. Adding a third accent hue is
what made the old pages look generated — don't.

## Script vault

Lua files are prefetched on page load and cached in memory so the copy handler
can run **synchronously**. Awaiting a fetch inside a click handler breaks
clipboard writes in iOS Safari. If you touch `js/product.js`, keep that
property. The clipboard write falls back to `execCommand` on rejection as well
as absence, because in-app webviews (Instagram, TikTok, the YouTube app) expose
the modern API and then refuse it.
