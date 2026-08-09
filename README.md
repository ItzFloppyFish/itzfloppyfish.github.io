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

## Before launch — values still needed

Open `_gen.py` and fill the block marked **VALUES STILL NEEDED**:

| Constant | What it is |
|---|---|
| `BUTTER_FREE_KEY` | Payhip key for the free butter models |
| `BUTTER_PAID_KEY` | Payhip key for the butter drop-in build |
| `BUTTER_VIDEO_ID` | 11-char YouTube id. Leaving it blank hides the video slide and the tutorial button — it does not break the page. |
| `UIPACK_KEY` | Payhip key for the Essential STUD UI Pack |

Any key left as `TODO_...` renders its button greyed out and unclickable
instead of sending a buyer to a dead Payhip link. Re-run `python3 _gen.py`
after editing.

## Product options

| Field | Effect |
|---|---|
| `hidden: True` | Page still builds and works by direct URL, but is `noindex` and must also be removed from the `SYSTEMS`/`FEATURED` arrays by hand |
| `singleTier: True` | No free/paid tabs — one price, one buy button. Used for resold products. |
| `paidName` | Label for the paid tier. Defaults to `Drop-in`. |
| `banner` | Raw HTML inserted under the hero — used for the partner notice. |
| `groups` | Category feature grid instead of free/paid tier cards. |
| `extraBtns` | Extra buttons under the buy button (icon keys: `play`, `doc`). |

## Colour rules

Two accents only: neutral glass for free/secondary, the blue→cyan gradient for
premium/primary. Green appears in exactly one place (the "Copied" flash) and red
in one (contact form errors). Amber survives only on the testimonial stars,
where it reads as an icon rather than an accent. Adding a third accent hue is
what made the old pages look generated — don't.

## Selling someone else's product

A Payhip product key belongs to the store that created it. You cannot paste
another seller's key into your own store — the checkout, the payment and the
file delivery all sit on their account, so the sale never touches yours.
Two legitimate routes:

1. **Their affiliate programme.** They add you as an affiliate; you get a
   tracked link and they pay you the agreed cut. Note that Payhip requires an
   affiliate account to use a *different email* from your seller account, and
   sellers pay affiliates manually rather than Payhip doing it automatically.
2. **A licence.** They give you the files, you create the product in your own
   store, and you pay them a share. You keep the customer and the data.

## Script vault

Lua files are prefetched on page load and cached in memory so the copy handler
can run **synchronously**. Awaiting a fetch inside a click handler breaks
clipboard writes in iOS Safari. If you touch `js/product.js`, keep that
property. The clipboard write falls back to `execCommand` on rejection as well
as absence, because in-app webviews (Instagram, TikTok, the YouTube app) expose
the modern API and then refuse it.
