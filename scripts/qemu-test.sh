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

ARGS=(-enable-kvm -cpu host -smp 4 -m 2048 -machine q35
      -qmp "unix:build/vm/qmp-$MODE.sock,server,nowait"
      -drive "file=$DISK,if=virtio,format=qcow2"
      -netdev user,id=n0 -device virtio-net-pci,netdev=n0
      -device virtio-vga-gl -display gtk,gl=on)

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
  if [[ -n $OVMF_VARS_SRC && ! -f $VARS ]]; then
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
  ARGS+=(-boot d -cdrom "$ISO")
fi

echo "Launching QEMU ($MODE mode, boot: $BOOT)..."
exec qemu-system-x86_64 "${ARGS[@]}"
