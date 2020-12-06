import os
from pathlib import Path


LOCAL_STEM = "local_settings"


def set_settings_module():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        f"app.{LOCAL_STEM}"
        if Path(f"app/{LOCAL_STEM}.py").exists()
        else "app.settings",
    )
