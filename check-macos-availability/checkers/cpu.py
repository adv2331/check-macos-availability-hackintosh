"""CPU compatibility checker."""
import subprocess, platform
from data.compat_db import SUPPORTED_CPU_FAMILIES


def get_cpu_info() -> dict:
    info = {"name":"Unknown","vendor":"Unknown","cores":0,"threads":0}
    try:
        r = subprocess.run(
            ["wmic","cpu","get",
             "Name,Manufacturer,NumberOfCores,NumberOfLogicalProcessors",
             "/format:list"],
            capture_output=True, text=True, timeout=10)
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Name="):
                info["name"] = line.split("=",1)[1].strip()
            elif line.startswith("Manufacturer="):
                m = line.split("=",1)[1].strip().lower()
                info["vendor"] = "intel" if "intel" in m else ("amd" if "amd" in m else m)
            elif line.startswith("NumberOfCores="):
                try: info["cores"] = int(line.split("=",1)[1].strip())
                except ValueError: pass
            elif line.startswith("NumberOfLogicalProcessors="):
                try: info["threads"] = int(line.split("=",1)[1].strip())
                except ValueError: pass
    except Exception:
        info["name"] = platform.processor()
        nl = info["name"].lower()
        info["vendor"] = "intel" if "intel" in nl else ("amd" if "amd" in nl else "Unknown")
    return info


def check_cpu(cpu_info: dict) -> dict:
    result = {
        "label":"CPU", "detail":cpu_info.get("name","Unknown"),
        "supported":False, "partial":False, "score":0,
        "notes":[], "suggestions":[],
    }
    vendor = cpu_info.get("vendor","").lower()
    name_l = cpu_info.get("name","").lower()

    if vendor not in ("intel","amd"):
        result["notes"].append("Unrecognised CPU vendor -- only Intel and AMD are supported.")
        result["suggestions"].append("Use an Intel 6th-13th gen Core or AMD Ryzen CPU.")
        return result

    db = SUPPORTED_CPU_FAMILIES[vendor]
    for pat in db["unsupported"]:
        if pat in name_l:
            result["notes"].append(f"CPU matches unsupported category: {pat!r}.")
            result["suggestions"].append(
                "Target Intel 6th-13th gen Core i-series or AMD Ryzen 1000-5000 series.")
            return result

    for pat in db["supported"]:
        if pat in name_l:
            result["supported"] = True
            result["score"]     = 90
            for nk, nv in db.get("notes",{}).items():
                if nk in name_l:
                    result["notes"].append(nv)
                    result["partial"] = True
                    result["score"]   = 70
            if vendor == "amd":
                g = db["notes"].get("amd_general","")
                if g and g not in result["notes"]:
                    result["notes"].append(g)
                result["score"] = min(result["score"], 80)
            if not result["notes"]:
                result["notes"].append("Well-supported CPU for Hackintosh.")
            return result

    result["partial"] = True
    result["score"]   = 30
    result["notes"].append("CPU not in database -- may work but needs manual research.")
    result["suggestions"].append("Check the Dortania OpenCore Install Guide for your CPU.")
    return result
