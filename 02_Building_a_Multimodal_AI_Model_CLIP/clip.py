# Lab Project: Building a Multimodal AI Model (CLIP)
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import torch.nn.functional as F
import os

def create_dummy_image():
    if not os.path.exists("dummy_image.png"):
        img = Image.new('RGB', (224, 224), color='red')
        img.save('dummy_image.png')

# Load model and processor
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

# 1. Load and preprocess image
create_dummy_image()
image = Image.open("dummy_image.png")

# Candidate captions
captions = [
    "a photo of a red square",
    "a photo of a blue circle",
    "a cat sitting on a couch",
    "a bright red colored image",
    "a green forest landscape",
]

# Process image + all captions together
inputs = processor(text=captions, images=image, return_tensors="pt", padding=True)

# 2 & 3. Extract image and text embeddings via single forward pass
with torch.no_grad():
    outputs = model(**inputs)

image_embedding = outputs.image_embeds   # (1, 512)
text_embeddings = outputs.text_embeds    # (N, 512)

# 4. Compute cosine similarity: normalize then dot product
image_embedding = F.normalize(image_embedding, dim=-1)
text_embeddings = F.normalize(text_embeddings, dim=-1)
similarities = (image_embedding @ text_embeddings.T).squeeze(0)  # (N,)

# 5. Sort and display top matches
ranked = similarities.argsort(descending=True)

print("Image: dummy_image.png (a solid red square)")
print("\nCandidate Captions & Cosine Similarities:")
for rank, idx in enumerate(ranked):
    print(f"  {rank+1}. [{similarities[idx]:.4f}] {captions[idx]}")

print(f"\nTop match: '{captions[ranked[0]]}'")
