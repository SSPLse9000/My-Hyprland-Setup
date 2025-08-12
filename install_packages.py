import subprocess

REQUIRED_PACKAGES = [
    "hyprland",
    "wofi",
    "python-pywal",
    "waybar",
    "nwg-displays",
    "swww",
]

OPTIONAL_PACKAGES = {
    "cmus": "Console music player",
    "yazi": "Terminal file manager",
    "neovim": "Modern Vim-based editor",
    "emote": "Emoji board"
    "nemo": "Graphical file manager",
}

def install_package(pkg):
    print(f"\n📦 Installing {pkg}...")
    try:
        subprocess.run(["sudo", "pacman", "-S", "--noconfirm", pkg], check=True)
        print(f"✅ {pkg} installed successfully.")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {pkg}.")

def prompt_optional(pkg, desc):
    while True:
        choice = input(f"\nDo you want to install {pkg} ({desc})? [y/N]: ").strip().lower()
        if choice == "y":
            install_package(pkg)
            break
        elif choice == "n" or choice == "":
            print(f"Skipping {pkg}.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    print("Installing main packages:")
    for pkg in REQUIRED_PACKAGES:
        install_package(pkg)

    print("\n Optional packages:")
    for pkg, desc in OPTIONAL_PACKAGES.items():
        prompt_optional(pkg, desc)

    print("\n Finished!")

if __name__ == "__main__":
    main()

