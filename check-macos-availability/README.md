# check-macos-availability

> Check if your Windows PC can run macOS (Hackintosh)

`check-macos-availability` scans your Windows hardware and reports
whether it is compatible with macOS via
[OpenCore](https://dortania.github.io/OpenCore-Install-Guide/).

---

## What it checks

| Component     | Details                                         |
|---------------|-------------------------------------------------|
| CPU           | Vendor, model, generation support               |
| GPU           | Vendor, model, driver / kext availability       |
| RAM           | Capacity vs macOS minimums                      |
| Storage       | Type (NVMe / SATA SSD / HDD) and capacity       |
| Wi-Fi         | Adapter model and kext availability             |
| Motherboard   | Vendor, chipset, known quirks                   |
| BIOS/Firmware | UEFI vs Legacy, Secure Boot, TPM                |

---

## Example output

```
==============================================================
               macOS Compatibility Report
==============================================================

CPU           Intel Core i7-10700K          Supported
GPU           NVIDIA RTX 3070               Unsupported
               -> Pascal+ NVIDIA GPUs have no macOS driver.
RAM           32 GB                          Supported
Storage       NVMe SSD (1000 GB)             Supported
Wi-Fi         Intel AX200                   Supported
Motherboard   ASUS ROG STRIX Z490-E          Supported
BIOS/Firmware UEFI                           Supported

--------------------------------------------------------------
  Compatibility Score:  [################......] 82%
--------------------------------------------------------------

  Recommendation:
    Workable with some effort and BIOS tweaks.
    Unsupported: NVIDIA RTX 3070
    Guide: https://dortania.github.io/OpenCore-Install-Guide/
```

---

## Installation

```bash
git clone https://github.com/yourusername/check-macos-availability.git
cd check-macos-availability
pip install -r requirements.txt
```

> Run as Administrator so WMIC and PowerShell can read all hardware info.

---

## Usage

```bash
python main.py           # scan and print report
python check.py          # identical alias
python main.py --json    # scan + save output/report.json
```

---

## Supported macOS versions

- macOS Ventura (13)
- macOS Sonoma (14)
- macOS Sequoia (15)

---

## Requirements

- Python 3.10+
- Windows 10 or Windows 11
- Administrator privileges recommended

---

## Project layout

```
check-macos-availability/
├── main.py
├── check.py
├── reporter.py
├── requirements.txt
├── checkers/
│   ├── cpu.py
│   ├── gpu.py
│   ├── ram.py
│   ├── storage.py
│   ├── wifi.py
│   ├── bios.py
│   └── motherboard.py
├── data/
│   └── compat_db.py
└── output/
```

---

## Roadmap

- [ ] GUI version (Tkinter / web)
- [x] JSON export (`--json` flag)
- [ ] Auto-download recommended kexts
- [ ] OpenCore config.plist generator
- [ ] Linux support

---

## Disclaimer

This tool does **not** install macOS. It only checks hardware compatibility.
Hackintosh success depends on firmware version, BIOS settings, and driver
availability. Always consult the
[Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/).

---

## License

MIT License -- Copyright (c) 2026 adv2331  
Built for the Hackintosh community
