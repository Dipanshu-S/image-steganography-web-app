import streamlit as st
import os
from PIL import Image
import stego_encryption
import stego_decryption

st.title("Image Steganography App")

# Create two tabs for Encryption and Decryption
tab1, tab2 = st.tabs(["🔐 Encrypt", "🔓 Decrypt"])

# ---------- Encryption Tab ----------
with tab1:
    st.header("Encrypt a Secret Message into an Image")
    st.write("A default image is used for encryption. Preview below:")

    default_image_path = "mypic.png"
    if os.path.exists(default_image_path):
        default_image = Image.open(default_image_path)
        st.image(default_image, caption="Default Image", use_container_width=True)
    else:
        st.error("Error: Default image not found in the current folder.")

    message = st.text_area("Enter the secret message")
    password = st.text_input("Enter a password", type="password")

    if st.button("Encrypt Message"):
        if not os.path.exists(default_image_path):
            st.error("Error: Default image not found.")
        elif message == "" or password == "":
            st.error("Message and password cannot be empty.")
        else:
            result = stego_encryption.encrypt_message(default_image_path, message, password)
            if isinstance(result, str) and result.startswith("Error"):
                st.error(result)
            else:
                encryption_id, output_image_path = result
                st.success(f"Message encrypted successfully! Encryption ID: {encryption_id}")
                encrypted_image = Image.open(output_image_path)
                st.image(encrypted_image, caption="Encrypted Image Preview", use_container_width=True)
                with open(output_image_path, "rb") as f:
                    st.download_button("Download Encrypted Image", f, file_name="encryptedImage.png", mime="image/png")

# ---------- Decryption Tab ----------
with tab2:
    st.header("Decrypt a Message from an Encrypted Image")
    st.write("Select your encrypted image. You can either use the default encrypted image or upload your own stego image.")

    option = st.radio("Select Image Source:", options=["Use Default Encrypted Image", "Upload Encrypted Image"])

    encrypted_image_path = None
    if option == "Upload Encrypted Image":
        uploaded_file = st.file_uploader("Upload the encrypted image (PNG)", type=["png"])
        if uploaded_file is not None:
            encrypted_image_path = "uploaded_encrypted.png"
            with open(encrypted_image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
    else:
        encrypted_image_path = "encryptedImage.png"

    decryption_password = st.text_input("Enter the password for decryption", type="password", key="decrypt_password")

    if st.button("Decrypt Message"):
        if encrypted_image_path is None or not os.path.exists(encrypted_image_path):
            st.error("Error: Encrypted image not found. Please upload an image or run the encryption process first.")
        elif decryption_password == "":
            st.error("Please enter the decryption password.")
        else:
            decrypted_message = stego_decryption.decrypt_message(encrypted_image_path, decryption_password)
            if decrypted_message.startswith("Error") or decrypted_message == "YOU ARE NOT AUTHORIZED":
                st.error(decrypted_message)
            else:
                st.success(f"Decrypted Message: {decrypted_message}")
