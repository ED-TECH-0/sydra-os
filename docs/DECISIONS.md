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
