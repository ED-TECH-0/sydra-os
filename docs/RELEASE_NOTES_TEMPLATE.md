# Sydra OS v0.1 Release Notes

**Release Date:** YYYY-MM-DD  
**ISO Image:** `sydra-os-YYYY.MM.DD-x86_64.iso`  
**Internal Architecture:** Siddha Core v0.1  

---

## Highlights

- **Siddha Glass Pro**: Modern spatial glass desktop powered by KDE Plasma 6 Wayland with dynamic contrast guard.
- **Out-of-the-Box Gaming**: Steam, Proton-GE, Gamemode, MangoHud, and automatic GPU driver detection for NVIDIA RTX (50-series and newer), AMD Radeon, and Intel.
- **Developer Workstation**: Preconfigured modern Zsh shell, Starship, container virtualization (Podman), and the `siddha-dev` CLI.
- **Btrfs Snapshot Rollback**: Boot directly into earlier snapshots via GRUB menu using Snapper.

---

## Checksums & Signatures

```
SHA256SUM:
[paste checksum here]
```

To verify:
```bash
sha256sum -c SHA256SUMS
gpg --verify SHA256SUMS.sig SHA256SUMS
```

---

## Known Issues & Limitations (v0.1)

- Secure Boot must be disabled in UEFI firmware.
- Games requiring kernel-level anti-cheat (e.g. Valorant) will not run under Proton.
- Legacy NVIDIA cards (Pascal/Maxwell and older) require manual proprietary driver installation.
