import os
import shutil
import subprocess
from pathlib import Path

script_dir = Path(__file__).resolve().parent
backup_dirs = sorted([d for d in script_dir.iterdir() if d.is_dir() and d.name.startswith("20")])
backup_dir = backup_dirs[-1] if backup_dirs else None

print(f"🔍 Using backup directory: {backup_dir}")

def mkPicture():
    subprocess.run(["mkdir", "$HOME/Pictures/Screenshots"])

targets = {
    "wofi": Path.home() / ".config" / "wofi",
    "wal": Path.home() / ".cache" / "wal",
    "waybar": Path.home() / ".config" / "waybar",
    "hypr": Path.home() / ".config" / "hypr",
    "nvim": Path.home() / ".config" / "nvim",
    "yazi": Path.home() / ".config" / "yazi",
    "zshrc": Path.home() / ".zshrc"
}

mkPicture()

for name, dest in targets.items():
    src = backup_dir / name
    if src.is_dir():
        print(f"📁 Restoring directory {name} to {dest}")
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(src, dest)
    elif src.is_file() or (src / name).is_file():
        file_src = next((f for f in src.glob("**/*") if f.name == name), None)
        if file_src:
            print(f"📄 Restoring file {name} to {dest}")
            shutil.copy2(file_src, dest)
        else:
            print(f"⚠️ Backup for {name} not found in {src}")
    else:
        print(f"⚠️ Backup for {name} not found in {src}")

