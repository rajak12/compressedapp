import streamlit as st
from PIL import Image
import io

def compress_to_target_size(img, target_kb=15):
    target_bytes = target_kb * 1024
    quality = 85
    width, height = img.size

    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.LANCZOS

    img = img.convert("RGB")  # Ensure RGB

    while True:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality)
        size = buffer.tell()

        if size <= target_bytes:
            return buffer, round(size / 1024, 2)

        if quality > 20:
            quality -= 5
        else:
            width = int(width * 0.9)
            height = int(height * 0.9)
            img = img.resize((width, height), resample)

        if width < 100 or height < 100:
            return None, round(size / 1024, 2)

# === Streamlit UI ===

st.set_page_config(page_title="Image Compressor (≤15 KB)", layout="centered")
st.title("📷 Image Compressor Web Tool")
st.markdown("Upload an image and download a version compressed to **15 KB or less**.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="Original Image", use_column_width=True)

    if st.button("🔽 Compress to ≤15 KB"):
        compressed_buffer, final_size = compress_to_target_size(input_image)

        if compressed_buffer:
            st.success(f"✅ Compression successful! Final size: {final_size} KB")
            st.download_button(
                label="📥 Download Compressed Image",
                data=compressed_buffer,
                file_name="compressed.jpg",
                mime="image/jpeg"
            )
        else:
            st.error(f"❌ Couldn't compress image below 15 KB. Closest size: {final_size} KB")
