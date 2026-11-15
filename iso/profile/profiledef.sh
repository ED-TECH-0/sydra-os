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
  'bios.syslinux'
  'uefi.systemd-boot'
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
  ["/etc/polkit-1/rules.d"]="0:0:755"
  ["/etc/polkit-1/rules.d/49-nopasswd_global.rules"]="0:0:644"
  ["/etc/skel/Desktop/siddha-installer.desktop"]="1000:1000:755"
  ["/etc/skel/.config/kiorc"]="1000:1000:644"
  ["/etc/xdg/kiorc"]="0:0:644"
  ["/usr/share/applications/siddha-installer.desktop"]="0:0:755"
  ["/usr/local/bin/siddha-installer"]="0:0:755"
  ["/usr/local/bin/siddha-desktop-init"]="0:0:755"
  ["/home/live"]="1000:1000:750"
  ["/home/live/Desktop/siddha-installer.desktop"]="1000:1000:755"
  ["/root"]="0:0:750"
  ["/root/.automated_script.sh"]="0:0:755"
  ["/root/.gnupg"]="0:0:700"
  ["/usr/local/bin/choose-mirror"]="0:0:755"
  ["/usr/local/bin/Installation_guide"]="0:0:755"
  ["/usr/local/bin/livecd-sound"]="0:0:755"
)
