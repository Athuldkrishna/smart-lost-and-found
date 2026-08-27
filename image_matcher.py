import torch
from torchvision import models, transforms
from PIL import Image
import torch.nn.functional as F


# Load a pretrained ResNet50 model
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

# Remove the final classification layer
model = torch.nn.Sequential(*list(model.children())[:-1])

model.eval()


# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def get_image_embedding(image_path):
    """Convert an image into a feature vector."""

    image = Image.open(image_path).convert("RGB")

    image_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        embedding = model(image_tensor)

    embedding = embedding.squeeze()

    return embedding


def compare_images(image1_path, image2_path):
    """Compare two images and return a similarity score."""

    embedding1 = get_image_embedding(image1_path)
    embedding2 = get_image_embedding(image2_path)

    similarity = F.cosine_similarity(
        embedding1.unsqueeze(0),
        embedding2.unsqueeze(0)
    )

    score = similarity.item()

    # Convert from -1 to 1 into approximately 0 to 100
    percentage = ((score + 1) / 2) * 100

    return round(percentage, 2)