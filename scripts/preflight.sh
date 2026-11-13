#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT=$PWD

echo "=== Sydra OS Preflight Check ==="

FAILURES=0
WARNINGS=0

pass() { echo "[PASS] $1"; }
warn() { echo "[WARN] $1"; WARNINGS=$((WARNINGS + 1)); }
fail() { echo "[FAIL] $1"; FAILURES=$((FAILURES + 1)); }

# 1. Host OS check
if [[ -f /etc/os-release ]]; then
  # shellcheck source=/dev/null
  source /etc/os-release
  if [[ "${ID_LIKE:-}" =~ arch ]] || [[ "${ID:-}" =~ arch ]] || [[ "${ID:-}" =~ endeavouros ]]; then
    pass "Host is Arch-based (${PRETTY_NAME:-$ID})"
  else
    fail "Host is not Arch-based (${PRETTY_NAME:-$ID})"
  fi
else
  fail "/etc/os-release not found"
fi

# 2. User check
if [[ $EUID -eq 0 ]]; then
  if [[ -n "${SUDO_USER:-}" ]]; then
    pass "Running via sudo from user $SUDO_USER"
  else
    warn "Running as root directly (recommended to run make check as regular user)"
  fi
else
  pass "Running as non-root user ($USER)"
fi

# 3. Disk space check (>= 25 GB free)
AVAIL_GB=$(df --output=avail -BG "$ROOT" | tail -1 | tr -dc '0-9')
if (( AVAIL_GB >= 25 )); then
  pass "Disk space sufficient: ${AVAIL_GB} GB available (minimum 25 GB)"
else
  fail "Insufficient disk space: ${AVAIL_GB} GB available (minimum 25 GB required)"
fi

# 4. Hardware Virtualization (/dev/kvm)
if [[ -r /dev/kvm && -w /dev/kvm ]]; then
  pass "KVM virtualization accessible (/dev/kvm)"
elif [[ -e /dev/kvm ]]; then
  warn "/dev/kvm exists but is not read/write accessible by current user"
else
  fail "/dev/kvm not found (enable VT-x/AMD-V in BIOS)"
fi

# 5. Core tools check
REQUIRED_TOOLS=(git repo-add python)
BUILD_TOOLS=(mkarchiso makechrootpkg qemu-system-x86_64)

for tool in "${REQUIRED_TOOLS[@]}"; do
  if command -v "$tool" &>/dev/null; then
    pass "Tool installed: $tool"
  else
    fail "Required tool missing: $tool"
  fi
done

for tool in "${BUILD_TOOLS[@]}"; do
  if command -v "$tool" &>/dev/null; then
    pass "Build tool installed: $tool"
  else
    warn "Build tool not yet installed: $tool (install before building ISO / VM testing)"
  fi
done

# Check UEFI OVMF firmware files
if [[ -f /usr/share/edk2/x64/OVMF_CODE.4m.fd || -f /usr/share/edk2-ovmf/x64/OVMF_CODE.fd || -f /usr/share/ovmf/x64/OVMF_CODE.fd ]]; then
  pass "UEFI OVMF firmware installed"
else
  warn "UEFI OVMF firmware not found (package: edk2-ovmf)"
fi

# 6. Memory check
TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
TOTAL_RAM_GB=$(( TOTAL_RAM_KB / 1024 / 1024 ))
pass "Total RAM detected: ${TOTAL_RAM_GB} GB"
if (( TOTAL_RAM_GB <= 8 )); then
  warn "RAM is <= 8 GB. Builds must use disk work directory, never tmpfs. QEMU tests use max 2GB RAM."
fi

echo "================================"
echo "Preflight complete: $FAILURES failures, $WARNINGS warnings."

if (( FAILURES > 0 )); then
  echo "Fix the failures above before proceeding."
  exit 1
fi

exit 0
