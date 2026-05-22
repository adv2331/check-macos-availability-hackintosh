"""
Renders the final compatibility report to the terminal and optionally to JSON.
"""
import json
import os
from datetime import datetime


RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
DIM    = "\033[2m"


def _status_icon(result: dict) -> str:
    if result.get("supported"):
        return f"{GREEN}✅ Supported{RESET}"
    if result.get("partial"):
        return f"{YELLOW}⚠️  Partial{RESET}"
    return f"{RED}❌ Unsupported{RESET}"


def _score_bar(score: int, width: int = 20) -> str:
    filled = int(score / 100 * width)
    bar    = "█" * filled + "░" * (width - filled)
    color  = GREEN if score >= 75 else (YELLOW if score >= 50 else RED)
    return f"{color}[{bar}] {score}%{RESET}"


def compute_overall_score(all_results: list[dict]) -> int:
    weights = {"CPU":2, "GPU":2, "RAM":1.5, "Storage":1, "Wi-Fi":1, "BIOS/Firmware":1.5, "Motherboard":1}
    total_w = 0.0
    total_s = 0.0
    for r in all_results:
        w = weights.get(r.get("label",""), 1)
        total_w += w
        total_s += r.get("score", 0) * w
    return int(total_s / total_w) if total_w else 0


def _recommendation(score: int, all_results: list[dict]) -> str:
    unsupported = [r["detail"] for r in all_results if not r.get("supported") and not r.get("partial")]
    partial     = [r["detail"] for r in all_results if r.get("partial")]

    if score >= 85:
        verdict = f"{GREEN}Excellent candidate for OpenCore Hackintosh.{RESET}"
    elif score >= 65:
        verdict = f"{YELLOW}Workable with some effort and BIOS tweaks.{RESET}"
    elif score >= 40:
        verdict = f"{YELLOW}Challenging — significant hardware changes needed.{RESET}"
    else:
        verdict = f"{RED}Poor candidate — major incompatibilities detected.{RESET}"

    lines = [verdict]
    if unsupported:
        lines.append(f"{RED}Unsupported components: {', '.join(unsupported)}{RESET}")
    if partial:
        lines.append(f"{YELLOW}Needs attention: {', '.join(partial)}{RESET}")
    lines.append(f"{DIM}Refer to https://dortania.github.io/OpenCore-Install-Guide/ for full guidance.{RESET}")
    return "\n  ".join(lines)


def print_report(all_results: list[dict]) -> int:
    score = compute_overall_score(all_results)
    width = 60

    print()
    print(f"{BOLD}{CYAN}{'=' * width}{RESET}")
    print(f"{BOLD}{CYAN}{'  macOS Compatibility Report  ':^{width}}{RESET}")
    print(f"{BOLD}{CYAN}{'=' * width}{RESET}")
    print()

    for r in all_results:
        label  = r.get("label","?")
        detail = r.get("detail","")
        icon   = _status_icon(r)
        extra  = r.get("extra", {})

        detail_trunc = (detail[:30] + "…") if len(detail) > 32 else detail
        line = f"  {BOLD}{label:<14}{RESET}{detail_trunc:<34}{icon}"
        print(line)

        if extra:
            for k, v in extra.items():
                print(f"  {DIM}  └─ {k.replace('_',' ').title()}: {v}{RESET}")

        for note in r.get("notes", []):
            print(f"  {DIM}    • {note}{RESET}")

        if r.get("suggestions"):
            for sug in r["suggestions"]:
                print(f"  {YELLOW}    → {sug}{RESET}")
        print()

    print(f"{BOLD}{'─' * width}{RESET}")
    print(f"  {BOLD}Compatibility Score:{RESET}  {_score_bar(score)}")
    print(f"{'─' * width}")
    print()
    print(f"  {BOLD}Recommendation:{RESET}")
    print(f"  {_recommendation(score, all_results)}")
    print()
    print(f"{BOLD}{CYAN}{'=' * width}{RESET}")
    print()
    return score


def export_json(all_results: list[dict], score: int, path: str = "output/report.json") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {
        "generated": datetime.now().isoformat(),
        "score": score,
        "results": all_results,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"  Report saved to {path}")
