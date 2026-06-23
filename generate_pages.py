#!/usr/bin/env python3
"""
generate_pages.py — D&S Clearances
Populates body_content in data/pages.json for all location service pages.
Does NOT write to build/ — run build.py after this to generate HTML.
Markup matches ds-styles.css exactly:
  - trust-list li > span (emoji) + text
  - faq-item > span.text + p.faq-answer
"""
import json
import sys

SW_LOCATIONS = {
    'truro','st-ives','falmouth','penzance','newquay','bude','padstow','helston',
    'redruth','camborne','hayle','st-austell','bodmin','launceston','liskeard',
    'saltash','torpoint','looe','polperro','mylor','perranporth','st-agatha',
    'st-agnes','st-blazey','st-columb-major','st-day','st-dennis','st-ewe',
    'st-germans','st-just','st-keverne','st-mawes','st-merryn','st-minver',
    'st-neot','st-newlyn-east','st-stephen','st-teath','st-veep',
    'plymouth','exeter','barnstaple','torquay','paignton','exmouth','newton-abbot',
    'tiverton','teignmouth','sidmouth','brixham','dawlish','crediton',
    'ottery-st-mary','honiton','axminster','seaton','cullompton','kingsbridge',
    'ivybridge','tavistock','okehampton','holsworthy','great-torrington',
    'south-molton','ilfracombe','lynmouth','lydford'
}

CORNWALL = {
    'truro','st-ives','falmouth','penzance','newquay','bude','padstow','helston',
    'redruth','camborne','hayle','st-austell','bodmin','launceston','liskeard',
    'saltash','torpoint','looe','polperro','mylor','perranporth','st-agatha',
    'st-agnes','st-blazey','st-columb-major','st-day','st-dennis','st-ewe',
    'st-germans','st-just','st-keverne','st-mawes','st-merryn','st-minver',
    'st-neot','st-newlyn-east','st-stephen','st-teath','st-veep'
}

def location_slug_from_page(page):
    service_slug = page['service_name'].lower().replace(' ', '-')
    slug = page['slug']
    if slug.startswith(service_slug + '-'):
        return slug[len(service_slug) + 1:]
    return None

def is_sw(loc_slug):
    return loc_slug in SW_LOCATIONS

def get_county(loc_slug):
    if loc_slug in CORNWALL:
        return 'Cornwall'
    return 'Devon'

def build_sibling_links(current_slug, location, all_pages, sw):
    siblings = [
        p for p in all_pages
        if p.get('location') == location
        and p.get('service_name')
        and p['slug'] != current_slug
        and p.get("service_name")
    ]
    links = []
    for s in siblings:
        service = s['service_name']
        slug = s['slug']
        if sw:
            links.append(f'      <div class="service-card"><h3>{service}</h3><a href="/{slug}/" class="btn-sm">View Service</a></div>')
        else:
            links.append(f'      <a href="/{slug}/" style="display:block;background:#fff;color:#0a4b78;border:2px solid #b8960c;padding:12px 16px;font-weight:700;border-radius:6px;text-decoration:none;">{service}</a>')
    return '\n'.join(links)

def build_sw_body(service, location, loc_slug, video_id, sibling_links):
    county = get_county(loc_slug)
    return f"""<section class="hero">
  <img src="/assets/images/Darren-with-DS-Clearance-Van.webp" alt="{service} in {location}" class="hero-img">
  <div class="hero-text">
    <h1>{service} in {location} — Based in {location}, D&S Clearances</h1>
    <h2>Family-run clearance business. Nowhere too far.</h2>
  </div>
</section>

<div class="cta-banner">
  <h2>⚡ {service} in {location}? Darren's on It.</h2>
  <p>D&S Clearances know {county} inside out. A family-run business serving {location} and across {county} for over 15 years. Send photos on WhatsApp and get a fixed price back fast — no call centres, no middlemen, just a local team you can trust.</p>
  <div class="cta-buttons">
    <a href="https://wa.me/447759375790" class="btn btn-whatsapp">WhatsApp 07759 375790 — Send images for a quick quote</a>
    <a href="tel:07759375790" class="btn btn-call">Call Now – 07759 375790</a>
    <a href="/contact/" class="btn btn-cta">Book Online</a>
  </div>
  <div style="display:inline-block;margin-top:15px;background:#006400;color:#ffffff;font-weight:bold;font-size:0.95em;padding:10px 22px;border-radius:8px;">💳 We now accept card payments — easier and more convenient for our customers.</div>
</div>

<div class="trust-banner">
  <h2>🏆 {location}'s Trusted {service} Team</h2>
  <ul class="trust-list">
    <li><span>✅</span> 15+ Years of {county} Clearances</li>
    <li><span>📋</span> Environment Agency Licensed — Waste Transfer Notes on Every Job</li>
    <li><span>🛡️</span> Fully Insured — Public Liability Cover in Place</li>
    <li><span>♻️</span> Up to 90% Recycled or Donated — Not Landfill</li>
    <li><span>⚡</span> Same-Day Availability Across {county}</li>
  </ul>
</div>

<div class="ds-scroll-gallery">
  <div class="ds-track">
    <img src="/assets/images/DS-Clearances-1-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-23-226x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-20-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-21-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-15-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-16-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-19-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-18-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-17-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-22-300x279.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-1-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-23-226x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-20-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-21-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-15-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-16-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-19-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-18-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-17-225x300.webp" alt="D&S Clearances {location}">
    <img src="/assets/images/DS-Clearances-22-300x279.webp" alt="D&S Clearances {location}">
  </div>
</div>

<div class="ds-grid-wrapper">
  <div class="faq-column">
    <div class="faq-section">
      <h2>{service} in {location} — Your Questions</h2>
      <div class="faq-item">
        <span class="text">How quickly can you get to {location}?</span>
        <p class="faq-answer">We offer same-day and next-day availability across {county}. Call or WhatsApp Darren for the fastest response.</p>
      </div>
      <div class="faq-item">
        <span class="text">Is {service} in {location} fully insured?</span>
        <p class="faq-answer">Yes — fully insured with public liability cover and Environment Agency licensed. We issue waste transfer notes on every job.</p>
      </div>
      <div class="faq-item">
        <span class="text">How do I get a quote for {location}?</span>
        <p class="faq-answer">Send Darren photos on WhatsApp and get a fixed price back fast. No call centres, no hidden fees.</p>
      </div>
      <div class="faq-item">
        <span class="text">Do you cover all of {county} including {location}?</span>
        <p class="faq-answer">Yes — we cover all of {county} including {location} and surrounding areas. Nowhere too far.</p>
      </div>
    </div>
  </div>
  <div class="testimonial-column">
    <div class="testimonial-section">
      <h2>What Makes D&S Different in {location}</h2>
      <div class="why-choose-card">
        <div class="why-point-title">📞 Direct Line to Darren</div>
        <div class="why-point-text">You speak to Darren directly — not a call centre. Fast, honest quotes every time.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">♻️ Up to 90% Recycled</div>
        <div class="why-point-text">We donate and recycle wherever possible. Waste transfer notes issued on every job.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">⚡ Same-Day Available</div>
        <div class="why-point-text">Need it done today? We take on same-day jobs across {county} including {location}.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">🛡️ Fully Insured</div>
        <div class="why-point-text">Public liability insurance in place. You're covered on every job we do.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">📋 Licensed Waste Carrier</div>
        <div class="why-point-text">Environment Agency licensed. We never fly-tip. Your waste is handled legally and responsibly.</div>
      </div>
    </div>
  </div>
</div>

<div class="ds-grid-wrapper">
  <div class="faq-column">
    <div class="faq-section">
      <h2>Booking D&S in {location}</h2>
      <div class="faq-item">
        <span class="text">Step 1 — Send Photos</span>
        <p class="faq-answer">WhatsApp Darren photos of what needs clearing. He'll come back with a fixed price fast.</p>
      </div>
      <div class="faq-item">
        <span class="text">Step 2 — Confirm the Job</span>
        <p class="faq-answer">Agree the price and confirm a date. Same-day and next-day slots available across {county}.</p>
      </div>
      <div class="faq-item">
        <span class="text">Step 3 — We Clear, You Relax</span>
        <p class="faq-answer">Darren and the team turn up, clear everything, and leave your property spotless.</p>
      </div>
    </div>
  </div>
  <div class="testimonial-column">
    <div class="testimonial-section">
      <h2>D&S and {county}'s Environment</h2>
      <div class="why-choose-card">
        <div class="why-point-title">♻️ {county} Charities Benefit First</div>
        <div class="why-point-text">Usable items go to local {county} charities and community groups before anything else.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">🌱 Minimal Landfill</div>
        <div class="why-point-text">Up to 90% of what we collect is recycled or donated. We take our environmental responsibility seriously.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">📋 Full Paperwork</div>
        <div class="why-point-text">Waste transfer notes issued on every job — your legal protection and ours.</div>
      </div>
    </div>
  </div>
</div>

<section class="video-section">
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;">
    <iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://www.youtube.com/embed/{video_id}" title="{service} in {location} — D&S Clearances" frameborder="0" allowfullscreen></iframe>
  </div>
</section>

<section id="contact">
  <div class="other-services-section">
    <h2>Other Services in {location}</h2>
    <p>D&S Clearances offer a full range of clearance services in {location}</p>
    <div class="services-grid-container">
{sibling_links}
    </div>
  </div>
  <div style="text-align:center;padding:40px 20px;">
    <h2>Book {service} in {location}</h2>
    <p>Fixed price. Local team. Nowhere too far. Call or WhatsApp Darren now.</p>
    <div class="cta-buttons">
      <a href="https://wa.me/447759375790" class="btn btn-whatsapp">WhatsApp Darren</a>
      <a href="tel:07759375790" class="btn btn-call">📞 07759 375790</a>
    </div>
  </div>
</section>"""


def build_uk_body(service, location, video_id, sibling_links):
    return f"""<section class="hero">
  <img src="/assets/images/Darren-with-DS-Clearance-Van.webp" alt="{service} in {location}" class="hero-img">
  <div class="hero-text">
    <h1>{service} in {location} — Based Locally, D&S Clearances</h1>
    <h2>Family-run clearance business. Nowhere too far. {location} covered.</h2>
  </div>
</section>

<div class="cta-banner">
  <h2>⚡ {service} in {location}? Call Darren.</h2>
  <p>Darren and the D&S team turn up, get the job done, and leave your property clear. Licensed, insured, and committed to keeping waste out of landfill. Send Darren a WhatsApp with photos and he'll price it up fast.</p>
  <div class="cta-buttons">
    <a href="https://wa.me/447759375790" class="btn btn-whatsapp">WhatsApp 07759 375790 — Send images for a quick quote</a>
    <a href="tel:07759375790" class="btn btn-call">Call Now – 07759 375790</a>
    <a href="/contact/" class="btn btn-cta">Book Online</a>
  </div>
  <div style="display:inline-block;margin-top:15px;background:#006400;color:#ffffff;font-weight:bold;font-size:0.95em;padding:10px 22px;border-radius:8px;">💳 We now accept card payments — easier and more convenient for our customers.</div>
</div>

<div class="trust-banner">
  <h2>🏆 Why {location} Chooses D&S Clearances</h2>
  <ul class="trust-list">
    <li><span>✅</span> 15+ Years Clearing Properties Across {location}</li>
    <li><span>📋</span> Environment Agency Licensed — Waste Transfer Notes Issued</li>
    <li><span>🛡️</span> Fully Insured with Public Liability Cover</li>
    <li><span>♻️</span> Up to 90% of Waste Recycled or Donated</li>
    <li><span>⚡</span> Same-Day Jobs Taken On</li>
  </ul>
</div>

<div class="ds-grid-wrapper">
  <div class="faq-column">
    <div class="faq-section">
      <h2>{service} — {location} Questions Answered</h2>
      <div class="faq-item">
        <span class="text">Do you cover {location}?</span>
        <p class="faq-answer">Yes — D&S Clearances cover {location} and the surrounding area. Call or WhatsApp Darren to confirm availability and get a fixed price.</p>
      </div>
      <div class="faq-item">
        <span class="text">Is {service} in {location} fully insured?</span>
        <p class="faq-answer">Yes — fully insured with public liability cover and Environment Agency licensed. We issue waste transfer notes on every job.</p>
      </div>
      <div class="faq-item">
        <span class="text">How do I get a quote for {location}?</span>
        <p class="faq-answer">Send Darren photos on WhatsApp and get a fixed price back fast. No call centres, no hidden fees.</p>
      </div>
      <div class="faq-item">
        <span class="text">How quickly can you get to {location}?</span>
        <p class="faq-answer">Call or WhatsApp Darren directly to check availability. Same-day and next-day slots are often available.</p>
      </div>
    </div>
  </div>
  <div class="testimonial-column">
    <div class="testimonial-section">
      <h2>Darren's Commitment to {location}</h2>
      <div class="why-choose-card">
        <div class="why-point-title">📞 Direct Line to Darren</div>
        <div class="why-point-text">You speak to Darren directly — not a call centre. Fast, honest quotes every time.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">♻️ Up to 90% Recycled</div>
        <div class="why-point-text">We donate and recycle wherever possible. Waste transfer notes issued on every job.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">⚡ Same-Day Available</div>
        <div class="why-point-text">Need it done today? Call Darren to check same-day availability in {location}.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">🛡️ Fully Insured</div>
        <div class="why-point-text">Public liability insurance in place. You're covered on every job we do.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">📋 Licensed Waste Carrier</div>
        <div class="why-point-text">Environment Agency licensed. We never fly-tip. Your waste is handled legally and responsibly.</div>
      </div>
    </div>
  </div>
</div>

<div class="ds-grid-wrapper">
  <div class="faq-column">
    <div class="faq-section">
      <h2>How It Works with D&S</h2>
      <div class="faq-item">
        <span class="text">Step 1 — Send Photos</span>
        <p class="faq-answer">WhatsApp Darren photos of what needs clearing. He'll come back with a fixed price fast.</p>
      </div>
      <div class="faq-item">
        <span class="text">Step 2 — Confirm the Job</span>
        <p class="faq-answer">Agree the price and confirm a date. Same-day and next-day slots often available.</p>
      </div>
      <div class="faq-item">
        <span class="text">Step 3 — We Clear, You Relax</span>
        <p class="faq-answer">Darren and the team turn up, clear everything, and leave your property spotless.</p>
      </div>
    </div>
  </div>
  <div class="testimonial-column">
    <div class="testimonial-section">
      <h2>D&S and the Environment</h2>
      <div class="why-choose-card">
        <div class="why-point-title">♻️ Charity and Reuse First</div>
        <div class="why-point-text">Usable items go to charities and community groups before anything else.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">🌱 Minimal Landfill</div>
        <div class="why-point-text">Up to 90% of what we collect is recycled or donated. We take our environmental responsibility seriously.</div>
      </div>
      <div class="why-choose-card">
        <div class="why-point-title">📋 Full Paperwork</div>
        <div class="why-point-text">Waste transfer notes issued on every job — your legal protection and ours.</div>
      </div>
    </div>
  </div>
</div>

<section class="video-section">
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;">
    <iframe style="position:absolute;top:0;left:0;width:100%;height:100%;" src="https://www.youtube.com/embed/{video_id}" title="{service} in {location} — D&S Clearances" frameborder="0" allowfullscreen></iframe>
  </div>
</section>

<section id="contact">
  <div class="other-services-section">
    <h2>Other Services in {location}</h2>
    <p>D&S Clearances offer a range of services in {location} and the surrounding area.</p>
    <div class="services-grid-container">
{sibling_links}
    </div>
  </div>
  <div style="text-align:center;padding:40px 20px;">
    <h2>Ready to Book {service} in {location}?</h2>
    <p>Call or WhatsApp Darren now. Fixed price. No fuss. Job done.</p>
    <div class="cta-buttons">
      <a href="https://wa.me/447759375790" class="btn btn-whatsapp">WhatsApp Darren</a>
      <a href="tel:07759375790" class="btn btn-call">📞 07759 375790</a>
    </div>
  </div>
</section>"""


def main():
    pages_path = 'data/pages.json'
    with open(pages_path) as f:
        pages = json.load(f)

    dry_run = '--dry-run' in sys.argv
    limit = None
    for arg in sys.argv:
        if arg.startswith('--limit='):
            limit = int(arg.split('=')[1])

    DEFAULT_VIDEOS = ['C_l9ltdR3Qs', 'cz_h_y2YiQI', 'c1rcSIiXhsQ']
    target_pages = [
        p for p in pages
        if p.get('service_name')
        and p.get('location')
        and p.get('slug', '').count('-') >= 2
    ]
    for p in target_pages:
        if not p.get('video_id'):
            p['video_id'] = DEFAULT_VIDEOS[hash(p['slug']) % 3]

    if limit:
        target_pages = target_pages[:limit]

    populated = 0
    skipped = 0

    for page in target_pages:
        slug = page['slug']
        service = page['service_name']
        location = page['location']
        video_id = page['video_id']
        loc_slug = location_slug_from_page(page)

        if not loc_slug:
            skipped += 1
            continue

        sw = is_sw(loc_slug)
        sibling_links = build_sibling_links(slug, location, pages, sw)

        if sw:
            body = build_sw_body(service, location, loc_slug, video_id, sibling_links)
        else:
            body = build_uk_body(service, location, video_id, sibling_links)

        if dry_run:
            print(f'[DRY RUN] {slug} ({"SW" if sw else "UK"}) — {len(body)} chars — {len(sibling_links.splitlines())} sibling links')
        else:
            page['body_content'] = body
        populated += 1

    if not dry_run:
        with open(pages_path, 'w') as f:
            json.dump(pages, f, indent=2)
        print(f'Written to {pages_path}')

    print(f'Populated: {populated} | Skipped: {skipped} | Total targeted: {len(target_pages)}')


if __name__ == '__main__':
    main()
