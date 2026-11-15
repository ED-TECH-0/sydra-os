# Technical Decisions & Verified Facts

Format:
`[DATE] [DECISION/VERIFICATION ID]: Summary`
- Context
- Evidence / Command output
- Chosen path

---

### [2026-11-13] DEC-001: Distro Naming & Identity Split
- **Context**: User requested public name `sydra` but real name `siddha` used inside Linux, hidden on public.
- **Decision**: 
  - Public facing: "Sydra OS", `sydra-os-*.iso`, ISO label `SYDRA_YYYYMM`, welcome app, Plymouth splash, Calamares title.
  - Internal system: `siddha` identifier for package namespace (`siddha-*`), local repository `[siddha]`, directory paths `/etc/siddha/`, `/usr/share/siddha/`.

### [2026-11-13] DEC-002: Build Host Environment Verification (Laptop A)
- **Host**: HP EliteBook 850 G5 running EndeavourOS.
- **Kernel**: `Linux 7.2.15-arch1-1 #1 SMP PREEMPT_DYNAMIC x86_64`.
- **CPU**: `Intel(R) Core(TM) i5-8350U CPU @ 1.70GHz` (4 cores, 8 threads, Intel UHD 620 graphics).
- **RAM**: `7.1 GiB` total. (Per D2 rule: build with a disk work directory, never in tmpfs, and use 2 GB RAM for QEMU VM runs).
- **Disk Free**: `224 GiB` available on `/dev/nvme0n1p2` (exceeds the 25 GB minimum requirement).
- **KVM Virtualization**: `/dev/kvm` present with read/write access.

### [2026-11-13] DEC-003: Core Package Availability Verification
- Verified against official sync databases (`core`, `extra`, `multilib`, `endeavouros`):
  - `archiso`: Available in `extra` (v92-1)
  - `devtools`: Available in `extra`
  - `qemu-desktop`: Available in `extra`
  - `edk2-ovmf`: Available in `extra`
  - `ckbcomp`: Available in `endeavouros` repository
  - `kpmcore`: Available in `extra`
  - `[multilib]` is already enabled in host `/etc/pacman.conf`.

### [2026-11-13] DEC-004: Filesystem Overlay for os-release and issue
- **Context**: `/usr/lib/os-release` and `/etc/issue` are owned by Arch's core `filesystem` package. Including them directly in `siddha-branding` caused pacman transaction conflict during `airootfs` generation.
- **Decision**: Overlay `/etc/os-release` and `/etc/issue` directly via `iso/profile/airootfs/etc/`. `siddha-branding` retains backup/reference copies at `/usr/share/siddha/branding/`.

### [2026-11-13] DEC-005: Calamares 3.4.2 Qt6 Packaging
- **Context**: Calamares is not in official Arch core/extra repositories. Needs native compilation for Qt6 installer integration.
- **Decision**: Compiled `calamares` 3.4.2 natively using CMake, Ninja, and Qt6 against `kpmcore` 26.08 and `libpwquality`. Packaged and hosted inside the local `[siddha]` pacman repository with custom module overrides (`unpackfs` targeting `/run/archiso/bootmnt/sydra/x86_64/airootfs.sfs`).


### [2026-11-15] DEC-006: Target Kernel & Initcpio Decoupling in Calamares
- **Context**: Archiso's `mkarchiso` build process strips all files from `${pacstrap_dir}/boot` before squashing `airootfs.sfs`, placing `vmlinuz-linux` on the outer ISO medium (`/sydra/boot/x86_64/`). Additionally, live drop-in `/etc/mkinitcpio.conf.d/archiso.conf` was leaking into the target root, causing `mkinitcpio -P` to look for live-only netboot binaries.
- **Evidence**: `mkinitcpio -P` inside target failed with `ERROR: Invalid option -k -- '/boot/vmlinuz-linux' must be readable`.
- **Decision**: 
  1. `siddha-installer` stages kernel and microcode at `/run/archiso/bootmnt/sydra/boot/` before Calamares begins.
  2. `siddha-initcpio-fix` runs via `shellprocess@initcpio-fix` inside the chroot, strips `archiso.conf` and `archiso.preset`, and guarantees `/boot/vmlinuz-linux` is copied directly from `/usr/lib/modules/*/vmlinuz` with `0644` permissions if missing or empty.
  3. Microcode images (`intel-ucode.img`, `amd-ucode.img`) are verified and copied to `/boot/`.

### [2026-11-15] DEC-007: KDE Plasma 6 System-Wide Glassmorphism Defaults
- **Context**: Newly created users and the live session booted with unstyled default Breeze without glassmorphism or blur active.
- **Decision**: Package system-wide XDG configuration overrides (`/etc/xdg/kdeglobals`, `/etc/xdg/kwinrc`, and GTK 3/4 CSS) inside `siddha-theme`. This enables KWin blur, translucency on dialogs and menus, Inter UI font, JetBrains Mono fixed font, and SiddhaGlassGraphite theme by default on all sessions.

### [2026-11-15] DEC-008: SDDM Wayland Compositor & Live User Initialization
- **Context**: Plasma Wayland session froze on boot with black screen / hang when running autologin.
- **Evidence**: 
  - SDDM running with `DisplayServer=wayland` defaulted to searching for `weston --shell=kiosk`. Because `weston` was not installed, SDDM greeter crashed before launching the user session.
  - `/home/live` did not exist in `airootfs`, causing Plasma Wayland and KWin to fail when writing XDG socket and runtime configuration files.
  - KWallet prompted interactively on startup, blocking session completion.
- **Decision**: 
  1. Set `CompositorCommand=kwin_wayland --drm --no-lockscreen --no-global-shortcuts --locale1` under `[Wayland]` in `/etc/sddm.conf.d/autologin.conf`.
  2. Pre-create `/home/live` in `airootfs` and configure `/etc/tmpfiles.d/siddha-live-user.conf` to guarantee `0750` ownership by user `live` (UID 1000).
  3. Pre-seed `/etc/skel/.config/kwalletrc` with `[Wallet] Enabled=false`.
  4. Ensure `nopasswdlogin:x:999:live` exists in `/etc/group` for SDDM autologin PAM authentication.

### [2026-11-15] DEC-009: Mac-Style Traffic Light Window Controls & Glass Themes
- **Context**: User provided reference images displaying smoked frosted glass windows with circular Red/Yellow/Green traffic-light controls on the top-left, 3D metallic torus wallpaper, and high background blur.
- **Decision**: 
  1. Configure `kwinrc` with `ButtonsOnLeft=XIA` (Close, Minimize, Maximize) and `ButtonsOnRight=` with `BorderSize=None`.
  2. Configure GTK 3/4 settings with `gtk-decoration-layout=close,minimize,maximize:`.
  3. Provide full 13-section color schemes (`SiddhaGlassGraphite`, `SiddhaGlassMidnight`, `SiddhaGlassSlateLight`, `SiddhaGlassHighContrast`) compliant with Qt6 and Plasma 6 requirements.
  4. Package 3D metallic torus (`sydra-metallic-torus.svg`) and vibrant cyber frost (`sydra-cyber-frost.svg`) wallpapers, with `siddha-desktop-init` applying the metallic torus theme automatically on session start.
