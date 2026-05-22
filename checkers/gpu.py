"""GPU compatibility checker."""
import subprocess
from data.compat_db import SUPPORTED_GPUS


def get_gpu_info() -> list[dict]:
    gpus = []
    try:
        r = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "Name,AdapterRAM", "/format:list"],
            capture_output=True, text=True, timeout=10
        )
        current: dict = {}
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Name="):
                current["name"] = line.split("=", 1)[1].strip()
            elif line.startswith("AdapterRAM="):
                try:
                    current["vram_gb"] = int(line.split("=",1)[1].strip()) // (1024**3)
                except (ValueError, ZeroDivisionError):
                    current["vram_gb"] = 0
                if current.get("name"):
                    gpus.append(current)
                current = {}
    except Exception:
        pass
    return gpus or [{"name": "Unknown", "vram_gb": 0}]


def _check_single_gpu(name: str) -> dict:
    name_l = name.lower()
    vendor = "unknown"
    if "nvidia" in name_l or "geforce" in name_l or "quadro" in name_l:
        vendor = "nvidia"
    elif "amd" in name_l or "radeon" in name_l or "rx " in name_l:
        vendor = "amd"
    elif "intel" in name_l or "uhd" in name_l or "iris" in name_l:
        vendor = "intel"

    result = {
        "label": "GPU",
        "detail": name,
        "vendor": vendor,
        "supported": False,
        "partial": False,
        "score": 0,
        "notes": [],
        "suggestions": [],
    }

    if vendor == "unknown":
        result["notes"].append("GPU vendor not recognised.")
        result["suggestions"].append("AMD Radeon RX 5xx/5xxx/6xxx or Intel UHD recommended.")
        return result

    db          = SUPPORTED_GPUS.get(vendor, {})
    unsupported = db.get("unsupported", [])
    supported   = db.get("supported", [])
    notes_map   = db.get("notes", {})

    for pat in unsupported:
        if pat in name_l:
            result["notes"].append(f"GPU matches unsupported pattern: {pat!r}.")
            if vendor == "nvidia":
                result["suggestions"].append("Pascal (10xx) and newer NVIDIA GPUs have no macOS driver. Replace with an AMD RX 5xx/6xxx or use Intel iGPU.")
            else:
                result["suggestions"].append("This GPU is not supported. Check the Dortania GPU Buyers Guide.")
            return result

    for pat in supported:
        if pat in name_l:
            result["supported"] = True
            result["score"]     = 90
            for nk, nv in notes_map.items():
                if nk in name_l:
                    result["notes"].append(nv)
                    result["partial"] = True
                    result["score"]   = 65
            if not result["notes"]:
                result["notes"].append("GPU is natively supported by macOS.")
            return result

    result["partial"]  = True
    result["score"]    = 40
    result["notes"].append("GPU not found in database — research required before proceeding.")
    result["suggestions"].append("Consult the Dortania GPU Buyers Guide for your model.")
    return result


def check_gpu(gpu_list: list[dict]) -> list[dict]:
    return [_check_single_gpu(g["name"]) for g in gpu_list]
