"""RAM compatibility checker."""
import subprocess
from data.compat_db import MIN_RAM_GB, RECOMMENDED_RAM_GB


def get_ram_info() -> dict:
    info = {"total_gb":0,"sticks":0,"speed_mhz":0}
    try:
        r = subprocess.run(
            ["wmic","memorychip","get","Capacity,Speed","/format:list"],
            capture_output=True, text=True, timeout=10)
        total = sticks = speed = 0
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Capacity="):
                try: total += int(line.split("=",1)[1].strip()); sticks += 1
                except ValueError: pass
            elif line.startswith("Speed=") and speed == 0:
                try: speed = int(line.split("=",1)[1].strip())
                except ValueError: pass
        info.update({"total_gb":total//(1024**3),"sticks":sticks,"speed_mhz":speed})
    except Exception:
        pass
    return info


def check_ram(ram_info: dict) -> dict:
    gb = ram_info.get("total_gb", 0)
    result = {
        "label":"RAM", "detail":f"{gb} GB" if gb else "Unknown",
        "supported":False, "partial":False, "score":0,
        "notes":[], "suggestions":[],
    }
    if gb == 0:
        result.update({"partial":True,"score":50})
        result["notes"].append("Could not read RAM -- assuming compatible.")
        return result
    if gb < MIN_RAM_GB:
        result["score"] = 10
        result["notes"].append(f"{gb} GB is below the {MIN_RAM_GB} GB minimum for macOS.")
        result["suggestions"].append(f"Upgrade to at least {MIN_RAM_GB} GB ({RECOMMENDED_RAM_GB} GB recommended).")
    elif gb < RECOMMENDED_RAM_GB:
        result.update({"supported":True,"partial":True,"score":70})
        result["notes"].append(f"{gb} GB meets the minimum; {RECOMMENDED_RAM_GB} GB+ recommended.")
        result["suggestions"].append(f"Consider upgrading to {RECOMMENDED_RAM_GB} GB or more.")
    else:
        result.update({"supported":True,"score":100})
        result["notes"].append(f"{gb} GB -- more than sufficient for macOS.")
    return result
