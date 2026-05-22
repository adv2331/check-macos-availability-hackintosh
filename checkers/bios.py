"""BIOS/firmware mode checker (UEFI vs Legacy)."""
import subprocess
import os


def get_bios_info() -> dict:
    info = {"mode": "Unknown", "secure_boot": "Unknown", "tpm": "Unknown"}
    # UEFI detection: EFI System Partition presence
    try:
        r = subprocess.run(
            ["bcdedit", "/enum", "firmware"],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0 and "firmware" in r.stdout.lower():
            info["mode"] = "UEFI"
        else:
            info["mode"] = "Legacy (BIOS)"
    except Exception:
        # Fallback: check for EFI env vars
        try:
            r2 = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "Confirm-SecureBootUEFI"],
                capture_output=True, text=True, timeout=10
            )
            info["mode"] = "UEFI" if r2.returncode == 0 else "Unknown"
        except Exception:
            pass

    # Secure Boot
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Confirm-SecureBootUEFI"],
            capture_output=True, text=True, timeout=10
        )
        out = r.stdout.strip().lower()
        info["secure_boot"] = "Enabled" if out == "true" else ("Disabled" if out == "false" else "Unknown")
    except Exception:
        pass

    # TPM
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-WmiObject -Namespace root/cimv2/security/microsofttpm -Class Win32_Tpm).IsEnabled_InitialValue"],
            capture_output=True, text=True, timeout=10
        )
        out = r.stdout.strip().lower()
        info["tpm"] = "Present" if out == "true" else ("Absent" if out == "false" else "Unknown")
    except Exception:
        pass

    return info


def check_bios(bios_info: dict) -> dict:
    mode = bios_info.get("mode", "Unknown")
    sb   = bios_info.get("secure_boot", "Unknown")
    tpm  = bios_info.get("tpm", "Unknown")

    result = {
        "label": "BIOS/Firmware",
        "detail": mode,
        "supported": False,
        "partial": False,
        "score": 0,
        "notes": [],
        "suggestions": [],
        "extra": {"secure_boot": sb, "tpm": tpm},
    }

    if mode == "UEFI":
        result["supported"] = True
        result["score"]     = 100
        result["notes"].append("UEFI firmware detected — required for OpenCore.")
    elif mode == "Legacy (BIOS)":
        result["notes"].append("Legacy BIOS detected. OpenCore requires UEFI mode.")
        result["suggestions"].append("Enable UEFI mode in your BIOS settings (disable CSM/Legacy Support).")
        result["score"] = 10
    else:
        result["partial"] = True
        result["score"]   = 50
        result["notes"].append("BIOS mode could not be determined.")

    if sb == "Enabled":
        result["notes"].append("Secure Boot is ON — must be disabled for OpenCore to boot.")
        result["suggestions"].append("Disable Secure Boot in BIOS/UEFI settings.")
        result["score"] = max(result["score"] - 20, 0)

    if tpm == "Present":
        result["notes"].append("TPM detected — not required for Hackintosh but not harmful.")

    return result
