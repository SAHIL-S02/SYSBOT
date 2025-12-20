from planner import ask_llm
from executor import execute_action
import json
import os
with open("user_profile.json", "r") as f:
    USER_PROFILE = json.load(f)
ALLOWED_ACTIONS = {
    "open_app",
    "type",
    "wait",
    "click",
    "move_mouse",
    "ensure_folder",
    "open_vscode",
    "save_file"
}


def validate(plan):
    for step in plan["actions"]:
        if step["action"] not in ALLOWED_ACTIONS:
            raise Exception(f"Blocked action: {step['action']}")

def ensure_before_open(actions):
    ensured = set()
    fixed = []

    for step in actions:
        if step["action"] == "open_vscode":
            path = step["path"]
            if path not in ensured:
                fixed.append({
                    "action": "ensure_folder",
                    "path": path
                })
                ensured.add(path)

        fixed.append(step)

    return fixed
def block_typed_paths(actions):
    blocked = []

    for step in actions:
        if step["action"] == "type":
            value = step.get("value", "")
            if ":" in value and "\\" in value:
                print("[BLOCKED] Typed file path detected:", value)
                continue  # skip this step

        blocked.append(step)

    return blocked
def find_folder(folder_name, drives=("C:\\", "D:\\")):
    folder_name = folder_name.lower()

    for drive in drives:
        for root, dirs, _ in os.walk(drive):
            for d in dirs:
                if d.lower() == folder_name:
                    return os.path.join(root, d)

    return None

def resolve_save_paths(actions):
    resolved = []

    for step in actions:
        if step["action"] == "save_file":
            path = step["path"]

            # Absolute path with drive but folder name only
            if os.path.isabs(path):
                base = os.path.basename(path)
                drive = os.path.splitdrive(path)[0] + "\\"

                found = find_folder(base, drives=(drive,))
                if not found:
                    raise Exception(f"Folder '{base}' not found in {drive}")

                step["path"] = found

            # Pure folder name (no drive)
            elif not os.path.isabs(path):
                found = find_folder(path)
                if not found:
                    raise Exception(f"Folder '{path}' not found in C or D drive")
                step["path"] = found

        resolved.append(step)

    return resolved



def normalize_save_file(actions):
    fixed = []

    for step in actions:
        if step["action"] == "save_file":
            # If filename is embedded in path
            path = step.get("path", "")
            filename = step.get("filename")

            if filename is None:
                folder, file = os.path.split(path)
                if not file:
                    file = "note.txt"
                step = {
                    "action": "save_file",
                    "path": folder,
                    "filename": file
                }

        fixed.append(step)

    return fixed


def main():
    print("SYSBOT ONLINE")
    while True:
        cmd = input("\nCommand > ")
        if cmd.lower() in {"exit", "quit"}:
            break

        plan = ask_llm(cmd, USER_PROFILE)
        print("\nPLAN:", json.dumps(plan, indent=2))

        actions = plan.get("actions", [])
        if not actions:
            print("No executable actions returned.")
            continue


        confirm = input("Execute? (y/n): ")
        if confirm.lower() != "y":
            continue

        validate(plan)
        plan["actions"] = ensure_before_open(plan["actions"])
        plan["actions"] = normalize_save_file(plan["actions"])
        plan["actions"] = resolve_save_paths(plan["actions"])
        plan["actions"] = block_typed_paths(plan["actions"])
        for step in plan["actions"]:
            execute_action(step)

if __name__ == "__main__":
    main()
