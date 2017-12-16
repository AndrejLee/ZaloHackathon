#!/usr/bin/env python
import sys
from webhook.server import initServer
from chatbot.settings import BASE_DIR
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot.settings")
    base_path = os.path.join(BASE_DIR)
    initServer(128, 2, base_path + "/webhook/Clustering_l2_1000000_13516675_128_50it.hdf5", "clusters", base_path + "/webhook/index.hdf5", 1000000, base_path + "/webhook/im_data", base_path + "/webhook/temp_feat")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
