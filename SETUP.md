# Itz_FloppyFish Site — Setup Guide

## File Structure

```
floppyfish-site/
├── index.html              ← Home page
├── systems.html            ← Systems listing / marketplace
├── about.html              ← About page
├── css/
│   └── main.css            ← Shared styles (don't edit unless you know what you're doing)
├── js/
│   └── main.js             ← Shared logic (particles, nav, fade-in)
└── systems/
    └── item-shop.html      ← Product page (duplicate this for every new system)
```

---

## Step 1 — Create a GitHub account and repository

1. Go to [github.com](https://github.com) and sign up (free)
2. Click **New repository**
3. Name it exactly: `itzfloppyfish.github.io`
   - If your GitHub username is different, name it `YOURUSERNAME.github.io`
4. Set it to **Public**
5. Click **Create repository**

---

## Step 2 — Upload the files

**Option A — GitHub web interface (easiest):**
1. Open your new repository
2. Click **uploading an existing file**
3. Drag and drop the entire `floppyfish-site` folder contents
4. **Important:** keep the folder structure intact — `css/`, `js/`, `systems/` must be folders, not flat files
5. Click **Commit changes**

**Option B — Git command line:**
```bash
cd floppyfish-site
git init
git add .
git commit -m "Initial site launch"
git remote add origin https://github.com/YOURUSERNAME/YOURUSERNAME.github.io.git
git push -u origin main
```

---

## Step 3 — Enable GitHub Pages

1. In your repository, go to **Settings** → **Pages** (left sidebar)
2. Under **Source**, select **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)`
4. Click **Save**
5. Wait ~2 minutes, then your site is live at:
   `https://YOURUSERNAME.github.io`

---

## Step 4 — Connect your custom domain

1. In GitHub Pages settings, enter your domain in the **Custom domain** field (e.g. `itzfloppyfish.com`)
2. Click **Save**
3. Go to your domain registrar (GoDaddy, Namecheap, etc.)
4. Add these DNS records:

| Type  | Name | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | YOURUSERNAME.github.io |

5. DNS changes take up to 24 hours to propagate
6. Once live, tick **Enforce HTTPS** in GitHub Pages settings

---

## Step 5 — Add your Payhip product keys

For each system, open `systems/item-shop.html` (or the relevant system file) and find:

```javascript
const PRODUCT = {
  freeKey:  "REPLACE_WITH_FREE_PRODUCT_KEY",
  premKey:  "REPLACE_WITH_PREM_PRODUCT_KEY",
  ...
```

**To find your Payhip product key:**
1. Go to [payhip.com/products](https://payhip.com/products)
2. Click **Share / Embed** on your product
3. The key is the short code at the end of the product URL — e.g. `payhip.com/b/W29xU` → key is `W29xU`

The buy buttons already use direct checkout links:
`https://payhip.com/buy?link=YOURKEY`

No embed script needed. Users click → land on Payhip checkout → buy and download. Done.

---

## Step 6 — Add a new system (every time you release a new tutorial)

1. **Duplicate** `systems/item-shop.html`
2. Rename it to match the system, e.g. `systems/rebirth-system.html`
3. Edit the top of the file:
   - Update `<title>` and `<meta name="description">`
   - Update the breadcrumb text
   - Update the hero icon and title
   - Update the `PRODUCT` config object with your Payhip keys, price, and feature lists
   - Update the comparison table rows
4. **Add it to `systems.html`** — find the `SYSTEMS` array and add a new entry:

```javascript
{
  name: "Rebirth System",
  cat: "Progression",
  desc: "Complete rebirth/prestige system with multiplier scaling.",
  href: "systems/rebirth-system.html",
  hasFree: true,
  hasPrem: true,
  pr: "$4.99",
  icon: "♻️"
}
```

5. **Add it to `index.html`** if you want it in the featured section (optional — keep featured to 3 max)
6. **Add it to the footer** of `index.html` under the Systems column
7. Commit and push — GitHub Pages auto-deploys within 1-2 minutes

---

## Step 7 — Add a hero screenshot (recommended)

Replace the placeholder icon in `ffdtl-hero` with a real screenshot:

```html
<!-- Find this in systems/item-shop.html: -->
<div class="ffdtl-hero">
  <div class="ffdtl-hero-icon">🏪</div>
</div>

<!-- Replace with: -->
<div class="ffdtl-hero">
  <img src="../images/item-shop-hero.png" alt="Item Shop System preview" style="width:100%;height:100%;object-fit:cover;">
</div>
```

Create an `images/` folder at the root and put screenshots there.

---

## Step 8 — Add your tutorial video

When your YouTube tutorial is published, find the video ID (the part after `watch?v=` in the URL) and update the video section in the system file:

```html
<!-- Find this block and replace it: -->
<div class="ff-vph">...</div>

<!-- With: -->
<iframe src="https://www.youtube.com/embed/YOUR_VIDEO_ID" allowfullscreen></iframe>
```

---

## Making changes going forward

Every change is:
1. Edit the file locally
2. Commit and push to GitHub
3. Live in ~2 minutes

If you're not using Git locally, you can edit files directly on GitHub via the web editor — click any file → pencil icon → edit → commit.

---

## Checklist before going live

- [ ] Payhip product keys added to `systems/item-shop.html`
- [ ] Custom domain connected and HTTPS enforced
- [ ] Test the buy buttons — click them and confirm they go to Payhip checkout
- [ ] Test the free download button — confirm it goes to Payhip checkout (free product)
- [ ] Check the site on mobile
- [ ] Update the Payhip embed page (if you still have one) to redirect to your new domain
