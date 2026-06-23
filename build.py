#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static-site generator for woodstockhvacpros.ca
Outputs pure static HTML (no runtime dependency) into the repo root.
Run:  python3 build.py
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ CONFIG
SITE_NAME   = "Woodstock Heating & Cooling"
SHORT_NAME  = "Woodstock Heating &amp; Cooling"
DOMAIN      = "https://woodstockhvacpros.ca"
CITY        = "Woodstock"
REGION      = "Ontario"
REGION_ABBR = "ON"
COUNTY      = "Oxford County"
PHONE_DISPLAY = "(519) 539-4170"
PHONE_TEL     = "+15195394170"
EMAIL         = "contact@woodstockhvacpros.ca"
ADDR_STREET   = "438 Dundas St"
ADDR_LOCALITY = "Woodstock"
ADDR_REGION   = "ON"
ADDR_POSTAL   = "N4S 1B9"
# -----------------------------------------------------------------------

# Canonical service-area list
SERVICE_AREAS = ['Woodstock', 'Ingersoll', 'Tillsonburg', 'Norwich', 'Thamesford', 'Embro']

# ------------------------------------------------------------------ ICONS (Lucide-style)
_IC = {
 "flame":'<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
 "snowflake":'<line x1="2" x2="22" y1="12" y2="12"/><line x1="12" x2="12" y1="2" y2="22"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/>',
 "wind":'<path d="M12.8 19.6A2 2 0 1 0 14 16H2"/><path d="M17.5 8a2.5 2.5 0 1 1 2 4H2"/><path d="M9.8 4.4A2 2 0 1 1 11 8H2"/>',
 "fan":'<path d="M10.827 16.379a6.082 6.082 0 0 1-8.618-7.002l5.412 1.45a6.082 6.082 0 0 1 7.002-8.618l-1.45 5.412a6.082 6.082 0 0 1 8.618 7.002l-5.412-1.45a6.082 6.082 0 0 1-7.002 8.618l1.45-5.412Z"/><circle cx="12" cy="12" r="1"/>',
 "refresh":'<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 "fireplace":'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 17.5a2.5 2.5 0 0 0 2.5-2.5c0-1-.6-1.7-1.1-2.2-.7-.7-.5-1.9 0-2.9-1.3.4-2.1 1.4-2.4 2.4-.4-.3-.6-.9-.5-1.5-.8.6-1.2 1.6-1.2 2.7a2.5 2.5 0 0 0 2.7 2.5"/>',
 "gauge":'<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
 "air-vent":'<path d="M6 12H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 8h12"/><path d="M18.3 19.3a2.5 2.5 0 0 1-3.96-.7 2.5 2.5 0 0 0-3.96-.69m7.92 1.39a2.5 2.5 0 0 0 .42-3.39"/><path d="M12 12v6"/>',
 "wrench":'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 "home":'<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
 "shield":'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 "clock":'<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
 "dollar":'<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/>',
 "check":'<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>',
 "check-sm":'<path d="M20 6 9 17l-5-5"/>',
 "phone":'<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "mail":'<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 "pin":'<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
 "chev-down":'<path d="m6 9 6 6 6-6"/>',
 "chev-right":'<path d="m9 18 6-6-6-6"/>',
 "arrow-right":'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 "plus":'<path d="M5 12h14"/><path d="M12 5v14"/>',
 "users":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "award":'<path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>',
 "droplets":'<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 4.7 7 2.7c-.29 2-1.14 3.34-2.29 4.36S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A11 11 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a7 7 0 0 1-11.91 4.97"/>',
 "zap":'<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
 "leaf":'<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>',
 "calendar":'<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
 "thermometer":'<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
 "settings":'<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
 "headset":'<path d="M3 11h3a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M18 11h3v7a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1z"/><path d="M3 11a9 9 0 0 1 18 0"/><path d="M18 19a3 3 0 0 1-3 3h-3"/>',
 "facebook":'<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 "instagram":'<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/>',
 "send":'<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
 "search":'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 "quote":'<path d="M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h3v2a2 2 0 0 1-2 2h-1a1 1 0 0 0 0 2h1a4 4 0 0 0 4-4V5a2 2 0 0 0-2-2z"/><path d="M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h3v2a2 2 0 0 1-2 2H5a1 1 0 0 0 0 2h1a4 4 0 0 0 4-4V5a2 2 0 0 0-2-2z"/>',
}
def icon(name, cls="", size=24, fill=False):
    inner = _IC[name]
    f = 'fill="currentColor" stroke="none"' if fill else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" {f} aria-hidden="true">{inner}</svg>'

STAR = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 2.9 6.26L22 9.27l-5 4.87L18.18 22 12 18.56 5.82 22 7 14.14l-5-4.87 7.1-1.01z"/></svg>'
def stars(n=5): return '<div class="stars" aria-label="'+str(n)+' out of 5 stars">'+STAR*n+'</div>'

# ------------------------------------------------------------------ LOGO
LOGO_MARK = '''<svg class="brand__mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{name} logo">
  <rect width="48" height="48" rx="13" fill="url(#ahcg)"/>
  <path d="M19 12.5c.4 2.4-.4 3.9-1.7 5.2-1.5 1.5-2.6 3-2.6 5.3a7 7 0 0 0 12.2 4.6" stroke="#d4a843" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <path d="M19 12.5c2.4 2.4 5.6 4.2 7.4 6.6 1.4 1.9 1.7 4 .5 6" stroke="#b8860b" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
  <g stroke="#d4a843" stroke-width="2" stroke-linecap="round">
    <line x1="33" y1="16" x2="33" y2="30"/><line x1="26.5" y1="23" x2="39.5" y2="23"/>
    <line x1="28.6" y1="18.6" x2="37.4" y2="27.4"/><line x1="37.4" y1="18.6" x2="28.6" y2="27.4"/>
  </g>
  <defs><linearGradient id="ahcg" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
    <stop stop-color="#d4a843"/><stop offset="1" stop-color="#1e293b"/></linearGradient></defs>
</svg>'''.replace("{name}", SITE_NAME)

def brand(footer=False):
    cls = "brand footer-brand" if footer else "brand"
    return f'''<a class="{cls}" href="/" aria-label="{SITE_NAME} home">
      {LOGO_MARK}
      <span class="brand__text">
        <span class="brand__name">{CITY}</span>
        <span class="brand__tag">Heating &amp; Cooling</span>
      </span>
    </a>'''

# ------------------------------------------------------------------ NAV / SERVICES DATA
SERVICES = [
 {"slug":"furnace-repair","nav":"Furnace Repair","icon":"flame"},
 {"slug":"ac-repair","nav":"AC Repair","icon":"snowflake"},
 {"slug":"ductless-ac-installation","nav":"Ductless AC Installation","icon":"fan"},
 {"slug":"heat-pump-repair-installation","nav":"Heat Pump Repair &amp; Installation","icon":"refresh"},
 {"slug":"fireplace-installation","nav":"Fireplace Installation","icon":"fireplace"},
 {"slug":"thermostat-repair-replacement","nav":"Thermostat Repair &amp; Replacement","icon":"gauge"},
 {"slug":"duct-cleaning","nav":"Duct Cleaning","icon":"air-vent"},
]

def nav_links(active=""):
    def cur(key): return ' aria-current="page"' if active==key else ''
    drop = "".join(
        f'<a href="/services/{s["slug"]}/">{icon(s["icon"],size=18)}<span>{s["nav"]}</span></a>'
        for s in SERVICES)
    return f'''
      <a class="nav__link" href="/"{cur('home')}>Home</a>
      <a class="nav__link" href="/about/"{cur('about')}>About</a>
      <div class="has-dropdown">
        <a class="nav__link" href="/services/"{cur('services')} aria-haspopup="true" aria-expanded="false">Services {icon('chev-down',size=15)}</a>
        <div class="dropdown">{drop}</div>
      </div>
      <a class="nav__link" href="/blog/"{cur('blog')}>Blog</a>
      <a class="nav__link" href="/contact/"{cur('contact')}>Contact</a>
      <div class="nav__cta">
        <a class="btn btn-primary" href="/contact/">Get a Free Quote</a>
      </div>'''

def header(active=""):
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container">
    <div class="topbar__left">
      <span class="topbar__item">{icon('clock',size=15)} 24/7 Emergency Service</span>
      <span class="topbar__item topbar__item--areas">{icon('pin',size=15)} Serving {CITY} &amp; {COUNTY}</span>
    </div>
    <a class="topbar__right" href="/contact/">{icon('check-sm',size=15)} Free, No-Obligation Quotes</a>
  </div>
</div>
<header class="site-header">
  <div class="container navbar">
    {brand()}
    <nav class="nav" id="primary-nav" aria-label="Primary">{nav_links(active)}</nav>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
<div class="nav-backdrop" aria-hidden="true"></div>'''

# ------------------------------------------------------------------ FOOTER
def footer():
    svc = "".join(f'<a href="/services/{s["slug"]}/">{s["nav"]}</a>' for s in SERVICES)
    areas = "".join(f'<li>{a}</li>' for a in SERVICE_AREAS)
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        {brand(footer=True)}
        <p class="footer-about">Honest, dependable heating and cooling for {CITY}, Ontario and the surrounding {COUNTY} communities. Family-run, licensed, and available 24/7.</p>
      </div>
      <div>
        <h4>Company</h4>
        <div class="footer-links">
          <a href="/">Home</a><a href="/about/">About</a>
          <a href="/services/">Services</a><a href="/blog/">Blog</a>
          <a href="/contact/">Contact</a><a href="/privacy-policy/">Privacy Policy</a>
        </div>
      </div>
      <div>
        <h4>Our Services</h4>
        <div class="footer-links">{svc}</div>
      </div>
      <div>
        <h4>Get in Touch</h4>
        <ul class="footer-contact">
          <li>{icon('phone',size=19)}<a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li>{icon('mail',size=19)}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{icon('pin',size=19)}<span>{CITY}, {REGION}, {ADDR_POSTAL}</span></li>
          <li>{icon('clock',size=19)}<span>Open 24 hours · 7 days a week</span></li>
        </ul>
        <h4 style="margin-top:6px">Service Areas</h4>
        <ul class="footer-links" style="columns:2">{areas}</ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> {SHORT_NAME}. All rights reserved.</span>
      <span><a href="/privacy-policy/">Privacy Policy</a> &nbsp;·&nbsp; <a href="/sitemap.xml">Sitemap</a></span>
    </div>
  </div>
</footer>
<div class="mobile-bar mobile-bar--single">
  <a class="btn btn-primary" href="/contact/">{icon('send',size=18)} Get a Free Quote</a>
</div>
<script src="/assets/js/main.js" defer></script>'''

# ------------------------------------------------------------------ QUOTE FORM
def quote_form(heading="Get a Free Quote", sub="No obligation. Fast response. Honest pricing.", id_suffix="hero"):
    return f'''<form class="quote-card" data-quote-form novalidate aria-label="Request a free quote">
  <div class="quote-card__head">
    <span class="badge">{icon('headset',size=24)}</span>
    <div><h3 id="quote">{heading}</h3></div>
  </div>
  <p class="sub">{sub}</p>
  <div class="form-status" role="status" aria-live="polite"></div>
  <div class="form-grid">
    <div class="field">
      <label for="name-{id_suffix}">Full Name <span class="req">*</span></label>
      <input class="input" id="name-{id_suffix}" name="name" type="text" autocomplete="name" placeholder="Jane Doe" required>
      <span class="error-text">Please enter your name.</span>
    </div>
    <div class="field row">
      <div>
        <label for="phone-{id_suffix}">Phone <span class="req">*</span></label>
        <input class="input" id="phone-{id_suffix}" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(905) 000-0000" required>
        <span class="error-text">Enter a phone number.</span>
      </div>
      <div>
        <label for="email-{id_suffix}">Email <span class="req">*</span></label>
        <input class="input" id="email-{id_suffix}" name="email" type="email" autocomplete="email" placeholder="you@email.com" required>
        <span class="error-text">Enter a valid email.</span>
      </div>
    </div>
    <div class="field">
      <label for="addr-{id_suffix}">Street Address</label>
      <input class="input" id="addr-{id_suffix}" name="address" type="text" autocomplete="address-line1" placeholder="123 Main St">
    </div>
    <div class="field row">
      <div>
        <label for="city-{id_suffix}">City</label>
        <input class="input" id="city-{id_suffix}" name="city" type="text" autocomplete="address-level2" placeholder="{CITY}">
      </div>
      <div>
        <label for="postal-{id_suffix}">Postal Code</label>
        <input class="input" id="postal-{id_suffix}" name="postal" type="text" autocomplete="postal-code" placeholder="N1A 1A1">
      </div>
    </div>
    <div class="field">
      <label for="msg-{id_suffix}">Briefly describe your issue <span class="req">*</span></label>
      <textarea class="input" id="msg-{id_suffix}" name="message" placeholder="e.g. Furnace won't turn on…" required></textarea>
      <span class="error-text">Tell us briefly what's going on.</span>
    </div>
    <button class="btn btn-primary btn-lg btn-block" type="submit">{icon('send',size=18)} Request My Free Quote</button>
    <p class="form-note">{icon('shield',size=15)} Your details stay private. We never share your information.</p>
  </div>
</form>'''

# ------------------------------------------------------------------ HEAD / PAGE WRAPPER
GOOGLE_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">')

FAVICON = ('<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">'
           '<link rel="apple-touch-icon" href="/assets/img/favicon.svg">')

OG_IMAGE = "https://woodstockhvacpros.ca/assets/img/og-default.png"

def hero_class():
    """Return hero class with optional background image support."""
    if os.path.exists(os.path.join(ROOT, "assets", "img", "hero.webp")):
        return "hero has-bg"
    return "hero"

def head(title, desc, path, schema_blocks=None, og_type="website", robots="index, follow", og_image=None):
    canonical = DOMAIN + path
    sb = "\n".join(schema_blocks or [])
    img = og_image or OG_IMAGE
    return f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js');</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="1e293b">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
{FAVICON}
{GOOGLE_FONTS}
<link rel="stylesheet" href="/assets/css/styles.css">
{sb}
</head>
<body>
{header(_active_for(path))}
<main id="main">'''

def _active_for(path):
    if path == "/": return "home"
    if path.startswith("/about"): return "about"
    if path.startswith("/services"): return "services"
    if path.startswith("/blog"): return "blog"
    if path.startswith("/contact"): return "contact"
    return ""

def page_end(): return f"</main>\n{footer()}\n</body>\n</html>\n"

# ------------------------------------------------------------------ SCHEMA
def plain(s):
    """Decode HTML entities used in display strings before placing inside JSON-LD."""
    return (s or "").replace("&amp;", "&").replace("&nbsp;", " ").replace("&ldquo;", '"').replace("&rdquo;", '"')

# NOTE: aggregateRating intentionally omitted, this is a new business with no
# verified reviews. Adding a fake rating violates Google's review-snippet policy.
# Add it back only when real, on-page review data exists.
def schema_localbusiness():
    return '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HVACBusiness","@id":"%s/#business",
"name":"%s","url":"%s","telephone":"%s","email":"%s","image":"%s/assets/img/og-default.png","logo":"%s/assets/img/favicon.svg",
"priceRange":"$$","areaServed":[%s],
"address":{"@type":"PostalAddress","streetAddress":"%s","addressLocality":"%s","addressRegion":"%s","postalCode":"%s","addressCountry":"CA"},
"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}}
</script>''' % (DOMAIN, plain(SITE_NAME), DOMAIN, PHONE_DISPLAY, EMAIL, DOMAIN, DOMAIN,
                ",".join('"%s, ON"' % a for a in SERVICE_AREAS),
                ADDR_STREET, ADDR_LOCALITY, ADDR_REGION, ADDR_POSTAL)

def schema_breadcrumb(items):
    el = ",".join(
      '{"@type":"ListItem","position":%d,"name":"%s","item":"%s"}' % (i+1, plain(n), DOMAIN+u)
      for i,(n,u) in enumerate(items))
    return '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}</script>' % el

def schema_service(name, desc, url):
    name = plain(name); desc = plain(desc).replace('"', "'")
    return '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Service","serviceType":"%s","name":"%s",
"description":"%s","url":"%s","areaServed":{"@type":"City","name":"%s"},
"provider":{"@type":"HVACBusiness","name":"%s","telephone":"%s","url":"%s"}}
</script>''' % (name, name, desc, DOMAIN+url, CITY, plain(SITE_NAME), PHONE_DISPLAY, DOMAIN)

def schema_faq(faqs):
    items = ",".join(
      '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
      % (q.replace('"',"'"), a.replace('"',"'")) for q,a in faqs)
    return '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}</script>' % items

def schema_blogpost(title, desc, url, date):
    t = plain(title).replace('"', "'"); d = plain(desc).replace('"', "'")
    return '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting","headline":"%s","description":"%s",
"image":"%s/assets/img/og-default.png","datePublished":"%s","dateModified":"%s","url":"%s",
"mainEntityOfPage":{"@type":"WebPage","@id":"%s"},
"author":{"@type":"Organization","name":"%s"},
"publisher":{"@type":"Organization","name":"%s","url":"%s","logo":{"@type":"ImageObject","url":"%s/assets/img/favicon.svg"}}}
</script>''' % (t, d, DOMAIN, date, date, DOMAIN+url, DOMAIN+url, plain(SITE_NAME), plain(SITE_NAME), DOMAIN, DOMAIN)

# ------------------------------------------------------------------ SHARED SECTIONS
def crumbs(items):
    parts=[]
    for i,(n,u) in enumerate(items):
        if i: parts.append(icon('chev-right',size=14))
        parts.append(f'<a href="{u}">{n}</a>' if u else f'<span>{n}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">'+"".join(parts)+'</nav>'

def cta_band(title="Ready to Restore Your Home Comfort?",
             text="Whatever your heating or cooling need, our licensed technicians are ready to help, fast. Get your free, no-obligation quote today."):
    return f'''<section class="section">
  <div class="container">
    <div class="cta-band reveal">
      <div class="cta-band__inner">
        <div>
          <h2>{title}</h2>
          <p>{text}</p>
        </div>
        <div style="display:flex;gap:14px;flex-wrap:wrap">
          <a class="btn btn-primary btn-lg" href="/contact/">Get a Free Quote</a>
        </div>
      </div>
    </div>
  </div>
</section>'''

def areas_section():
    chips = "".join(f'<li><a href="/contact/">{icon("pin",size=15)} {a}</a></li>' for a in SERVICE_AREAS)
    return f'''<section class="section bg-soft">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Proudly Local</span>
      <h2>Serving {CITY} &amp; Surrounding Communities</h2>
      <p>We provide fast, reliable HVAC service throughout {CITY} and {COUNTY}. If you don't see your town listed, give us a call, chances are we cover it.</p>
    </div>
    <ul class="areas reveal">{chips}</ul>
  </div>
</section>'''

def write(path_dir, content):
    out = os.path.join(ROOT, path_dir.strip("/"))
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)

def write_root(filename, content):
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(content)

print("build.py loaded, run build_pages() (see build_pages.py)")
