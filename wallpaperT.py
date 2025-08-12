import os
import re
import subprocess
from pathlib import Path
import hashlib
from PIL import Image

HOME = Path.home()
WALLPAPER_DIR = HOME / "Downloads" / "wallpaper"
CONFIG_DIR = HOME / ".config"
CACHE_DIR = HOME / ".cache" / "wallpaper_thumbs"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

HYPERPAPER_CONF = CONFIG_DIR / "hypr" / "hyprpaper.conf"
HYPERLOCK_CONF = CONFIG_DIR / "hypr" / "hyprlock.conf"
COLORS_CSS = HOME / ".cache" / "wal" / "colors.css"
WAYBAR_STYLE = CONFIG_DIR / "waybar" / "style.css"
WOFI_STYLE = CONFIG_DIR / "wofi" / "style.css"
SOCKET_DIR = os.path.expanduser("~/.cache/nvim_sockets")

waybar_opacity = 0.5

def natural_sort_key(path: Path):
    name = path.stem.lower()
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', name)]

def scan_wallpapers(folder):
    try:
        wallpapers = [Path(entry.path) for entry in os.scandir(folder)
                      if entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        return sorted(wallpapers, key=natural_sort_key)
    except Exception as e:
        print(f"[ERROR] Scanning wallpapers: {e}")
        return []

def hex_to_rgba(hex_color, alpha):
    try:
        hex_color = hex_color.strip().lstrip("#").rstrip(";")
        if len(hex_color) != 6:
            return None
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, {alpha})"
    except Exception as e:
        print(f"[ERROR] Converting hex to RGBA: {e}")
        return None

def apply_wallpaper_settings(wallpaper: Path):
    print(f"\n🖼️ Applying wallpaper: {wallpaper.name}")

    try:
        if HYPERPAPER_CONF.exists():
            text = HYPERPAPER_CONF.read_text()
            text = re.sub(r"^preload = .*$", f"preload = {wallpaper}", text, flags=re.M)
            text = re.sub(r"^wallpaper = .*$", f"wallpaper = eDP-1,{wallpaper}", text, flags=re.M)
            HYPERPAPER_CONF.write_text(text)
    except Exception as e:
        print(f"[ERROR] Updating hyprpaper.conf: {e}")

    try:
        if HYPERLOCK_CONF.exists():
            text = HYPERLOCK_CONF.read_text()
            text = re.sub(r"^\s*path\s*=.*$", f"path = {wallpaper}", text, flags=re.M)
            HYPERLOCK_CONF.write_text(text)
    except Exception as e:
        print(f"[ERROR] Updating hyprlock.conf: {e}")

    try:
        subprocess.run(["pkill", "hyprpaper"], check=False)
        subprocess.run(["pkill", "waybar"], check=False)
        subprocess.Popen(["hyprpaper"])
    except Exception as e:
        print(f"[ERROR] Restarting hyprpaper/waybar: {e}")

    try:
        subprocess.run(["swww", "img", str(wallpaper), "--transition-type", "fade", "--transition-duration", "1"], check=False)
        subprocess.run(["wal", "-i", str(wallpaper)], check=False)
    except Exception as e:
        print(f"[ERROR] Applying wallpaper with swww/pywal: {e}")

    bg_color = fg_color = border_color = ""
    try:
        with open(COLORS_CSS) as f:
            for line in f:
                if "background" in line and not bg_color:
                    bg_color = line.split()[1].strip(";")
                elif "foreground" in line and not fg_color:
                    fg_color = line.split()[1].strip(";")
                elif "color6" in line and not border_color:
                    border_color = line.split()[1].strip(";")
    except Exception as e:
        print(f"[ERROR] Reading colors.css: {e}")

    rgba_bg = hex_to_rgba(bg_color, waybar_opacity) or "rgba(0,0,0,0.7)"
    hover_color = hex_to_rgba(fg_color, 0.2) or "rgba(255,255,255,0.2)"
    active_color = hex_to_rgba(border_color, 0.2) or "rgba(255,255,255,0.2)"

    try:
        if WAYBAR_STYLE.exists():
            subprocess.run(["sed", "-i", f"s/@define-color bg_main .*/@define-color bg_main {rgba_bg};/", str(WAYBAR_STYLE)])
            subprocess.run(["sed", "-i", f"s/@define-color bg_hover .*/@define-color bg_hover {hover_color};/", str(WAYBAR_STYLE)])
            subprocess.run(["sed", "-i", f"s/@define-color bg_active .*/@define-color bg_active {active_color};/", str(WAYBAR_STYLE)])
            subprocess.run(["sed", "-i", f"s/@define-color border_main .*/@define-color border_main {border_color};/", str(WAYBAR_STYLE)])
            subprocess.run(["sed", "-i", f"s/color: .*/color: {border_color};/", str(WAYBAR_STYLE)])
    except Exception as e:
        print(f"[ERROR] Updating Waybar style: {e}")

    try:
        if WOFI_STYLE.exists():
            subprocess.run(["sed", "-i", f"s/background-color: .*/background-color: {rgba_bg};/", str(WOFI_STYLE)])
    except Exception as e:
        print(f"[ERROR] Updating Wofi style: {e}")

    try:
        subprocess.Popen(["waybar"])
    except Exception as e:
        print(f"[ERROR] Starting waybar: {e}")

    print("✅ Wallpaper applied and system updated.")

def get_all_active_sockets():
    sockets = []
    try:
        if not os.path.isdir(SOCKET_DIR):
            return sockets
        for entry in os.listdir(SOCKET_DIR):
            socket_file = os.path.join(SOCKET_DIR, entry)
            try:
                with open(socket_file, "r") as f:
                    socket_path = f.read().strip()
                if os.path.exists(socket_path):
                    sockets.append(socket_path)
            except Exception as e:
                print(f"[WARN] Could not read socket file '{socket_file}': {e}")
    except Exception as e:
        print(f"[ERROR] Scanning Neovim sockets: {e}")
    return sockets

def main():
    wallpapers = scan_wallpapers(WALLPAPER_DIR)
    if not wallpapers:
        print("[ERROR] No wallpapers found.")
        return

    print("\n📁 Available Wallpapers:\n")
    for i, wp in enumerate(wallpapers, 1):
        print(f"{i}. {wp.name}")

    try:
        choice = int(input("\n👉 Enter the number of the wallpaper to apply: "))
        if not (1 <= choice <= len(wallpapers)):
            print("[ERROR] Invalid selection.")
            return
    except Exception as e:
        print(f"[ERROR] Invalid input: {e}")
        return

    selected = wallpapers[choice - 1]
    apply_wallpaper_settings(selected)

    sockets = get_all_active_sockets()
    if not sockets:
        print("[WARN] No active Neovim instances found.")
        return

    for socket_path in sockets:
        try:
            cmd = f"nvim --server {socket_path} --remote-send ':lua require(\"pywal\").setup()<CR>'"
            exit_code = os.system(cmd)
            if exit_code == 0:
                print(f"[INFO] Sent command to Neovim at {socket_path}")
            else:
                print(f"[ERROR] Failed to send command to Neovim at {socket_path}")
        except Exception as e:
            print(f"[ERROR] Neovim command failed: {e}")

if __name__ == "__main__":
    main()
