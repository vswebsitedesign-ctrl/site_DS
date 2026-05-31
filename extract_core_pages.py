import json, subprocess, re, os

LIVE = 'root@217.154.33.12'
LIVE_ROOT = '/var/www/vhosts/dandsclearances.co.uk/httpdocs'
PAGES_JSON = '/home/chubert/omni-builder/sites/site_DS/data/pages.json'

MISSING = [
    'index','services','rubbish-removal','house-clearance','office-clearance',
    'garage-clearance','wheelie-bin-waste-removal','wait-and-load','scrap-car-collection',
    'old-caravan-collection','old-bike-disposal','keyholding-service','house-move',
    'hotel-clearance','hazardous-waste-removal','gutter-cleaning','free-motorhome-collection',
    'driveway-cleaning','domestic-waste-clearance','complete-house-clean','care-home-clearance',
    'bulky-item-disposal','black-bag-disposal','bin-cleaning'
]

TITLES = {
    'index': 'D&S Clearances | Nowhere too far to clear your property',
    'services': 'Our Services | D&S Clearances',
    'rubbish-removal': 'Rubbish Removal | D&S Clearances',
    'house-clearance': 'House Clearance | D&S Clearances',
    'office-clearance': 'Office Clearance | D&S Clearances',
    'garage-clearance': 'Garage Clearance | D&S Clearances',
    'wheelie-bin-waste-removal': 'Wheelie Bin Waste Removal | D&S Clearances',
    'wait-and-load': 'Wait and Load | D&S Clearances',
    'scrap-car-collection': 'Scrap Car Collection | D&S Clearances',
    'old-caravan-collection': 'Old Caravan Collection | D&S Clearances',
    'old-bike-disposal': 'Old Bike Disposal | D&S Clearances',
    'keyholding-service': 'Keyholding Service | D&S Clearances',
    'house-move': 'House Move | D&S Clearances',
    'hotel-clearance': 'Hotel Clearance | D&S Clearances',
    'hazardous-waste-removal': 'Hazardous Waste Removal | D&S Clearances',
    'gutter-cleaning': 'Gutter Cleaning | D&S Clearances',
    'free-motorhome-collection': 'Free Motorhome Collection | D&S Clearances',
    'driveway-cleaning': 'Driveway Cleaning | D&S Clearances',
    'domestic-waste-clearance': 'Domestic Waste Clearance | D&S Clearances',
    'complete-house-clean': 'Complete House Clean | D&S Clearances',
    'care-home-clearance': 'Care Home Clearance | D&S Clearances',
    'bulky-item-disposal': 'Bulky Item Disposal | D&S Clearances',
    'black-bag-disposal': 'Black Bag Disposal | D&S Clearances',
    'bin-cleaning': 'Bin Cleaning | D&S Clearances',
}

with open(PAGES_JSON) as f:
    pages = json.load(f)

slug_index = {p.get('slug','').strip('/'): i for i, p in enumerate(pages)}

for slug in MISSING:
    live_path = f'{LIVE_ROOT}/index.html' if slug == 'index' else f'{LIVE_ROOT}/{slug}/index.html'
    print(f'Fetching: {slug} ... ', end='', flush=True)
    result = subprocess.run(['ssh', LIVE, f'cat {live_path}'], capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print(f'FAILED — not found on live server')
        continue
    html = result.stdout
    match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if not match:
        print(f'FAILED — no <main> tag found')
        continue
    body = match.group(1).strip()
    if slug in slug_index:
        pages[slug_index[slug]]['body_content'] = body
        print(f'UPDATED in pages.json ({len(body)} chars)')
    else:
        pages.append({
            'slug': slug,
            'title': TITLES.get(slug, slug),
            'body_content': body,
            'description': ''
        })
        print(f'ADDED to pages.json ({len(body)} chars)')

with open(PAGES_JSON, 'w') as f:
    json.dump(pages, f, ensure_ascii=False)

print('\nAll done. pages.json updated.')
