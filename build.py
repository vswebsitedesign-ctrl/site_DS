#!/usr/bin/env python3
import json, os, shutil
from datetime import date, datetime

DOMAIN = 'https://dandsclearances.co.uk'

def snapshot_pages():
    src = 'data/pages.json'
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    dest = f'data/pages.json.bak.{ts}'
    shutil.copy2(src, dest)
    print(f'Snapshot: {dest}')

def build():
    snapshot_pages()
    with open('data/pages.json') as f: pages = json.load(f)
    with open('theme/base.html') as f: template = f.read()
    if os.path.exists('build'): shutil.rmtree('build')
    os.makedirs('build')
    built = 0
    skipped = 0
    built_slugs = []
    for page in pages:
        slug = page['slug']
        body = page.get('body_content', '').strip()
        if not body:
            skipped += 1
            continue
        rel = 'index.html' if slug == 'index' else f'{slug}/index.html'
        html = template.replace('{{ content }}', body)
        if not page.get('description') and page.get('service_name') and page.get('location'):
            page['description'] = f"{page['service_name']} {page['location']} - Based Locally - Free Quotes from Darren"
        if not page.get('description') and page.get('service_name') and page.get('location'):
            page['description'] = f"{page['service_name']} {page['location']} - Based Locally - Free Quotes from Darren"
        if page.get('title'):
            html = html.replace('<title>D&S Clearances | Nowhere too far to clear your property</title>', f'<title>{page["title"]}</title>')
        if page.get('description'):
            html = html.replace('content="D&S Clearances — professional house clearance and rubbish removal across Cornwall, Devon and the UK. Nowhere too far. Free quotes from Darren."', f'content="{page["description"]}"')
        dest = os.path.join('build', rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w') as f: f.write(html)
        built += 1
        built_slugs.append(slug)
    if os.path.exists('php'):
        shutil.copy('php/send.php', 'build/send.php')
    if os.path.exists('assets'):
        shutil.copytree('assets', 'build/assets', dirs_exist_ok=True)
    today = str(date.today())
    urls = []
    built_slugs = [s for s in built_slugs if s != '404.html']
    for slug in built_slugs:
        url = DOMAIN + '/' if slug == 'index' else f'{DOMAIN}/{slug}/'
        urls.append(f'  <url><loc>{url}</loc><lastmod>{today}</lastmod></url>')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += '\n'.join(urls)
    sitemap += '\n</urlset>'
    with open('build/sitemap.xml', 'w') as f: f.write(sitemap)
    robots = f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n'
    with open('build/robots.txt', 'w') as f: f.write(robots)
    print(f'Built: {built} | Skipped (empty body_content): {skipped} | Total: {len(pages)}')
    print(f'Sitemap: {len(built_slugs)} URLs written to build/sitemap.xml')
    print(f'Robots: build/robots.txt written')

if __name__ == '__main__': build()
