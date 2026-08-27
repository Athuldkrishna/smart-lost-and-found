from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

print("Loading CLIP model...")

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

print("CLIP model loaded successfully!")


def get_embedding(image_path):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = model.get_image_features(**inputs)

    features = output.pooler_output

    # Normalize
    features = features / features.norm(dim=-1, keepdim=True)

    return features


def compare_images(image1_path, image2_path):
    embedding1 = get_embedding(image1_path)
    embedding2 = get_embedding(image2_path)

    similarity = torch.matmul(
        embedding1,
        embedding2.T
    ).item()

    percentage = max(0, min(100, similarity * 100))

    return round(percentage, 2)