"""Storage compatibility checker."""
import subprocess
from data.compat_db import MIN_STORAGE_GB, RECOMMENDED_STORAGE_GB


def get_storage_info() -> list[dict]:
    drives = []
    try:
        r = subprocess.run(
            ["wmic", "diskdrive", "get", "Model,Size,MediaType", "/format:list"],
            capture_output=True, text=True, timeout=10
        )
        current: dict = {}
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Model="):
                current["model"] = line.split("=",1)[1].strip()
            elif line.startswith("Size="):
                try: current["size_gb"] = int(line.split("=",1)[1].strip()) // (1024**3)
                except ValueError: current["size_gb"] = 0
            elif line.startswith("MediaType="):
                current["media_type"] = line.split("=",1)[1].strip()
                if current.get("model"):
                    drives.append(current)
                current = {}
    except Exception:
        pass
    return drives or [{"model": "Unknown", "size_gb": 0, "media_type": "Unknown"}]


def _classify(model: str, media_type: str) -> str:
    m = (model + " " + media_type).lower()
    if "nvme" in m or "m.2" in m:  return "NVMe SSD"
    if "ssd" in m:                  return "SATA SSD"
    if "hdd" in m or "hard disk" in m or "fixed" in m: return "HDD"
    return "Unknown"


def check_storage(drive_list: list[dict]) -> list[dict]:
    results = []
    for d in drive_list:
        storage_type = _classify(d.get("model",""), d.get("media_type",""))
        gb = d.get("size_gb", 0)
        r = {
            "label": "Storage",
            "detail": f"{storage_type} ({gb} GB)" if gb else storage_type,
            "supported": False,
            "partial": False,
            "score": 0,
            "notes": [],
            "suggestions": [],
        }
        if storage_type == "NVMe SSD":
            r["supported"] = True
            r["score"]     = 100
            r["notes"].append("NVMe SSD — optimal for macOS.")
        elif storage_type == "SATA SSD":
            r["supported"] = True
            r["score"]     = 90
            r["notes"].append("SATA SSD — fully supported.")
        elif storage_type == "HDD":
            r["supported"] = True
            r["partial"]   = True
            r["score"]     = 60
            r["notes"].append("HDD works but macOS will feel sluggish.")
            r["suggestions"].append("An NVMe or SATA SSD is strongly recommended.")
        else:
            r["partial"] = True
            r["score"]   = 50
            r["notes"].append("Storage type unclear — likely compatible.")

        if 0 < gb < MIN_STORAGE_GB:
            r["supported"] = False
            r["score"]     = max(r["score"] - 40, 0)
            r["notes"].append(f"Drive is only {gb} GB — macOS needs at least {MIN_STORAGE_GB} GB free.")
            r["suggestions"].append(f"Use a drive with at least {RECOMMENDED_STORAGE_GB} GB.")
        results.append(r)
    return results
