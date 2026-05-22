"""Storage compatibility checker."""
import subprocess
from data.compat_db import MIN_STORAGE_GB, RECOMMENDED_STORAGE_GB


def get_storage_info() -> list:
    drives = []
    try:
        r = subprocess.run(
            ["wmic","diskdrive","get","Model,Size,MediaType","/format:list"],
            capture_output=True, text=True, timeout=10)
        cur = {}
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Model="):
                cur["model"] = line.split("=",1)[1].strip()
            elif line.startswith("Size="):
                try: cur["size_gb"] = int(line.split("=",1)[1].strip()) // (1024**3)
                except ValueError: cur["size_gb"] = 0
            elif line.startswith("MediaType="):
                cur["media_type"] = line.split("=",1)[1].strip()
                if cur.get("model"):
                    drives.append(cur)
                cur = {}
    except Exception:
        pass
    return drives or [{"model":"Unknown","size_gb":0,"media_type":"Unknown"}]


def _classify(model: str, media_type: str) -> str:
    m = (model + " " + media_type).lower()
    if "nvme" in m or "m.2" in m: return "NVMe SSD"
    if "ssd" in m:                 return "SATA SSD"
    if "hdd" in m or "fixed" in m or "hard disk" in m: return "HDD"
    return "Unknown"


def check_storage(drive_list: list) -> list:
    results = []
    for d in drive_list:
        stype = _classify(d.get("model",""), d.get("media_type",""))
        gb    = d.get("size_gb", 0)
        r = {
            "label":"Storage",
            "detail":f"{stype} ({gb} GB)" if gb else stype,
            "supported":False, "partial":False, "score":0,
            "notes":[], "suggestions":[],
        }
        if stype == "NVMe SSD":
            r.update({"supported":True,"score":100})
            r["notes"].append("NVMe SSD -- optimal for macOS.")
        elif stype == "SATA SSD":
            r.update({"supported":True,"score":90})
            r["notes"].append("SATA SSD -- fully supported.")
        elif stype == "HDD":
            r.update({"supported":True,"partial":True,"score":60})
            r["notes"].append("HDD works but macOS will feel sluggish.")
            r["suggestions"].append("An NVMe or SATA SSD is strongly recommended.")
        else:
            r.update({"partial":True,"score":50})
            r["notes"].append("Storage type unclear -- likely compatible.")
        if 0 < gb < MIN_STORAGE_GB:
            r["supported"] = False
            r["score"]     = max(r["score"]-40, 0)
            r["notes"].append(f"Drive is only {gb} GB -- macOS needs at least {MIN_STORAGE_GB} GB.")
            r["suggestions"].append(f"Use a drive with at least {RECOMMENDED_STORAGE_GB} GB.")
        results.append(r)
    return results
