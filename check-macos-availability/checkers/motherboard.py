"""Motherboard / chipset compatibility checker."""
import subprocess
from data.compat_db import GOOD_CHIPSETS, UNSUPPORTED_CHIPSETS, KNOWN_BOARD_VENDORS


def get_mobo_info() -> dict:
    info = {"manufacturer":"Unknown","model":"Unknown"}
    try:
        r = subprocess.run(
            ["wmic","baseboard","get","Manufacturer,Product","/format:list"],
            capture_output=True, text=True, timeout=10)
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Manufacturer="):
                info["manufacturer"] = line.split("=",1)[1].strip()
            elif line.startswith("Product="):
                info["model"] = line.split("=",1)[1].strip()
    except Exception:
        pass
    return info


def check_motherboard(mobo_info: dict) -> dict:
    mfr    = mobo_info.get("manufacturer","Unknown")
    model  = mobo_info.get("model","Unknown")
    name_l = (mfr + " " + model).lower()
    result = {
        "label":"Motherboard", "detail":f"{mfr} {model}",
        "supported":False, "partial":True, "score":55,
        "notes":[], "suggestions":[],
    }
    if any(v in name_l for v in KNOWN_BOARD_VENDORS):
        result["score"] += 10
        result["notes"].append(f"{mfr} is a well-supported board vendor in the Hackintosh community.")
    for cs in UNSUPPORTED_CHIPSETS:
        if cs in name_l:
            result["score"] = max(result["score"]-30, 5)
            result["notes"].append(f"Chipset {cs.upper()} has limited/no Hackintosh support yet.")
            result["suggestions"].append("Check Dortania guides for the latest chipset support status.")
    for cs in GOOD_CHIPSETS:
        if cs in name_l:
            result.update({"supported":True,"partial":False})
            result["score"] = min(result["score"]+25, 100)
            result["notes"].append(f"Chipset {cs.upper()} has known Hackintosh support.")
            break
    else:
        result["notes"].append("Chipset not auto-detected -- may still be compatible.")
        result["suggestions"].append("Verify at https://dortania.github.io/OpenCore-Install-Guide/")
    return result
