import os
from pathlib import Path
import json

MAX_RENDER_THREADS   = 4
MAX_HISTORY_ENTRIES  = 10

TMP_DIR     = Path('tmp')
if not os.path.isdir(TMP_DIR): TMP_DIR.mkdir(exist_ok=True)
PREVIEW_DIR = Path(TMP_DIR, 'previews')
if not os.path.isdir(PREVIEW_DIR): PREVIEW_DIR.mkdir(exist_ok=True)
PREVIEW_VIDEO_DIR = Path(PREVIEW_DIR, 'video')
if not os.path.isdir(PREVIEW_VIDEO_DIR): PREVIEW_VIDEO_DIR.mkdir(exist_ok=True)

ROOT_DIR         = Path(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
STATIC_DIR       = Path(ROOT_DIR, 'static')
JSON_DIR         = Path(STATIC_DIR, 'json')
EFFECTS_JSON_DIR = Path(JSON_DIR, 'effects')
GRAPHICS_DIR     = Path(STATIC_DIR, 'graphics')
STYLES_DIR       = Path(STATIC_DIR, 'styles')

EFFECTS           = {}
EFFECT_CATEGORIES = {}
EFFECT_COMMANDS   = {}

for json_path in EFFECTS_JSON_DIR.iterdir():
    if json_path.suffix == '.json':
        with Path(json_path).open() as f:
            json_dict = json.loads(f.read())
            prefix = json_path.parts[-1].split('.')[0]
            for effect_name, effect in json_dict['effects'].items(): EFFECTS['{}.{}'.format(prefix, effect_name)] = effect
            for category_name, effect_list in json_dict['categories'].items(): EFFECT_CATEGORIES['{}.{}'.format(prefix, category_name)] = effect_list
            EFFECT_COMMANDS[prefix] = json_dict['commands']

shared_objects = {
    'data_manager':     None,
    'frontend_manager': None,
}
