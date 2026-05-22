"""CPU compatibility checker."""
import re
import subprocess
import platform
from data.compat_db import SUPPORTED_CPU_FAMILIES


def get_cpu_info() -> dict:
    info = {"name": "Unknown", "vendor": "Unknown", "cores": 0, "threads": 0}
    try:
        r = subprocess.run(
            ["wmic", "cpu", "get", "Name,Manufacturer,NumberOfCores,NumberOfLogicalProcessors", "/format:list"],
            capture_output=True, text=True, timeout=10
        )
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Name="):
                info["name"] = line.split("=", 1)[1].strip()
            elif line.startswith("Manufacturer="):
                mfr = line.split("=", 1)[1].strip().lower()
                info["vendor"] = "intel" if "intel" in mfr else ("amd" if "amd" in mfr else mfr)
            elif line.startswith("NumberOfCores="):
                try: info["cores"] = int(line.split("=",1)[1].strip())
                except ValueError: pass
            elif line.startswith("NumberOfLogicalProcessors="):
                try: info["threads"] = int(line.split("=",1)[1].strip())
                except ValueError: pass
    except Exception:
        info["name"] = platform.processor()
        name_l = info["name"].lower()
        if "intel" in name_l: info["vendor"] = "intel"
        elif "amd" in name_l: info["vendor"] = "amd"
    return info


def check_cpu(cpu_info: dict) -> dict:
    result = {
        "label": "CPU",
        "detail": cpu_info.get("name", "Unknown"),
        "supported": False,
        "partial": False,
        "score": 0,
        "notes": [],
        "suggestions": [],
    }
    vendor  = cpu_info.get("vendor", "").lower()
    name_l  = cpu_info.get("name", "").lower()

    if vendor not in ("intel", "amd"):
        result["notes"].append("Unrecognised CPU vendor — only Intel and AMD are supported.")
        result["suggestions"].append("Use an Intel (6th–13th gen) or AMD Ryzen CPU.")
        return result

    db           = SUPPORTED_CPU_FAMILIES[vendor]
    unsupported  = db["unsupported"]
    supported    = db["supported"]
    notes_map    = db.get("notes", {})

    for pat in unsupported:
        if pat in name_l:
            result["notes"].append(f"CPU matches unsupported category: {pat!r}.")
            if vendor == "intel":
                result["suggestions"].append("Low-end / too-new Intel CPUs are not supported. Target 6th–13th gen Core i-series.")
            else:
                result["suggestions"].append("This AMD CPU family is not supported. Use Ryzen 1000–5000 series.")
            return result

    for pat in supported:
        if pat in name_l:
            result["supported"] = True
            result["score"]     = 90
            for nk, nv in notes_map.items():
                if nk in name_l:
                    result["notes"].append(nv)
                    result["partial"] = True
                    result["score"]   = 70
            if vendor == "amd":
                gen_note = notes_map.get("amd_general", "")
                if gen_note and gen_note not in result["notes"]:
                    result["notes"].append(gen_note)
                result["score"] = min(result["score"], 80)
            if not result["notes"]:
                result["notes"].append("Well-supported CPU for Hackintosh.")
            return result

    result["partial"]  = True
    result["score"]    = 30
    result["notes"].append("CPU not found in database — may work but requires manual research.")
    result["suggestions"].append("Check the Dortania OpenCore install guide for your CPU.")
    return result
