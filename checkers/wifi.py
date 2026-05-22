"""Wi-Fi / Bluetooth compatibility checker."""
import subprocess
from data.compat_db import SUPPORTED_WIFI


def get_wifi_info() -> list[dict]:
    adapters = []
    try:
        r = subprocess.run(
            ["wmic", "path", "Win32_NetworkAdapter", "where",
             "AdapterTypeId=9", "get", "Name,MACAddress", "/format:list"],
            capture_output=True, text=True, timeout=10
        )
        current: dict = {}
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Name="):
                current["name"] = line.split("=",1)[1].strip()
            elif line.startswith("MACAddress="):
                current["mac"] = line.split("=",1)[1].strip()
                if current.get("name"):
                    adapters.append(current)
                current = {}
    except Exception:
        pass
    return adapters or [{"name": "Unknown", "mac": ""}]


def _check_single_wifi(name: str) -> dict:
    name_l = name.lower()
    result = {
        "label": "Wi-Fi",
        "detail": name,
        "supported": False,
        "partial": False,
        "score": 0,
        "notes": [],
        "suggestions": [],
    }
    notes_map   = SUPPORTED_WIFI.get("notes", {})
    unsupported = SUPPORTED_WIFI.get("unsupported", [])
    supported   = SUPPORTED_WIFI.get("supported", [])

    for pat in unsupported:
        if pat in name_l:
            result["notes"].append(f"Wi-Fi adapter matches unsupported pattern: {pat!r}.")
            result["suggestions"].append(
                "Replace with a Broadcom BCM94360/BCM94352 card or use Intel AX200/AX210 with itlwm kext."
            )
            return result

    for pat in supported:
        if pat in name_l:
            result["supported"] = True
            result["score"]     = 90
            if any(b in name_l for b in ("bcm94", "dw1")):
                result["notes"].append(notes_map.get("broadcom", "Broadcom — full native support."))
                result["score"] = 100
            elif any(i in name_l for i in ("ax200","ax201","ax210","ax211","ac 9","ac 8","ac 7","ac 3")):
                result["notes"].append(notes_map.get("intel", "Intel — works via itlwm kext."))
                result["score"] = 80
            else:
                result["notes"].append("Adapter appears supported.")
            return result

    result["partial"]  = True
    result["score"]    = 40
    result["notes"].append("Wi-Fi adapter not in database — compatibility unknown.")
    result["suggestions"].append("Check OpenIntelWireless or AppleIntelWiFi project pages.")
    return result


def check_wifi(adapter_list: list[dict]) -> list[dict]:
    return [_check_single_wifi(a["name"]) for a in adapter_list]
