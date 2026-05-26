from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

from PIL import Image

# Load BLIP model
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


def generate_caption(image_path):

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Preprocess image
    inputs = processor(
        image,
        return_tensors="pt"
    )

    # Generate caption
    output = model.generate(**inputs)

    # Decode result
    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption