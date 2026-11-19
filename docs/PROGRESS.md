# Task Progress Log

Task logging format:
- Status: `TODO` | `CLAIMED by <agent> on <date>` | `DONE`
- Entry: Task ID, date, commands run, output summary, verification result, issues.

---

## Phase 0: Foundation

### T0.1 Create the repository
- Status: DONE
- Date: 2026-11-13
- Result: Repository structure initialized, `.gitignore`, `LICENSE`, `AGENTS.md`, `README.md`, `docs/MASTER_PLAN.md` created. Pushed to `https://github.com/ED-TECH-0/sydra-os.git`.

### T0.2 Makefile and logging
- Status: DONE
- Date: 2026-11-13
- Result: `Makefile` created with targets `check`, `packages`, `repo`, `iso`, `qemu-bios`, `qemu-uefi`, `sums`, `clean`. `scripts/preflight.sh` executes with 0 failures.

### T0.3 Secret hygiene
- Status: DONE
- Date: 2026-11-13
- Result: `.env.example` created with variable names only. `.pre-commit-config.yaml` configured with gitleaks and shellcheck hooks. `.env` and `*.key` added to `.gitignore`.

### T0.4 Progress, decisions and blockers files
- Status: DONE
- Date: 2026-11-13
- Result: Created `docs/PROGRESS.md`, `docs/DECISIONS.md`, `docs/BLOCKERS.md`, `docs/LICENSES.md`, `docs/TEST_MATRIX.md`, `docs/RELEASE_NOTES_TEMPLATE.md`. Initial entries recorded for T0.1–T0.4 and DEC-001 through DEC-003.

### T0.5 Build machine bootstrap (Laptop A)
- Status: DONE
- Date: 2026-11-19
- Result: Host toolchain verified on Laptop A (EndeavourOS): `mkarchiso` (archiso 79), `makechrootpkg` (devtools), `qemu-system-x86_64` (11.1.3), `repo-add` (7.1.0), `/dev/kvm` active, 208 GiB free disk, 7.1 GiB RAM.

### T0.6 Name, trademark and domain check
- Status: DONE
- Date: 2026-11-18
- Result: Rebranded to **Sydra OS** by E (Master Plan 2.0). Internal repository and packaging namespaces retain `siddha` (`siddha-*`) to ensure backward compatibility. Public facing identifiers (`/etc/os-release`, ISO volume label, Calamares branding, logo) standardized to Sydra OS.

---

## Phase 1: Base Profile Setup

### T1.1 & T1.2 Profile Definition and Boot Configurations
- Status: DONE
- Date: 2026-11-13
- Result: 
  - `iso/profile/profiledef.sh` configured with Sydra OS branding.
  - `iso/profile/pacman.conf` and `pacman.conf.in` rendered with `[multilib]` and local `[siddha]` repo.
  - `iso/profile/airootfs/` setup: live user, autologin, passwordless sudo, systemd service symlinks.
  - Bootloader configurations complete: UEFI systemd-boot entries (`efiboot/`), GRUB (`grub/grub.cfg`), BIOS syslinux (`syslinux/`).

### T1.3 Base ISO Compilation
- Status: DONE
- Date: 2026-11-13
- Target: Run `make iso` to compile `build/out/sydra-os-*.iso` using mkarchiso with custom siddha repository.
- Result: Successfully produced `build/out/sydra-os-2026.11.13-x86_64.iso` (4.1 GiB). SHA256 checksum recorded in `build/out/SHA256SUMS` (`d8db54e54a3faab9e0ba2365259751cb17c356af7fd389c04b7e14aab988d499`). Hybrid BIOS/UEFI partition layout verified via `fdisk -l`.

### T1.4 Live Desktop QEMU Boot Verification
- Status: DONE
- Date: 2026-11-13
- Target: Boot live ISO in QEMU (2GB RAM cap), verify autologin, KDE Plasma 6 session, and Sydra OS branding.
- Result: PASS. QEMU booted into graphical session within 45s. Verified via screendump:
  - KDE Plasma 6 Wayland desktop active with autologin (`liveuser`).
  - "Install Sydra OS" desktop launcher present.
  - Welcome Center opens: "Welcome to the Sydra OS operating system running KDE Plasma!" with Sydra OS documentation link.
  - Floating bottom panel, status tray, NetworkManager active.

---

## Phase 3: Desktop Base (COSMIC Main Edition)

### T3.1 Package groups (COSMIC)
- Status: DONE
- Date: 2026-11-19
- Target: Replace KDE Plasma packages in `packages/desktop.txt` with verified COSMIC Epoch 1 packages (`cosmic-session` v1:1.11.0-1, `cosmic-comp`, `cosmic-panel`, `cosmic-files`, `cosmic-terminal`, `cosmic-greeter`, etc.). Move KDE packages to `packages/desktop-kde.txt` for Appendix K. Regenerate `iso/profile/packages.x86_64`.
- Result:
  - Verified and bundled all official Arch COSMIC packages: `cosmic-session` (v1:1.11.0-1), `cosmic-comp`, `cosmic-panel`, `cosmic-applets`, `cosmic-app-library`, `cosmic-launcher`, `cosmic-bg`, `cosmic-notifications`, `cosmic-osd`, `cosmic-settings`, `cosmic-greeter`, `cosmic-icon-theme`, `cosmic-wallpapers`, `cosmic-files`, `cosmic-terminal`, `cosmic-text-editor`, `cosmic-player`, `cosmic-store`, `xdg-desktop-portal-cosmic`.
  - Moved previous KDE Plasma package group to `packages/desktop-kde.txt`.
  - Regenerated `iso/profile/packages.x86_64` (185 package groups).
  - Built ISO `build/out/sydra-os-2026.11.19-x86_64.iso` (4.5 GiB).
    - SHA-256: `d38e61ead9bdc5a04cb908ae3dae1095cae7358353734a1422e0b45cf1d201f8`.

### T3.2 Live user and automatic desktop start (COSMIC)
- Status: DONE
- Date: 2026-11-19
- Target: Automatic live user autologin into native COSMIC Wayland session without login prompt, configure `cosmic-greeter` (greetd), provide "Install Sydra OS" launcher, and boot directly to desktop.
- Result:
  - Configured `display-manager.service -> /usr/lib/systemd/system/cosmic-greeter.service`.
  - Configured `/etc/greetd/cosmic-greeter.toml` with `[initial_session]` for user `live` running `start-cosmic`.
  - Pre-seeded Sydra Obsidian Waves wallpaper in `~/.config/cosmic/com.system76.CosmicBackground/v1/all`.
  - Pre-seeded Frosted Glass theme settings (`frosted_panel=true`, `frosted_windows=true`, `frosted=Medium`).
  - Added desktop entry `/etc/skel/Desktop/siddha-installer.desktop` ("Install Sydra OS").
  - QEMU UEFI boot test PASS: Booted straight into native COSMIC Wayland desktop. Top panel (Workspaces, Applications, centered Clock, Status applets) and floating bottom frosted dock active and responsive. Screen capture verified.

### T3.5 Installer Configuration for COSMIC Desktop & End-to-End Target Boot Verification
- Status: DONE
- Date: 2026-11-19
- Target: Adapt Calamares modules and execution sequence for COSMIC desktop: remove obsolete displaymanager module from exec sequence, enable cosmic-greeter in target systemd services, remove live-user initial autologin from target greeter configuration on cleanup, resolve GRUB Btrfs kernel premature EOF by mounting ESP at `/boot`, and verify end-to-end installation to target disk.
- Result:
  - Updated Calamares `settings.conf`: Removed `displaymanager` from exec sequence.
  - Updated `services-systemd.conf`: Configured `cosmic-greeter` service as mandatory.
  - Updated `shellprocess_firstboot.conf`: Enabled `cosmic-greeter.service` in installed system.
  - Updated `shellprocess_cleanup.conf`: Automatically strips live user autologin (`initial_session`) from `/etc/greetd/cosmic-greeter.toml` upon install completion.
  - Resolved GRUB Btrfs kernel premature EOF: Configured `partition.conf` with `efi.mountPoint: "/boot"` (1024 MiB FAT32). Kernels and initramfs reside directly on FAT32 bypassing GRUB Btrfs decompression limitations while preserving full Btrfs root layout (`/@`, `/@home`, `/@snapshots`, `/@cache`, `/@log`) with `compress=zstd:1`.
  - Added `/usr/local/bin/mkfs.btrfs` wrapper to disable `block-group-tree` for bootloader compatibility.
  - Hardened `scripts/qemu-test.sh` to refresh NVRAM on ISO boot (`-boot order=d,menu=on`).
  - Built package `siddha-calamares-config-0.1.0-11`.
  - Built Release ISO `build/out/sydra-os-2026.11.19-x86_64.iso` (4.5 GiB, SHA-256: `455d302bd2cab39b2713c50a0eade5c6f4c22e509c32ca3a1cf18df7b009310b`).
  - Integrated 4K Sydra Moon Landscape as default system wallpaper across live and installed COSMIC sessions (`/usr/share/wallpapers/Sydra/contents/images/3840x2160.png`), featuring the official Sydra OS faceted glass hexagonal prism logo, glowing cyan orbital ring, and star flare.
  - Implemented Sydra Glassmorphism Engine: tuned alpha mapping (`alpha_map`), 8 designer glass presets, dedicated GUI control panel (`sydra-glass-control`), expanded Welcome app, dock intellihide controls, and fixed regional xkbcommon locale compose tables.
  - End-to-End QEMU installation test PASS: Calamares installed cleanly to 30 GB virtual drive. Rebooted directly from disk into native COSMIC Greeter login interface. Screen verified.

---

## Phase 4: Glassmorphism Visual Identity

### T4.1 Design tokens (`tokens/glass.json`)
- Status: DONE
- Date: 2026-11-13
- Result: `tokens/glass.json` created with radii, blur scales, layer opacity, shadow, fonts, and presets (`graphite`, `midnight`, `slate-light`, `high-contrast`).

### T4.2 COSMIC Theming Research Spike
- Status: DONE
- Date: 2026-11-19
- Target: Map and document COSMIC Epoch 1 (v1.11.0) appearance options, file storage paths under `~/.config/cosmic/`, live-apply responsiveness, and scripting capabilities.
- Result:
  - Documented complete architecture in `docs/COSMIC_THEMING.md`.
  - Mapped all `CosmicTheme.Dark.Builder/v2` keys (`frosted`, `frosted_windows`, `frosted_panel`, `frosted_applets`, `frosted_system_interface`, `accent`, `bg_color`, `corner_radii`, `gaps`).
  - Verified RON schema for wallpaper background management (`com.system76.CosmicBackground/v1/all`).
  - Mapped panel/dock configuration under `com.system76.CosmicPanel.Panel` and `com.system76.CosmicPanel.Dock`.
  - Verified consistency pipeline for GTK and Qt/Kvantum applications.

### T4.3 Generator (`tools/glassgen.py`)
- Status: DONE
- Date: 2026-11-19
- Target: Generate COSMIC theme files, GTK CSS overrides, and terminal configs deterministically from `tokens/glass.json`.
- Result:
  - Enhanced `tools/glassgen.py` to compile COSMIC theme files (`com.system76.CosmicTheme.Dark.Builder/v2`) and terminal profiles (`com.system76.CosmicTerm/v1`).
  - Validated contrast ratios (> 8.98:1 on all test backgrounds) and verified byte-for-byte deterministic output across repeat executions (`DETERMINISM PASS`).

### T4.7 Presets and Intensity Switcher (`siddha-glass-set`)
- Status: DONE
- Date: 2026-11-19
- Target: Implement `siddha-glass-set <preset> <intensity>` supporting live switching of COSMIC Frosted Glass levels (`pro`, `standard`, `heavy`, `flat`) and color palettes (`graphite`, `midnight`, `slate-light`, `high-contrast`).
- Result:
  - Updated `siddha-glass-set` with native COSMIC RON key writers.
  - Built and updated package `siddha-theme-0.1.0-9`.

### T4.5 Procedural 4K Wallpapers & Branding Logo
- Status: DONE
- Date: 2026-11-13
- Result: 4 procedural frosted glass SVG wallpapers generated in `assets/wallpapers/`. Vector logo `assets/logo/sydra-logo.svg` created. Pushed to remote repo.

---

## Phase 2 & 7: Core Custom Packages (`siddha-*`)

### Custom Package Recipes Prepared & Tested
- Status: DONE
- Date: 2026-11-13
- Packages in `repo/pkgbuilds/`:
  - `calamares`: Compiled v3.4.2 installer framework for Qt6.
  - `siddha-calamares-config`: Calamares modules preventing archiso initcpio leakage, cleaning live configs, and configuring squashfs unpack.
  - `siddha-branding`: `/etc/os-release`, `/etc/issue` with public name Sydra OS and internal codename siddha, bundled wallpapers and logo.
  - `siddha-theme`: Compiled color schemes, Konsole profiles, GTK styles, and `siddha-glass-set` switcher.
  - `siddha-settings`: Zsh, Starship, `99-siddha.conf` gaming sysctl, ZRAM, and dynamic blur GameMode hook.
  - `siddha-gpu-setup`: Hardware detection verified on Laptop A (detected Intel UHD 620), PRIME offload toggle.
  - `siddha-dev`: Interactive terminal hub for Rust, Node, Go, Docker.
  - `siddha-welcome`: PySide6 onboarding app.
  - `siddha-gamehub`: PySide6 game browser and launcher; `--dump-badges` passes offline test.
  - `siddha-keyring`: Pacman GPG validation package.

### T2.1 Calamares Framework & Sydra Integration
- Status: DONE
- Date: 2026-11-13
- Target: Compile `calamares` 3.4.2 against Qt6 and add to local `[siddha]` repo. Integrate with `siddha-calamares-config` (branding, unpackfs squashfs configuration, initcpio cleanup, service setup).
- Result: Built `calamares-3.4.2-2-x86_64.pkg.tar.zst` (5.0 MB) and `siddha-calamares-config-0.1.0-2-any.pkg.tar.zst`. Added to `repo/x86_64/siddha.db`. Enabled in `packages/siddha.txt`. `scripts/gen-packages.sh` updated `iso/profile/packages.x86_64`.

### T2.2 Calamares Installer ISO Build & Live Boot Verification
- Status: DONE
- Date: 2026-11-13
- Target: Rebuild Sydra OS ISO with `calamares` included; verify via QEMU.
- Result: Successfully produced `build/out/sydra-os-2026.11.13-x86_64.iso` (4.1 GiB). Boot verified in QEMU: "Install Sydra OS" launcher backed by `sudo calamares` and Sydra branding present on desktop.

### T2.3 Calamares Kernel, Initcpio, & Post-Install Hardening
- Status: DONE
- Date: 2026-11-15
- Target: Permanently resolve `mkinitcpio -P` exit code 1 (`/boot/vmlinuz-linux must be readable`), ensure microcode copying, and clean up installer artifacts post-install.
- Result: 
  - Overhauled `siddha-initcpio-fix`: unconditionally validates `/boot/vmlinuz-linux` size, copies valid kernel binary directly from `/usr/lib/modules/*/vmlinuz`, removes live drop-ins (`archiso.conf`, `archiso.preset`), and verifies microcode images.
  - Hardened `siddha-installer`: guarantees that `airootfs.sfs`, `vmlinuz-linux`, and ucode files exist at `/run/archiso/bootmnt/sydra/` before Calamares launches.
  - Enhanced `mount.conf`: added Btrfs `@snapshots` subvolume (`/.snapshots`) for Snapper rollbacks.
  - Enhanced `shellprocess_cleanup.conf` & `firstboot.conf`: scrubs installer desktop shortcuts from installed user desktop, configures `siddha` keyring alongside `archlinux`.
  - Built `siddha-calamares-config-0.1.0-7` and updated `[siddha]` repository.
  - Built fresh release candidate ISO `build/out/sydra-os-2026.11.15-x86_64.iso` (4.1 GiB). SHA-256: `b2742024c22fcd567ef1e43176e0ca555f70f49b6f9009c46fd59636cc9586d5`.

### T4.3 Global KDE Plasma 6 & GTK Glass Defaults
- Status: DONE
- Date: 2026-11-15
- Target: Provide out-of-the-box glassmorphism, blur effects, typography (Inter / JetBrains Mono), and GTK styling.
- Result: Built `siddha-theme-0.1.0-3` with `/etc/xdg/kdeglobals` (SiddhaGlassGraphite default), `/etc/xdg/kwinrc` (blur & translucency enabled), and `/etc/xdg/gtk-{3,4}.0/gtk.css`. Updated `[siddha]` repository.

### T4.4 Traffic Light Window Controls & Glass Aesthetic Alignment
- Status: DONE
- Date: 2026-11-15
- Target: Implement user-specified visual identity: macOS-style traffic-light buttons on the top-left, smoked frosted glass windows with blur, left vertical dock, and 3D metallic torus wallpaper.
- Result: 
  - Configured top-left window controls (`ButtonsOnLeft=XIA`, `ButtonsOnRight=`) across Qt6/KDE and GTK 3/4 (`gtk-decoration-layout=close,minimize,maximize:`).
  - Packaged `org.sydra.glass.desktop` Look-and-Feel package into `siddha-theme-0.1.0-4` implementing dual-panel architecture: top translucent status bar + left vertical capsule dock (Dolphin, Konsole, Firefox, Sydra Game Hub, System Settings).
  - Bundled 3D metallic torus (`sydra-metallic-torus.svg`) and vibrant cyber frost (`sydra-cyber-frost.svg`) vector wallpapers.
  - Resolved Plasma Wayland boot freeze: configured `kwin_wayland` compositor for SDDM, created `/home/live` in `airootfs` with `1000:1000` ownership, disabled KWallet first-run prompt, and completed 13-section color schemes.
  - Built production release ISO `build/out/sydra-os-2026.11.15-x86_64.iso` (4.1 GiB). SHA-256: `1feafa893c983198f96ba4b10b9c95c95402b8775a15a88b0842f235dff522cc`. Verified live boot and captured screenshot sequence in `~/Pictures/Screenshots/` and `~/Pictures/sydra-os-gui.png`. Includes `squashfs-tools` (`unsquashfs`), `parted`, and `gptfdisk`.

---

## Phase 8: System Defaults & Hardening

### T8.1 & T8.3 Snapshot Rollback & Safe Update Workflow
- Status: DONE
- Date: 2026-11-15
- Target: Implement safe system update workflow (`siddha-update`), automated pre-update Snapper snapshotting, and snapshot rollback manager (`siddha-rollback`).
- Result:
  - Created `siddha-update`: verifies ≥ 5 GB root disk space, generates pre-update Snapper snapshot, upgrades official + Sydra pacman packages, refreshes Flatpak applications, and flags kernel updates requiring reboot.
  - Created `siddha-rollback`: provides user-friendly CLI to inspect Btrfs/Snapper snapshot history and perform targeted rollback with single reboot.
  - Packaged into `siddha-settings-0.1.0-2` and integrated into local `[siddha]` repository.
  - Created `sydra-smoke-test` installed to `/usr/local/bin/sydra-smoke-test` on live ISO for automated post-boot verification of session, audio, network, core binaries, and custom utilities.

### T4.6 & T7.1 Desktop Black Screen Fix, Sydra Game Hub Overhaul, & Obsidian Waves Wallpaper
- Status: DONE
- Date: 2026-11-15
- Target: Resolve black screen on live session boot, fix Sydra Game Hub launch failure, and replace metallic torus wallpaper with authentic minimalist luxury dark wallpaper.
- Result:
  - **Sydra Game Hub**: Completed truncated `__main__` entrypoint in `siddha-gamehub.py` with `QApplication` lifecycle, multi-path catalog search (`/usr/share/siddha/catalog/native-games.yaml`), fallback parser, and verified `--dump-badges` passes offline. Packaged into `siddha-gamehub-0.1.0-2`.
  - **Minimalist Luxury Wallpaper**: Replaced metallic torus with **Sydra Obsidian Waves** (`sydra-obsidian-waves.png` and `.svg`) — authentic deep obsidian (`#07090E` to `#121724`) with violet, cyan, and indigo wave contours, crisp 1.5px edge highlights, and dot matrix developer accents. Structured as a native KDE Wallpaper Package (`/usr/share/wallpapers/Sydra/contents/images/3840x2160.png`, `metadata.json`, and `screenshot.png`). Packaged into `siddha-branding-0.1.0-4`.
  - **Black Screen Resolution**: Removed disruptive dynamic `plasma-apply-lookandfeel` reload from `siddha-desktop-init`, pre-seeded `plasma-org.kde.plasma.desktop-appletsrc` into `/etc/skel` and `/home/live`, and added DBus readiness check. Built `siddha-theme-0.1.0-5`.
  - **Complete Local Repository**: Rebuilt `siddha.db.tar.zst` and `siddha.db.tar.gz` ensuring all 10 packages (`calamares`, `siddha-branding`, `siddha-calamares-config`, `siddha-dev`, `siddha-gamehub`, `siddha-gpu-setup`, `siddha-keyring`, `siddha-settings`, `siddha-theme`, `siddha-welcome`) are properly indexed.
  - **ISO Build & QEMU Verification**: Rebuilt production release ISO `build/out/sydra-os-2026.11.15-x86_64.iso` (4.1 GiB). SHA-256: `80cd531626e62f1f12223720cd10275f865e657ce06ff6e635f476ec0a331b10`. Includes full 45-game Sydra Game Hub catalog (`siddha-gamehub-0.1.0-3`), glassmorphism stack (Kvantum dark glass engine, `kwinrulesrc` window opacity, `kwinrc` blur & translucency effects, and floating frosted glass panels with `translucencyMode=1`).
  - Verified live boot in QEMU: Clean desktop loaded with Sydra Obsidian Waves wallpaper, floating translucent top bar, left floating capsule dock with Sydra Game Hub launcher, and traffic light window controls. Captured screenshot saved to `~/Pictures/sydra-os-gui.png`.

### T7.4 40+ Curated Native Linux & Steam Games Catalog
- Status: DONE
- Date: 2026-11-15
- Target: Curate 40+ verified native Linux games in `catalog/native-games.yaml` with offline metadata (genre, badge, package/steam ID, license, launch notes).
- Result:
  - Curated 45 verified games across open-source native Linux titles (SuperTuxKart, Xonotic, 0 A.D., OpenTTD, Battle for Wesnoth, Mindustry, OpenRA, Luanti, SuperTux, Endless Sky, Teeworlds, Hedgewars, Warzone 2100, Simutrans, Cataclysm: DDA, Naev, Armagetron, Widelands, Freeciv, FreeCol, FreedroidRPG, AstroMenace, Dwarf Fortress, DCSS, NetHack, Shattered Pixel Dungeon, Empty Epsilon, Knights, KMines, KPatience) and native Steam hits (Counter-Strike 2, Dota 2, Team Fortress 2, Portal 2, Half-Life 2, Left 4 Dead 2, Factorio, Hollow Knight, Dead Cells, Celeste, Stardew Valley, Terraria, Valheim, Slay the Spire, RimWorld).
  - Validated offline badge parsing via `python3 siddha-gamehub.py --dump-badges` (45/45 verified).
  - Built `siddha-gamehub-0.1.0-3` and updated repository index.
  - Updated `tests/smoke-live.sh` with new asset checks.

### T2.5 Calamares Unpackfs & Installer Environment Hardening
- Status: DONE
- Date: 2026-11-15
- Target: Resolve Calamares unpackfs failure ("Failed to find unsquashfs, make sure you have the squashfs-tools package installed"), preserve environment PATH for Calamares under sudo, resolve bash package conflict, and optimize build compression.
- Result:
  - **Unpackfs & Toolchain**: Bundled `squashfs-tools` (providing `/usr/bin/unsquashfs`), `parted`, and `gptfdisk` into `packages/base.txt` and `packages/live-only.txt`.
  - **Calamares Environment**: Updated `/usr/local/bin/siddha-installer` and `/etc/sudoers.d/g_wheel` (`env_keep += "PATH"`) to preserve root PATH under `sudo -E`.
  - **Packaging Conflict Resolution**: Resolved file conflict between `bash` and `siddha-settings` over `/etc/skel/.bashrc` by migrating defaults into `/etc/profile.d/siddha.sh` (built package `siddha-settings-0.1.0-4`).
  - **Build Speedup**: Tuned `iso/profile/profiledef.sh` with `-comp zstd -Xcompression-level 3 -b 1M`, reducing squashfs compression time from ~5 hours to ~4 minutes.
  - **Release ISO**: Successfully built `build/out/sydra-os-2026.11.15-x86_64.iso` (4.2 GiB).
    - SHA-256: `c4372e0379ab9ee24ce1594c3085cd33470cd0f75d022d36f2bc891d6f548a3f`.
    - Bundles `siddha-theme-0.1.0-7` (Force opacity rules, OpenGL compositing, kvantum lookandfeel default) and `squashfs-tools-4.7.5-1` (`unsquashfs`).

### T4.10 Brand Assets from Sydra Logo & Master Plan 2.0 Integration
- Status: DONE
- Date: 2026-11-19
- Target: Integrate official Sydra OS glass prism logo (`assets/logo/sydra-logo.svg`), generate all brand variants deterministically (PNGs 16–512, multi-res favicon.ico, monochrome white/dark SVGs, horizontal lockup), update brand palette (`#12141A`, `#5B8DEF`, `#4FB3BF`), and update Calamares/branding packages.
- Result:
  - Saved official logo to `assets/logo/sydra-logo.svg`.
  - Created `tools/brandgen.sh`: generated PNG sizes 16, 24, 32, 48, 64, 128, 256, 512, `favicon.ico`, monochrome white/dark SVGs, and horizontal lockup `sydra-logo-lockup.png` / `.svg`.
  - Updated `tokens/glass.json` with brand palette: base `#12141A`, primary `#5B8DEF`, secondary `#4FB3BF`.
  - Updated `siddha-calamares-config` (pkgrel 9): installed official logo to Calamares branding and updated `branding.desc` with brand color scheme.
  - Updated `siddha-branding` (pkgrel 5): packaged hicolor scalable SVG, standard PNG resolutions (16–512), pixmaps, and horizontal lockup.
  - Updated `siddha-theme` (pkgrel 7): enforced active/inactive window opacity (85%/80%), enabled OpenGL compositing in kwinrc, and set kvantum style default.
  - Updated `AGENTS.md` and `docs/MASTER_PLAN.md` to version 2.0.
  - Successfully built Release ISO: `build/out/sydra-os-2026.11.19-x86_64.iso` (4.2 GiB).
    - SHA-256: `6eefb90dd294a26334926ac1eedf441ecea4b851f970c8e9d857fee27a34d44b`.

---

### T8.4 OS Architecture Comparison & Distribution Hardening Audit
- Status: DONE
- Date: 2026-11-19
- Target: Audit Sydra OS package sets and architecture against tier-1 open-source distributions (Arch releng, EndeavourOS, Pop!_OS, CachyOS). Identify and eliminate missing core hardware utilities, wireless stacks, font metrics, permission bugs, and live environment leaks.
- Result:
  - **Core Utilities**: Added `pciutils` (lspci), `usbutils` (lsusb), `diffutils` (diff/cmp), `nvme-cli` (SSD health), `xdg-utils` (xdg-open/mime), `mesa-utils` (glxinfo/glxgears).
  - **Wireless & Network**: Added `wpa_supplicant` (NetworkManager WPA2/WPA3 engine) and `wireless-regdb` (regulatory channel unlocker for 5GHz/6GHz Wi-Fi).
  - **Laptop Power & Display**: Added `brightnessctl` (backlight control without root) and `upower` (power/battery enumeration for COSMIC panel applet).
  - **Typography & Compatibility**: Added `ttf-liberation` (standard Arial/Times/Courier metrics for Web and Proton) and `ttf-dejavu`.
  - **Security & Polkit**: Fixed Polkit SUID bit (`chmod 4755 /usr/lib/polkit-1/polkit-agent-helper-1`), stripped live-only passwordless wheel rule (`49-nopasswd_global.rules`) from target installs, and sanitized `/etc/pacman.conf` to avoid broken local build URLs on target systems.
  - **Boot Speed & Systemd Services**: Masked `systemd-loop@.service` to prevent bogus loopback block device attach failures on `/dev/sr0`, purged `systemd-time-wait-sync.service` from `sysinit.target.wants` to eliminate indefinite boot hangs waiting for NTP before desktop launch, and cleaned dangling `cloud-init` symlinks.
  - **Time Synchronization**: Enabled `systemd-timesyncd.service` on installed system.
  - Built `siddha-calamares-config-0.1.0-15` with silent bootloader parameters and `siddha-settings-0.1.0-5` with guarded shell profiles.
  - Rebuilt production ISO `build/out/sydra-os-2026.11.19-x86_64.iso` (4.5 GiB). SHA-256: `cf672a3cdc196c03aeb04594d43315f9a90ab7585aea0cc588c21f7867f30fd2`.
  - **Silent Boot & Clean Console**: Configured `quiet loglevel=3 udev.log_level=3 systemd.show_status=false rd.systemd.show_status=false vt.global_cursor_default=0` across UEFI (`systemd-boot`, GRUB) and BIOS (`syslinux`), added `/etc/systemd/system.conf.d/10-quiet.conf` (`ShowStatus=no`), masked `getty@tty1.service` and `kmsconvt@tty1.service` to prevent VT1 display manager contention, purged legacy systemd-networkd wait-online drop-ins and sockets in favor of NetworkManager, removed 7 dangling VM daemon symlinks (Hyper-V, VirtualBox, VMware), purged `systemd-udev-settle` alsa-unmuter dependency, removed dangling `resolv.conf` to restore clean NetworkManager DNS, and optimized `siddha-desktop-init`.
  - **Dynamic QEMU Memory Management**: Added dynamic memory scaling to `scripts/qemu-test.sh` based on `/proc/meminfo` available memory and `-overcommit mem-lock=off`, preventing out-of-memory aborts on lower-memory host environments. Interactive UEFI boot verified working directly into COSMIC Live Desktop.

---

## HUMAN ACTIONS NEEDED
- **Interactive QEMU GUI Testing (Laptop A)**:
  Run in terminal to test the installer UI interactively:
  ```bash
  make qemu-uefi
  ```
- **Physical USB Flash for Hardware Testing (Laptop B / Nitro RTX 5050)**:
  Insert a USB pendrive (<= 256GB), check device name with `lsblk`, then run:
  ```bash
  sudo scripts/flash-usb.sh build/out/sydra-os-2026.11.19-x86_64.iso /dev/sdX  # replace /dev/sdX with USB drive (e.g. /dev/sdb)
  ```
  *(Current Release ISO SHA-256: `cf672a3cdc196c03aeb04594d43315f9a90ab7585aea0cc588c21f7867f30fd2`)*
