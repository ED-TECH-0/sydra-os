# SIDDHA OS (SYDRA OS) — MASTER BUILD PLAN

- Document version: 1.1 (2026-11-13)
- Owner: E (solo developer)
- Public Name: **Sydra OS**
- Internal Codename / System Identifier: **siddha**
- Target Hardware:
  - Laptop A: HP EliteBook 850 G5 (Intel UHD 620, EndeavourOS build host, QEMU test target)
  - Laptop B: Acer Nitro V 15 (RTX 5050 8GB, Intel i5-13420H, Windows host / Live-USB gaming test target)

---

## 1. PRODUCT DEFINITION

### 1.1 Names & Identity
- **Public name**: **Sydra OS**. Displayed on UI, bootloader menus, welcome screens, documentation, ISO label `SYDRA_YYYYMM`, and release ISO filename `sydra-os-YYYY.MM.DD-x86_64.iso`.
- **Internal name**: **siddha**. Used inside Linux system files, package namespace (`siddha-theme`, `siddha-welcome`, `siddha-gpu-setup`, etc.), local pacman repository `[siddha]`, and `/etc/siddha/` configuration directories.

### 1.2 Target Users
1. Developers (web, systems, security) wanting a preconfigured workstation.
2. Gamers wanting Windows games to run smoothly on Linux out-of-the-box.
3. Global desktop users (internationalized from day 1).

### 1.3 Desktop Aesthetic: Siddha Glass Pro
- Smoked dark glass (`rgba(18,20,28,0.50)`), 1px gradient edge light, 20–24px radius, soft drop shadow.
- Dual-panel layout: thin translucent top panel + floating bottom capsule dock.
- Automatic contrast guard guaranteeing ≥ 4.5:1 text readability over any wallpaper.
- Dynamic blur unload during 3D gaming via D-Bus hook.

---

## 2. GOLDEN RULES (BINDING)

1. Never write to block devices directly except via `scripts/flash-usb.sh` (removable-only check).
2. Never touch Laptop B's Windows partitions or Laptop A's host EndeavourOS system partitions.
3. No secrets in git. Keep `.env` untracked.
4. Shell scripts must start with `#!/usr/bin/env bash` and `set -euo pipefail`.
5. Check disk space: ≥ 25 GB free required before running ISO builds.
6. Bandwidth discipline: preserve pacman cache `/var/cache/pacman/pkg`, never wipe with `-Scc`.

---

## 3. ARCHITECTURE SUMMARY

| Component | Choice |
| :--- | :--- |
| **Base** | Arch Linux (built with `mkarchiso`, derived from `releng`) |
| **Kernel** | `linux` (base) -> `linux-zen` + `linux-lts` in Phase 3.6 |
| **Desktop** | KDE Plasma 6 Wayland session (X11 fallback available) |
| **Display Manager** | SDDM with custom glass theme |
| **Installer** | Calamares (custom Sydra branding, Btrfs subvolumes, ZRAM swap) |
| **Filesystem** | Btrfs default (`@`, `@home`, `@log`, `@pkg`, `@snapshots`), ext4 option |
| **Snapshots** | Snapper + `grub-btrfs` boot menu integration |
| **Audio** | PipeWire + WirePlumber |
| **Network** | NetworkManager |
| **Gaming** | Steam, Proton-GE, Lutris, gamemode, MangoHud, gamescope |
| **GPU Setup** | `siddha-gpu-setup` supporting Intel, AMD, NVIDIA (RTX 5050 open-dkms) |
| **Developer Stack** | Zsh + Starship, full toolchains, rootless Podman, `siddha-dev` |
