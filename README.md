# FluxState: Zero-Trace Edge Intelligence SDK

[![PyPI version](https://badge.fury.io/py/fluxstate-edge.svg)](https://badge.fury.io/py/fluxstate-edge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**FluxState Edge** is an enterprise-grade, camera-agnostic video analytics SDK designed for high-security environments. It operates as a headless Intelligence layer, ingesting RTSP streams from existing IP cameras and applying advanced, multi-modal behavioral reasoning.

Unlike legacy security systems that rely on hardcoded tripwires or controversial facial recognition, FluxState utilizes a **Behavioral Threat Matrix**. It fuses geometric Vision (YOLOv8), 3D Skeletal Kinetics (MediaPipe), Acoustic Escalation (PyAudio), and RF Payload signatures to generate a dynamic, anonymous Reality Graph.

---

## 🚀 Core Enterprise Capabilities

- **Zero-Trace Privacy Engine:** Engineered for strict GDPR and Defense data-retention compliance. Raw pixel buffers are processed entirely in ephemeral RAM and cryptographically overwritten (zeroed out) instantly post-inference, neutralizing memory-dump attacks.
- **Hardware Agnostic (RTSP):** Connects to any existing IP camera via standard RTSP URLs. No proprietary hardware required.
- **Swarm Ledger (GPASS):** Introduces **G**eometric **P**erceptual **A**nonymous **S**ignature **S**warm tracking. Associates behaviors to cryptographic hashes based on upper-body geometry instead of faces.
- **Over-The-Air (OTA) Policies:** Threat definitions, behavioral thresholds, and VMS Webhook destinations are loaded dynamically from `intelligence_policy.json`, allowing central command to update remote edge nodes without restarting the stream.
- **Webhooks Integration Bus:** Operates completely headlessly. Emits near-instant JSON telemetry payloads to centralized Video Management Systems (VMS) only when behavioral threats are confirmed.

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

## 🛠️ Seamless Developer Integration (The SDK)

FluxState is designed as the "Intel Inside" for your security infrastructure. It is meant to be embedded directly into your proprietary backend.

### 1. Minimal 5-Line Integration
Create an entrypoint script (e.g., `main.py`):

```python
import time
from app import FluxStateNode

# Initialize the SDK (Zero-Trace Mode Enabled by Default)
sdk = FluxStateNode()

# Define your seamless integration hooks
def handle_threat(event_payload):
    print(f"\n[🚨 INTEGRATION BUS] Threat Detected! Escalating to VMS...")
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

### 2. Available Event Hooks
The `FluxStateNode` exposes the following native Python hooks for your backend:
*   `on_threat_detected(payload: dict)`: Fires immediately when the behavioral reasoning engine crosses the threshold defined in the active Intelligence Policy.
*   `on_telemetry_update(payload: dict)`: A silent telemetry hook that fires 30 times a second. Useful for bridging the raw geometric track data into local caching databases (Redis/Kafka) without triggering alarms.

---

## ⚙️ Configuration: The Intelligence Policy

FluxState uses a dynamic JSON file (`intelligence_policy.json`) located in the runtime directory to configure behavioral thresholds. This file is hot-reloaded by the AI engine, allowing you to tweak camera sensitivity OTA.

```json
{
  "SECTOR_ID": "ENTERPRISE-HQ-01",
  "RTSP_STREAM_URL": "0",
  "INTEGRATION_WEBHOOK_URL": "https://api.your-vms.com/v1/telemetry",
  "THREAT_VECTORS": {
    "ARMS_RAISED_OR_REACHING": {
      "enabled": true,
      "escalation_threshold": 0.85
    },
    "RAPID_KINETIC_SHIFT": {
      "enabled": true,
      "escalation_threshold": 0.90
    }
  }
}
```

---

## 🛡️ Architecture Overview

For a deep dive into the threading model, asynchronous OCR extraction, and the mathematical implementation of the Zero-Trace Privacy Engine, please refer to the `architecture.md` file in the source repository.

*FluxState is developed as an intelligence overlay for modern video management infrastructure.*
