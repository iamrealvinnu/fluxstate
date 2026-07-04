"""
Agentic VLM Reasoner (Vision-Language Model Orchestrator)
This module acts as the bridge between the lower-level FluxState tracking/detection
and higher-level semantic reasoning.

It intercepts complex temporal events and passes them to a Vision-Language Model
(e.g., Qwen2.5-VL, LLaVA, or a cloud API) for deep contextual understanding.
"""
import requests
import json
import base64
import cv2

class SemanticAgent:
    def __init__(self, endpoint=None):
        # By default, prepare for local edge VLM integration
        self.vlm_endpoint = endpoint or "http://localhost:11434/api/generate"
        self.enabled = False # Set to True when VLM is attached
        
    def investigate_scene(self, context_log, frame, prompt="What is suspicious about this behavior?"):
        """
        Takes a flagged event and a raw frame, and asks an AI to reason about it.
        This provides true 'Scene Understanding' beyond simple bounding boxes.
        """
        if not self.enabled or frame is None:
            return "[VLM Offline] Fallback to standard rule-engine."
            
        try:
            # Encode frame for VLM
            _, buffer = cv2.imencode('.jpg', frame)
            base64_image = base64.b64encode(buffer).decode('utf-8')
            
            payload = {
                "model": "qwen2.5-vl", 
                "prompt": f"Context Log: {context_log}. Query: {prompt}",
                "images": [base64_image],
                "stream": False
            }
            
            # Example API call to local Ollama or Edge VLM
            response = requests.post(self.vlm_endpoint, json=payload, timeout=5.0)
            if response.status_code == 200:
                return response.json().get("response", "No response generated.")
            return "[VLM Error] Non-200 status code."
        except Exception as e:
            return f"[VLM Error] {str(e)}"
            
    def query_temporal_memory(self, sql_results, natural_language_query):
        """
        Allows an operator to ask: 'What happened between 2 PM and 3 PM?'
        Takes the SQLite output and uses an LLM to generate a human-readable summary.
        """
        if not self.enabled:
            return "[VLM Offline] Temporal summary requires an active reasoning agent."
            
        try:
            # Format the raw SQL forensics into a context block
            context_block = "\n".join([f"[{row[0]}] {row[1]}" for row in sql_results])
            
            prompt = (
                f"You are a Forensic AI. Based on the following surveillance logs, answer the operator's query.\n"
                f"Operator Query: {natural_language_query}\n\n"
                f"Logs:\n{context_block}"
            )
            
            payload = {
                "model": "qwen2.5-vl", 
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.vlm_endpoint, json=payload, timeout=10.0)
            if response.status_code == 200:
                return response.json().get("response", "No summary generated.")
            return "[Agent Error] Non-200 status code."
        except Exception as e:
            return f"[Agent Error] {str(e)}"
