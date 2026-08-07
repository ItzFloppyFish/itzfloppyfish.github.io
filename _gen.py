#!/usr/bin/env python3
# Generates every /systems/<product>/index.html from one template.
# Run from the repo root:  python3 _gen.py
import json, os, io

CHECK = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
SPARK = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 18h20l-1.5-9-4.5 4-4-6-4 6-4.5-4z"/></svg>'
CODEIC = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/></svg>'
ARROW = '<svg class="ffarr" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>'
PLAY = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2C0 8.1 0 12 0 12s0 3.9.5 5.8a3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1C24 15.9 24 12 24 12s0-3.9-.5-5.8zM9.8 15.5V8.5l6.3 3.5-6.3 3.5z"/></svg>'
VAULTIC = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>'
CHEV = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>'

NAV = '''<nav class="ffnav" id="ffnav">
  <div class="ffnav-i">
    <a href="/" class="fflogo">
      <img src="/images/YouTube%20Profile%20Picture.png" class="fflogo-img" alt="Itz_FloppyFish" width="34" height="34" onerror="this.style.display='none';document.getElementById('fflf').style.display='flex'">
      <div class="fflogo-fb" id="fflf">FF</div>
      <span class="fflogo-txt">Itz_FloppyFish</span>
    </a>
    <div class="ffnav-links">
      <a class="ffnl" href="/">Home</a>
      <a class="ffnl on" href="/systems/">Systems</a>
      <a class="ffnl" href="/about/">About</a>
      <a class="ffnl" href="/contact/">Contact</a>
    </div>
    <div class="ffnav-r">
      <button class="ffnav-burger" id="ffburger" aria-label="Menu" aria-expanded="false" aria-controls="ffmenu">
        <svg class="mn" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        <svg class="x" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
      </button>
      <a href="https://payhip.com/auth/login" target="_blank" rel="noopener" class="ff-ibtn" title="My downloads" aria-label="My downloads">
        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7"/></svg>
      </a>
      <a href="/systems/" class="ff-btn-pr">All Systems <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
    </div>
  </div>
</nav>

<div class="ffmenu-ovl" id="ffmenuOvl"></div>
<aside class="ffmenu" id="ffmenu" aria-label="Mobile navigation">
  <a href="/">Home</a>
  <a href="/systems/" class="on">Systems</a>
  <a href="/about/">About</a>
  <a href="/contact/">Contact</a>
  <div class="ffmenu-div"></div>
  <a href="https://payhip.com/auth/login" target="_blank" rel="noopener">My downloads</a>
  <a href="/systems/" class="ffmenu-cta">Browse systems</a>
</aside>'''

FOOTER = '''<footer class="ffoot">
  <div class="ffoot-bottom-bar">
    <div class="ffoot-bot-left">
      <span>&#169; 2026 Itz_FloppyFish. All rights reserved.</span>
      <span class="ffoot-sep">&#183;</span>
      <span>Not affiliated with Roblox Corporation.</span>
    </div>
    <div class="ffoot-bot-right">v3.1.0</div>
  </div>
</footer>'''


def tier_card(name, tag, sub, items, premium=False):
    ic = SPARK if premium else CHECK
    lis = ''.join(
        '\n            <li class="fftier-f">%s<span>%s</span></li>' % (ic, i) for i in items)
    return '''        <div class="fftier%s">
          <div class="fftier-top">
            <span class="fftier-name">%s</span>
            <span class="fftier-tag">%s</span>
          </div>
          <p class="fftier-sub">%s</p>
          <ul class="fftier-l">%s
          </ul>
        </div>''' % (' pm' if premium else '', name, tag, sub, lis)


def build(p):
    both = ''.join('\n          <div class="ffboth-i"><span class="d"></span><span>%s</span></div>' % b
                   for b in p['both'])

    setup_html = ''
    if p.get('setup'):
        steps = ''.join('\n            <li>%s</li>' % s for s in p['setup'])
        setup_html = '''
      <section class="ffsec">
        <h2 class="ffsec-h">Before you start</h2>
        <p class="ffsec-sub">%s</p>
        <div class="ffsetup">
          <ol>%s
          </ol>
        </div>
      </section>
''' % (p['setup_sub'], steps)

    actions = '''        <a href="#ffdl" class="ffbtn ffbtn-ghost" id="ffJumpScripts">%s<span>%s</span>%s</a>
        <a href="%s" class="ffbtn ffbtn-ghost" target="_blank" rel="noopener">%s<span>Watch the tutorial</span></a>''' % (
        CODEIC, p['jump_label'], ARROW, p['video_url'], PLAY)

    cfg = {
        'name': p['title'],
        'freeKey': p['freeKey'],
        'premKey': p['premKey'],
        'premPrice': p['premPrice'],
        'premOriginal': p.get('premOriginal', p['premPrice']),
        'freeLabel': p['freeLabel'],
        'freeFeatures': p['buy_free'],
        'premFeatures': p['buy_prem'],
    }

    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="/images/YouTube%%20Profile%%20Picture.png">
<title>%(title)s | Itz_FloppyFish</title>
<meta name="description" content="%(meta)s">
<link rel="canonical" href="https://itzfloppyfish.com%(slug)s">
<meta property="og:type" content="product">
<meta property="og:title" content="%(title)s | Itz_FloppyFish">
<meta property="og:description" content="%(meta)s">
<meta property="og:url" content="https://itzfloppyfish.com%(slug)s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&family=Montserrat:wght@400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/main.css">
<link rel="stylesheet" href="/css/product.css">
</head>
<body>
<div class="ff-grid-bg"></div>
<canvas id="ff-cv"></canvas>
<div class="ff-wrap-inner">

%(nav)s

<main class="ffdtl">

  <header class="ffdtl-head">
    <h1>%(title)s</h1>
    <p class="ffdtl-lead">%(lead)s</p>
    <div class="ffdtl-actions">
%(actions)s
    </div>
    <p class="ffdtl-honest">%(honest)s</p>
  </header>

  <div class="ffmedia" id="ffmedia">
    <div class="ffcar" id="ffcar">
      <div class="ffcar-track" id="ffcarTrack"></div>
      <button class="ffcar-btn prev" type="button" aria-label="Previous">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <button class="ffcar-btn next" type="button" aria-label="Next">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
      </button>
      <div class="ffcar-dots" id="ffcarDots"></div>
    </div>
  </div>

  <div class="ffdtl-cols">
    <div class="ffdtl-main">

%(setup)s
      <section class="ffsec">
        <h2 class="ffsec-h">The scripts</h2>
        <p class="ffsec-sub">%(vault_sub)s</p>
        <div class="ffdl open" id="ffdl">
          <button class="ffdl-head" id="ffdlHead" type="button" aria-expanded="true" aria-controls="ffdlBody">
            <span class="ffdl-head-ic">%(vaultic)s</span>
            <span class="ffdl-head-tx">
              <span class="t">Copy the code from the video</span>
              <span class="s">Every script, in full, free — no sign-up, no paywall</span>
            </span>
            <span class="ffdl-chev" aria-hidden="true">%(chev)s</span>
          </button>
          <div class="ffdl-body" id="ffdlBody" role="region" aria-labelledby="ffdlHead">
            <div class="ffdl-inner" id="ffdlRows"></div>
          </div>
        </div>
      </section>

      <section class="ffsec">
        <h2 class="ffsec-h">Free or premium</h2>
        <p class="ffsec-sub">%(tiers_sub)s</p>

        <div class="ffboth">
          <div class="ffboth-t">In both versions</div>
          <div class="ffboth-g">%(both)s
          </div>
        </div>

        <div class="fftiers">
%(free_card)s
%(prem_card)s
        </div>

        <p class="ffnote">%(note)s</p>
      </section>

    </div>

    <aside>
      <div class="ff-buy">
        <div class="ff-buy-tabs" role="tablist" aria-label="Version">
          <button class="ff-buy-tb fr act" id="fftbf" type="button" role="tab" aria-selected="true">Free</button>
          <button class="ff-buy-tb pm" id="fftbp" type="button" role="tab" aria-selected="false">%(spark)s Premium</button>
        </div>
        <div id="ffbc"></div>
        <div class="ff-buy-feats" id="ffbf"></div>
      </div>
    </aside>
  </div>
</main>

%(footer)s

</div>
<script src="/js/main.js"></script>
<script>
/* ---------------------------------------------------------------
   Product config. This is the only part of the page that changes
   between products — everything else lives in /css/product.css
   and /js/product.js.
   --------------------------------------------------------------- */
var PRODUCT = %(cfg)s;

var MEDIA = %(media)s;

var SCRIPTS = %(scripts)s;
</script>
<script src="/js/product.js"></script>
</body>
</html>
''' % {
        'title': p['title'], 'meta': p['meta'], 'slug': p['slug'],
        'nav': NAV, 'footer': FOOTER,
        'lead': p['lead'], 'honest': p['honest'], 'actions': actions,
        'tiers_sub': p['tiers_sub'], 'both': both,
        'free_card': tier_card(p['free_name'], 'Free', p['free_sub'], p['free_items'], False),
        'prem_card': tier_card('Premium', p['premPrice'], p['prem_sub'], p['prem_items'], True),
        'note': p['note'], 'setup': setup_html, 'vault_sub': p['vault_sub'],
        'vaultic': VAULTIC, 'chev': CHEV, 'spark': SPARK,
        'cfg': json.dumps(cfg, indent=2),
        'media': json.dumps(p['media'], indent=2),
        'scripts': json.dumps(p['scripts'], indent=2),
    }


REDIRECT = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Redirecting&#8230;</title>
<link rel="canonical" href="%(slug)s">
<meta http-equiv="refresh" content="0; url=%(slug)s">
<meta name="robots" content="noindex">
<script>window.location.replace("%(slug)s");</script>
</head>
<body>Redirecting to <a href="%(slug)s">%(slug)s</a>&#8230;</body>
</html>
'''

PRODUCTS = [
    # ------------------------------------------------------------------
    {
        'key': 'asmr-bubble-wrap',
        'slug': '/systems/asmr-bubble-wrap/',
        'title': 'ASMR Bubble Wrap',
        'meta': 'Poppable ASMR bubble wrap for Roblox. Walk over it and every bubble squashes with a real pop. Free model and full scripts, or the ready-to-go premium build.',
        'lead': 'Bubble wrap you can actually walk on. Every bubble squashes under your feet with a proper pop, re-inflates a few seconds later, and never sounds the same twice — the pitch and volume shift slightly on every pop, so a whole sheet doesn\'t turn into a machine gun.',
        'jump_label': 'Copy the scripts — free',
        'video_url': 'https://www.youtube.com/watch?v=AfkSKUOUKA4',
        'honest': 'Everything in the video is free. <b>Both scripts are right here on this page</b> and the model is a free download. Premium is the same system already assembled, for people who\'d rather not do the setup.',
        'tiers_sub': 'Same system either way. The difference is how much of it is already built.',
        'both': [
            'The exact system from the video',
            'Works on PC, mobile and console',
            'Full readable source — nothing obfuscated or locked',
            'Free to use in your own games, commercial or not',
        ],
        'free_name': 'Free',
        'free_sub': 'Everything shown in the tutorial, in pieces.',
        'free_items': [
            'The bubble wrap Blender model',
            'ASMRCore and Bubble scripts — copy them below',
            'You add the sounds and place the bubbles yourself',
        ],
        'prem_sub': 'The same thing, already put together.',
        'prem_items': [
            'Drop-in place file — no setup at all',
            'Pop sound pack included and wired up',
            'Bubbles placed, tagged and tuned',
            'Extra polish and effects from the video',
            'Priority support if something breaks',
        ],
        'note': '<b>To be clear:</b> premium adds no capability you can\'t build from the free files. It is a shortcut, not a better system. If you have an hour and follow the video, you get the same result for nothing.',
        'setup_sub': 'The free scripts run silently until these three things exist. If nothing pops, it is almost always one of these.',
        'setup': [
            'Script 1 must be a <b>ModuleScript named exactly <code>ASMRCore</code></b>, inside <code>ReplicatedStorage</code>. Script 2 looks it up by that name and will sit there doing nothing if it is spelled differently.',
            'Create a <b>Folder in <code>ReplicatedStorage</code> called <code>ASMRSounds</code></b> and put your pop sounds in it, named <code>Pop1</code>, <code>Pop2</code>, <code>Pop3</code> and so on. The name prefix is how variations get picked — no folder means no audio.',
            'Every bubble <b>Model</b> needs the attribute <code>ASMRType</code> set to the text <code>Bubble</code>, and at least one <b>BasePart</b> inside it. Models without the attribute are ignored completely.',
        ],
        'vault_sub': 'Both scripts in full, straight off the page. No character limit, no comment section, no description hunting.',
        'freeKey': 'qdN84',
        'premKey': 'fV5h0',
        'premPrice': '$1.99',
        'freeLabel': 'Download the free model',
        'buy_free': [
            'The bubble wrap Blender model',
            'Both scripts (also copyable below)',
            'No email wall, no account needed',
        ],
        'buy_prem': [
            'Drop-in place file, zero setup',
            'Pop sound pack included',
            'Bubbles placed, tagged and tuned',
            'Extra polish and effects',
            'Priority support',
        ],
        'media': [{'type': 'video', 'id': 'AfkSKUOUKA4'}],
        'scripts': [
            {'name': 'ASMRCore', 'kind': 'ModuleScript', 'location': 'ReplicatedStorage',
             'file': '/scripts/asmr-bubble-wrap/ASMRCore.lua'},
            {'name': 'Bubble', 'kind': 'LocalScript', 'location': 'StarterPlayerScripts',
             'file': '/scripts/asmr-bubble-wrap/Bubble.lua'},
        ],
    },
    # ------------------------------------------------------------------
    {
        'key': 'asmr-keyboard',
        'slug': '/systems/asmr-keyboard/',
        'title': 'ASMR Keyboard',
        'meta': 'A giant walkable keyboard for Roblox. Every key drops and clicks as you step on it, with randomised colours and letters. Free model and full scripts, or the ready-to-go premium build.',
        'lead': 'A giant keyboard you walk across. Each key sinks under your weight with a clean mechanical click and springs back when you step off, and the keys colour themselves and pick their own letters on join, so no two servers look the same.',
        'jump_label': 'Copy the scripts — free',
        'video_url': 'https://www.youtube.com/watch?v=IHcgO49qaJA',
        'honest': 'Everything in the video is free. <b>Both scripts are right here on this page</b> and the key model is a free download. Premium is the same system already assembled, for people who\'d rather not do the setup.',
        'tiers_sub': 'Same system either way. The difference is how much of it is already built.',
        'both': [
            'The exact system from the video',
            'Works on PC, mobile and console',
            'Full readable source — nothing obfuscated or locked',
            'Free to use in your own games, commercial or not',
        ],
        'free_name': 'Free',
        'free_sub': 'Everything shown in the tutorial, in pieces.',
        'free_items': [
            'The Key Blender model from the video',
            'Both scripts — copy them below',
            'You lay out the keyboard and add the sound yourself',
        ],
        'prem_sub': 'The same thing, already put together.',
        'prem_items': [
            'Full keyboard laid out and ready to drop in',
            'Multiple keypress sound variations',
            'Key model included and set up',
            'Tuned drop distance, timing and detection',
            'Priority support if something breaks',
        ],
        'note': '<b>To be clear:</b> premium adds no capability you can\'t build from the free files. It is a shortcut, not a better system. If you have an hour and follow the video, you get the same result for nothing.',
        'setup_sub': 'A few things the scripts assume. If your keys do nothing, it is almost always one of these.',
        'setup': [
            'Every key must be <b>named exactly <code>Key</code></b> — that name is what both scripts search for. If a key is a <b>Model</b> rather than a single part, it needs its <code>PrimaryPart</code> set, or it gets skipped.',
            'The click sound is set inside the LocalScript as <code>SoundId</code>. The one in the video is included, but swap in your own asset id whenever you like.',
            'For the letters, put a <b>SurfaceGui with a TextLabel</b> on each key. The server script picks a random colour and letter per key and sets the text colour so it stays readable.',
        ],
        'vault_sub': 'Both scripts in full, straight off the page. No character limit, no comment section, no description hunting.',
        'freeKey': '4wF3G',
        'premKey': 'eKqY7',
        'premPrice': '$1.99',
        'freeLabel': 'Download the free model',
        'buy_free': [
            'The Key Blender model',
            'Both scripts (also copyable below)',
            'No email wall, no account needed',
        ],
        'buy_prem': [
            'Full keyboard laid out, zero setup',
            'Multiple keypress sound variations',
            'Key model included and set up',
            'Tuned timing and detection',
            'Priority support',
        ],
        'media': [
            {'type': 'video', 'id': 'IHcgO49qaJA'},
            {'type': 'image', 'src': '/images/NewKey.jpg'},
        ],
        'scripts': [
            {'name': 'ASMRKeyboard', 'kind': 'LocalScript', 'location': 'StarterPlayerScripts',
             'file': '/scripts/asmr-keyboard/ASMRKeyboard.lua'},
            {'name': 'KeyColour', 'kind': 'Script', 'location': 'ServerScriptService',
             'file': '/scripts/asmr-keyboard/KeyColour.lua'},
        ],
    },
    # ------------------------------------------------------------------
    {
        'key': 'item-shop',
        'slug': '/systems/item-shop/',
        'title': 'Item Shop System',
        'meta': 'A complete in-game shop for Roblox with categories, item previews and buy confirmations. Free tutorial version, or the polished premium build.',
        'lead': 'A complete in-game shop. Categories, item previews, buy confirmations and a purchase log, all working out of the box on PC and mobile, so you can drop it in and get back to building the actual game.',
        'jump_label': 'Jump to the scripts',
        'video_url': 'https://www.youtube.com/watch?v=W4TD81WCRQc',
        'honest': 'The full tutorial build is free — the video walks through all of it. Premium is the same shop with the interface finished off and the extras wired up.',
        'tiers_sub': 'The back end is identical in both. Premium is the same shop, further along.',
        'both': [
            'The same shop back end and data handling',
            'Works on PC, mobile and console',
            'Full readable source — nothing obfuscated or locked',
            'Free to use in your own games, commercial or not',
        ],
        'free_name': 'Free',
        'free_sub': 'The build from the tutorial, exactly as shown.',
        'free_items': [
            'Working shop UI you can buy from',
            'Item data set up and easy to extend',
            'Drops straight into an existing game',
        ],
        'prem_sub': 'The same shop, finished and dressed up.',
        'prem_items': [
            'Polished, animated interface',
            'Category tabs and sale timers',
            'Confetti on a successful purchase',
            'Purchase log via Discord webhooks',
            'Priority support if something breaks',
        ],
        'note': '<b>To be clear:</b> the free version is a working shop, not a demo. Premium adds presentation and convenience on top of the same foundation.',
        'setup_sub': '',
        'setup': [],
        'vault_sub': 'Copy-paste versions of the shop scripts are being added here.',
        'freeKey': 'W29xU',
        'premKey': '8vZLn',
        'premPrice': '$4.99',
        'freeLabel': 'Download the free version',
        'buy_free': [
            'Working shop from the tutorial',
            'Item data set up and extendable',
            'No email wall, no account needed',
        ],
        'buy_prem': [
            'Polished animated interface',
            'Category tabs and sale timers',
            'Confetti purchase effect',
            'Discord webhook purchase log',
            'Priority support',
        ],
        'media': [
            {'type': 'image', 'src': '/images/ItemShop.jpg'},
            {'type': 'video', 'id': 'W4TD81WCRQc'},
        ],
        'scripts': [],
    },
]

root = os.path.dirname(os.path.abspath(__file__))
for p in PRODUCTS:
    d = os.path.join(root, 'systems', p['key'])
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(build(p))
    with io.open(os.path.join(root, 'systems', p['key'] + '.html'), 'w', encoding='utf-8') as f:
        f.write(REDIRECT % {'slug': p['slug']})
    print('wrote', p['slug'])
