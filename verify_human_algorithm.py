"""Check the bounded homepage change against the retained live-site baseline."""
from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).parent
class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(); self.sections=[]; self.text=[]; self.skip=0
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag in ('script','style'): self.skip+=1
        if tag=='section': self.sections.append(attrs.get('id', attrs.get('class')))
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip-=1
    def handle_data(self, text):
        if not self.skip and text.strip(): self.text.append(text.strip())

before=Page((ROOT/'qa/homepage-before.html').read_text())
source=(ROOT/'dist/index.html').read_text()
after=Page(source)
assert before.sections==after.sections, 'Homepage section order or spacing wrapper changed'
assert all(text in after.text for text in before.text), 'Existing homepage copy removed'
assert source.count('class="human-fragment"')==9
hero=source[source.index('<section class="spatial-hero"'):source.index('<!-- Selected real-world')]
signals=source[source.index('<section class="signal-story"'):source.index('<section class="lab-spotlight')]
assert 'human-stage' in hero and '<iframe' not in hero
assert 'data-src="/lab/spatial-studio/?hero"' in signals
assert 'data-signal-pulse' in signals
assert 'aria-pressed="false"' in hero and 'data-human-sound' in hero
assert '/assets/vendor/three.min.js' not in source
assert '/assets/vendor/RoomEnvironment.js' not in source
assert (ROOT/'dist/assets/human-algorithm.webp').stat().st_size < 150_000
js=(ROOT/'dist/assets/human-algorithm.js').read_text()
assert 'prefers-reduced-motion' in js and 'visibilitychange' in js
assert 'touchWasActive' in js and 'AudioContext' in js
assert (ROOT/'homepage.html').read_text()==source
print('PASS: preserved homepage copy and section order; nine fragments; lazy relocated sculpture; silent sound default; reduced-motion support; optimized artwork; authoring template synchronized.')
