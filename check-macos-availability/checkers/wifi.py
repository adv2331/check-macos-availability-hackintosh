"""Wi-Fi / Bluetooth compatibility checker."""
import subprocess
from data.compat_db import SUPPORTED_WIFI


def get_wifi_info() -> list:
    adapters = []
    try:
        r = subprocess.run(
            ["wmic","path","Win32_NetworkAdapter",
             "where","AdapterTypeId=9",
             "get","Name,MACAddress","/format:list"],
            capture_output=True, text=True, timeout=10)
        cur = {}
        for line in r.stdout.splitlines():
            line = line.strip()
            if line.startswith("Name="):
                cur["name"] = line.split("=",1)[1].strip()
            elif line.startswith("MACAddress="):
                cur["mac"] = line.split("=",1)[1].strip()
                if cur.get("name"):
                    adapters.append(cur)
                cur = {}
    except Exception:
        pass
    return adapters or [{"name":"Unknown","mac":""}]


def _check_single(name: str) -> dict:
    name_l = name.lower()
    nm = SUPPORTED_WIFI.get("notes", {})
    result = {
        "label":"Wi-Fi", "detail":name,
        "supported":False, "partial":False, "score":0,
        "notes":[], "suggestions":[],
    }
    for pat in SUPPORTED_WIFI.get("unsupported",[]):
        if pat in name_l:
            result["notes"].append(f"Adapter matches unsupported pattern: {pat!r}.")
            result["suggestions"].append(
                "Replace with a Broadcom BCM94360/BCM94352 card, "
                "or use an Intel AX200/AX210 with the itlwm kext.")
            return result

    for pat in SUPPORTED_WIFI.get("supported",[]):
        if pat in name_l:
            result["supported"] = True
            result["score"]     = 90
            if any(b in name_l for b in ("bcm94","dw1")):
                result["notes"].append(nm.get("broadcom","Broadcom -- full native support."))
                result["score"] = 100
            elif any(i in name_l for i in ("ax2","ax1","ac 9","ac 8","ac 7","ac 3")):
                result["notes"].append(nm.get("intel","Intel -- works via itlwm kext."))
                result["score"] = 80
            else:
                result["notes"].append("Adapter appears supported.")
            return result

    result.update({"partial":True,"score":40})
    result["notes"].append("Wi-Fi adapter not in database -- compatibility unknown.")
    result["suggestions"].append("Check OpenIntelWireless project or community forums.")
    return result


def check_wifi(adapter_list: list) -> list:
    return [_check_single(a["name"]) for a in adapter_list]
