"""
check-macos-availability
Usage:  python main.py [--json]
"""
import sys, argparse

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
        description="check-macos-availability -- Hackintosh hardware scanner")
    p.add_argument("--json", action="store_true",
                   help="Also export results to output/report.json")
    return p.parse_args()


def main():
    args = parse_args()
    print("\n  Scanning hardware -- please wait...\n")

    results = []
    results.append(check_cpu(get_cpu_info()))
    results.extend(check_gpu(get_gpu_info()))
    results.append(check_ram(get_ram_info()))
    results.extend(check_storage(get_storage_info()))
    results.extend(check_wifi(get_wifi_info()))
    results.append(check_motherboard(get_mobo_info()))
    results.append(check_bios(get_bios_info()))

    score = print_report(results)
    if args.json:
        export_json(results, score)
    sys.exit(0 if score >= 60 else 1)


if __name__ == "__main__":
    main()
