# Hardware Compatibility Database for Hackintosh
# Based on Dortania OpenCore guides and community knowledge

SUPPORTED_CPU_FAMILIES = {
    "intel": {
        "supported": [
            "i3-4","i5-4","i7-4","i3-5","i5-5","i7-5",
            "i3-6","i5-6","i7-6","i3-7","i5-7","i7-7",
            "i3-8","i5-8","i7-8","i9-8","i3-9","i5-9","i7-9","i9-9",
            "i3-10","i5-10","i7-10","i9-10",
            "i5-11","i7-11","i9-11",
            "i3-12","i5-12","i7-12","i9-12",
            "i3-13","i5-13","i7-13","i9-13",
            "xeon e3","xeon e5","xeon w",
        ],
        "unsupported": [
            "atom","celeron","pentium",
            "i3-14","i5-14","i7-14","i9-14",
            "ultra 5","ultra 7","ultra 9",
        ],
        "notes": {
            "i3-12":"Requires E-core disabling via ACPI patches.",
            "i5-12":"Requires E-core disabling via ACPI patches.",
            "i7-12":"Requires E-core disabling via ACPI patches.",
            "i9-12":"Requires E-core disabling via ACPI patches.",
            "i3-13":"Requires E-core disabling via ACPI patches.",
            "i5-13":"Requires E-core disabling via ACPI patches.",
            "i7-13":"Requires E-core disabling via ACPI patches.",
            "i9-13":"Requires E-core disabling via ACPI patches.",
        },
    },
    "amd": {
        "supported": [
            "ryzen 3 1","ryzen 5 1","ryzen 7 1",
            "ryzen 3 2","ryzen 5 2","ryzen 7 2",
            "ryzen 3 3","ryzen 5 3","ryzen 7 3","ryzen 9 3",
            "ryzen 5 5","ryzen 7 5","ryzen 9 5",
            "ryzen 5 7","ryzen 7 7","ryzen 9 7",
            "threadripper",
        ],
        "unsupported": [
            "fx-","athlon","a4-","a6-","a8-","a10-","a12-",
            "ryzen 3 4","ryzen 5 4","ryzen 7 4",
        ],
        "notes": {
            "amd_general":"AMD requires a patched XNU kernel. DRM and virtualisation apps may misbehave.",
            "ryzen 5 7":"Ryzen 7000 is highly experimental; BIOS downgrades may be needed.",
            "ryzen 7 7":"Ryzen 7000 is highly experimental; BIOS downgrades may be needed.",
            "ryzen 9 7":"Ryzen 7000 is highly experimental; BIOS downgrades may be needed.",
        },
    },
}

SUPPORTED_GPUS = {
    "nvidia": {
        "supported": [
            "gtx 650","gtx 660","gtx 670","gtx 680","gtx 690",
            "gtx 760","gtx 770","gtx 780","gtx titan",
            "gtx 750","gtx 950","gtx 960","gtx 970","gtx 980","gtx 980 ti",
        ],
        "unsupported": [
            "gtx 1050","gtx 1060","gtx 1070","gtx 1080","gtx 1650","gtx 1660",
            "rtx 2060","rtx 2070","rtx 2080",
            "rtx 3060","rtx 3070","rtx 3080","rtx 3090",
            "rtx 4060","rtx 4070","rtx 4080","rtx 4090",
            "rtx 5060","rtx 5070","rtx 5080","rtx 5090",
        ],
        "notes": {
            "gtx 750":"Maxwell GPUs require web drivers and cap at macOS High Sierra 10.13.",
            "gtx 950":"Maxwell GPUs require web drivers and cap at macOS High Sierra 10.13.",
            "gtx 960":"Maxwell GPUs require web drivers and cap at macOS High Sierra 10.13.",
            "gtx 970":"Maxwell GPUs require web drivers and cap at macOS High Sierra 10.13.",
            "gtx 980":"Maxwell GPUs require web drivers and cap at macOS High Sierra 10.13.",
            "gtx 650":"Kepler — native support but dropped from macOS 12 (Monterey)+.",
            "gtx 660":"Kepler — native support but dropped from macOS 12 (Monterey)+.",
        },
    },
    "amd": {
        "supported": [
            "rx 460","rx 470","rx 480",
            "rx 560","rx 570","rx 580","rx 590",
            "vega 56","vega 64","radeon vii",
            "rx 5500","rx 5600","rx 5700",
            "rx 6600","rx 6700","rx 6800","rx 6900",
            "rx 7600","rx 7700","rx 7800","rx 7900",
            "r9 270","r9 280","r9 290","r9 380","r9 390","r9 fury",
        ],
        "unsupported": [
            "rx 6400","rx 6500",
            "radeon hd 5","radeon hd 6","radeon hd 7",
        ],
        "notes": {
            "rx 6400":"No hardware video encode/decode; PCIe x4 bandwidth issues.",
            "rx 7600":"RDNA 3 support is maturing; some features may be missing.",
            "rx 7700":"RDNA 3 support is maturing; some features may be missing.",
            "rx 7800":"RDNA 3 support is maturing; some features may be missing.",
            "rx 7900":"RDNA 3 support is maturing; some features may be missing.",
        },
    },
    "intel": {
        "supported": [
            "uhd 620","uhd 630","uhd 750","uhd graphics",
            "iris plus","iris xe",
            "hd 4000","hd 4600","hd 5000","hd 5500","hd 6000",
        ],
        "unsupported": [
            "arc a380","arc a580","arc a750","arc a770","intel arc",
        ],
        "notes": {
            "iris xe":"Iris Xe (12th gen+) has limited and experimental support.",
            "intel arc":"Intel Arc GPUs are currently unsupported in Hackintosh.",
        },
    },
}

SUPPORTED_WIFI = {
    "supported": [
        "bcm94360","bcm943602","bcm94352","bcm94350","bcm94331",
        "dw1820a","dw1560","dw1830",
        "ax200","ax201","ax210","ax211",
        "ac 9560","ac 9462","ac 8265","ac 8260",
        "ac 7265","ac 3160","ac 3165",
        "wi-fi 6e","wi-fi 6",
    ],
    "unsupported": [
        "rtl8","realtek 8","qca61","qca956","mt7921","mt7922",
    ],
    "notes": {
        "intel":"Intel Wi-Fi works via itlwm kext but AirDrop/Handoff may be limited.",
        "broadcom":"Broadcom cards offer full AirDrop, Handoff, and Sidecar support.",
        "realtek":"Realtek Wi-Fi adapters have no macOS driver support.",
    },
}

MACOS_VERSIONS = {
    "ventura":  {"name":"macOS Ventura",  "version":"13"},
    "sonoma":   {"name":"macOS Sonoma",   "version":"14"},
    "sequoia":  {"name":"macOS Sequoia",  "version":"15"},
}

MIN_RAM_GB             = 8
RECOMMENDED_RAM_GB     = 16
MIN_STORAGE_GB         = 60
RECOMMENDED_STORAGE_GB = 120
