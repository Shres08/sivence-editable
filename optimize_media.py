"""Create responsive delivery sizes from existing, approved site artwork."""
from pathlib import Path
from PIL import Image
import re, json

root = Path(__file__).parent / 'dist'
names = set()
for page in root.glob('*.html'):
    names.update(re.findall(r'<img[^>]*src="\./assets/([^"]+)"', page.read_text()))
manifest = {}
for name in sorted(names):
    path = root / 'assets' / name
    with Image.open(path) as img:
        w, h = img.size
        info = {'width': w, 'height': h, 'variants': []}
        if name == 'sivence-logo-ink.png':
            image = img.copy()
            image.thumbnail((440, 200))
            image.save(root / 'assets' / 'sivence-header.webp', 'WEBP', quality=90)
            info['replacement'] = 'sivence-header.webp'
        elif w > 1000:
            for size in (640, 960):
                target = path.with_name(path.stem + '-' + str(size) + '.webp')
                image = img.copy()
                image.thumbnail((size, 5000))
                image.save(target, 'WEBP', quality=84)
                info['variants'].append({'file': target.name, 'width': image.width})
        manifest[name] = info
print(json.dumps(manifest))
