"""RAM compatibility checker."""
import subprocess
from data.compat_db import MIN_RAM_GB, RECOMMENDED_RAM_GB


def get_ram_info() -> dict:
    info = {"total_gb": 0, "sticks": 0, "speed_mhz": 0}
    try:
        r = subprocess.run(
            ["wmic", "memorychip", "get", "Capacity,Speed", "/format:list"],
            capture_output=True, text=True, timeout=10
        )
        total_bytes = 0
        sticks = 0
        speed  = 0
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Capacity="):
                try:
                    total_bytes += int(line.split("=",1)[1].strip())
                    sticks += 1
                except ValueError: pass
            elif line.startswith("Speed=") and speed == 0:
                try: speed = int(line.split("=",1)[1].strip())
                except ValueError: pass
        info["total_gb"] = total_bytes // (1024**3)
        info["sticks"]   = sticks
        info["speed_mhz"] = speed
    except Exception:
        pass
    return info


def check_ram(ram_info: dict) -> dict:
    gb = ram_info.get("total_gb", 0)
    result = {
        "label": "RAM",
        "detail": f"{gb} GB",
        "supported": False,
        "partial": False,
        "score": 0,
        "notes": [],
        "suggestions": [],
    }
    if gb == 0:
        result["notes"].append("Could not read RAM information.")
        result["score"] = 50
        return result
    if gb < MIN_RAM_GB:
        result["notes"].append(f"Only {gb} GB detected — macOS requires at least {MIN_RAM_GB} GB.")
        result["suggestions"].append(f"Upgrade to at least {MIN_RAM_GB} GB RAM ({RECOMMENDED_RAM_GB} GB recommended).")
        result["score"] = 10
    elif gb < RECOMMENDED_RAM_GB:
        result["supported"] = True
        result["partial"]   = True
        result["score"]     = 70
        result["notes"].append(f"{gb} GB meets the minimum but {RECOMMENDED_RAM_GB} GB is recommended for comfort.")
        result["suggestions"].append(f"Consider upgrading to {RECOMMENDED_RAM_GB} GB or more.")
    else:
        result["supported"] = True
        result["score"]     = 100
        result["notes"].append(f"{gb} GB — more than sufficient for macOS.")
    return result
