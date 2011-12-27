# madduck production server settings.

import os, os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql',               # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'icrackitdb2',           # Or path to database file if using sqlite3.
        'USER': 'icrackituser',          # Not used with sqlite3.
        'PASSWORD': 'thisistherooftop',  # Not used with sqlite3.
        'HOST': 'localhost',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                  # Set to empty string for default. Not used with sqlite3.
    }
}

#time-zone.
TIME_ZONE = 'America/Chicago'

SITE_ID = 1

#for internationalizaton machinery.
USE_I18N = True

#format dates, numbers and calenders according to locale.
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
MEDIA_URL = 'http://static.icrack.it/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a trailing slash.
ADMIN_MEDIA_PREFIX = 'http://static.icrack.it/'

