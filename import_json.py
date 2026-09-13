import json
import os

from profile import Profile

PROFILE_FOLDER = "Profiles"


def load_profile(name):
    filename = os.path.join(PROFILE_FOLDER)
    