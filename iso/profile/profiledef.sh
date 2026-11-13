#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="sydra-os"
iso_label="SYDRA_$(date +%Y%m)"
iso_publisher="Sydra OS <https://sydra-os.org>"
iso_application="Sydra OS Live/Install CD"
iso_version="$(date +%Y.%m.%d)"
install_dir="sydra"
buildmodes=('iso')
bootmodes=(
  'bios.syslinux.mbr'
  'bios.syslinux.eltorito'
  'uefi-ia32.systemd-boot.esp'
  'uefi-x64.systemd-boot.esp'
  'uefi-ia32.systemd-boot.eltorito'
  'uefi-x64.systemd-boot.eltorito'
)
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'zstd')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/etc/gshadow"]="0:0:400"
  ["/etc/sudoers.d"]="0:0:750"
  ["/etc/sudoers.d/g_wheel"]="0:0:440"
  ["/root"]="0:0:750"
)
