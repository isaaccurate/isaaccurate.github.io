#!/usr/bin/env python3
"""Check generated local links and assets for root or subpath builds."""
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import yaml

root = Path(sys.argv[1] if len(sys.argv) > 1 else '_site')
base = yaml.safe_load(Path('_config.yml').read_text()).get('baseurl', '').rstrip('/')
if len(sys.argv) > 2:
    base = sys.argv[2].rstrip('/')
errors = []
class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.source = source
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key not in ('href', 'src') or not value:
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            if path.startswith('/'):
                if base and not (path == base or path.startswith(base + '/')):
                    errors.append(f'{self.source}: missing baseurl in {value}')
                    continue
                path = path[len(base):] if base else path
                target = root / path.lstrip('/')
            else:
                target = self.source.parent / path
            if not target.exists() and not (target / 'index.html').exists():
                errors.append(f'{self.source}: broken {value}')
for source in root.rglob('*.html'):
    Links(source).feed(source.read_text())
for required in ['index.html', 'projects/index.html', 'academics/index.html', 'knowledge/index.html', 'contact/index.html', 'feed.xml', 'knowledge/feed.xml', 'sitemap.xml', '404.html']:
    if not (root / required).is_file():
        errors.append(f'Missing output: {required}')
if errors:
    sys.exit('\n'.join(errors))
print('Generated pages, internal links, assets, sitemap, and both feeds passed.')
