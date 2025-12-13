# model_config.py

MODEL_CONFIGS = {
    "gemma3:4b": {
        "context_window": 8192,
        "recommended_output": 700,
    },
    "llama3.1:8b": {
        "context_window": 8192,
        "recommended_output": 800,
    },
    "mixtral:8x7b": {
        "context_window": 32768,
        "recommended_output": 1200,
    },
}
