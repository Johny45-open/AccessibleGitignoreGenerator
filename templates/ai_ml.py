TEMPLATE_AI_ML = {
    "header": "AI / Machine Learning modely",
    "rules": [
        # EasyOCR - lokalni cache modelu (default ~/.EasyOCR/model, pri model_storage_directory v projektu)
        ".EasyOCR/",
        # PyTorch modely a checkpointy
        "*.pth",
        "*.pt",
        "*.ckpt",
        # ONNX
        "*.onnx",
        # Hugging Face / obecne vahami - safetensors
        "*.safetensors",
    ],
}

# Alias pro konzistenci s jupyter.py
AI_ML_RULES = TEMPLATE_AI_ML
