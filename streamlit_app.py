import streamlit as st
from keras.models import load_model 
from PIL import Image
from util import classify


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


def classify(image, model, class_names):
    return 'dummy_class_name', 0
