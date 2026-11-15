#!/usr/bin/env python3
import json
import os
import shutil
import socket
import subprocess
import sys
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ISO_PATH = os.path.join(ROOT_DIR, "build/out/sydra-os-2026.11.15-x86_64.iso")
QMP_SOCK = os.path.join(ROOT_DIR, "build/vm/qmp-screendump.sock")
VARS_PATH = os.path.join(ROOT_DIR, "build/vm/OVMF_VARS-screendump.fd")
OVMF_CODE = "/usr/share/edk2/x64/OVMF_CODE.4m.fd"
OVMF_VARS_SRC = "/usr/share/edk2/x64/OVMF_VARS.4m.fd"

PICTURES_DIR = os.path.expanduser("~/Pictures")
SCREENSHOTS_DIR = os.path.join(PICTURES_DIR, "Screenshots")
FINAL_IMG = os.path.join(PICTURES_DIR, "sydra-os-gui.png")

os.makedirs(os.path.join(ROOT_DIR, "build/vm"), exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

if os.path.exists(QMP_SOCK):
    os.remove(QMP_SOCK)

if not os.path.exists(VARS_PATH):
    shutil.copyfile(OVMF_VARS_SRC, VARS_PATH)

def send_qmp(sock, cmd_obj):
    sock.sendall(json.dumps(cmd_obj).encode("utf-8") + b"\n")
    buffer = ""
    while True:
        chunk = sock.recv(4096).decode("utf-8", errors="replace")
        if not chunk:
            break
        buffer += chunk
        lines = buffer.split("\n")
        buffer = lines[-1]
        for line in lines[:-1]:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "return" in data or "error" in data:
                    return data
            except json.JSONDecodeError:
                continue
    return None

print(f"[*] Booting QEMU with ISO: {ISO_PATH}")
qemu_cmd = [
    "qemu-system-x86_64",
    "-enable-kvm",
    "-cpu", "host",
    "-smp", "4",
    "-m", os.environ.get("QEMU_RAM", "2560"),
    "-machine", "q35",
    "-device", "virtio-vga",
    "-display", "none",
    "-qmp", f"unix:{QMP_SOCK},server,nowait",
    "-drive", f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
    "-drive", f"if=pflash,format=raw,file={VARS_PATH}",
    "-boot", "d",
    "-cdrom", ISO_PATH
]

proc = subprocess.Popen(qemu_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    print("[*] Waiting for QMP socket to appear...")
    for _ in range(30):
        if os.path.exists(QMP_SOCK):
            break
        time.sleep(0.5)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(QMP_SOCK)

    # Initial greeting line
    init_data = s.recv(4096).decode("utf-8", errors="replace")
    send_qmp(s, {"execute": "qmp_capabilities"})

    print("[*] Connected to QMP. Monitoring boot sequence...")
    intervals = [15, 30, 45, 60, 75, 90]
    start_time = time.time()
    last_idx = 0

    while True:
        elapsed = int(time.time() - start_time)
        if elapsed > 95:
            break

        if last_idx < len(intervals) and elapsed >= intervals[last_idx]:
            sec = intervals[last_idx]
            last_idx += 1
            ppm_file = f"/tmp/qemu-{sec}s.ppm"
            png_file = os.path.join(SCREENSHOTS_DIR, f"sydra-boot-{sec}s.png")

            resp = send_qmp(s, {"execute": "screendump", "arguments": {"filename": ppm_file}})
            time.sleep(0.5)

            if os.path.exists(ppm_file):
                subprocess.run(["convert", ppm_file, png_file], check=True)
                shutil.copyfile(png_file, FINAL_IMG)
                os.remove(ppm_file)
                print(f"[+] Captured screenshot at {sec}s -> {png_file}")

        time.sleep(1)

    print(f"[+] Final OS GUI screenshot saved to {FINAL_IMG}")

    # Clean shutdown
    try:
        send_qmp(s, {"execute": "system_powerdown"})
        time.sleep(2)
        send_qmp(s, {"execute": "quit"})
    except Exception:
        pass
    s.close()

finally:
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    if os.path.exists(QMP_SOCK):
        os.remove(QMP_SOCK)

print("[*] QEMU boot test completed successfully.")
