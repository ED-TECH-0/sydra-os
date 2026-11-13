# Sydra OS

> A professional glass desktop for people who build things and play games.

Sydra OS (internal architecture codename: `siddha`) is an Arch-based Linux distribution built for developers and gamers. It features a spatial glassmorphism desktop environment powered by KDE Plasma 6 on Wayland, an automated Calamares installer, an out-of-the-box AAA gaming stack with automatic GPU detection (including RTX 50-series and hybrid PRIME offload), and a zero-friction developer workstation.

---

## Features

- **Siddha Glass Pro**: Smoked glass panels, floating capsule dock, 1px gradient edge light, and built-in contrast safety ensuring WCAG AA 4.5:1 text readability over any wallpaper.
- **Developer Workstation**: Modern shell defaults (Zsh, Starship prompt, `fzf`, `zoxide`), full compilers and build tools (`clang`, `gcc`, `cmake`, `ninja`), Rust, Node, Go, Python (`uv`), and rootless Podman/Docker.
- **Gaming Ready**: Steam, Proton-GE, Lutris, Gamemode (with dynamic compositor blur toggle), MangoHud overlay, Gamescope, and automatic driver management for Intel, AMD, and NVIDIA.
- **Safe Rolling Base**: Arch Linux core with Btrfs default subvolumes, ZRAM swap, and automated Snapper snapshots integrated into the GRUB boot menu.

---

## Build Prerequisites (Laptop A: EndeavourOS)

Building the ISO requires an Arch-based Linux host with root/sudo access and at least 25 GB free disk space:

```bash
sudo pacman -Syu --needed archiso devtools git base-devel qemu-desktop edk2-ovmf squashfs-tools libisoburn mtools dosfstools rsync reflector shellcheck jq python btrfs-progs gnupg
```

## Quick Start

```bash
# Verify environment and free space
make check

# Generate package manifests
make packages

# Build custom packages in clean chroot
make repo

# Build bootable hybrid ISO
make iso

# Test boot in QEMU
make qemu-uefi
make qemu-bios
```

---

## Repository Structure

- `docs/`: Master architectural plan, progress log, decision records, test matrix.
- `iso/profile/`: Customized `archiso` profile based on official Arch `releng`.
- `packages/`: Modular package list manifests (`base`, `desktop`, `dev`, `gaming`, etc.).
- `repo/`: PKGBUILD recipes for custom `siddha-*` packages and local repository.
- `tokens/`: Design tokens (`glass.json`) for system-wide glass styling.
- `tools/`: Theme generator scripts (`glassgen.py`).
- `scripts/`: ISO build, repo build, preflight, QEMU runner, and flash utilities.

---

## License

Original code licensed under [GPL-3.0-or-later](LICENSE).
Third-party component licenses documented in [docs/LICENSES.md](docs/LICENSES.md).
