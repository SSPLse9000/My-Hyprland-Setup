import shutil
from pathlib import Path

script_dir = Path(__file__).resolve().parent
backup_dir = script_dir / "DOTS"

print(f"🔍 Using backup directory: {backup_dir}")

def mkPicture():
    pictures_dir = Path.home() / "Pictures" / "Screenshots"
    pictures_dir.mkdir(parents=True, exist_ok=True)

mkPicture()

for item in backup_dir.iterdir():
    name = item.name

    if name.lower() == "zshrc":
        zshrc_file = item / "zshrc"
        if zshrc_file.is_file():
            dest = Path.home() / ".zshrc"
            print(f"📄 Restoring ZSHRC file to {dest}")
            shutil.copy2(zshrc_file, dest)
        else:
            print(f"⚠️ No zshrc file found in {item}")
        continue

    dest = Path.home() / ".config" / name
    if item.is_dir():
        print(f"📁 Restoring directory {name} to {dest}")
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(item, dest)
    elif item.is_file():
        print(f"📄 Restoring file {name} to {dest}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)
    else:
        print(f"⚠️ Skipping {item} (not file or dir)")
