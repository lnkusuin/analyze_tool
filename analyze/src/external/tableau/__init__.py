from pathlib import Path
import os

TABLEAU_AUTH_URL = os.environ.get("TABLEAU_AUTH_URL")
TABLEAU_AUTH_USERNAME = os.environ.get("TABLEAU_AUTH_USERNAME")
TABLEAU_AUTH_PASSWORD = os.environ.get("TABLEAU_AUTH_PASSWORD")
TABLEAU_AUTH_SITENAME = os.environ.get("TABLEAU_AUTH_SITENAME")
TABLEAU_PUBLISH_BASE_PROJECT_ID = os.environ.get("TABLEAU_PUBLISH_BASE_PROJECT_ID")

MODULE_ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
