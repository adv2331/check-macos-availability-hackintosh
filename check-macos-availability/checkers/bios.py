"""BIOS/firmware checker (UEFI vs Legacy, Secure Boot, TPM)."""
import subprocess


def get_bios_info() -> dict:
    info = {"mode":"Unknown","secure_boot":"Unknown","tpm":"Unknown"}
    try:
        r = subprocess.run(["bcdedit","/enum","firmware"],
                           capture_output=True, text=True, timeout=10)
        info["mode"] = "UEFI" if r.returncode==0 and "firmware" in r.stdout.lower()                        else "Legacy (BIOS)"
    except Exception:
        try:
            r2 = subprocess.run(
                ["powershell","-NoProfile","-Command","Confirm-SecureBootUEFI"],
                capture_output=True, text=True, timeout=10)
            info["mode"] = "UEFI" if r2.returncode==0 else "Unknown"
        except Exception:
            pass
    try:
        r = subprocess.run(
            ["powershell","-NoProfile","-Command","Confirm-SecureBootUEFI"],
            capture_output=True, text=True, timeout=10)
        o = r.stdout.strip().lower()
        info["secure_boot"] = "Enabled" if o=="true" else ("Disabled" if o=="false" else "Unknown")
    except Exception:
        pass
    try:
        r = subprocess.run(
            ["powershell","-NoProfile","-Command",
             "(Get-WmiObject -Namespace root/cimv2/security/microsofttpm "
             "-Class Win32_Tpm).IsEnabled_InitialValue"],
            capture_output=True, text=True, timeout=10)
        o = r.stdout.strip().lower()
        info["tpm"] = "Present" if o=="true" else ("Absent" if o=="false" else "Unknown")
    except Exception:
        pass
    return info


def check_bios(bios_info: dict) -> dict:
    mode = bios_info.get("mode","Unknown")
    sb   = bios_info.get("secure_boot","Unknown")
    tpm  = bios_info.get("tpm","Unknown")
    result = {
        "label":"BIOS/Firmware", "detail":mode,
        "supported":False, "partial":False, "score":0,
        "notes":[], "suggestions":[],
        "extra":{"Secure Boot":sb, "TPM":tpm},
    }
    if mode == "UEFI":
        result.update({"supported":True,"score":100})
        result["notes"].append("UEFI firmware detected -- required by OpenCore.")
    elif mode == "Legacy (BIOS)":
        result["score"] = 10
        result["notes"].append("Legacy BIOS detected -- OpenCore requires UEFI mode.")
        result["suggestions"].append("Enable UEFI in BIOS settings and disable CSM/Legacy Support.")
    else:
        result.update({"partial":True,"score":50})
        result["notes"].append("BIOS mode could not be determined -- try running as Administrator.")
    if sb == "Enabled":
        result["score"] = max(result["score"]-20, 0)
        result["notes"].append("Secure Boot is ON -- must be disabled for OpenCore.")
        result["suggestions"].append("Disable Secure Boot in your UEFI settings.")
    if tpm == "Present":
        result["notes"].append("TPM detected -- not required for Hackintosh, not harmful either.")
    return result
