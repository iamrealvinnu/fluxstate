# config.py
import os

class AppConfig:
    # Product Metadata
    PROJECT_NAME = "FluxState"
    VERSION = "1.0.0-MVP"
    
    # Edge Model Settings
    # Target model optimized for local unified memory
    VISION_MODEL_PATH = "gdinexus/Nexus-Lumina-3B-v3" 
    
    # State Transition Anchoring (STA) Hyperparameters
    ENTROPY_THRESHOLD = 0.15      # Minimum frame delta to trigger deep reasoning
    SPATIAL_TRANSITION_COOLDOWN = 1.5  # Seconds to lock state before allowing next delta
    
    # Hardware/Inference Controls
    MAX_CONTEXT_TOKENS = 2048
    USE_MLX_ASH_KV = True         # Toggle proprietary stable caching
