SHELL := /bin/bash
.PHONY: check packages repo iso qemu-bios qemu-uefi flash clean sums

check:
	scripts/preflight.sh

packages:
	scripts/gen-packages.sh

repo:
	scripts/build-repo.sh

iso: check packages
	sudo scripts/build-iso.sh

qemu-bios:
	scripts/qemu-test.sh bios

qemu-uefi:
	scripts/qemu-test.sh uefi

sums:
	cd build/out && sha256sum *.iso > SHA256SUMS

clean:
	sudo rm -rf build/work
