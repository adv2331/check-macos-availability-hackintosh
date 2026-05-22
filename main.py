"""
check-macos-availability — main entry point.
Usage:  python main.py [--json]
"""
import sys
import argparse

from checkers.cpu         import get_cpu_info,     check_cpu
from checkers.gpu         import get_gpu_info,     check_gpu
from checkers.ram         import get_ram_info,     check_ram
from checkers.storage     import get_storage_info, check_storage
from checkers.wifi        import get_wifi_info,    check_wifi
from checkers.bios        import get_bios_info,    check_bios
from checkers.motherboard import get_mobo_info,    check_motherboard
from reporter             import print_report, export_json


def parse_args():
    p = argparse.ArgumentParser(
        description="check-macos-availability — Hackintosh compatibility scanner"
    )
    p.add_argument("--json", action="store_true", help="Export results to output/report.json")
    return p.parse_args()


def main():
    args = parse_args()

    print()
    print("  🍎  Scanning hardware — this may take a few seconds…")
    print()

    all_results: list[dict] = []

    # CPU
    cpu_info = get_cpu_info()
    all_results.append(check_cpu(cpu_info))

    # GPU (may return multiple)
    gpu_list = get_gpu_info()
    all_results.extend(check_gpu(gpu_list))

    # RAM
    ram_info = get_ram_info()
    all_results.append(check_ram(ram_info))

    # Storage (may return multiple)
    drive_list = get_storage_info()
    all_results.extend(check_storage(drive_list))

    # Wi-Fi
    wifi_list = get_wifi_info()
    all_results.extend(check_wifi(wifi_list))

    # Motherboard
    mobo_info = get_mobo_info()
    all_results.append(check_motherboard(mobo_info))

    # BIOS
    bios_info = get_bios_info()
    all_results.append(check_bios(bios_info))

    # Print report
    score = print_report(all_results)

    # Optional JSON export
    if args.json:
        export_json(all_results, score)

    sys.exit(0 if score >= 60 else 1)


if __name__ == "__main__":
    main()
