import os
from tracker.slx_parser import extract_block_info  # ← if you use a helper module
from difflib import unified_diff

project_path = 'projects/ExampleProject/versions'
log_path = 'projects/ExampleProject/change_log.txt'

def find_latest_versions(path):
    files = sorted(
        [f for f in os.listdir(path) if f.endswith('.slx')],
        key=lambda x: os.path.getmtime(os.path.join(path, x))
    )
    return files[-2:] if len(files) >= 2 else []

def compare_versions(file1, file2):
    blocks1 = extract_block_info(os.path.join(project_path, file1))
    blocks2 = extract_block_info(os.path.join(project_path, file2))
    block_lines1 = sorted([f"{b['Name']}={b['Value']}" for b in blocks1])
    block_lines2 = sorted([f"{b['Name']}={b['Value']}" for b in blocks2])
    return list(unified_diff(block_lines1, block_lines2, fromfile=file1, tofile=file2, lineterm=''))

def write_to_log(diff_lines):
    with open(log_path, 'a') as log:
        log.write("\n--- New Change Detected ---\n")
        for line in diff_lines:
            log.write(line + '\n')

if __name__ == "__main__":
    latest = find_latest_versions(project_path)
    if len(latest) < 2:
        print("Not enough .slx versions to compare.")
    else:
        diffs = compare_versions(*latest)
        if diffs:
            write_to_log(diffs)
            print("✅ change_log.txt updated.")
        else:
            print("No changes detected.")
