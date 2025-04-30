    if st.button("Investigasi"):
        st.subheader("Hasil Investigasi")
        for name, img in images_to_check:
            label_idx = predict_image(img)
            pred_label = class_names[label_idx]  # pakai dari label.txt

            color = (0, 255, 0) if pred_label.upper() == "REAL" else (255, 0, 0)

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
