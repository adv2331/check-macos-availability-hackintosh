"""GPU compatibility checker."""
import subprocess
from data.compat_db import SUPPORTED_GPUS


def get_gpu_info() -> list:
    gpus = []
    try:
        r = subprocess.run(
            ["wmic","path","win32_VideoController",
             "get","Name,AdapterRAM","/format:list"],
            capture_output=True, text=True, timeout=10)
        cur = {}
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Name="):
                cur["name"] = line.split("=",1)[1].strip()
            elif line.startswith("AdapterRAM="):
                try: cur["vram_gb"] = int(line.split("=",1)[1].strip()) // (1024**3)
                except (ValueError, ZeroDivisionError): cur["vram_gb"] = 0
                if cur.get("name"):
                    gpus.append(cur)
                cur = {}
    except Exception:
        pass
    return gpus or [{"name":"Unknown","vram_gb":0}]


def _vendor(name_l: str) -> str:
    if any(k in name_l for k in ("nvidia","geforce","quadro","rtx ","gtx ")):
        return "nvidia"
    if any(k in name_l for k in ("amd","radeon","rx ","vega","r9 ")):
        return "amd"
    if any(k in name_l for k in ("intel","uhd","iris","hd graphics")):
        return "intel"
    return "unknown"


def _check_single(name: str) -> dict:
    name_l = name.lower()
    vendor = _vendor(name_l)
    result = {
        "label":"GPU", "detail":name, "vendor":vendor,
        "supported":False, "partial":False, "score":0,
        "notes":[], "suggestions":[],
    }
    if vendor == "unknown":
        result["notes"].append("GPU vendor not recognised.")
        result["suggestions"].append("AMD Radeon RX 5xx/5xxx/6xxx or Intel UHD is recommended.")
        return result

    db = SUPPORTED_GPUS.get(vendor, {})
    for pat in db.get("unsupported",[]):
        if pat in name_l:
            result["notes"].append(f"GPU matches unsupported pattern: {pat!r}.")
            if vendor == "nvidia":
                result["suggestions"].append(
                    "Pascal (10xx)+ NVIDIA GPUs have no macOS driver. "
                    "Replace with an AMD RX 5xx/6xxx or use the Intel iGPU.")
            else:
                result["suggestions"].append("Check the Dortania GPU Buyers Guide for alternatives.")
            return result

    for pat in db.get("supported",[]):
        if pat in name_l:
            result["supported"] = True
            result["score"]     = 90
            for nk, nv in db.get("notes",{}).items():
                if nk in name_l:
                    result["notes"].append(nv)
                    result["partial"] = True
                    result["score"]   = 65
            if not result["notes"]:
                result["notes"].append("GPU has native macOS support.")
            return result

    result["partial"] = True
    result["score"]   = 40
    result["notes"].append("GPU not in database -- research needed before proceeding.")
    result["suggestions"].append("Consult the Dortania GPU Buyers Guide for your model.")
    return result


def check_gpu(gpu_list: list) -> list:
    return [_check_single(g["name"]) for g in gpu_list]
