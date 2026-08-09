import json
import time

from . import paths


def load_state():
    try:
        with open(paths.STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_state(state):
    paths.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(paths.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def is_installed(tool_id):
    return tool_id in load_state()


def mark_installed(tool_id):
    state = load_state()
    state[tool_id] = {"ts": int(time.time())}
    save_state(state)


def mark_removed(tool_id):
    state = load_state()
    state.pop(tool_id, None)
    save_state(state)
