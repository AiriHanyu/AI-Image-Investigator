import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os

# Caching biar model gak diload berulang-ulang
@st.cache_resource
def load_vgg_model():
    return load_model("model_vgg.keras")  # Pastikan path ini sesuai posisi file di repo

model = load_vgg_model()

st.title(":green[AI Image Investigator] :mag_right:")

uploaded_files = st.file_uploader(
    "Upload Gambar",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def predict_image(img_pil):
    img_resized = img_pil.resize((128, 128))
    img_array = img_to_array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    return np.argmax(prediction)

if uploaded_files:
    images_to_check = []
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")  # Convert biar aman
        st.image(image, caption=uploaded_file.name, use_container_width=True)
        images_to_check.append((uploaded_file.name, image))

    st.success(f"{len(uploaded_files)} gambar berhasil diunggah!")

    if st.button("Investigasi"):
        st.subheader("Hasil Investigasi")
        for name, img in images_to_check:
            label_idx = predict_image(img)
            pred_label = ["REAL", "FAKE"][label_idx]
            color = (0, 255, 0) if pred_label == "REAL" else (255, 0, 0)

            img_with_text = img.copy()
            draw = ImageDraw.Draw(img_with_text)

            font_size = int(img_with_text.width * 0.1)
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font = ImageFont.truetype(font_path, font_size)

            text = pred_label
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2], text_bbox[3]
            pos = ((img.width - text_width) // 2, (img.height - text_height) // 2)

            text_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text(pos, text, fill=color, font=font)

            text_img_rotated = text_img.rotate(45, resample=Image.BICUBIC, expand=True)
            rotated_pos = ((img.width - text_img_rotated.width) // 2,
                           (img.height - text_img_rotated.height) // 2)

            img_with_text.paste(text_img_rotated, rotated_pos, mask=text_img_rotated)
            st.image(img_with_text, caption=f"{name} - {pred_label}", use_container_width=True)
