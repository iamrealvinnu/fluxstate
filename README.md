# FluxState: Edge Intelligence SDK

FluxState is an enterprise-grade, **Zero-Trace Edge Video Analytics SDK**. It operates as a camera-agnostic intelligence overlay (Intelligent Video Recorder model), designed to ingest RTSP streams from legacy IP cameras and apply advanced, multi-modal behavioral reasoning.

Unlike legacy systems that rely on facial recognition or hardcoded rules, FluxState utilizes a **Behavioral Threat Matrix**—fusing kinetic movement, acoustic escalation, and RF network device tracking into a singular Reality Graph. 

## 🚀 Core Enterprise Features

- **Zero-Trace Privacy Engine:** Compliant with strict GDPR and Defense data-retention policies. Pixel buffers are processed entirely in ephemeral RAM and cryptographically overwritten (zeroed out) instantly post-inference, preventing memory-dump attacks.
- **RTSP IP Camera Integration:** Connects seamlessly to existing infrastructure. No proprietary hardware required.
- **Webhooks Integration Bus:** Operates purely headlessly. Emits near-instant JSON telemetry payloads to centralized Video Management Systems (VMS) or command center dashboards via POST webhooks only when threats are detected.
- **Over-The-Air (OTA) Policy Engine:** Threat definitions and thresholds are defined in `intelligence_policy.json`, allowing central command to push dynamic parameter updates to fleet edge nodes without restarting the stream.
- **Multi-Modal Swarm Tracking (GPASS):** Tracks anonymous geometric identities across frames. Uses YOLOv8 (Vision), Mediapipe (Skeletal Kinetics), PyAudio (Acoustic Impact), and ARP Scanning (RF Device Payloads) to generate a unified threat vector.

## 📦 Installation & Setup

1. **System Dependencies:** Ensure Tesseract OCR and network tools are installed.
   ```bash
   brew install tesseract
   ```
2. **Install the SDK:**
   You can build and install this SDK directly via pip:
   ```bash
   pip install -e .
   ```

## 🛠️ Seamless Developer Integration

FluxState is designed as a **Headless B2B SDK**. It is the intelligence layer ("The Brain") that you embed into your own proprietary backend or UI.

Create a Python script (e.g., `example_integration.py`):

```python
import time
from app import FluxStateNode

# 1. Initialize the SDK (Zero-Trace Mode Enabled by Default)
sdk = FluxStateNode()

# 2. Define your seamless integration hooks
def handle_threat(event_payload):
    print(f"\n[🚨 INTEGRATION BUS] Threat Detected! Escalating to VMS...")
    print(f"Target: {event_payload['entities']}")
    print(f"Vector: {event_payload['context_log']}")

# 3. Bind hooks to the SDK
sdk.on_threat_detected = handle_threat

# 4. Deploy Headlessly (Runs entirely in background RAM, no UI)
sdk.start_headless_daemon()

try:
    while True: time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down SDK...")
```

## 🔐 Publishing to PyPI (Trusted Publisher)

This repository is configured for highly secure **OIDC Trusted Publishing** to PyPI via GitHub Actions. There is no need for manual API tokens or `twine`.

1. Go to the [PyPI Pending Publishers](https://pypi.org/manage/account/publishing/) page.
2. Enter the following exact details to link your repository:
   - **PyPI Project Name**: `fluxstate-edge`
   - **Owner**: `IAMVINAY` (or your GitHub username)
   - **Repository name**: `fluxstate`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
3. Click "Add".
4. On GitHub, create a new **Release**. The included `.github/workflows/publish.yml` will automatically build the SDK wheel and securely publish it to PyPI!
