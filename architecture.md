# FluxState SDK Architecture Overview

FluxState operates as a **Camera-Agnostic Intelligent Video Recorder (IVR)**. It discards the legacy "dumb camera" paradigm in favor of a layered, multi-modal semantic reasoning architecture designed specifically for headless B2B enterprise deployments.

## 1. Zero-Latency Ingestion Layer (RTSP & Local)
*(Handled by `EdgeVideoStream` in `utils/video_stream.py`)*

To prevent the AI inference loop from causing video buffer lag, camera ingestion is decoupled into a **Daemon Background Thread**. 
- The thread continuously pulls frames from RTSP streams (IP cameras) or local USB hardware.
- The inference loop requests `frame.copy()`, guaranteeing a 0ms latency differential between reality and inference.

## 2. Multi-Modal Semantic Extraction
When kinetic energy (motion) is detected, the SDK fires a four-pronged extraction pipeline:

- **A. YOLOv8 ByteTrack (Object Semantics)**: `ultralytics` YOLOv8n classifies 80+ objects and assigns a persistent ByteTrack ID to track the object across temporal frames.
- **B. Mediapipe Tasks API (Kinetic Intent)**: The `PoseLandmarker` extracts 33 3D skeletal joints. Simple limb-geometry heuristics map physical positions into semantic actions (`"ARMS_RAISED"`, `"WALKING"`).
- **C. PyAudio (Acoustic Impact)**: A background audio daemon calculates RMS volume, classifying anomalies like `KINETIC_IMPACT_OR_SHATTERING` or `VOCAL_ESCALATION`.
- **D. ARP Scanner (RF Intel)**: Subprocesses ping local subnet routing tables to enumerate active network-emitting payloads carried by physical entities.

## 3. The Behavioral Threat Matrix (Reasoning Engine)
*(Handled by `FluxInferenceEngine` in `core/engine.py`)*

Instead of a binary state machine, telemetry is fed to the `FluxInferenceEngine` and cross-referenced with the OTA (Over-The-Air) `intelligence_policy.json`.
- It fuses the modes (e.g., if kinetic action == `"ARMS_RAISED"` AND acoustic == `"VOCAL_ESCALATION"`).
- It generates a natural-language contextual summary and flags threats.
- It promotes entities to the `SWARM LEDGER` using anonymous GPASS cryptographic hashes, tracking behavior without relying on facial recognition.

## 4. Zero-Trace Privacy Engine
*(Handled in `poll_telemetry` loop)*

Data privacy is the cornerstone of the SDK. FluxState is built to operate under strict GDPR and Defense requirements:
- **No Data Retention**: The system does not save images or video files to disk.
- **Cryptographic Memory Wiping**: Immediately after the inference loop extracts the semantic metadata (bounding boxes, GPASS IDs), the SDK executes a `frame.fill(0)` command. This explicitly zeros out the raw pixel array in RAM *before* the Python garbage collector runs, ensuring that malicious actors cannot extract video data via RAM heap dumps.

## 5. Headless Integration Bus (Webhooks)
*(Handled by `_push_to_integration_bus` in `app.py`)*

FluxState is designed as the "Intel Inside" for enterprise firms. It runs completely silently as a background daemon.
- When the Threat Matrix flags an anomaly, the SDK instantly fires an HTTP `POST` request to the client's proprietary Video Management System (VMS) webhook.
- The payload contains the full JSON Reality Graph telemetry, allowing the client to render alerts in their own custom UIs.
