import torch
import torchvision.transforms as T
from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt

# Load DeepLabV3 model
model = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()

# Input and output paths
input_path = "Water Bodies Dataset/Images/water_body_8774.jpg"
output_path = "segmented_mask.png"

# Load and preprocess image
image = Image.open(input_path).convert("RGB")
transform = T.Compose([
    T.Resize(520),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
])
input_tensor = transform(image).unsqueeze(0)

# Predict
with torch.no_grad():
    output = model(input_tensor)['out'][0]
seg_mask = output.argmax(0).byte().cpu()

# Save mask image
mask_img = Image.fromarray(seg_mask.numpy())
mask_img.save(output_path)
print(f"Saved segmented mask to {output_path}")
