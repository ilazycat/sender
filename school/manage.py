#!/usr/bin/env python
import os
import sys
#sudo sysctl fs.inotify.max_user_watches=16384
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
