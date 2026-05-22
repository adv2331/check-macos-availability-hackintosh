# check-macos-availability

Check if your Windows computer can support macOS.

## What is this?

`check-macos-availability` scans your Windows PC and determines whether it can run macOS (Hackintosh).

It checks your hardware and gives:
- compatibility status
- a score
- unsupported components
- suggested fixes

---

## Features

- Detect CPU compatibility
- Detect GPU compatibility
- Check RAM requirements
- Check storage compatibility
- Check motherboard/chipset support
- Detect Wi-Fi/Bluetooth support
- Detect BIOS mode (UEFI/Legacy)
- Compatibility score output
- Suggestions for unsupported hardware

---

## Example Output

```text
=== macOS Compatibility Report ===

CPU: Intel Core i7-10700K      ✅ Supported
GPU: NVIDIA RTX 3070           ❌ Unsupported
RAM: 32GB                      ✅ Supported
Storage: NVMe SSD              ✅ Supported
Wi-Fi: Intel AX200             ✅ Supported

Compatibility Score: 86%

Recommendation:
Compatible with OpenCore.
GPU may require replacement.
```

---

## Installation

Clone the repo:

```bash
git clone https://github.com/yourusername/check-macos-availability.git
cd check-macos-availability
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run:

```bash
python check.py
```

or:

```bash
python main.py
```

---

## Supported Checks

This tool checks:

- CPU vendor/model
- GPU model
- Motherboard/chipset
- RAM size
- Storage type
- Network adapters
- BIOS mode
- TPM/Secure Boot

---

## Supported macOS Versions

- macOS Ventura
- macOS Sonoma
- macOS Sequoia

---

## Requirements

- Python 3.10+
- Windows 10 or Windows 11
- Administrator privileges recommended

---

## Roadmap

- [ ] GUI version
- [ ] Export results to JSON
- [ ] Auto-download recommended kexts
- [ ] OpenCore config suggestions
- [ ] Linux support

---

## Disclaimer

This tool does not install macOS.

It only checks compatibility.

Hackintosh support depends on firmware, BIOS settings, and driver availability.

---

## License

MIT License

Copyright (c) 2026 adv2331

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
---

Built for the Hackintosh community 🍎
