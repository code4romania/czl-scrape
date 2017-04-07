import os
import time
import logging

if 'SENTRY_DSN' in os.environ:
    import logging
    from raven.handlers.logging import SentryHandler
    from raven.conf import setup_logging
    setup_logging(SentryHandler(os.environ['SENTRY_DSN'], level=logging.WARN))

logging.Formatter.converter = time.gmtime
