import json
from bot.settings import BLACKLIST_FILE


def read_blacklist():
    try:
        with open(BLACKLIST_FILE, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def write_blacklist(blacklist):
    with open(BLACKLIST_FILE, 'w') as f:
        json.dump(list(blacklist), f)


def add_to_blacklist(user_id):
    blacklist = read_blacklist()
    blacklist.add(user_id)
    write_blacklist(blacklist)


def remove_from_blacklist(user_id):
    blacklist = read_blacklist()
    blacklist.discard(user_id)
    write_blacklist(blacklist)
