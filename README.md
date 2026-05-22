# check-macos-availability 🍎

> **Check if your Windows PC can run macOS (Hackintosh)**

`check-macos-availability` scans your Windows hardware and tells you
whether it is compatible with macOS via OpenCore.

---

## What it checks

| Component | Details |
|-----------|---------|
| CPU | Vendor, model, generation, AVX2 support |
| GPU | Vendor, model, driver availability |
| RAM | Total capacity vs. macOS minimums |
| Storage | Drive type (NVMe / SATA SSD / HDD) and size |
| Wi-Fi | Adapter model and kext availability |
| Motherboard | Vendor, chipset, known quirks |
| BIOS/Firmware | UEFI vs Legacy, Secure Boot, TPM |

---

## Example output

```
============================================================
              macOS Compatibility Report
============================================================

CPU           Intel Core i7-10700K          ✅ Supported
GPU           NVIDIA RTX 3070               ❌ Unsupported
               → Pascal+ NVIDIA GPUs have no macOS driver.
RAM           32 GB                          ✅ Supported
Storage       NVMe SSD (1000 GB)             ✅ Supported
Wi-Fi         Intel AX200                    ✅ Supported
Motherboard   ASUS ROG STRIX Z490-E          ✅ Supported
BIOS/Firmware UEFI                           ✅ Supported

────────────────────────────────────────────────────────────
  Compatibility Score:  [████████████████░░░░] 82%
────────────────────────────────────────────────────────────

  Recommendation:
  Workable with some effort and BIOS tweaks.
  Unsupported components: NVIDIA RTX 3070
  Refer to https://dortania.github.io/OpenCore-Install-Guide/
```

---

## Installation

```bash
git clone https://github.com/yourusername/check-macos-availability.git
cd check-macos-availability
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py          # standard scan
python check.py         # alias — identical behaviour
python main.py --json   # scan + export output/report.json
```

> **Administrator privileges are recommended** so that WMIC and
> PowerShell calls can read all hardware information.

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

## Project structure

```
check-macos-availability/
├── main.py               # Main entry point
├── check.py              # Alias entry point
├── reporter.py           # Terminal + JSON output
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
│   └── compat_db.py      # Hardware compatibility database
└── output/               # JSON reports saved here
```

---

## Roadmap

- [ ] GUI version (Tkinter / web)
- [ ] Export results to JSON (`--json` flag ✅ done)
- [ ] Auto-download recommended kexts
- [ ] OpenCore `config.plist` suggestions
- [ ] Linux support

---

## Disclaimer

This tool **does not install macOS**. It only checks compatibility.
Hackintosh success depends on firmware settings, BIOS version, and
driver availability. Always consult the
[Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/).

---

## License

MIT License — Copyright (c) 2026 adv2331

Built for the Hackintosh community 🍎
