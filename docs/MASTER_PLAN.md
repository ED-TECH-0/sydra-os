# SYDRA OS — MASTER BUILD PLAN (for AI coding agents)

- Document version: 2.0 (2026-11-18): renamed to Sydra OS, COSMIC as main desktop, logo and brand added
- Owner: E (solo developer, no team)
- Audience of this file: an AI coding agent (Antigravity/Gemini, Hermes agent with an NVIDIA-hosted model, or any other). Read it carefully before doing anything.
- Project: **Sydra OS** — an Arch-based Linux distribution for **developers and gamers**, with a professional glassmorphism desktop built on **COSMIC** (System76's Rust-based desktop). KDE Plasma is an optional, later edition (Appendix K).

---

## 0. HOW TO USE THIS FILE

1. Read sections 1–7 fully (once per project; see 2.4 for context-saving rules). They define the product, the hardware, the rules and the architecture. They are binding.
2. Work through section 8 (phases and tasks) **in order**. Every task has an ID (for example `T2.3`), steps, and a `DONE WHEN` acceptance test.
3. Do not start the next task until the current task's `DONE WHEN` passes. Record the result in `docs/PROGRESS.md` (task ID, date, commands run, result, problems).
4. Anything marked `VERIFY:` is something this plan is not sure about (package name, flag, file path, API). **Do not guess.** Check with `pacman -Si`, `pacman -F`, `paru -Si`, `man`, the Arch Wiki, or upstream documentation, then write what you found in `docs/DECISIONS.md`.
5. If a task cannot be completed after 3 honest attempts, stop, write the problem, what you tried, and your best hypothesis into `docs/BLOCKERS.md`, then continue with any task that does not depend on it.
6. Only ask the human (E) when: (a) a physical action is needed (plug in USB, change BIOS, press a key), (b) a decision from section 14 is needed, or (c) a command would risk data loss. Do not ask routine check-ins. E dislikes repeated check-ins and short, abbreviated replies: report fully, but without padding.
7. Never claim something works unless you ran it and saw the result. Paste the real output (trimmed) into `docs/PROGRESS.md`.

---

## 1. PRODUCT DEFINITION

### 1.1 Names
- Public name: **Sydra OS**. Identifier in code, packages and file names: `sydra` (for example `sydra-theme`, `sydra-welcome`, repo `[sydra]`, ISO `sydra-os-YYYY.MM.DD-x86_64.iso`, label `SYDRA_YYYYMM`).
- History: the working names were "Siddha OS" and "Sida OS". **Do not use either in new code, packages or public text.** (Reason: "SIDA" means AIDS in Spanish, French and Portuguese.) "Siddha" remains the cultural root for the later Tamil layer (Phase 10) and for the separate Siddha processor research track; it is no longer the product name.
- Name safety (task T0.6): a quick web search on 2026-11-18 found no Linux distribution called "Sydra", but similar names exist (for example HydraPWK, Lyra OS, SlyOS), so a proper check is still required before public release.

### 1.2 Target users (in priority order)
1. Developers (web, systems, security) who want a ready workstation.
2. Gamers who want Windows games to run on Linux with minimal setup.
3. People worldwide. **The first release is NOT Tamil-first.** Tamil identity (language pack, Tamil games, Siddha story) is a later layer (Phase 10). Keep internationalization clean now (gettext/Qt translation files, standard locales, full Unicode fonts) so that layer is easy later.

### 1.3 One-line positioning
> A professional glass desktop for people who build things and play games.

### 1.4 Look and feel: "Sydra Glass Pro"
- Fully glassmorphism **but professional, not colorful**: graphite/near-black frosted glass, white text, **one** muted accent color (default cool blue/teal).
- Glass is used for structure (top panel, floating dock, menus, sidebars, notifications, launcher, terminal). Code editors and games stay almost opaque.
- The reference layout (from the owner's mock-up screenshot): thin translucent top bar (menus left; Wi-Fi, Bluetooth, volume, battery, clock right); floating rounded bottom dock (Terminal, Firefox, Files, VS Code, Settings, Trash); rounded translucent windows with centered titles; system monitor and file manager styled as glass.
- The screenshot is a concept render and cannot be copied exactly. Reproduce its structure and feel.
- **Desktop decision (made by E):** COSMIC is the main desktop; KDE Plasma is an optional edition. Reasons: the audience is developers, builders and gamers, and COSMIC has built-in frosted glass, built-in tiling and a Rust-based, lightweight design. E knowingly accepts that COSMIC is young and has bugs and plans to fix them through updates. Agents must respect this decision and must not switch the main desktop back to KDE.
- COSMIC mapping of the reference layout: top panel (workspaces, applications launcher, clock, status area with network/Bluetooth/sound/battery/power) and a bottom dock (pinned apps), both provided by `cosmic-panel`; windows use COSMIC's Frosted Glass appearance option. COSMIC has no KDE-style global menu bar, so the "Applications / Places / System" menu text of the screenshot becomes the launcher button plus the Files app.

### 1.5 v0.1 "Gaming + Dev Preview" scope (what must exist)
1. Bootable ISO (BIOS and UEFI) that boots a live COSMIC (Wayland) session.
2. Calamares installer that installs a working system (Btrfs default, ext4 option).
3. Sydra Glass theme built on COSMIC's built-in Frosted Glass (panel, dock, windows, terminal, login screen, wallpapers) with matching colors for GTK and Qt apps.
4. Gaming stack preconfigured (Steam, Proton-GE, Lutris, Heroic, gamemode, MangoHud, gamescope) and automatic GPU driver setup (NVIDIA, AMD, Intel, hybrid laptops).
5. Developer stack preconfigured (shell, editors, toolchains, containers).
6. Welcome app (first-run) and Game Hub MVP (native vs Proton vs anti-cheat-blocked badges).
7. Signed checksums, release notes, known-issues list.

### 1.6 Explicit non-goals for v0.1
Tamil language pack, Agatiyan agent, Rust Tamil syscalls, Pallanguzhi scheduler, custom kernel, bspwm "Lite" edition, KDE Plasma optional edition (Appendix K), ARM builds, AppArmor profiles, own mirror network. These come after real users exist.

### 1.7 Brand and logo (provided by E)

The official logo is **`assets/logo/sydra-logo.svg`** (provided by E). It is the single source of truth: never redraw it, trace it, or recolor it by hand. Generate every other format from it (T4.10).

- **What it shows:** a dark glass hexagonal capsule (graphite `#12141A`, about 55% opacity) with a soft blue ambient glow, two inner prism facets (top right in blue `#5B8DEF`, bottom left in teal `#4FB3BF`), a faint glass ribbon in the center, and a thin white specular edge. The shape reads as a glass "S" and as a prism: it matches the "professional glass" identity.
- **Brand palette (use these exact values everywhere):**

| Role | Color | Where it is used |
|---|---|---|
| Base / graphite | `#12141A` | Glass tint of the Graphite preset, backgrounds, login screen, website dark mode |
| Primary accent (blue) | `#5B8DEF` | Default accent color in COSMIC, links, selection, focus rings, Game Hub `NATIVE` badge |
| Secondary accent (teal) | `#4FB3BF` | Midnight preset accent, small highlights, charts |
| Text / highlight | `#F2F4F8` on dark, `#12141A` on light | Body text |

- **Rules:** keep clear space around the logo of at least one eighth of its width; minimum size 16 px (use the simplified favicon variant below 32 px); do not stretch, rotate, add text inside, add drop shadows, or change the gradient colors; on light backgrounds use the dark-on-light variant; the full-color logo is used on dark or mid-tone backgrounds.
- **Variants to generate (T4.10):** full-color SVG and PNG sizes 16/24/32/48/64/128/256/512; simplified favicon (no glow, thicker strokes); single-color white and single-color dark versions; horizontal lockup (logo + "Sydra OS" in Inter semibold); square app icon with transparent background.
- **Where the logo appears:** installer (Calamares), GRUB boot menu, login screen/greeter if supported, About/Settings screens through `os-release`, launcher icon, Welcome app, Game Hub window icon, fastfetch, wallpapers (optional small watermark), website header and favicon, README, release notes.
- **Licensing:** the logo is E's original work. Record this in `docs/LICENSES.md` (suggested: all rights reserved for the name and logo, code under GPL; decide in T0.6).

---

## 2. THE OWNER'S RESOURCES AND CONSTRAINTS

### 2.1 Hardware and accounts

| Item | Details | Role in this project |
|---|---|---|
| Laptop A: EliteBook 850 G5 | Intel UHD 620 graphics, 256 GB storage, runs **EndeavourOS** (Arch-based). Has an NVIDIA API key. | **BUILD MACHINE.** All archiso builds, package-repo builds, QEMU tests. Also the low-end test target: if glass runs acceptably on UHD 620, it runs anywhere. |
| Laptop B: Nitro V 15 | RTX 5050 8 GB VRAM, Intel i5 13th gen H, 16 GB RAM (stated earlier), 512 GB storage, runs **Windows** with the Hermes agent. Has an NVIDIA API key and Antigravity (Google Gemini Pro plan via Jio). | **GPU/GAMING TEST LAB** and UI/app development machine. Windows stays the main OS. |
| Phone: Poco X6 Pro | 512 GB. Provides a **mobile hotspot** for both laptops. | The only internet link. Treat bandwidth as limited and variable. |
| Pendrive | One only (size unknown; assume 16 GB or more, plan for 8 GB). | Boot media for both laptops. |

### 2.2 What this implies (binding design decisions)

1. **Archiso must be built on Arch.** Build only on Laptop A (EndeavourOS). The Windows laptop cannot build the ISO. Do not attempt WSL-based ISO builds.
2. **Do not install over Laptop A.** It is the only build machine. Test installs on Laptop A happen only inside QEMU virtual disks. Physical installs happen on Laptop B only after E approves (see T9.3).
3. **Laptop B's Windows must be protected.** Never modify its partitions. Before E changes BIOS settings or partitions, E must back up the BitLocker recovery key (if BitLocker/Device Encryption is on) and important files. Disabling Secure Boot or changing boot order can trigger a BitLocker recovery prompt.
4. **Bandwidth is scarce.** Download each package once. Reuse caches. Move files between the two laptops over the local network or the pendrive, never by downloading twice (see section 7.4 and 12).
5. **Disk on Laptop A is tight (256 GB).** Keep at least 25 GB free before every build. Delete the archiso work directory after each build. Keep VM disk images small (20–30 GB sparse).
6. **One pendrive.** Use **Ventoy** on it so ISOs can be copied as ordinary files, and keep a second normal partition for logs/files. Do not repeatedly `dd` unless Ventoy fails to boot an ISO.
7. **Secure Boot.** archiso ISOs are not signed for Secure Boot. Test machines need Secure Boot off (or Ventoy key enrollment). Document this in release notes.
8. **Hybrid graphics.** Laptop B has Intel iGPU plus NVIDIA dGPU: use PRIME render offload. Do not assume a MUX switch.
9. **Solo developer with AI agents.** Prefer simple, boring, well-documented technology. Every script must be idempotent and logged. Prefer small commits.

### 2.3 AI agent roles (the agents E actually has)

E has three AI resources: **Antigravity** (Google's agentic IDE, Gemini Pro plan via Jio), the **Hermes agent** (installed on the Windows laptop), and an **NVIDIA API key** (hosted models). There is no Claude Code. Default split:

| Resource | Where it runs | Default responsibilities |
|---|---|---|
| **Antigravity (Gemini Pro)** — PRIMARY BUILDER | **Laptop A (EndeavourOS)**. Install Antigravity on Laptop A (`VERIFY:` official Linux download/package and that it runs on EndeavourOS; if the AUR is used, read the PKGBUILD first). | Build system, package repo, Calamares config, theme packaging, scripts, running builds and QEMU tests, git. This is the only agent that runs `make iso`. |
| **Hermes agent** (model served by the NVIDIA API) | **Laptop B (Windows)** | Game Hub and Welcome app (Python/PySide6, Phase 7), native game catalog, documentation, writing up test results E collects from Live-USB sessions, code review. |
| **NVIDIA API key** | Backend for Hermes, and fallback for any tool that accepts an OpenAI-compatible endpoint | Read the key from the environment variable `NVIDIA_API_KEY`. `VERIFY:` current base URL (OpenAI-compatible) and the best available coding model names at build.nvidia.com; choose the strongest coding/agentic model offered and record the choice in `docs/DECISIONS.md`. |

Optional: if Hermes supports an SSH terminal backend (`VERIFY:` in Hermes documentation), it may drive Laptop A over SSH. This is an extra convenience, not a requirement. If used, create a dedicated non-root user on Laptop A, require key-based login, and do not give that user passwordless root.

Rules for multi-agent work:
- **Git is the single source of truth.** Both laptops work in clones of the same repository and sync through a remote (GitHub/GitLab) or through a bare repo on the pendrive.
- Only the build machine (Laptop A) produces official ISOs.
- One agent per task at a time. Claim a task by writing `CLAIMED by <agent> on <date>` in `docs/PROGRESS.md` and committing.
- **API keys never go into the repository** (see rule 3 in section 4).

### 2.4 Working safely and effectively with these agents

1. **Command approval stays ON.** In Antigravity, set terminal command execution to the mode that asks for review before running commands (`VERIFY:` the exact setting name in the current version). Never use a fully automatic mode on Laptop A: it holds the build environment, and the Golden Rules (section 4) concern disks. Allow-list only harmless commands (`ls`, `cat`, `git status`, `pacman -Si`).
2. **Context economy.** This file is long. An agent does **not** need to hold all of it at once: read sections 0–7 once, then load only the section of the **current phase** plus the templates it names in section 9. Re-read section 4 (Golden Rules) at the start of every session.
3. **Small steps.** Open-source models served through the NVIDIA API can be weaker at long autonomous runs than frontier agents. Work one task at a time, run one or two commands at a time, read the real output before the next command, and stop after each `DONE WHEN`.
4. **Fresh session per phase.** Start a new chat/session at each phase boundary and begin it with: the repo's `AGENTS.md` (see 15.0), the tail of `docs/PROGRESS.md`, and the phase text. The files, not the chat history, carry the memory.
5. **Cross-check risky output.** Use the other agent as reviewer for: shell scripts that touch disks, Calamares configs, package signing, and anything marked `VERIFY:`. Reviewer writes findings to `docs/REVIEW_<date>.md`; the builder applies fixes.
6. **Quota awareness.** Antigravity (Gemini Pro plan) has usage limits that can run out mid-task. Save state in `PROGRESS.md` before long operations so another agent can resume. Switch to the Hermes + NVIDIA route when the Antigravity quota is exhausted.
7. **Never paste secrets into any agent chat.** That includes the NVIDIA key, the GPG private key, Wi-Fi passwords and BitLocker recovery keys.

---

## 3. GLOSSARY (so every agent uses the same words)

- **archiso**: Arch's tool (`mkarchiso`) that builds a live ISO from a "profile" directory.
- **profile**: directory with `profiledef.sh`, `pacman.conf`, `packages.x86_64`, `airootfs/`, boot configs.
- **airootfs**: files overlaid onto the live system's root filesystem.
- **Calamares**: graphical installer framework (not in official Arch repos; built from AUR sources).
- **Own repo / `[sydra]`**: our pacman repository of custom-built packages (Calamares, theme, apps).
- **Proton / Proton-GE**: Valve's / community's Wine-based compatibility layers for Windows games.
- **PRIME offload**: run a specific app on the NVIDIA GPU while the Intel GPU drives the display.
- **Glass tokens**: the single file defining blur, opacity, radius, accent for every themed surface.
- **COSMIC**: System76's desktop environment, written in Rust with the iced toolkit (libcosmic). Its first stable series is called **Epoch 1** (versions 1.x). Compositor: `cosmic-comp` (built on Smithay). Panel and dock: `cosmic-panel`. Login manager: `cosmic-greeter` (based on greetd). Settings: `cosmic-settings`. Config files live under `~/.config/cosmic/` (`cosmic-config`).
- **Frosted Glass**: COSMIC's built-in appearance option that gives panels and windows a translucent blurred look.

---

## 4. GOLDEN RULES (BINDING; VIOLATING THESE IS A FAILURE)

1. **Never write to a block device directly** except through `scripts/flash-usb.sh`, which refuses non-removable devices. Never run `dd`, `mkfs`, `parted`, `fdisk`, `wipefs`, `cfdisk` or `sgdisk` against any real device in agent-run commands. Virtual disk images in QEMU are fine.
2. **Never touch the Windows partitions on Laptop B**, and never touch the EndeavourOS system partitions on Laptop A.
3. **No secrets in git.** API keys, tokens and passwords live only in environment variables or in a local untracked `.env` file. The repo must contain `.env.example` and a pre-commit secret scan (`gitleaks`, `VERIFY:` package availability). If a secret is ever committed, stop, tell E, and rotate the key.
4. All shell scripts start with `#!/usr/bin/env bash` and `set -euo pipefail`, are idempotent (safe to run twice), print what they do, and log to `build/logs/`.
5. **One logical change per commit.** Commit messages use the style `area: short summary` (for example `iso: enable multilib in pacman.conf`).
6. The ISO must always be buildable from a clean checkout with `make iso`. If a change breaks that, fix or revert before doing anything else.
7. **Third-party repositories:** the only repositories in the final ISO are Arch official repos (`core`, `extra`, `multilib`) and our own `[sydra]` repo. Chaotic-AUR may be used only as a documented temporary fallback and must be removed from release builds.
8. **Check disk space first:** `df -h .` must show at least 25 GB free before building.
9. **Save bandwidth:** never run `pacman -Scc`, never delete `/var/cache/pacman/pkg` on the build machine, always use the shared package cache (section 7.4).
10. **Privilege:** use `sudo` only for `mkarchiso`, `pacman`, mounting loop devices, and the flash script. Build packages with `makepkg` as a normal user inside a clean chroot (`devtools`).
11. **No telemetry, no analytics, no phone-home** in any Sydra component.
12. **Verify before claiming.** Do not invent package names, options or file paths. Use `VERIFY:` items and record the proof.
13. **Licenses:** record the license of every third-party asset (themes, icons, wallpapers, fonts) in `docs/LICENSES.md`. Do not include assets with unclear licenses. Do not use Valve, Steam, Arch, KDE or other trademarks as Sydra's own branding. Original Sydra code: GPL-3.0-or-later unless a file says otherwise.
14. **Never run unknown scripts from the internet** with `curl | bash` on the build machines.

---

## 5. ARCHITECTURE DECISIONS (LOCKED FOR v0.1)

| Area | Decision | Reason / note |
|---|---|---|
| Base | Arch Linux, built with archiso, starting from a **copy of the official `releng` profile** (`/usr/share/archiso/configs/releng/`) | Proven boot configs; don't hand-write boot loader files. |
| Kernel (Phase 1–3) | Stock `linux` | Fewest moving parts while the installer is being built. |
| Kernel (Phase 4+) | `linux-zen` (+ `linux-lts` as fallback in the installed system) from official repos | Gaming-friendly, no third-party repo. `linux-cachyos` can come later via our own repo. Kernel swap is a high-risk task (see T3.6). |
| Desktop | **COSMIC (Epoch 1.x) on Wayland**, installed from Arch packages (`cosmic-session` or the `cosmic` group) | E's decision. Built-in Frosted Glass, tiling, VRR support. Young: expect bugs; track them (Phase 3 intro). Optional later: KDE Plasma edition (Appendix K). |
| Keyring | `gnome-keyring` | The Arch Wiki notes COSMIC has no secrets store of its own. |
| Display manager | `cosmic-greeter` (greetd-based; enable `cosmic-greeter.service`) | Native to COSMIC. Limited theming; keep customization small. |
| Installer | Calamares from our own repo | Not available in official repos. |
| Bootloader (installed system) | GRUB (+ `grub-btrfs`) | Wide hardware compatibility; snapshot boot entries. |
| Filesystem | Btrfs default (subvolumes for `@`, `@home`, `@log`, `@pkg`, `@snapshots`), ext4 option; Snapper + `snap-pac` for pre/post-update snapshots; ZRAM swap | Safe rollback on a rolling distro. |
| Audio | PipeWire (+ WirePlumber, pipewire-pulse, pipewire-alsa) | Standard. |
| Network | NetworkManager | Standard; works with COSMIC's network applet. |
| Package managers | pacman, `paru` (AUR helper, from our repo), Flatpak (Flathub enabled) | |
| Firewall | `firewalld`, enabled by default; simple on/off and status in the Welcome app (a GUI such as `firewall-config` is optional, `VERIFY:`) | Security by default. |
| Theme engine | COSMIC theme/config files (`~/.config/cosmic/`) + Frosted Glass option + GTK CSS overrides + Qt styling (`qt6ct` + Kvantum) + terminal profile | One token file generates them all (`tools/glassgen.py`, one module per target so a COSMIC theming-engine change in a later Epoch only affects one module). |
| Icons / cursors / fonts | Papirus icons; a clean cursor theme (`VERIFY:` license); Inter (UI), JetBrains Mono (code), Noto fonts (coverage incl. Tamil, CJK, emoji) | Fonts must cover all scripts for later i18n. |
| Game Hub | **Python 3 + PySide6 (Qt 6)** for v0.1, JSON/YAML catalog, packaged as `sydra-gamehub` | Fastest for a solo developer with AI agents. Qt apps will not get COSMIC's native look automatically (see T4.5). A rewrite in Rust with libcosmic is a good later option because it would look native on COSMIC. |
| Welcome app | Python 3 + PySide6, package `sydra-welcome` | Same toolchain as Game Hub. |
| Dev Hub | Shell CLI `sydra-dev` (menu via `gum`, `VERIFY:` package) | Simple and scriptable. |
| Release hosting | SourceForge and/or Internet Archive + torrent; GitHub for source | `VERIFY:` GitHub release assets are limited to 2 GiB per file; the ISO may exceed that. |

---

## 6. REPOSITORY LAYOUT (CREATE EXACTLY THIS IN T0.1)

```
sydra-os/
├── README.md
├── LICENSE                      # GPL-3.0-or-later for original code
├── Makefile
├── .gitignore                   # build/, *.iso, .env, *.pkg.tar.*, work/, out/
├── .env.example                 # names of variables only, no values
├── .pre-commit-config.yaml      # gitleaks + shellcheck
├── docs/
│   ├── MASTER_PLAN.md           # this file
│   ├── PROGRESS.md              # task log (append-only)
│   ├── DECISIONS.md             # verified facts and choices
│   ├── BLOCKERS.md              # unresolved problems
│   ├── LICENSES.md              # third-party asset licenses
│   ├── TEST_MATRIX.md           # hardware/test results
│   └── RELEASE_NOTES_TEMPLATE.md
├── iso/
│   └── profile/                 # archiso profile (copy of releng, modified)
│       ├── profiledef.sh
│       ├── pacman.conf
│       ├── packages.x86_64      # GENERATED by scripts/gen-packages.sh — do not edit by hand
│       ├── airootfs/            # live-system overlay (etc/, usr/, root/)
│       ├── efiboot/  syslinux/  grub/   # boot configs from releng
│       └── bootstrap_packages*  # only if present in releng
├── packages/                    # human-edited package lists (one package per line, # comments)
│   ├── base.txt
│   ├── desktop.txt              # COSMIC desktop (main edition)
│   ├── desktop-kde.txt          # optional KDE edition only (Appendix K)
│   ├── dev.txt
│   ├── gaming.txt
│   ├── drivers-oss.txt
│   ├── sydra.txt               # our own sydra-* packages (add once they exist)
│   └── live-only.txt
├── repo/
│   ├── pkgbuilds/               # one directory per custom package, each with PKGBUILD
│   │   ├── calamares/  ckbcomp/  paru/  (AUR sources pinned by commit)
│   │   ├── sydra-branding/  sydra-theme/  sydra-calamares-config/
│   │   ├── sydra-welcome/   sydra-gamehub/  sydra-dev/  sydra-gpu-setup/
│   │   └── sydra-settings/         # skel, defaults, sysctl, zram, snapper, firewall
│   └── x86_64/                  # built packages + sydra.db (gitignored; served locally)
├── tokens/
│   └── glass.json               # the single source of truth for the look
├── tools/
│   └── glassgen.py              # generates COSMIC theme/config, GTK CSS, Qt (qt6ct/Kvantum) and terminal files from tokens
├── assets/
│   ├── wallpapers/              # generated or properly licensed; see docs/LICENSES.md
│   ├── logo/                    # sydra-logo.svg (from E, source of truth) + generated variants (T4.10)
│   └── sounds/                  # optional
├── catalog/
│   ├── native-games.yaml        # curated native Linux games (verified)
│   └── notes.md
├── scripts/
│   ├── preflight.sh
│   ├── gen-packages.sh
│   ├── build-repo.sh
│   ├── build-iso.sh
│   ├── qemu-test.sh
│   ├── flash-usb.sh
│   ├── ventoy-copy.sh
│   ├── serve-cache.sh
│   └── sign-release.sh
└── tests/
    ├── smoke-live.sh            # runs inside the live ISO
    └── checklist-hardware.md
```

---

## 7. ENVIRONMENT BOOTSTRAP

### 7.1 Laptop A (EndeavourOS) — build machine setup (task T0.5 does this)

Install the toolchain (run once; verify names with `pacman -Si` if a package is not found):

```bash
sudo pacman -Syu --needed \
  archiso devtools git base-devel \
  qemu-desktop edk2-ovmf \
  squashfs-tools libisoburn mtools dosfstools \
  rsync reflector shellcheck jq python python-pip \
  btrfs-progs gnupg
# AUR helper already exists on EndeavourOS (yay). For Calamares sources use the clean-chroot flow in T2.1.
```

Check virtualization: `ls /dev/kvm` must exist (enable VT-x/AMD-V in BIOS if not). QEMU without KVM is too slow for useful tests.

### 7.2 Laptop B (Windows) — what happens there
- Git (and the Hermes agent) for editing docs/code, Python + PySide6 for Game Hub/Welcome app development and UI screenshots.
- Ventoy (Windows installer) is used to prepare the pendrive if E prefers to do it from Windows.
- **Booting the Sydra ISO from USB** is the GPU/gaming test. No installation is needed for the first tests (live session only).
- Do not run archiso builds there.

### 7.3 Pendrive layout
1. Install **Ventoy** on the pendrive (Ventoy2Disk). `VERIFY:` current Ventoy version and Secure Boot instructions at ventoy.net.
2. Copy ISO files into the Ventoy partition as normal files: `cp build/out/sydra-os-*.iso /run/media/$USER/Ventoy/` (`scripts/ventoy-copy.sh` does this safely).
3. If Ventoy fails to boot a Sydra ISO in its default mode, try "GRUB2 mode" in the Ventoy boot menu; as last resort use `scripts/flash-usb.sh` (this erases the Ventoy setup).
4. Keep `logs/` and `sydra-offline-cache/` on the free space/exFAT area for moving data between laptops.

### 7.4 Bandwidth discipline (phone hotspot)
- First `pacman -Syu` on Laptop A downloads packages into `/var/cache/pacman/pkg`. **Never clear this cache.**
- `scripts/serve-cache.sh` starts a tiny HTTP server (for example `python -m http.server 8080 --directory /var/cache/pacman/pkg`) so Laptop B (when it runs Linux, live or installed) can fetch from Laptop A over the hotspot's local network instead of the internet. `VERIFY:` hotspot client isolation: some phones block device-to-device traffic. If blocked, transfer via the pendrive (`rsync` the cache to the exFAT area).
- Use a fast nearby mirror: `sudo reflector --country India,Singapore --protocol https --latest 10 --sort rate --save /etc/pacman.d/mirrorlist` (run once per week at most).
- The archiso build downloads packages through pacman, so it uses the same cache.
- Measure and record in `docs/DECISIONS.md`: the hotspot's daily data cap (unknown; ask E once), and the size of the package cache after the first full ISO build.
- Do large downloads (full system update, Proton-GE, Flatpak runtimes) in one planned session, not repeatedly.

---

## 8. PHASES AND TASKS

Timeline assumes one person working part-time with agents: roughly 14 weeks to v0.1. Treat the timeline as a guide; the acceptance tests are the truth.

```
Phase 0  Foundation ................ week 1
Phase 1  Base ISO boots ............ weeks 1-2
Phase 2  Own repo + installer ...... weeks 2-4
Phase 3  Desktop base .............. weeks 4-6
Phase 4  Sydra Glass .............. weeks 5-8
Phase 5  Developer experience ...... weeks 7-9
Phase 6  Gaming + GPU .............. weeks 8-11
Phase 7  Game Hub + Welcome ........ weeks 10-13
Phase 8  System defaults/hardening . weeks 11-13
Phase 9  Test matrix + release ..... weeks 13-14
Phase 10 After v0.1 ................ later (Tamil layer, Agatiyan, Lite edition)
```

---

### PHASE 0 — FOUNDATION

**T0.1 Create the repository**
- Steps: create the layout from section 6 (empty files with a one-line header are fine). `git init`. Add `.gitignore` (build outputs, ISOs, `.env`, package files). Add `LICENSE` (GPL-3.0-or-later text). Copy this file to `docs/MASTER_PLAN.md`. Copy E's logo file to `assets/logo/sydra-logo.svg` (do not modify it).
- DONE WHEN: `tree -a -L 3` matches section 6 and `git log` shows the first commit.

**T0.2 Makefile and logging**
- Steps: add the `Makefile` from section 9.1. Create `build/logs/` handling inside scripts.
- DONE WHEN: `make check` runs `scripts/preflight.sh` and prints a PASS/FAIL list.

**T0.3 Secret hygiene**
- Steps: `.env.example` with variable names only (`NVIDIA_API_KEY=`, etc.). Add pre-commit with `gitleaks` and `shellcheck` (`VERIFY:` hook repositories and versions). Run the hooks on all files.
- DONE WHEN: committing a file containing the string `NVIDIA_API_KEY=nvapi-test123` is blocked by the hook (test it, then remove the test file).

**T0.4 Progress, decisions and blockers files**
- Steps: create `docs/PROGRESS.md`, `docs/DECISIONS.md`, `docs/BLOCKERS.md` with headers and one example entry format each.
- DONE WHEN: files exist and an entry for T0.1–T0.3 is present in `PROGRESS.md`.

**T0.5 Build machine bootstrap (Laptop A)**
- Steps: run the install command from section 7.1. Verify `/dev/kvm`. Run `df -h` and record free space in `DECISIONS.md`. Record RAM (`free -h`) and CPU (`lscpu | head`) in `DECISIONS.md`. Run `reflector` once (section 7.4).
- DONE WHEN: `mkarchiso --help`, `makechrootpkg -h`, `qemu-system-x86_64 --version` and `repo-add` all run; at least 40 GB free (if less, write a BLOCKER and ask E to free space).

**T0.6 Name, trademark and domain check (before anything is published)**
- Steps: search for conflicts with "Sydra" / "Sydra OS" on: DistroWatch, GitHub, the Arch/AUR package names (`sydra*`), Wikipedia, LinuxLinks' distribution lists, and general web search. Check trademark databases (India's trademark search, WIPO Global Brand Database, USPTO) for "Sydra" in software/computing classes. Check domain and handle availability (`sydra.org`, `sydra.dev`, `sydra-os.org`, GitHub organization, Discord/Telegram/X handles). Check the word's meaning in major languages (Spanish, French, Portuguese, Arabic, Hindi, Tamil, Chinese, Japanese) and ask E to ask native speakers if any doubt remains. Record the table in `docs/DECISIONS.md` and propose licensing for the name/logo (trademark policy).
- DONE WHEN: the table is complete and E has written "go" or "rename" in `PROGRESS.md`. Until E writes "go", nothing is published and no domain or organization is registered (searches only).

---

### PHASE 1 — BASE ISO BOOTS (STOCK ARCH, NO DESKTOP YET)

Goal: prove the toolchain end to end with the smallest possible change.

**T1.1 Copy the releng profile**
- Steps: `cp -r /usr/share/archiso/configs/releng/ iso/profile/`. Move the contents of releng's `packages.x86_64` into `packages/live-only.txt` (keep every line for now). Create `scripts/gen-packages.sh` (section 9.3) so `packages.x86_64` is generated from `packages/*.txt`.
- DONE WHEN: `scripts/gen-packages.sh` regenerates a `packages.x86_64` that is identical in content (ignoring order/comments) to releng's original.

**T1.2 Rename and configure the profile**
- Steps: edit `iso/profile/profiledef.sh`: `iso_name="sydra-os"`, `iso_label="SYDRA_$(date +%Y%m)"` (keep the label ≤ 32 characters, uppercase letters/digits/underscore), `iso_publisher="Sydra OS"`, `iso_application="Sydra OS Live/Install"`, `iso_version="$(date +%Y.%m.%d)"`. Keep `bootmodes` exactly as in the copied releng profile (do not hand-edit boot mode names). In `iso/profile/pacman.conf`: enable `[multilib]`. (The `[sydra]` repo is added in T2.2.)
- DONE WHEN: `grep -n 'sydra' iso/profile/profiledef.sh` shows the new names; `git diff` shows only intended edits.

**T1.3 First ISO build**
- Steps: `make iso` (uses `scripts/build-iso.sh`, section 9.4). Expect 10–30 minutes and a few GB of downloads on first run. Record ISO size and the cache size afterwards in `DECISIONS.md`.
- DONE WHEN: `build/out/sydra-os-*.iso` exists and `sha256sum` is stored in `build/out/SHA256SUMS`.

**T1.4 Boot test in QEMU (BIOS and UEFI)**
- Steps: `scripts/qemu-test.sh bios` and `scripts/qemu-test.sh uefi` (section 9.5). Both must reach a shell prompt (root autologin as in releng).
- DONE WHEN: both modes boot; screenshot or serial log saved in `docs/TEST_MATRIX.md`.

**T1.5 Prepare the pendrive (Ventoy)**
- Steps (HUMAN ACTION for E): install Ventoy on the pendrive (erases it; E must confirm nothing important is on it), then run `scripts/ventoy-copy.sh build/out/sydra-os-*.iso`.
- DONE WHEN: the ISO is visible in the Ventoy menu on Laptop A.

**T1.6 Boot the stock ISO on both laptops (live only, no install)**
- HUMAN ACTION: E boots Laptop A, then Laptop B from the pendrive. Laptop B needs Secure Boot off (and BitLocker key backed up first; see 2.2). Record results in `docs/TEST_MATRIX.md`: boots? display OK? Wi-Fi? On Laptop B: does the live session display correctly on the RTX 5050 laptop (nouveau/modesetting)? If black screen: retry with the `nomodeset` boot option and write it down.
- DONE WHEN: `TEST_MATRIX.md` has one row per laptop with PASS/FAIL and notes.
- Why it matters: this tells us early whether the NVIDIA GPU needs the proprietary/open driver inside the live ISO (see Risk R3).

---

### PHASE 2 — OWN REPOSITORY AND INSTALLER

**T2.1 Clean chroot for package builds**
- Steps:
  ```bash
  mkdir -p ~/chroot
  sudo mkarchroot ~/chroot/root base-devel
  ```
  (`VERIFY:` current devtools usage; the repo's `scripts/build-repo.sh` wraps this.) Packages are always built with `makechrootpkg -c -r ~/chroot` so builds are clean and reproducible. Dependencies that exist only in our repo are injected with `-I <pkgfile>`.
- DONE WHEN: a trivial test PKGBUILD (`sydra-hello`) builds inside the chroot and produces a `.pkg.tar.zst`.

**T2.2 Local repo and wiring into archiso**
- Steps: create `repo/x86_64/`. After each package build: `repo-add repo/x86_64/sydra.db.tar.zst repo/x86_64/*.pkg.tar.zst`. Add a template `iso/profile/pacman.conf.in` with:
  ```
  [sydra]
  SigLevel = Optional TrustAll
  Server = file://@REPO_DIR@/repo/x86_64
  ```
  and have `scripts/build-iso.sh` render it into `iso/profile/pacman.conf` with the absolute path before calling `mkarchiso`. (Local file repo is for build time only; see T8.5 for the published repo used by installed systems. `VERIFY:` whether the profile's pacman.conf is copied into the live image, and make sure the live/installed `/etc/pacman.conf` does **not** contain the build-time `file://` path.)
- DONE WHEN: `pacman -Sy` with the generated config lists the `sydra` repo and `sydra-hello` can be installed into a temp root, e.g. `sudo pacman --config iso/profile/pacman.conf -r /tmp/testroot --dbpath /tmp/testroot/var/lib/pacman -Sy sydra-hello` (create the dirs first).

**T2.3 Build Calamares and its dependencies**
- Steps: fetch the AUR sources for `calamares` and `ckbcomp` into `repo/pkgbuilds/`, **pin the exact commit** in a `SOURCE.txt` in each folder, read the PKGBUILDs (security: you are a security-minded builder; check `source=`/checksums, no strange install scripts). Build `ckbcomp` first, then `calamares` with `makechrootpkg -c -r ~/chroot -I <ckbcomp pkg>`. Add both to the repo. `VERIFY:` AUR package names (`calamares`, `ckbcomp`, `kpmcore` availability in official repos) and build time (it can take 20–60 minutes on the UHD 620 laptop; this is normal).
- Fallback (documented, temporary): if the build fails and E agrees, use the Chaotic-AUR prebuilt `calamares` for development only. Remove before release (rule 7). `VERIFY:` current Chaotic-AUR keyring/mirrorlist instructions on its official page.
- DONE WHEN: `calamares-*.pkg.tar.zst` is in `repo/x86_64/` and `pacman -Si calamares` (with our config) shows it.

**T2.4 Sydra Calamares configuration package (`sydra-calamares-config`)**
- Steps: provide `/etc/calamares/settings.conf`, `/etc/calamares/modules/*.conf`, and branding in `/usr/share/calamares/branding/sydra/` (`branding.desc`, the Sydra logo and slideshow images generated by T4.10, `show.qml`). Use the module sequence in section 9.9. Key modules: `welcome`, `locale`, `keyboard`, `partition` (default fs btrfs with subvolumes, ext4 optional, swap handled by ZRAM so no swap partition by default), `users`, `summary`, then `partition`, `mount`, `unpackfs` (source: `/run/archiso/airootfs/airootfs.sfs`, `sourcefs: squashfs`, `VERIFY:` exact path), `machineid`, `fstab`, `locale`, `keyboard`, `localecfg`, `users`, `networkcfg`, `hwclock`, `services-systemd`, `initcpiocfg`, `initcpio`, `grubcfg`, `bootloader`, `shellprocess` (post-install cleanup and first-boot prep), `umount`, `finished`.
- DONE WHEN: `calamares -d` starts in a test session and shows the branded welcome page.

**T2.5 Installer end-to-end in QEMU (the hardest early task)**
Known pitfalls that MUST be handled (study the open-source EndeavourOS and Arch-based Calamares configs for reference; `VERIFY:` against current versions):
1. **archiso mkinitcpio config leaks into the target.** The live image uses `/etc/mkinitcpio.conf.d/archiso.conf` and an `archiso` preset. After `unpackfs`, a `shellprocess` step must remove the archiso-specific config and restore the standard `linux` preset (default + fallback images with normal hooks such as `base udev autodetect microcode modconf kms keyboard keymap consolefont block filesystems fsck`, plus `btrfs` module handling if Btrfs is used), then `initcpio` regenerates images.
2. **Live-only settings must be removed from the installed system:** the `live` user, passwordless sudo file, live-session autologin (greeter or console), Calamares autostart/desktop file, live-only services.
3. **Kernel and microcode in `/boot`:** confirm `/boot/vmlinuz-linux` exists in the target after unpacking; `intel-ucode` and `amd-ucode` must be installed in the image so GRUB can load them.
4. **UEFI and BIOS both** must install and boot. Test both.
5. **Btrfs subvolume layout** (`@`, `@home`, `@log`, `@pkg`, `@snapshots`) and fstab must be correct; `grub-btrfs` and Snapper config created in post-install.
6. **Pacman keyring and mirrorlist** in the target must be initialised (`pacman-key --init`, `--populate archlinux`) on first boot if not already valid.
7. **Calamares is a Qt application and must run as root inside a COSMIC Wayland live session.** Root GUI apps on Wayland are a known trouble spot. Test early (T3.2): launch via a desktop file using `pkexec` or `sudo -E` with `WAYLAND_DISPLAY`/`XDG_RUNTIME_DIR` passed through (`VERIFY:` the working method), or run Calamares through XWayland (`QT_QPA_PLATFORM=xcb`, needs `xorg-xwayland`). Record the method that works in `DECISIONS.md`.
8. **The Calamares `displaymanager` module probably does not know `cosmic-greeter`/greetd** (`VERIFY:`). It is therefore left out of the sequence; the `firstboot` shellprocess enables `cosmic-greeter.service` in the installed system.
- Steps: in QEMU, create a 30 GB virtual disk (`qemu-img create -f qcow2 build/vm/test.qcow2 30G`), boot the ISO, run the installer, reboot from the disk. Repeat for BIOS and UEFI and for ext4 and Btrfs.
- DONE WHEN: all four combinations (BIOS/UEFI × ext4/Btrfs) install, reboot, and reach a login prompt (or the desktop once Phase 3 is done). Log everything in `TEST_MATRIX.md`.

---

### PHASE 3 — DESKTOP BASE (COSMIC, NO CUSTOM THEME YET)

**Decision record.** E decided that **COSMIC is the main desktop** and KDE Plasma is an optional edition (Appendix K). E accepts that COSMIC is young, has bugs, and will be fixed through Sydra updates. Therefore every agent must: (a) record each COSMIC bug found in `docs/KNOWN_ISSUES.md` with the COSMIC package versions and exact reproduction steps, (b) check the upstream issue trackers (`github.com/pop-os/cosmic-epoch` and the component repositories) before inventing a workaround, (c) prefer small, documented workarounds shipped in `sydra-settings` over patching COSMIC itself, and (d) never hide a known bug from the release notes.

**Facts checked on 2026-11-18 (re-check; they change quickly):**
- COSMIC Epoch 1.0 became stable in December 2025 and the 1.x series continues (1.8 was released in September 2026).
- Arch packages exist: install via `cosmic-session` or the `cosmic` group (Arch Wiki). Login manager is `cosmic-greeter` (greetd-based; enable `cosmic-greeter.service`). `start-cosmic` starts a session from a console.
- The Arch Wiki notes COSMIC has no secrets store (install `gnome-keyring`) and does not yet implement the Wayland protocol that night-light tools need (so no night light yet).
- Frosted Glass is a built-in appearance option (Settings > Desktop > Appearance).
- VRR is supported. HDR, a Vulkan renderer, and gamepad/controller work are listed by System76 as planned, not shipped; do not promise them. `VERIFY:` the current status before writing any claim in documentation or on the website.
- Release 1.8 contains fixes for Steam overlays and for hybrid-GPU laptops, which matters for Laptop B.

**T3.1 Package groups**
- Steps: fill `packages/desktop.txt`, `packages/base.txt`, `packages/drivers-oss.txt` from section 9.2. Run `pacman -Sg cosmic` and `pacman -Si cosmic-session` on Laptop A, replace the COSMIC package list in `desktop.txt` with the verified result, and record the COSMIC version (`pacman -Q cosmic-session`) in `DECISIONS.md`. Regenerate `packages.x86_64`. Remove from `live-only.txt` what the desktop makes unnecessary only after the ISO boots (keep `mkinitcpio-archiso`, `syslinux`, `edk2-shell`, `memtest86+`, `memtest86+-efi`, `efibootmgr`, firmware and filesystem tools).
- DONE WHEN: `make iso` succeeds and the ISO size is recorded (target below 4.5 GB; if larger, record why).

**T3.2 Live user and automatic desktop start**
- Steps (all in `iso/profile/airootfs/`): add a `live` user (entries in `etc/passwd`, `etc/shadow`, `etc/group`, `etc/gshadow`; shadow/gshadow need `file_permissions` entries in `profiledef.sh`); `etc/sudoers.d/g_wheel` with `%wheel ALL=(ALL:ALL) NOPASSWD: ALL` (live only). Enable services with symlinks in `etc/systemd/system/` (`display-manager.service` → `/usr/lib/systemd/system/cosmic-greeter.service`, plus `NetworkManager`, `bluetooth`, `firewalld`); disable releng's `systemd-networkd`/`iwd` enabling if present.
- Automatic login for the live user, in order of preference (`VERIFY:` which works): (A) greetd/cosmic-greeter autologin configuration; (B) fallback: console autologin of `live` on tty1 (getty drop-in using `agetty --autologin live`) plus a login-shell snippet that runs `exec start-cosmic` when `$XDG_VTNR` is 1 and no session is running. Option B is robust but must be removed in the installed system (T3.5).
- Add a desktop file/dock entry "Install Sydra OS" that starts Calamares with the method found in T2.5 pitfall 7.
- Add `gnome-keyring`, `xdg-desktop-portal-cosmic`, PipeWire stack, NetworkManager, `xorg-xwayland` (needed for Steam and many games).
- DONE WHEN: the ISO boots in QEMU (UEFI) straight to a COSMIC desktop with working networking. If `cosmic-comp` shows a black screen in QEMU, try a different virtual GPU (`-vga virtio`, `-device virtio-vga-gl`, or `-vga std`) and record what works; real hardware (T1.6 style test) is the final judge.

**T3.3 Default layout (structure only)**
- Steps: configure COSMIC once, by hand, inside a live session: top panel with Workspaces, Applications launcher, centered Time, and a status area (network, Bluetooth, sound, battery, power); bottom dock with pinned Terminal (`cosmic-terminal`), Firefox, Files (`cosmic-files`), Text Editor, Settings, Store. Then **discover the config files empirically instead of guessing**: create a marker file before changing settings (`touch /tmp/marker`), change one thing at a time, and run `find ~/.config/cosmic -newer /tmp/marker -type f`. Copy the resulting files into `repo/pkgbuilds/sydra-settings` under `/etc/skel/.config/cosmic/` (`VERIFY:` that COSMIC picks up defaults from `/etc/skel` for new users; COSMIC may also support system-wide defaults under `/usr/share/cosmic/`, check upstream documentation). Record the table "setting → file path" in `docs/COSMIC_THEMING.md` (used again in Phase 4).
- DONE WHEN: a fresh user in a fresh install gets both panels as described in 1.4 without manual setup.

**T3.4 Sound, network, Bluetooth, power basics**
- DONE WHEN: in a live session on real hardware, Wi-Fi connects, audio plays, brightness keys and suspend/resume work on Laptop A. Failures go to `docs/KNOWN_ISSUES.md`.

**T3.5 Installer works with the COSMIC ISO**
- Repeat T2.5 with the desktop ISO. In the installed system: `cosmic-greeter.service` enabled (since the Calamares `displaymanager` module is not used), live user and console autologin removed, `/etc/skel` COSMIC defaults applied to the new user, `gnome-keyring` working.
- DONE WHEN: BIOS/UEFI × ext4/Btrfs all reach the installed COSMIC desktop in QEMU with the user created in the installer.

**T3.6 (HIGH RISK, OPTIONAL BEFORE v0.1) Switch to `linux-zen`**
- Only after T3.5 passes. Replace `linux` with `linux-zen` and `linux-zen-headers`. Update: `airootfs/etc/mkinitcpio.d/` preset (rename to `linux-zen.preset` with `ALL_kver='/boot/vmlinuz-linux-zen'`), every boot entry that references `vmlinuz-linux`/`initramfs-linux.img` in `syslinux/`, `efiboot/loader/entries/`, `grub/`, and the Calamares shellprocess from T2.5. Add `linux-lts` as a second kernel in the installed system (post-install step).
- DONE WHEN: ISO boots in BIOS and UEFI QEMU, installs, and the installed system boots `linux-zen`. If this takes more than a day, write a BLOCKER, revert, and ship v0.1 with the stock `linux` kernel. (Check `ls /dev/ntsync` after `sudo modprobe ntsync` on either kernel; `VERIFY:` Wine/Proton support state.)

---

### PHASE 4 — SYDRA GLASS ON COSMIC (THE VISUAL IDENTITY)

Principle: **use COSMIC's built-in Frosted Glass; do not add third-party blur effects or patch the compositor.** Colors come from the brand palette in 1.7 (graphite `#12141A`, blue `#5B8DEF`, teal `#4FB3BF`). Sydra's job is to supply a restrained, professional preset (graphite, one muted accent), consistent colors for apps COSMIC does not theme itself, and good wallpapers. Keep all COSMIC-specific code in one place (`tools/glassgen.py` COSMIC module) because System76's roadmap mentions a new theming engine in a later Epoch, and that change must not force a rewrite of everything.

**T4.1 Design tokens (`tokens/glass.json`)**
- Steps: create the file from section 9.6. All visual values come from here. Not every token can be applied to COSMIC (it exposes fewer knobs than KDE): tokens COSMIC cannot apply are still used for GTK, Qt, the terminal and the website/screenshots.
- DONE WHEN: `python tools/glassgen.py --check` validates the JSON (types, ranges, contrast ratios ≥ 4.5:1 for text on the glass tint over a light and a dark test background).

**T4.2 COSMIC theming research spike (1 day, produce a document)**
- Steps: in a live session or VM, inventory what Settings > Desktop > Appearance offers (dark/light mode, accent color, Frosted Glass and any strength/option it has, roundness, window gaps, interface density, fonts, icon theme, GTK-app theming toggle if present, theme import/export if present). For each setting find where it is stored (use the marker + `find -newer` method from T3.3), whether it applies **live** when the file changes, and whether it can be changed from a script. Also inventory `cosmic-terminal` options (font, colors, opacity, whether blur-behind works), and test whether **non-COSMIC windows** (Firefox, a GTK app, a Qt app, Steam) receive blur or any glass effect (`VERIFY:`; do not assume).
- Output: `docs/COSMIC_THEMING.md` with a table: setting | UI path | config file/key | live-apply (yes/no) | scriptable (yes/no) | notes. Include the COSMIC version tested.
- DONE WHEN: the document exists and every claim in it was tested, not assumed.

**T4.3 Generator (`tools/glassgen.py`)**
- Steps: from the tokens and `docs/COSMIC_THEMING.md`, generate (one module per target): COSMIC theme/config files for each preset; GTK 3/4 CSS overrides (libadwaita-style, `~/.config/gtk-4.0/gtk.css`; `VERIFY:` interaction with COSMIC's own GTK-theming option); Qt color scheme for `qt6ct` and a Kvantum config; `cosmic-terminal` profile/colors and, optionally, Alacritty/Kitty configs for developers who prefer them. Output goes to `repo/pkgbuilds/sydra-theme/` and `sydra-settings/`.
- DONE WHEN: running the generator twice produces identical files (deterministic) and a fresh session loads them with no errors.

**T4.4 Frosted Glass baseline**
- Steps: ship the Graphite preset with Frosted Glass enabled and the most subtle setting COSMIC offers; verify text readability over bright and dark wallpapers; verify no flicker over 10 minutes of use; record the CPU/GPU cost on Laptop A (UHD 620) with and without Frosted Glass in `DECISIONS.md`.
- DONE WHEN: panel, dock, menus and COSMIC windows are visibly frosted; the result is documented with screenshots.

**T4.5 Consistency for non-COSMIC apps**
- Steps: make GTK apps (Firefox, Lutris, many tools), Qt apps (Game Hub, Welcome app, Qt tools) and Electron apps (VS Code) use the same colors, corner feel and fonts as COSMIC. Qt: `qt6ct` + Kvantum with a generated theme (`VERIFY:` how to set the platform theme for Qt 6 on COSMIC, usually `QT_QPA_PLATFORMTHEME=qt6ct` in `/etc/environment.d/`). Accept that some apps (Steam, Electron apps) stay opaque; the goal is color/shape consistency, not blur everywhere. Document which apps look native and which do not.
- DONE WHEN: Files, Terminal, Firefox, a Qt app and a GTK app share one consistent look, and screenshots are stored in `docs/`.

**T4.6 Wallpapers (no copyright trouble)**
- Steps: generate 6–8 dark, low-saturation wallpapers programmatically (gradients, soft light blobs, glass shapes) with Python (Pillow/numpy) in `tools/`, 3840×2160, plus one solid-color option. Store the generator and outputs; they are original work (license GPL/CC0). No third-party wallpapers unless the license is recorded.
- DONE WHEN: wallpapers exist, are selectable in System Settings, and text on the panel passes the contrast check over every wallpaper.

**T4.7 Presets and intensity**
- Presets: **Graphite** (default dark), **Midnight**, **Slate Light**, **High Contrast**, implemented as COSMIC theme files plus matching GTK/Qt/terminal files. Intensity: only what COSMIC exposes (at minimum Frosted Glass on/off; "Flat" = off; any strength control COSMIC provides). Implement `sydra-glass-set <preset> <intensity>` as a script that writes the generated files and, where possible, applies them live.
- Optional wallpaper-adaptive accent: `sydra-theme-sync` extracts **only an accent color** from the wallpaper, caps saturation (see `accentLimits` in the tokens), and keeps the glass neutral. `VERIFY:` whether COSMIC already offers accent-from-wallpaper before writing extraction code.
- DONE WHEN: switching presets from a terminal and from the Welcome app works, and "Flat" really disables the glass effect.

**T4.8 Login screen, fonts, icons, cursor**
- Steps: `cosmic-greeter` styling is limited: set the greeter background/wallpaper if supported (`VERIFY:`) and do not try to rebuild the greeter in v0.1. Defaults: Inter (interface), JetBrains Mono (monospace), Noto families for coverage; icons: start with COSMIC's own icon theme; evaluate Papirus only if it looks better and is consistent (`VERIFY:` how COSMIC selects icon themes). Skip a custom boot splash (Plymouth) for v0.1.
- DONE WHEN: the boot-to-login-to-desktop sequence looks coherent in a screen recording.

**T4.9 Visual QA**
- Check: readability on bright and dark wallpapers, HiDPI at 125%/150%, text in Terminal/Text Editor/VS Code stays crisp, no unreadable translucent menus, load of `cosmic-comp` at idle on the UHD 620 laptop (record `intel_gpu_top` and `top`; target: compositor under ~5% CPU at idle with Frosted Glass on).
- DONE WHEN: `TEST_MATRIX.md` has a "Glass visual QA" section with results and screenshots.

**T4.10 Brand assets from the Sydra logo**
- Steps: write `tools/brandgen.py` (or a shell script) that reads `assets/logo/sydra-logo.svg` and generates, deterministically, into `assets/logo/generated/` and into the packages that need them (tools: `rsvg-convert` from `librsvg`, ImageMagick `magick`/`convert`, or Inkscape; `VERIFY:` package names): (1) PNG sizes 16, 24, 32, 48, 64, 128, 256, 512; (2) `favicon.ico` (16/32/48) from a **simplified** variant without the glow and with thicker strokes, because the full logo's thin strokes disappear at small sizes; (3) monochrome white and monochrome dark SVGs; (4) horizontal lockup with "Sydra OS" set in Inter semibold; (5) Calamares branding images: `logo.png`, `icon.png`, welcome image, slideshow slides (3 to 5, dark glass style, no marketing claims that are not true yet); (6) GRUB theme assets (background in graphite with the logo; `/boot/grub/themes/sydra/`); (7) an icon-theme entry `sydra-logo` (SVG in `hicolor/scalable/apps/` plus PNGs) so launchers and the Settings "About" page can show it; (8) a fastfetch config and logo (image or ASCII) for the terminal.
- Distribution identity files (package `sydra-branding`): `/etc/os-release` with `NAME="Sydra OS"`, `PRETTY_NAME="Sydra OS"`, `ID=sydra`, `ID_LIKE=arch`, `ANSI_COLOR` set to the blue accent, `HOME_URL` (after T0.6), `LOGO=sydra-logo`; `/etc/issue`; a short MOTD (optional). `VERIFY:` the cleanest way to override `/etc/os-release`: it belongs to the `filesystem` package, so a plain file in another package will conflict; the usual approach is a post-install step plus a pacman hook that re-applies the file after `filesystem` updates. `VERIFY:` that Steam, Proton, COSMIC, Calamares and common scripts still behave correctly with `ID=sydra` and `ID_LIKE=arch`; if something breaks, record it and keep `ID_LIKE=arch`.
- Do not use the logo on wallpapers at large size by default. Provide an optional small watermark variant.
- DONE WHEN: all generated files exist; the logo is visible and readable at 16, 32 and 128 px on both dark and light backgrounds (screenshots in `docs/`); `cat /etc/os-release` on an installed VM shows Sydra OS; the Calamares welcome page, GRUB menu and Welcome app show the logo.

---

## 9. TEMPLATES AND REFERENCE FILES

(See MASTER_PLAN.md sections 9.1 through 9.11)

---

## APPENDIX K — OPTIONAL KDE PLASMA EDITION (START ONLY AFTER v0.1 SHIPS)

Purpose: give users who prefer KDE Plasma an alternative edition. Method: create a second archiso profile `iso/profile-kde/` that shares `packages/base.txt`, `dev.txt`, `gaming.txt`, `sydra.txt` and `drivers-oss.txt`, and swaps the desktop file for `packages/desktop-kde.txt` (section 9.2). Display manager: SDDM. Calamares can use its normal `displaymanager` module for SDDM.
