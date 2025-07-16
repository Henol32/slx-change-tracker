
# tracker/slx_diff.py
import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT = "ExampleProject"
VERSIONS_DIR = Path(f"projects/{PROJECT}/versions")
CHANGELOG_PATH = Path(f"projects/{PROJECT}/change_log.txt")

def extract_blocks(slx_path):
    with zipfile.ZipFile(slx_path, 'r') as z:
        for name in z.namelist():
            if name.endswith("simulink/blockdiagram.xml"):
                with z.open(name) as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    return set(b.get("Name") for b in root.iter("Block") if b.get("Name"))
    return set()

def main():
    slx_files = sorted(VERSIONS_DIR.glob("*.slx"), key=os.path.getmtime)
    if len(slx_files) < 2:
        print("Not enough .slx files to compare.")
        return

    old_file, new_file = slx_files[-2], slx_files[-1]
    blocks_old = extract_blocks(old_file)
    blocks_new = extract_blocks(new_file)

    added = blocks_new - blocks_old
    removed = blocks_old - blocks_new

    with open(CHANGELOG_PATH, "a") as log:
        log.write(f"\n--- Change detected: {old_file.name} → {new_file.name} ---\n")
        if added:
            log.write(f"🟢 Added blocks: {', '.join(sorted(added))}\n")
        if removed:
            log.write(f"🔴 Removed blocks: {', '.join(sorted(removed))}\n")
        if not added and not removed:
            log.write("No changes in block structure.\n")

if __name__ == "__main__":
    main()
