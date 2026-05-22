"""Terminal report renderer + optional JSON export."""
import json, os
from datetime import datetime

RST  = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
GRN  = "\033[92m"
YLW  = "\033[93m"
RED  = "\033[91m"
CYN  = "\033[96m"
W    = 62


def _icon(r: dict) -> str:
    if r.get("supported"): return f"{GRN}Supported{RST}"
    if r.get("partial"):   return f"{YLW}Partial{RST}"
    return f"{RED}Unsupported{RST}"


def _bar(score: int, width: int = 22) -> str:
    filled = int(score / 100 * width)
    bar    = chr(9608)*filled + chr(9617)*(width-filled)
    col    = GRN if score >= 75 else (YLW if score >= 50 else RED)
    return f"{col}[{bar}] {score}%{RST}"


def _overall(results: list) -> int:
    weights = {"CPU":2,"GPU":2,"RAM":1.5,"Storage":1,
               "Wi-Fi":1,"BIOS/Firmware":1.5,"Motherboard":1}
    tw = ts = 0.0
    for r in results:
        w   = weights.get(r.get("label",""), 1)
        tw += w
        ts += r.get("score",0) * w
    return int(ts/tw) if tw else 0


def _verdict(score: int, results: list) -> list:
    bad  = [r["detail"] for r in results if not r.get("supported") and not r.get("partial")]
    warn = [r["detail"] for r in results if r.get("partial")]
    lines = []
    if score >= 85:
        lines.append(f"{GRN}Excellent candidate for OpenCore Hackintosh.{RST}")
    elif score >= 65:
        lines.append(f"{YLW}Workable with some effort and BIOS tweaks.{RST}")
    elif score >= 40:
        lines.append(f"{YLW}Challenging -- significant hardware changes needed.{RST}")
    else:
        lines.append(f"{RED}Poor candidate -- major incompatibilities detected.{RST}")
    if bad:  lines.append(f"{RED}Unsupported: {', '.join(bad)}{RST}")
    if warn: lines.append(f"{YLW}Needs attention: {', '.join(warn)}{RST}")
    lines.append(f"{DIM}Guide: https://dortania.github.io/OpenCore-Install-Guide/{RST}")
    return lines


def print_report(results: list) -> int:
    score = _overall(results)
    print()
    print(f"{BOLD}{CYN}{'=' * W}{RST}")
    print(f"{BOLD}{CYN}{' macOS Compatibility Report ':^{W}}{RST}")
    print(f"{BOLD}{CYN}{'=' * W}{RST}")
    print()
    for r in results:
        lbl    = r.get("label","?")
        detail = r.get("detail","")
        trunc  = (detail[:28]+"...") if len(detail) > 30 else detail
        icon   = _icon(r)
        # status icons for terminal
        sym = "[OK]" if r.get("supported") else ("[??]" if r.get("partial") else "[X]")
        print(f"  {BOLD}{lbl:<14}{RST}{trunc:<32}{icon}")
        for k,v in r.get("extra",{}).items():
            print(f"  {DIM}     + {k}: {v}{RST}")
        for n in r.get("notes",[]):
            print(f"  {DIM}     * {n}{RST}")
        for s in r.get("suggestions",[]):
            print(f"  {YLW}     -> {s}{RST}")
        print()
    print(f"{BOLD}{'-' * W}{RST}")
    print(f"  {BOLD}Compatibility Score:{RST}  {_bar(score)}")
    print(f"{'-' * W}")
    print()
    print(f"  {BOLD}Recommendation:{RST}")
    for line in _verdict(score, results):
        print(f"    {line}")
    print()
    print(f"{BOLD}{CYN}{'=' * W}{RST}")
    print()
    return score


def export_json(results: list, score: int, path: str = "output/report.json") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8") as f:
        json.dump({"generated":datetime.now().isoformat(),
                   "score":score,"results":results}, f, indent=2)
    print(f"  Report saved -> {path}")
