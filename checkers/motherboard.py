"""Motherboard / chipset compatibility checker."""
import subprocess

UNSUPPORTED_CHIPSETS = [
    "z790", "z890",   # Too new, limited
    "b760", "b860",
    "h770", "h870",
    "w790",
]

GOOD_CHIPSETS = [
    "z490","z590","z690","z790","h470","b460","b560","b660",
    "z390","z370","h370","b360","h310",
    "z270","z170","h270","b250","h170",
    "x299","x399","x570","b550","a520","x470","b450","x370","b350","a320",
]

SUPPORTED_VENDORS = ["asus","gigabyte","msi","asrock","biostar","supermicro"]


def get_mobo_info() -> dict:
    info = {"manufacturer": "Unknown", "model": "Unknown", "chipset": "Unknown"}
    try:
        r = subprocess.run(
            ["wmic", "baseboard", "get", "Manufacturer,Product", "/format:list"],
            capture_output=True, text=True, timeout=10
        )
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
    mfr   = mobo_info.get("manufacturer", "Unknown")
    model = mobo_info.get("model", "Unknown")
    name_l = (mfr + " " + model).lower()

    result = {
        "label": "Motherboard",
        "detail": f"{mfr} {model}",
        "supported": False,
        "partial": True,
        "score": 60,
        "notes": [],
        "suggestions": [],
    }

    vendor_ok = any(v in name_l for v in SUPPORTED_VENDORS)
    if vendor_ok:
        result["score"] += 15
        result["notes"].append(f"{mfr} is a well-known board vendor with Hackintosh community support.")

    chipset_found = False
    for cs in GOOD_CHIPSETS:
        if cs in name_l:
            chipset_found = True
            result["supported"] = True
            result["partial"]   = False
            result["score"]     = min(result["score"] + 20, 100)
            result["notes"].append(f"Chipset {cs.upper()} has known Hackintosh support.")
            break

    for cs in UNSUPPORTED_CHIPSETS:
        if cs in name_l:
            result["notes"].append(f"Chipset {cs.upper()} has limited / no Hackintosh support currently.")
            result["suggestions"].append("Check Dortania guides for the latest chipset support status.")
            result["score"] = max(result["score"] - 30, 10)

    if not chipset_found:
        result["notes"].append("Chipset not auto-detected — may still be compatible.")
        result["suggestions"].append("Verify your chipset at https://dortania.github.io/OpenCore-Install-Guide/")

    return result
