#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

[[ $EUID -eq 0 ]] || { echo "Run with sudo: sudo scripts/flash-usb.sh [iso] <device>"; exit 1; }

ISO=""
DEV=""

LATEST_ISO=$(ls -1t build/out/sydra-os-*.iso build/out/*.iso 2>/dev/null | head -n1 || true)

if [[ $# -eq 0 ]]; then
  echo "Usage: sudo scripts/flash-usb.sh [iso] <device>"
  echo ""
  echo "Available ISO: ${LATEST_ISO:-None found in build/out/}"
  echo ""
  echo "Connected USB / removable storage devices:"
  lsblk -d -o NAME,SIZE,MODEL,TRAN,RM | grep -E "usb| 1$" || echo "  (No USB drives detected)"
  echo ""
  echo "Example: sudo scripts/flash-usb.sh ${LATEST_ISO:-build/out/sydra-os-*.iso} /dev/sdb"
  exit 1
elif [[ $# -eq 1 ]]; then
  if [[ -b $1 ]]; then
    DEV="$1"
    ISO="$LATEST_ISO"
  elif [[ -f $1 ]]; then
    ISO="$1"
    echo "Device not specified. Connected USB / removable drives:"
    lsblk -d -o NAME,SIZE,MODEL,TRAN,RM | grep -E "usb| 1$" || echo "  (No USB drives detected)"
    echo "Usage: sudo scripts/flash-usb.sh \"$ISO\" /dev/sdX"
    exit 1
  else
    echo "Error: '$1' is neither an existing file nor a block device."
    echo "Connected USB / removable drives:"
    lsblk -d -o NAME,SIZE,MODEL,TRAN,RM | grep -E "usb| 1$" || echo "  (No USB drives detected)"
    exit 1
  fi
else
  ISO="$1"
  DEV="$2"
fi

[[ -n $ISO && -f $ISO ]] || { echo "ISO not found: '$ISO'"; exit 1; }
[[ -n $DEV && -b $DEV ]] || {
  echo "Block device not found: '$DEV'"
  echo "Connected USB / removable drives:"
  lsblk -d -o NAME,SIZE,MODEL,TRAN,RM | grep -E "usb| 1$" || echo "  (No USB drives detected)"
  exit 1
}

[[ $(lsblk -dno TYPE "$DEV") == disk ]] || { echo "Pass the whole disk (e.g. /dev/sdb), not a partition (e.g. /dev/sdb1)"; exit 1; }

TRAN=$(lsblk -dno TRAN "$DEV" || true)
RM=$(lsblk -dno RM "$DEV" || true)
[[ $TRAN == usb || $RM == 1 ]] || { echo "REFUSING: $DEV is not a removable/USB device"; exit 1; }

if lsblk -nro MOUNTPOINTS "$DEV" | grep -qE '^(/|/boot|/boot/efi|/home)$'; then
  echo "REFUSING: $DEV holds a system mount point"; exit 1
fi

SIZE_GB=$(( $(lsblk -bdno SIZE "$DEV") / 1024 / 1024 / 1024 ))
(( SIZE_GB <= 256 )) || { echo "REFUSING: $DEV is ${SIZE_GB} GB, too large for a pendrive"; exit 1; }

echo "Selected ISO: $ISO ($(du -h "$ISO" | cut -f1))"
echo "Target Device: $DEV"
lsblk -o NAME,SIZE,MODEL,TRAN,MOUNTPOINTS "$DEV"
echo ""
echo "WARNING: ALL DATA ON $DEV WILL BE ERASED."
read -rp "Type the device path ('$DEV') to confirm: " C
[[ $C == "$DEV" ]] || { echo "Aborted by user."; exit 1; }

echo "Unmounting existing partitions on $DEV..."
umount "${DEV}"* 2>/dev/null || true
echo "Writing ISO to $DEV..."
dd if="$ISO" of="$DEV" bs=4M status=progress conv=fsync oflag=direct
sync
echo "Flashing complete! USB is ready to boot."
