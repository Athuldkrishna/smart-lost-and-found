from functools import lru_cache
from io import BytesIO

import requests
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

print("Loading CLIP model...")

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP model loaded successfully!")


def load_image(source):
    """Open an image from a local path or an http(s) URL (e.g. Supabase Storage)."""
    if source.startswith(("http://", "https://")):
        response = requests.get(source, timeout=15)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert("RGB")

    return Image.open(source).convert("RGB")


@lru_cache(maxsize=512)
def get_embedding(image_source):
    # Cached per path/URL so each image is downloaded and embedded only once.
    image = load_image(image_source)

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = model.get_image_features(**inputs)

    # Newer transformers return an output object, older ones a tensor.
    features = output.pooler_output if hasattr(output, "pooler_output") else output

    # Normalize
    features = features / features.norm(dim=-1, keepdim=True)

    return features


def compare_images(image1_source, image2_source):
    try:
        embedding1 = get_embedding(image1_source)
        embedding2 = get_embedding(image2_source)
    except Exception as error:
        print(f"Image comparison skipped: {error}")
        return 0

    similarity = torch.matmul(
        embedding1,
        embedding2.T
    ).item()

    percentage = max(0, min(100, similarity * 100))

    return round(percentage, 2)
