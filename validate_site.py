"""Check published routes, media references and structural accessibility."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import re

root = Path(__file__).parent / 'dist'
errors = []
class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes = []
        self.stack = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        node = dict(attrs)
        node['_tag'] = tag
        node['_text'] = ''
        self.nodes.append(node)
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append(node)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i]['_tag'] == tag:
                self.stack = self.stack[:i]
                return
    def handle_data(self, value):
        for node in self.stack:
            node['_text'] += value
pages = {p.name: Document(p.read_text()) for p in root.glob('*.html')}
for name, soup in pages.items():
    ids = [n['id'] for n in soup.nodes if 'id' in n]
    if len(ids) != len(set(ids)): errors.append(f'{name}: duplicate IDs')
    if len([n for n in soup.nodes if n['_tag'] == 'h1']) != 1: errors.append(f'{name}: expected one h1')
    for node in soup.nodes:
        for key in ('href', 'src', 'poster', 'data-src'):
            value = node.get(key, '')
            if not value or value.startswith(('http:', 'https:', 'data:', 'mailto:', 'tel:')): continue
            url = urlsplit(value)
            target = root / unquote(url.path) if url.path else root / name
            if not target.exists(): errors.append(f'{name}: missing {value}')
            if url.fragment and target.suffix == '.html':
                target_soup = pages.get(target.name)
                if target_soup and not any(n.get('id') == url.fragment for n in target_soup.nodes): errors.append(f'{name}: missing anchor {value}')
        if node['_tag'] == 'img':
            if 'alt' not in node: errors.append(f'{name}: missing image alt')
            if not node.get('width') or not node.get('height'): errors.append(f'{name}: missing image dimensions')
            for item in node.get('srcset', '').split(','):
                if item.strip() and not (root / item.strip().split()[0]).exists(): errors.append(f'{name}: missing srcset file')
        if node['_tag'] == 'button' and not (node['_text'].strip() or node.get('aria-label')): errors.append(f'{name}: unlabeled button')
    if name.startswith('case-') and any('hidden' in n for n in soup.nodes): errors.append(f'{name}: case content hidden')
for css in root.glob('*.css'):
    for ref in re.findall(r'url\([\"\']?([^\)\"\']+)', css.read_text()):
        if ref.startswith('./') and not (root / ref).exists(): errors.append(f'{css.name}: missing {ref}')
home = pages['index.html']
order = [a.get('id') for a in home.nodes if a['_tag'] == 'article' and 'case' in a.get('class', '').split()]
if order != ['camfire', 'minimalance', 'remic', 'xipster']: errors.append('Wrong case order')
if any(n['_tag'] == 'video' and ('autoplay' in n or n.get('preload') == 'auto') for n in home.nodes): errors.append('Unexpected eager video')
if any(n['_tag'] == 'video' and 'data-hero-video' in n and 'loop' in n for n in home.nodes): errors.append('Hero must play once')
if '150%' in ''.join(p.read_text() for p in root.glob('*.html')): errors.append('Ambiguous 150% claim remains')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; links, anchors, assets, image dimensions, controls and project order checked.')
