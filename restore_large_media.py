"""Restore the large original catalogue from lossless repository parts."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).parent
TARGET=ROOT/'dist/assets/minimalance-catalogue.pdf'
EXPECTED='84c531772df33998f03dccf78fe5346dae478c3c40ed6b151f338a33a9770fe6'
if TARGET.exists() and hashlib.sha256(TARGET.read_bytes()).hexdigest()==EXPECTED:
 print('Catalogue verified.');raise SystemExit(0)
parts=sorted((ROOT/'source-media').glob('minimalance-catalogue.pdf.part-*'))
data=b''.join(p.read_bytes() for p in parts)
if hashlib.sha256(data).hexdigest()!=EXPECTED:raise SystemExit('Catalogue parts are missing or fail verification')
TARGET.parent.mkdir(parents=True,exist_ok=True)
TARGET.write_bytes(data)
print('Original catalogue restored and SHA-256 verified.')
