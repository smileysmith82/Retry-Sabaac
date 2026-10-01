import json
import os
import hmac
import hashlib
import shutil
from profile import Profile

PROFILE_FOLDER = "Profiles"
SECRET_KEY = b"542a1b91bc21bd84"

def save_profile(profile):
    if profile.guest:
        return
    
    os.makedirs(PROFILE_FOLDER, exist_ok=True)

    filename = os.path.join(PROFILE_FOLDER, profile.name + ".json")

    backup_filename = filename + ".bak"
    
    data = to_json(profile)
    data["signature"] = create_signature(data)

    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                old_data = json.load(file)

            if verify_profile(old_data):
                shutil.copyfile(filename, backup_filename)

        except json.JSONDecodeError:
            print("Existing file is corrupted")
            print("It will be overwritten with the new profile")
        
    with open(filename, 'w') as file:
        json.dump(data, file, indent= 4)

    if not os.path.exists(backup_filename):
        shutil.copyfile(filename, backup_filename)

def restore_backup(filename, backup_filename):
    if not os.path.exists(backup_filename):
        print("No backup available")
        return None

    try:
        with open(backup_filename, "r") as file:
            backup_data = json.load(file)
        if not verify_profile(backup_data):
            print("Backup verification failed.")
            return None

        shutil.copyfile(backup_filename, filename)

        print("Backup restored successfully")

        return from_json(backup_data)
    except json.JSONDecodeError:
        print("Backup file is corrupted")
        return None

def load_profile(name):
    filename = os.path.join(PROFILE_FOLDER, name + ".json")
    backup_filename = filename + ".bak"

    if not os.path.exists(filename):
        return None

    try:
        with open(filename, 'r') as file:
            data = json.load(file)

        if verify_profile(data):
            return from_json(data)

        print ("Profile Verification failed.")
        print("Attempting to restore backup...")

        return restore_backup(filename, backup_filename)
    
    except json.JSONDecodeError:
        print("Profile file is corrupted")
        print("Attempting to restore backup")
        return restore_backup(filename, backup_filename)

def delete_profile(name):
    filename = os.path.join(PROFILE_FOLDER, name + ".json")
    
    backup_filename = filename + ".bak"

    if os.path.exists(filename):
        os.remove(filename)

    if os.path.exists(backup_filename):
        os.remove(backup_filename)

def verify_profile(data):
    profile_data = data.copy()

    stored_signature = profile_data.pop("signature", None)

    if stored_signature is None:
        return False

    expected_signature = create_signature(profile_data)

    return hmac.compare_digest(stored_signature, expected_signature)

def get_profiles():
    profiles = []

    if not os.path.exists(PROFILE_FOLDER):
        return profiles

    for filename in os.listdir(PROFILE_FOLDER):
        if filename.endswith(".json"):
            name = filename[:-5]
            profiles.append(name)

    profiles.sort()

    return profiles

def create_profile(name):

    profile = Profile(name)
    save_profile(profile)

    return profile

def to_json(profile):
    return{
        "name": profile.name,
        "credits": profile.credits,
        "wins": profile.wins,
        "losses": profile.losses,
        "settings": profile.settings,
        "profile_picture": profile.profile_picture
    }

def create_signature(data):
    data_string = json.dumps( data, sort_keys=True)

    signature = hmac.new(SECRET_KEY, data_string.encode(), hashlib.sha256).hexdigest()
    return signature
def from_json(data):
    p = Profile(data["name"])
    p.credits = data["credits"]
    p.wins = data["wins"]
    p.losses = data["losses"]
    p.settings = data["settings"]
    p.profile_picture = data.get("profile_picture")
    
    return p



