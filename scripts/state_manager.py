#!/usr/bin/env python3
import json, sys
from pathlib import Path

STATE_FILE = Path(".opc_state.json")

def load():
    if STATE_FILE.exists():
        try:
            return json.load(open(STATE_FILE, encoding='utf-8'))
        except Exception:
            return {}
    return {}

def save(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def cmd_get(key):
    state = load()
    print(json.dumps(state.get(key, {}), ensure_ascii=False))

def cmd_set(key, value_json):
    state = load()
    try:
        parsed = json.loads(value_json)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    state[key] = parsed
    save(state)

def cmd_update(key, updates_json):
    state = load()
    if key not in state:
        state[key] = {}
    try:
        updates = json.loads(updates_json)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    state[key].update(updates)
    save(state)

def cmd_clear():
    save({})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: state_manager.py get|set|update|clear <key> [value_json]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "get":
        if len(sys.argv) < 3:
            print("Key required")
            sys.exit(1)
        cmd_get(sys.argv[2])
    elif cmd == "set":
        if len(sys.argv) < 4:
            print("Key and value required")
            sys.exit(1)
        cmd_set(sys.argv[2], sys.argv[3])
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Key and updates required")
            sys.exit(1)
        cmd_update(sys.argv[2], sys.argv[3])
    elif cmd == "clear":
        cmd_clear()
    else:
        print("Unknown command")
        sys.exit(1)