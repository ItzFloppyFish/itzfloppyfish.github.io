#!/usr/bin/env python3
# Generates every /systems/<product>/index.html from one template.
# Run from the repo root:  python3 _gen.py
import json, os, io

CHECK = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
SPARK = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 18h20l-1.5-9-4.5 4-4-6-4 6-4.5-4z"/></svg>'
CODEIC = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m18 16 4-4-4-4"/><path d="m6 8-4 4 4 4"/><path d="m14.5 4-5 16"/></svg>'
ARROW = '<svg class="ffarr" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>'
ARROW_R = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
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
    <div class="ffoot-bot-right">v3.3.0</div>
  </div>
</footer>'''



# =====================================================================
#  TEMPLATE PIECES
# =====================================================================

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


def tiers_section(p):
    if not p.get('tiers'):
        return ''
    both = ''.join('\n          <div class="ffboth-i"><span class="d"></span><span>%s</span></div>' % b
                   for b in p['both'])
    return '''      <section class="ffsec">
        <h2 class="ffsec-h">Free or %(paid_lc)s</h2>
        <p class="ffsec-sub">%(tiers_sub)s</p>

        <div class="ffboth">
          <div class="ffboth-t">In both versions</div>
          <div class="ffboth-g">%(both)s
          </div>
        </div>

        <div class="fftiers">
%(free_card)s
%(paid_card)s
        </div>

        <p class="ffnote">%(note)s</p>
      </section>

''' % {
        'paid_lc': p['paidName'].lower(),
        'tiers_sub': p['tiers_sub'], 'both': both,
        'free_card': tier_card('Free', 'Free', p['free_sub'], p['free_items'], False),
        'paid_card': tier_card(p['paidName'], p['premPrice'], p['paid_sub'], p['paid_items'], True),
        'note': p['note'],
    }


def grid_section(p):
    if not p.get('groups'):
        return ''
    cols = ''.join('''
          <div class="ffgrp">
            <div class="ffgrp-h">%s</div>
            <ul>%s
            </ul>
          </div>''' % (g['t'], ''.join('\n              <li>%s</li>' % i for i in g['i']))
                   for g in p['groups'])
    return '''      <section class="ffsec">
        <h2 class="ffsec-h">What's inside</h2>
        <p class="ffsec-sub">%s</p>
        <div class="ffgrid">%s
        </div>
      </section>

''' % (p['groups_sub'], cols)


def video_section(p):
    if not p.get('video_url'):
        return ''
    return '''      <section class="ffsec">
        <a class="ffvid" href="%s" target="_blank" rel="noopener">
          <span class="ffvid-ic">%s</span>
          <span class="ffvid-tx">
            <span class="t">Setup is in the video</span>
            <span class="s">%s</span>
          </span>
          <span class="ffvid-ar">%s</span>
        </a>
      </section>

''' % (p['video_url'], PLAY, p['video_note'], ARROW_R)


def vault_section(p):
    if not p.get('scripts'):
        return ''
    return '''      <section class="ffsec">
        <h2 class="ffsec-h">The scripts</h2>
        <p class="ffsec-sub">%(vault_sub)s</p>
        <div class="ffdl open" id="ffdl">
          <button class="ffdl-head" id="ffdlHead" type="button" aria-expanded="true" aria-controls="ffdlBody">
            <span class="ffdl-head-ic">%(vaultic)s</span>
            <span class="ffdl-head-tx">
              <span class="t">Copy the code from the video</span>
              <span class="s">Every script, in full, free</span>
            </span>
            <span class="ffdl-chev" aria-hidden="true">%(chev)s</span>
          </button>
          <div class="ffdl-body" id="ffdlBody" role="region" aria-labelledby="ffdlHead">
            <div class="ffdl-inner" id="ffdlRows"></div>
          </div>
        </div>
      </section>

''' % {'vault_sub': p['vault_sub'], 'vaultic': VAULTIC, 'chev': CHEV}


def pitch_section(p):
    if not p.get('pitch'):
        return ''
    t, b, label, href = p['pitch']
    return '''      <section class="ffsec">
        <div class="ffpitch">
          <div class="ffpitch-tx">
            <span class="t">%s</span>
            <span class="s">%s</span>
          </div>
          <a class="ffbtn ffbtn-ghost" href="%s">%s</a>
        </div>
      </section>

''' % (t, b, href, label)


def build(p):
    p.setdefault('paidName', 'Drop-in')
    p.setdefault('tiers', True)
    p.setdefault('scripts', [])
    p.setdefault('singleTier', False)

    acts = []
    if p.get('scripts'):
        acts.append('        <a href="#ffdl" class="ffbtn ffbtn-ghost" id="ffJumpScripts">%s<span>%s</span>%s</a>'
                    % (CODEIC, 'Copy the scripts — free', ARROW))
    if p.get('video_url'):
        acts.append('        <a href="%s" class="ffbtn ffbtn-ghost" target="_blank" rel="noopener">%s<span>Watch the tutorial</span></a>'
                    % (p['video_url'], PLAY))
    for b in p.get('heroBtns', []):
        acts.append('        <a href="%s" class="ffbtn ffbtn-ghost" target="_blank" rel="noopener">%s<span>%s</span></a>'
                    % (b['href'], b.get('icon', ''), b['label']))

    tabs = '' if p['singleTier'] else '''        <div class="ff-buy-tabs" role="tablist" aria-label="Version">
          <button class="ff-buy-tb fr act" id="fftbf" type="button" role="tab" aria-selected="true">Free</button>
          <button class="ff-buy-tb pm" id="fftbp" type="button" role="tab" aria-selected="false">%s %s</button>
        </div>
''' % (SPARK, p['paidName'])

    cfg = {
        'name': p['title'],
        'freeKey': p.get('freeKey', ''),
        'premKey': p['premKey'],
        'premPrice': p['premPrice'],
        'premOriginal': p.get('premOriginal', p['premPrice']),
        'paidName': p['paidName'],
        'freeLabel': p.get('freeLabel', 'Download the free files'),
        'freeFeatures': p.get('buy_free', []),
        'premFeatures': p['buy_paid'],
    }
    if p['singleTier']:
        cfg['singleTier'] = True
        cfg['featsLabel'] = p.get('featsLabel', 'Includes')
        if p.get('priceNote'):
            cfg['priceNote'] = p['priceNote']
        if p.get('buyFoot'):
            cfg['buyFoot'] = p['buyFoot']
        if p.get('extraBtns'):
            cfg['extraBtns'] = p['extraBtns']

    noindex = '\n<meta name="robots" content="noindex">' if p.get('hidden') else ''

    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="/images/YouTube%%20Profile%%20Picture.png">
<title>%(title)s | Itz_FloppyFish</title>
<meta name="description" content="%(meta)s">%(noindex)s
<link rel="canonical" href="https://itzfloppyfish.com%(slug)s">
<meta property="og:type" content="product">
<meta property="og:title" content="%(title)s | Itz_FloppyFish">
<meta property="og:description" content="%(meta)s">
<meta property="og:url" content="https://itzfloppyfish.com%(slug)s">%(ogimg)s
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
%(banner)s  </header>

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

%(sections)s    </div>

    <aside>
      <div class="ff-buy">
%(tabs)s        <div id="ffbc"></div>
        <div class="ff-buy-feats" id="ffbf"></div>
      </div>
    </aside>
  </div>
</main>

%(footer)s

</div>
<script src="/js/main.js"></script>
<script>
/* Product config. The only part of this page that changes between
   products — styling lives in /css/product.css, logic in /js/product.js. */
var PRODUCT = %(cfg)s;

var MEDIA = %(media)s;

var SCRIPTS = %(scripts)s;
</script>
<script src="/js/product.js"></script>
</body>
</html>
''' % {
        'title': p['title'], 'meta': p['meta'], 'slug': p['slug'], 'noindex': noindex,
        'ogimg': ('\n<meta property="og:image" content="https://itzfloppyfish.com%s">' % p['ogimg']) if p.get('ogimg') else '',
        'nav': NAV, 'footer': FOOTER,
        'lead': p['lead'],
        'actions': '\n'.join(acts),
        'banner': p.get('banner', ''),
        'sections': vault_section(p) + video_section(p) + grid_section(p) + tiers_section(p) + pitch_section(p),
        'tabs': tabs,
        'cfg': json.dumps(cfg, indent=2),
        'media': json.dumps(p['media'], indent=2),
        'scripts': json.dumps([{'name': s['name'], 'kind': s['kind'], 'file': s['file']}
                               for s in p.get('scripts', [])], indent=2),
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

# =====================================================================
#  >>> VALUES STILL NEEDED BEFORE LAUNCH <<<
#  Anything left as TODO_ renders its button greyed out and unclickable
#  rather than sending a buyer to a dead Payhip link.
# =====================================================================
BUTTER_FREE_KEY = 'lzCJM'
BUTTER_PAID_KEY = '8oPMH'
BUTTER_VIDEO_ID = 'TR973nb8pCE'
UIPACK_KEY      = 'TODO_uipack'  # see README — cannot be another store's id


COMMON_BOTH = [
    'The exact system from the video',
    'Works on PC, mobile and console',
    'Full readable source — nothing obfuscated',
    'Free to use in your own games, commercial or not',
]

PRODUCTS = [
    # ------------------------------------------------------------------
    {
        'key': 'asmr-butter',
        'slug': '/systems/asmr-butter/',
        'title': 'ASMR Butter',
        'meta': 'Walkable ASMR butter for Roblox. Sink into a soft block, or crack the crust on the crunchy version. Free Blender models and all four scripts, or the drop-in build.',
        'lead': 'Butter you sink into. Stand on the soft block and it dents under you, slowly easing back once you step off. The crunchy version adds a brittle shell that splits open as you press in and closes again behind you.',
        'video_url': 'https://www.youtube.com/watch?v=' + BUTTER_VIDEO_ID if BUTTER_VIDEO_ID else '',
        'video_note': 'The models need bones and the sounds need naming. Both are covered start to finish.',
        'tiers_sub': 'Same system either way. The difference is how much of it is already built.',
        'both': COMMON_BOTH,
        'free_sub': 'The models, plus every script on this page.',
        'free_items': [
            'Both Blender models — smooth and crunchy',
            'All four scripts, copyable below',
            'You add the sounds and set the models up',
        ],
        'paid_sub': 'The same thing, already put together.',
        'paid_items': [
            'Place file with everything assembled',
            'Butter sounds included and wired up',
            'Both butter types ready to walk on',
            'Priority support if something breaks',
        ],
        'note': '<b>To be clear:</b> the drop-in build adds nothing you can\'t make from the free files. It is a shortcut, not a better system.',
        'vault_sub': 'All four scripts in full, straight off the page.',
        'freeKey': BUTTER_FREE_KEY,
        'premKey': BUTTER_PAID_KEY,
        'premPrice': '$1.99',
        'freeLabel': 'Download the free models',
        'buy_free': [
            'Both Blender models',
            'All four scripts (copyable below)',
            'No email wall, no account needed',
        ],
        'buy_paid': [
            'Place file, everything assembled',
            'Butter sounds included',
            'Both butter types ready to go',
            'Priority support',
        ],
        'media': ([{'type': 'video', 'id': BUTTER_VIDEO_ID}] if BUTTER_VIDEO_ID else []) +
                 [{'type': 'image', 'src': '/images/ASMRButter1.jpg'}],
        'ogimg': '/images/ASMRButter1.jpg',
        'scripts': [
            {'name': 'ASMRCore', 'kind': 'ModuleScript', 'file': '/scripts/asmr-butter/ASMRCore.lua'},
            {'name': 'ASMRControls', 'kind': 'ModuleScript', 'file': '/scripts/asmr-butter/ASMRControls.lua'},
            {'name': 'Butter', 'kind': 'LocalScript', 'file': '/scripts/asmr-butter/Butter.lua'},
            {'name': 'CrunchyButter', 'kind': 'LocalScript', 'file': '/scripts/asmr-butter/CrunchyButter.lua'},
        ],
    },
    # ------------------------------------------------------------------
    {
        'key': 'asmr-bubble-wrap',
        'slug': '/systems/asmr-bubble-wrap/',
        'title': 'ASMR Bubble Wrap',
        'meta': 'Poppable ASMR bubble wrap for Roblox. Walk over it and every bubble squashes with a real pop. Free model and both scripts, or the drop-in build.',
        'lead': 'Bubble wrap you can actually walk on. Every bubble squashes under your feet with a proper pop, re-inflates a few seconds later, and never sounds the same twice — pitch and volume shift on every pop, so a whole sheet doesn\'t turn into a machine gun.',
        'video_url': 'https://www.youtube.com/watch?v=AfkSKUOUKA4',
        'video_note': 'The sounds need naming and the models need tagging. Both are covered start to finish.',
        'tiers_sub': 'Same system either way. The difference is how much of it is already built.',
        'both': COMMON_BOTH,
        'free_sub': 'The model, plus both scripts on this page.',
        'free_items': [
            'The bubble wrap Blender model',
            'Both scripts, copyable below',
            'You add the sounds and place the bubbles',
        ],
        'paid_sub': 'The same thing, already put together.',
        'paid_items': [
            'Place file with everything assembled',
            'Pop sound pack included and wired up',
            'Bubbles placed, tagged and tuned',
            'Priority support if something breaks',
        ],
        'note': '<b>To be clear:</b> the drop-in build adds nothing you can\'t make from the free files. It is a shortcut, not a better system.',
        'vault_sub': 'Both scripts in full, straight off the page.',
        'freeKey': 'qdN84',
        'premKey': 'fV5h0',
        'premPrice': '$1.99',
        'freeLabel': 'Download the free model',
        'buy_free': [
            'The bubble wrap Blender model',
            'Both scripts (copyable below)',
            'No email wall, no account needed',
        ],
        'buy_paid': [
            'Place file, everything assembled',
            'Pop sound pack included',
            'Bubbles placed, tagged and tuned',
            'Priority support',
        ],
        'media': [
            {'type': 'video', 'id': 'AfkSKUOUKA4'},
            {'type': 'image', 'src': '/images/BubbleWrapThumbnail.jpg'},
        ],
        'ogimg': '/images/BubbleWrapThumbnail.jpg',
        'scripts': [
            {'name': 'ASMRCore', 'kind': 'ModuleScript', 'file': '/scripts/asmr-bubble-wrap/ASMRCore.lua'},
            {'name': 'Bubble', 'kind': 'LocalScript', 'file': '/scripts/asmr-bubble-wrap/Bubble.lua'},
        ],
    },
    # ------------------------------------------------------------------
    {
        'key': 'asmr-keyboard',
        'slug': '/systems/asmr-keyboard/',
        'title': 'ASMR Keyboard',
        'meta': 'A giant walkable keyboard for Roblox. Every key drops and clicks as you step on it, with randomised colours and letters. Free model and both scripts, or the drop-in build.',
        'lead': 'A giant keyboard you walk across. Each key sinks under your weight with a clean mechanical click and springs back when you step off, and the keys colour themselves and pick their own letters on join, so no two servers look the same.',
        'video_url': 'https://www.youtube.com/watch?v=IHcgO49qaJA',
        'video_note': 'Key naming and the letter setup both matter. Covered start to finish.',
        'tiers_sub': 'Same system either way. The difference is how much of it is already built.',
        'both': COMMON_BOTH,
        'free_sub': 'The model, plus both scripts on this page.',
        'free_items': [
            'The Key Blender model from the video',
            'Both scripts, copyable below',
            'You lay out the keyboard and add the sound',
        ],
        'paid_sub': 'The same thing, already put together.',
        'paid_items': [
            'Full keyboard laid out and ready to drop in',
            'Multiple keypress sound variations',
            'Key model included and set up',
            'Priority support if something breaks',
        ],
        'note': '<b>To be clear:</b> the drop-in build adds nothing you can\'t make from the free files. It is a shortcut, not a better system.',
        'vault_sub': 'Both scripts in full, straight off the page.',
        'freeKey': '4wF3G',
        'premKey': 'eKqY7',
        'premPrice': '$1.99',
        'freeLabel': 'Download the free model',
        'buy_free': [
            'The Key Blender model',
            'Both scripts (copyable below)',
            'No email wall, no account needed',
        ],
        'buy_paid': [
            'Full keyboard laid out, zero setup',
            'Multiple keypress sound variations',
            'Key model included and set up',
            'Priority support',
        ],
        'media': [
            {'type': 'video', 'id': 'IHcgO49qaJA'},
            {'type': 'image', 'src': '/images/NewKey.jpg'},
        ],
        'ogimg': '/images/NewKey.jpg',
        'scripts': [
            {'name': 'ASMRKeyboard', 'kind': 'LocalScript', 'file': '/scripts/asmr-keyboard/ASMRKeyboard.lua'},
            {'name': 'KeyColour', 'kind': 'Script', 'file': '/scripts/asmr-keyboard/KeyColour.lua'},
        ],
    },
    # ------------------------------------------------------------------
    {
        'key': 'essential-ui-pack',
        'slug': '/systems/essential-ui-pack/',
        'title': 'Essential STUD UI Pack',
        'meta': 'Eleven-plus fully scripted Roblox UI systems — shops, rewards, codes, leaderboards and settings — with secure server-side handling. Built by Viral Templates.',
        'lead': 'Eleven-plus complete UI systems, front end and back end, ready to drop into a live game. Shops, daily rewards, codes, leaderboards, settings and the data layer behind them are already built, animated and validated server-side.',
        'banner': '''    <div class="ffpartner">
      <span class="ffpartner-b">Partner</span>
      <span class="ffpartner-t">Built by <b>Viral Templates</b>, stocked here as part of an ongoing partnership.</span>
    </div>
''',
        'singleTier': True,
        'tiers': False,
        'groups_sub': 'Every system ships with its own configuration module, so prices, rewards, timers and visuals change without touching the core scripts.',
        'groups': [
            {'t': 'Monetisation', 'i': [
                'Complete Robux shop', 'Game Pass shop and gifting',
                'Developer Product shop and gifting', 'Packs system']},
            {'t': 'Rewards &amp; retention', 'i': [
                'Daily login rewards', 'Playtime rewards', 'Group rewards',
                'Wheel spin with free-spin countdown', 'Purchasable extra spins']},
            {'t': 'Player engagement', 'i': [
                'Redeemable codes', 'Top players leaderboard',
                'Side promotions', 'Animated notification system']},
            {'t': 'Player experience', 'i': [
                'Animated loading screen with skip', 'Settings menu with music and SFX sliders',
                'Background music system', 'Cash gain and loss animations',
                'Purchase celebration confetti', 'Fully animated buttons and UI']},
            {'t': 'Backend &amp; admin', 'i': [
                'Secure data saving via ProfileStore', 'Server-side purchase validation',
                'Admin commands: GiveCash, GivePack, GivePass, GiveProduct',
                'Clean, organised, expandable codebase']},
        ],
        'premKey': UIPACK_KEY,
        'premPrice': '$19.99',
        'paidName': 'UI Pack',
        'featsLabel': 'Highlights',
        'priceNote': 'One-time purchase \u00b7 Instant download',
        'buyFoot': 'Sold in partnership with Viral Templates.',
        'buy_paid': [
            '11+ complete UI systems',
            'Front end and back end included',
            'Secure server-side validation',
            'ProfileStore data saving',
            'Config modules for every system',
        ],
        'extraBtns': [
            {'label': 'Try it in Roblox', 'href': 'https://www.roblox.com/games/102413875159603/Viral-Templates', 'icon': 'play'},
            {'label': 'Viral Templates terms', 'href': 'https://viraltemplates.co/terms', 'icon': 'doc'},
        ],
        'media': [
            {'type': 'image', 'src': '/images/UiPackUpdated.jpg'},
            {'type': 'image', 'src': '/images/EssentialUiPack1.jpg'},
            {'type': 'image', 'src': '/images/PackUpdated.jpg'},
            {'type': 'image', 'src': '/images/PackThumbnail2.jpg'},
        ],
        'ogimg': '/images/UiPackUpdated.jpg',
        'pitch': ('Building Roblox systems of your own?',
                  'I am open to stocking a small number of systems I did not make. '
                  'If yours would sit well alongside the rest of the shelf, send it over.',
                  'Get in touch', '/contact/'),
    },
    # ------------------------------------------------------------------
    #  HIDDEN — page still builds and works by direct URL, but it is not
    #  listed anywhere and is marked noindex. Remove 'hidden' to relist.
    # ------------------------------------------------------------------
    {
        'key': 'item-shop',
        'hidden': True,
        'slug': '/systems/item-shop/',
        'title': 'Item Shop System',
        'meta': 'A complete in-game shop for Roblox with categories, item previews and buy confirmations.',
        'lead': 'A complete in-game shop. Categories, item previews, buy confirmations and a purchase log, all working out of the box on PC and mobile.',
        'video_url': 'https://www.youtube.com/watch?v=W4TD81WCRQc',
        'video_note': 'The full build is walked through end to end.',
        'tiers_sub': 'The back end is identical in both. The paid build is the same shop, further along.',
        'both': COMMON_BOTH,
        'free_sub': 'The build from the tutorial, exactly as shown.',
        'free_items': [
            'Working shop UI you can buy from',
            'Item data set up and easy to extend',
            'Drops straight into an existing game',
        ],
        'paid_sub': 'The same shop, finished and dressed up.',
        'paid_items': [
            'Polished, animated interface',
            'Category tabs and sale timers',
            'Confetti on a successful purchase',
            'Purchase log via Discord webhooks',
        ],
        'note': '<b>To be clear:</b> the free version is a working shop, not a demo.',
        'vault_sub': '',
        'freeKey': 'W29xU',
        'premKey': '8vZLn',
        'premPrice': '$4.99',
        'paidName': 'Premium',
        'freeLabel': 'Download the free version',
        'buy_free': [
            'Working shop from the tutorial',
            'Item data set up and extendable',
            'No email wall, no account needed',
        ],
        'buy_paid': [
            'Polished animated interface',
            'Category tabs and sale timers',
            'Confetti purchase effect',
            'Discord webhook purchase log',
        ],
        'media': [
            {'type': 'image', 'src': '/images/ItemShop.jpg'},
            {'type': 'video', 'id': 'W4TD81WCRQc'},
        ],
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
    print('wrote %-34s %s' % (p['slug'], '(hidden)' if p.get('hidden') else ''))
