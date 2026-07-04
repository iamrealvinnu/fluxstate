import time
from app import FluxStateNode

# 1. Initialize the SDK (Zero-Trace Mode Enabled by Default)
sdk = FluxStateNode()

# 2. Define your seamless integration hooks
def handle_threat(event_payload):
    print(f"\n[🚨 INTEGRATION BUS] Threat Detected! Escalating to VMS...")
    print(f"Target: {event_payload['entities']}")
    print(f"Vector: {event_payload['context_log']}")

def handle_telemetry(data):
    # This fires 30 times a second silently
    pass

# 3. Bind hooks to the SDK
sdk.on_threat_detected = handle_threat
sdk.on_telemetry_update = handle_telemetry

# 4. Deploy Headlessly (Runs entirely in background RAM, no UI)
print("Deploying FluxState SDK Headlessly...")
sdk.start_headless_daemon()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down SDK...")
    sdk.stop()
