#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

MODE=${1:?usage: qemu-test.sh bios|uefi [disk-only]}
BOOT=${2:-iso}
mkdir -p build/vm

ISO=$(ls -1t build/out/sydra-os-*.iso 2>/dev/null | head -n1 || true)
if [[ -z $ISO ]]; then
  ISO=$(ls -1t build/out/*.iso 2>/dev/null | head -n1 || true)
fi

DISK="build/vm/test-$MODE.qcow2"
[[ -f $DISK ]] || qemu-img create -f qcow2 "$DISK" 30G

rm -f "build/vm/qmp-$MODE.sock"

# Auto-detect display backend
DISPLAY_ARGS=()
if qemu-system-x86_64 -display sdl,gl=on -help >/dev/null 2>&1; then
  DISPLAY_ARGS=(-device virtio-vga-gl -display sdl,gl=on)
elif qemu-system-x86_64 -display gtk -help >/dev/null 2>&1; then
  DISPLAY_ARGS=(-device virtio-vga -display gtk)
else
  DISPLAY_ARGS=(-vga virtio -display sdl)
fi

RAM="${QEMU_RAM:-2560}"
SMP="${QEMU_SMP:-2}"

DISK_BOOTINDEX="1"
if [[ $BOOT != disk-only ]]; then
  DISK_BOOTINDEX="2"
fi

ARGS=(-enable-kvm -cpu host -smp "$SMP" -m "$RAM" -machine q35
      -qmp "unix:build/vm/qmp-$MODE.sock,server,nowait"
      -drive "file=$DISK,if=virtio,format=qcow2,bootindex=$DISK_BOOTINDEX"
      -netdev user,id=n0 -device virtio-net-pci,netdev=n0
      "${DISPLAY_ARGS[@]}")

if [[ $MODE == uefi ]]; then
  OVMF_CODE=""
  for candidate in /usr/share/edk2/x64/OVMF_CODE.4m.fd /usr/share/edk2-ovmf/x64/OVMF_CODE.fd /usr/share/ovmf/x64/OVMF_CODE.fd; do
    if [[ -f $candidate ]]; then
      OVMF_CODE=$candidate
      break
    fi
  done

  OVMF_VARS_SRC=""
  for candidate in /usr/share/edk2/x64/OVMF_VARS.4m.fd /usr/share/edk2-ovmf/x64/OVMF_VARS.fd /usr/share/ovmf/x64/OVMF_VARS.fd; do
    if [[ -f $candidate ]]; then
      OVMF_VARS_SRC=$candidate
      break
    fi
  done

  VARS="build/vm/OVMF_VARS-$MODE.fd"
  if [[ $BOOT != disk-only ]]; then
    # Reset NVRAM when booting ISO so previous disk installs do not hijack boot order
    if [[ -n $OVMF_VARS_SRC ]]; then
      cp -f "$OVMF_VARS_SRC" "$VARS"
    fi
  elif [[ -n $OVMF_VARS_SRC && ! -f $VARS ]]; then
    cp "$OVMF_VARS_SRC" "$VARS"
  fi

  if [[ -n $OVMF_CODE ]]; then
    ARGS+=(-drive "if=pflash,format=raw,readonly=on,file=$OVMF_CODE")
  fi
  if [[ -f $VARS ]]; then
    ARGS+=(-drive "if=pflash,format=raw,file=$VARS")
  fi
fi

if [[ $BOOT != disk-only ]]; then
  [[ -n $ISO && -f $ISO ]] || { echo "No ISO found in build/out/"; exit 1; }
  ARGS+=(-drive "file=$ISO,media=cdrom,readonly=on,bootindex=1")
fi

echo "Launching QEMU ($MODE mode, boot: $BOOT)..."
exec qemu-system-x86_64 "${ARGS[@]}"
