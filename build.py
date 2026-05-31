#!/usr/bin/env python3
import json, os, shutil, sys, subprocess

LIVE_SERVER = 'root@217.154.33.12'
LIVE_ROOT = '/var/www/vhosts/dandsclearances.co.uk/httpdocs'

PROTECTED = [
    'index.html',
    'about-us/index.html',
    'contact/index.html',
    'privacy-policy/index.html',
    'cookie-policy/index.html',
    'terms-and-conditions/index.html',
    'services/index.html',
    'rubbish-removal/index.html',
    'house-clearance/index.html',
    'office-clearance/index.html',
    'garage-clearance/index.html',
    'loft-clearance/index.html',
    'probate-clearance/index.html',
    'hoarder-clearance/index.html',
    'bereavement-clearance/index.html',
    'shed-clearance/index.html',
    'man-with-van/index.html',
    'building-site-rubbish/index.html',
    'commercial-waste-removal/index.html',
    'wheelie-bin-waste-removal/index.html',
    'wait-and-load/index.html',
    'scrap-car-collection/index.html',
    'old-caravan-collection/index.html',
    'old-bike-disposal/index.html',
    'keyholding-service/index.html',
    'house-move/index.html',
    'hotel-clearance/index.html',
    'hazardous-waste-removal/index.html',
    'gutter-cleaning/index.html',
    'free-motorhome-collection/index.html',
    'driveway-cleaning/index.html',
    'domestic-waste-clearance/index.html',
    'complete-house-clean/index.html',
    'care-home-clearance/index.html',
    'bulky-item-disposal/index.html',
    'black-bag-disposal/index.html',
    'bin-cleaning/index.html',
    'thank-you/index.html',
]

def fetch_from_live(rel):
    dest = os.path.join('build', rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    result = subprocess.run(
        ['ssh', LIVE_SERVER, f'cat {LIVE_ROOT}/{rel}'],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        with open(dest, 'w') as f:
            f.write(result.stdout)
        print(f'  Fetched from live: {rel}')
        return True
    else:
        print(f'  WARNING: could not fetch {rel} from live server')
        return False

def build():
    with open('data/pages.json') as f: pages = json.load(f)
    with open('theme/base.html') as f: template = f.read()

    # Ensure all protected files exist in build/ — pull from live if missing
    for rel in PROTECTED:
        src = os.path.join('build', rel)
        if not os.path.exists(src):
            print(f'  Missing protected file: {rel} — fetching from live')
            fetch_from_live(rel)

    # Backup protected files
    backups = {}
    for rel in PROTECTED:
        src = os.path.join('build', rel)
        if os.path.exists(src):
            with open(src) as f: backups[rel] = f.read()
            print(f'  Backed up: {rel}')

    if os.path.exists('build'): shutil.rmtree('build')
    os.makedirs('build')

    # Restore protected files
    for rel, content in backups.items():
        dest = os.path.join('build', rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w') as f: f.write(content)
        print(f'  Restored: {rel}')

    built = 0
    skipped = 0
    for page in pages:
        slug = page['slug']
        body = page.get('body_content', '').strip()
        rel = 'index.html' if slug == 'index' else f'{slug}/index.html'
        if rel in backups and not body:
            skipped += 1
            continue
        html = template.replace('{{ content }}', body)
        dest = os.path.join('build', rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w') as f: f.write(html)
        built += 1

    if os.path.exists('assets'):
        shutil.copytree('assets', 'build/assets', dirs_exist_ok=True)

    print(f'Built: {built} | Skipped (protected): {skipped} | Total: {len(pages)}')

if __name__ == '__main__': build()
