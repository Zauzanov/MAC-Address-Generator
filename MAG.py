#!/usr/bin/env python3

import random
import subprocess
import sys

# MAC address generator:
def generate_mac() -> str:
    parts = [
        0x00,
        random.randint(0x00, 0x7F),
        0x29,
        0x47,
        0x74,
        random.randint(0x00, 0xFF),
    ]
    return ":".join(f"{p:02x}" for p in parts)
    
# Running a shell and printing errors:
def run_cmd(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {' '.join(cmd)}:\n{result.stderr}", file=sys.stderr)
    else:
        print(result.stdout.strip())

def change_mac(interface: str) -> None:
    new_mac = generate_mac()
    print("New MAC Address:", new_mac)

    print("\nOLD MAC ADDRESS:")
    run_cmd(["ip", "link", "show", interface])

    # bring interface down, set MAC, bring it up
    run_cmd(["ip", "link", "set", "dev", interface, "down"])
    run_cmd(["ip", "link", "set", "dev", interface, "address", new_mac])
    run_cmd(["ip", "link", "set", "dev", interface, "up"])

    print("\nNEW MAC ADDRESS:")
    run_cmd(["ip", "link", "show", interface])
    print()

if __name__ == "__main__":
    iface = sys.argv[1] if len(sys.argv) > 1 else "eth0"
    change_mac(iface)

