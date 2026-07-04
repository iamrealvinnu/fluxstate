# FluxState: Edge Intelligence SDK

[![PyPI version](https://badge.fury.io/py/fluxstate-edge.svg)](https://badge.fury.io/py/fluxstate-edge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FluxState Edge** is an extensible, camera-agnostic video analytics SDK designed for integration into enterprise security backends. It processes RTSP streams locally on the edge, extracting behavioral metadata using a combination of object detection, 3D skeletal posing, and audio processing.

The system is designed to minimize storage overhead by saving structured metadata (JSON telemetry and SQLite logs) rather than raw video footage, making it useful for privacy-conscious environments.

---

## 🚀 Core Capabilities

- **Temporal Forensic Database:** Events and behavioral anomalies are logged directly into a local SQLite database (`core/forensics.py`). This allows operators to run SQL or text searches to locate past incidents (e.g., finding instances of specific anomalies or entity interactions) without needing to scrub through hours of video.
- **Hardware Agnostic (RTSP):** Connects to existing IP cameras via standard RTSP URLs without requiring proprietary recording hardware.
- **C-Level Memory Mitigation:** Python's garbage collector can leave image data in memory longer than desired. FluxState uses `ctypes.memset` to manually zero out numpy array pixel buffers at the C-level immediately after inference. While OS and GPU drivers may still cache buffers, this mitigates raw image lingering in the Python heap.
- **Over-The-Air (OTA) Policies:** Behavioral thresholds and integration webhooks can be updated dynamically via the `intelligence_policy.json` file. The SDK hot-reloads these parameters without restarting the stream.
- **Headless Telemetry Hooks:** Designed to run purely in the background. It emits Python callback events or HTTP POST webhooks when behavioral thresholds are crossed, acting as a data-feed for your own Video Management System (VMS).

---

## 📦 Installation & System Requirements

**System Dependencies:**
FluxState relies on native system libraries for optical character recognition and audio streaming.
*   **macOS:** `brew install tesseract portaudio`
*   **Linux (Ubuntu/Debian):** `sudo apt-get install tesseract-ocr libportaudio2 libportaudiocpp0 portaudio19-dev`

**Install the SDK:**
```bash
pip install fluxstate-edge
```

---

## 🛠️ SDK Integration

FluxState is designed to be embedded into your proprietary backend.

### Minimal 5-Line Integration
Create an entrypoint script (e.g., `main.py`):

```python
import time
from app import FluxStateNode

# Initialize the SDK
sdk = FluxStateNode()

# Define your integration hook
def handle_threat(event_payload):
    print(f"\n[INTEGRATION BUS] Threat Detected! Escalating to VMS...")
    print(f"Target Identity: {event_payload['entities']}")
    print(f"Behavioral Vector: {event_payload['context_log']}")

# Bind the hook to the SDK
sdk.on_threat_detected = handle_threat

# Deploy Headlessly (Runs as a background daemon)
sdk.start_headless_daemon()

try:
    while True: 
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down SDK cleanly...")
    sdk.stop()
```

### Forensic Searching
You can query the SQLite database to retrieve past events:
```python
from core.forensics import ForensicDatabase

db = ForensicDatabase()
results = db.query_forensics("ANOMALY")
for timestamp, context in results:
    print(f"[{timestamp}] {context}")
```

---

## ⚙️ Configuration: The Intelligence Policy

FluxState uses a dynamic JSON file (`intelligence_policy.json`) located in the runtime directory to configure behavioral thresholds. 

```json
{
  "SECTOR_ID": "ENTERPRISE-HQ-01",
  "RTSP_STREAM_URL": "0",
  "INTEGRATION_WEBHOOK_URL": "https://api.your-vms.com/v1/telemetry",
  "THREAT_VECTORS": {
    "ARMS_RAISED_OR_REACHING": {
      "enabled": true,
      "escalation_threshold": 0.85
    }
  }
}
```

---

## 🛡️ Architecture Overview

Please refer to the `architecture.md` file in the source repository for a deeper dive into the threading model, the telemetry pipeline, and the SQLite database schema.
