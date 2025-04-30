import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import os

st.title(":green[AI Image Investigator] :mag_right:")

uploaded_files = st.file_uploader(
    "Upload Gambar",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

model = load_model('model_vgg.keras')

with open('labels.txt', 'r') as f:
    class_names = [a[:-1].split(' ')[1] for a in f.readlines()]
    f.close()

if uploaded_files is not None:
    image = Image.open(uploaded_files).convert('RGB')
    st.image(image, use_column_width = True)
