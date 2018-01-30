from .production import *

# All environment settings can be overwritten with `docker run -e`

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['demo.django-fluent.org'])
ALLOWED_HOSTS.append('localhost')

# Safe defaults to allow startups without many settings.
CACHES['default'] = env.cache(default='locmemcache://')

# When the container restarts, and memcache still indicates the files are present,
# django-compressor will not recreate the files on the fly. Better use offline compression
CACHES['compressor'] = env.cache('COMPRESSOR_CACHE', 'locmemcache://')
COMPRESS_CACHE_BACKEND = 'compressor'
COMPRESS_CSS_HASHING_METHOD = 'hash'  # Not using mtime in case it differs between servers.
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'  # generate .gz too for uwsgi static-gzip-dir

# Need to different way to get the release, since there is no .git folder to read.
try:
    with open(SRC_DIR + '/.docker-git-version') as f:
        GIT_VERSION = f.read().strip()
    RAVEN_CONFIG['release'] = GIT_VERSION
except IOError:
    pass

SILENCED_SYSTEM_CHECKS = (
    'security.W004',  # SECURE_HSTS_SECONDS is handled by uWSGI
    'security.W006',  # SECURE_CONTENT_TYPE_NOSNIFF is handled by uWSGI
    'security.W007',  # SECURE_BROWSER_XSS_FILTER is handled by uWSGI
    'security.W008',  # SECURE_SSL_REDIRECT is handled by uWSGI
)

# Docker sites typically run behind a HTTP proxy.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
