#!/usr/bin/env bash
set -euo pipefail
ISO=${1:?usage: flash-usb.sh <iso> </dev/sdX>}
DEV=${2:?usage: flash-usb.sh <iso> </dev/sdX>}

[[ $EUID -eq 0 ]]              || { echo "run with sudo"; exit 1; }
[[ -f $ISO ]]                  || { echo "ISO not found: $ISO"; exit 1; }
[[ -b $DEV ]]                  || { echo "$DEV is not a block device"; exit 1; }
[[ $(lsblk -dno TYPE "$DEV") == disk ]] || { echo "pass the whole disk, not a partition"; exit 1; }

TRAN=$(lsblk -dno TRAN "$DEV" || true)
RM=$(lsblk -dno RM "$DEV" || true)
[[ $TRAN == usb || $RM == 1 ]] || { echo "REFUSING: $DEV is not a removable/USB device"; exit 1; }

if lsblk -nro MOUNTPOINTS "$DEV" | grep -qE '^(/|/boot|/boot/efi|/home)$'; then
  echo "REFUSING: $DEV holds a system mount point"; exit 1
fi

SIZE_GB=$(( $(lsblk -bdno SIZE "$DEV") / 1024 / 1024 / 1024 ))
(( SIZE_GB <= 256 )) || { echo "REFUSING: $DEV is ${SIZE_GB} GB, too large for a pendrive"; exit 1; }

lsblk -o NAME,SIZE,MODEL,TRAN,MOUNTPOINTS "$DEV"
echo "ALL DATA ON $DEV WILL BE ERASED (this also removes Ventoy)."
read -rp "Type the device path again to confirm: " C
[[ $C == "$DEV" ]] || { echo "aborted"; exit 1; }

umount "${DEV}"* 2>/dev/null || true
dd if="$ISO" of="$DEV" bs=4M status=progress conv=fsync oflag=direct
sync
echo "Flashing complete."
