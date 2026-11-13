# Hardware & Virtualization Test Matrix

| Test Case | Laptop A (UHD 620 Live) | Laptop B (RTX 5050 Live) | QEMU BIOS | QEMU UEFI | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Boots to desktop** | | | PASS | PASS | Autologin to KDE Plasma 6 |
| **Display correct / resolution** | | | PASS | PASS | 1024x768 graphical compositor |
| **Wi-Fi connects** | | | N/A | N/A | NetworkManager active |
| **Audio output (PipeWire)** | | | N/A | N/A | PipeWire daemon running |
| **Bluetooth** | | | N/A | N/A | |
| **Brightness keys / suspend** | | | N/A | N/A | |
| **Touchpad gestures** | | | N/A | N/A | |
| **HiDPI scaling (125% / 150%)** | | | | | |
| **Glass Visual QA (Contrast ≥ 4.5:1)**| | | PASS | PASS | Contrast token checks pass |
| **Idle CPU of compositor** | | | | | |
| **Installer: ext4** | N/A | N/A | | | |
| **Installer: Btrfs + snapshots** | N/A | N/A | | | |
| **Installed system boots** | N/A | | | | |
| **Steam client starts** | | | | | |
| **`nvidia-smi` / PRIME offload**| N/A | | N/A | N/A | |
| **One native game** | | | N/A | N/A | |
| **One Proton game** | | | N/A | N/A | |
| **Game Hub badges correct** | | | | | |
| **Welcome app flow** | | | PASS | PASS | Welcome Center autostarted |
| **`systemctl --failed` empty** | | | | | |
| **`ss -tulpn` no unexpected listeners** | | | | | |
