from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json, subprocess, re
ROOT=Path(__file__).parent
OUT=ROOT/'dist'
ROUTES=json.loads((ROOT/'routes.json').read_text())
errors=[]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.tags=[];self.ids=set();self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a));self.h1+=tag=='h1'
  if 'id' in a:self.ids.add(a['id'])
parsed={}
for f in OUT.rglob('*.html'):
 p=Page();p.feed(f.read_text());parsed[f]=p
 if p.h1!=1:errors.append(f'{f.relative_to(OUT)} has {p.h1} H1s')
 for tag,a in p.tags:
  if tag=='img' and a.get('src') and (not a.get('alt') or not a.get('width') or not a.get('height')):errors.append(f'{f}: image lacks alt or dimensions')
  for key in ['href','src','poster']:
   value=a.get(key)
   if not value:continue
   url=urlparse(value)
   if url.scheme or value.startswith('//'):continue
   if not url.path:
    if url.fragment and url.fragment not in p.ids:errors.append(f'{f}: missing fragment {value}')
    continue
   target=OUT/unquote(url.path).lstrip('/') if url.path.startswith('/') else f.parent/unquote(url.path)
   if target.is_dir():target=target/'index.html'
   if not target.exists():errors.append(f'{f.relative_to(OUT)} broken {key}: {value}')
 for tag,a in p.tags:
  if tag=='script' and a.get('type')=='application/ld+json':pass
for route,data in ROUTES.items():
 f=OUT/data['file'];p=parsed[f];html=f.read_text()
 if f'<title>{data["title"].replace("&","&amp;")}</title>' not in html:errors.append(f'{route}: title mismatch')
 if not any(t=='meta' and a.get('name')=='description' and a.get('content') for t,a in p.tags):errors.append(f'{route}: missing description')
 if not any(t=='link' and a.get('rel')=='canonical' and a.get('href')=='https://sivencestudio.com'+route for t,a in p.tags):errors.append(f'{route}: invalid canonical')
 if route!='/lab/spatial-studio/' and not any(t=='link' and a.get('href')=='/ambient.css' for t,a in p.tags):errors.append(f'{route}: missing artwork lighting stylesheet')
 if route!='/lab/spatial-studio/' and not any(t=='script' and a.get('src')=='/ambient.js' for t,a in p.tags):errors.append(f'{route}: missing artwork lighting interaction')
 if route!='/lab/spatial-studio/' and not any(t=='body' and a.get('data-ambient') for t,a in p.tags):errors.append(f'{route}: missing page lighting family')
 for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html):json.loads(block)
 for forbidden in ['[Insert','lorem ipsum','Sreshta Bhatt','RevOps','$2.7M','$800K','ROI +27%','150% above target']:
  if forbidden in html:errors.append(f'{route}: stale or unsupported {forbidden}')
original_assets=subprocess.check_output(['git','ls-tree','-r','--name-only','HEAD','dist/assets'],cwd=ROOT,text=True).splitlines()
retired_sound_assets = {'dist/assets/motion-sound.css','dist/assets/motion-sound.js','dist/assets/motion-score.wav'}
for asset in retired_sound_assets:
 if (ROOT/asset).exists():errors.append(f'Retired sound asset still present: {asset}')
for asset in original_assets:
 if asset in retired_sound_assets:continue
 if asset.endswith('Sreshta-Joshi-Resume.pdf'):continue
 if asset.endswith('remic-campaign-dashboard-2025.png'):continue
 if asset.endswith(('titanfile-plan-01.webp','titanfile-plan-11.webp','titanfile-plan-12.webp')):continue
 if not (ROOT/asset).exists():errors.append(f'Missing original asset: {asset}')
if (OUT/'assets/remic-campaign-dashboard-2025.png').exists():errors.append('Removed REMIC campaign dashboard is still present')
for video in (OUT/'assets').glob('*.mp4'):
 audio=subprocess.check_output(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0',str(video)],text=True)
 if audio.strip():errors.append(f'Film contains audio: {video.name}')
 result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(video)],capture_output=True,text=True)
 if result.returncode or not result.stdout.strip() or float(result.stdout)<1:errors.append(f'Invalid video: {video.name}')
assert len(ROUTES)==30 and '/lab/spatial-studio/' in ROUTES
assert '/work/nett-technologies/' in ROUTES and '/work/camfire/' in ROUTES and '/thinking/the-sivence-method/' in ROUTES
assert '/lab/paintings/' in ROUTES
assert '/work/titanfile/' in ROUTES and '/lab/titanfile/' not in ROUTES
assert '/work/incuse/' in ROUTES
work_html=(OUT/'work/index.html').read_text()
assert work_html.count('data-case-choice=')==10 and 'href="/work/titanfile/"' in work_html
assert 'TitanFile' not in (OUT/'lab/index.html').read_text()
assert 'titanfile-plan-02.webp' in (OUT/'work/titanfile/index.html').read_text()
assert 'titanfile-plan-10.webp' in (OUT/'work/titanfile/index.html').read_text()
assert 'url=/work/titanfile/' in (OUT/'lab/titanfile/index.html').read_text()
contact_html=(OUT/'contact/index.html').read_text()
assert 'data-contact-form' not in contact_html and 'Open email draft' not in contact_html
assert 'Request résumé' not in contact_html and f'href="mailto:joshisreshta@gmail.com"' in contact_html
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(ROUTES)} canonical pages, {len(parsed)} HTML files, navigation/assets/metadata, {len(original_assets)} original assets, all videos and approved metrics.')
