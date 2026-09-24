import json
import os

from profile import Profile

PROFILE_FOLDER = "Profiles"


def load_profile(name):
    filename = os.path.join(PROFILE_FOLDER)


def to_json(self):
    return{
        "name": self.name,
        "credits": self.credits,
        "wins": self.wins,
        "losses": self.losses,
        "settings": self.settings
    }

def from_json(data):
    p = Profile(data["name"])
    p.credits = data["credits"]
    p.wins = data["wins"]
    p.losses = data["losses"]
    p.settings = data["settings"]
    return p



