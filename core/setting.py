# settings.py

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URL prefix for media files
MEDIA_URL = '/media/'

# Directory where media files will be uploaded and stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')