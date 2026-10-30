"""Prepare only reviewed public files for the official static hosting project."""
from pathlib import Path
import json
import shutil
from official_skill_release import verify_release

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.deploy'
PUBLIC = OUTPUT / 'public'
PUBLIC.mkdir(parents=True, exist_ok=True)
(PUBLIC / 'packages').mkdir(exist_ok=True)
(PUBLIC / 'catalog').mkdir(exist_ok=True)
for release in sorted((ROOT / 'packages').glob('*.release.json')):
    metadata = json.loads(release.read_text())
    bundle = ROOT / 'packages' / metadata['bundleFile']
    if bundle.parent != ROOT / 'packages':
        raise ValueError('Bundle must be inside packages/')
    verify_release(bundle_path=bundle, release_path=release)
    for path in (bundle, release):
        shutil.copy2(path, PUBLIC / 'packages' / path.name)
shutil.copy2(ROOT / 'catalog/runtime-skills.json', PUBLIC / 'catalog/runtime-skills.json')
shutil.copy2(ROOT / 'LICENSES/Apache-2.0.txt', PUBLIC / 'LICENSE')
shutil.copy2(ROOT / 'hosting/vercel.json', OUTPUT / 'vercel.json')
print(OUTPUT)
