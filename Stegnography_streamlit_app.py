import streamlit as st
import os
from PIL import Image
import stego_encryption
import stego_decryption

st.title("Image Steganography App")

tab1, tab2 = st.tabs(["🔐 Encrypt", "🔓 Decrypt"])

# ----------------- Encryption Tab -----------------
with tab1:
    st.header("Encrypt a Secret Message into an Image")
    st.write("A default image is used for encryption. Preview below:")
    
    # Show preview of the default image without revealing its file name
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
            enc_id, result = stego_encryption.encrypt_message(default_image_path, message, password)
            if result is None or (isinstance(result, str) and result.startswith("Error")):
                st.error(result)
            else:
                st.success("Message encrypted successfully!")
                st.write(f"**Encryption ID:** `{enc_id}` (Keep this ID for decryption)")
                encrypted_image = Image.open(result)
                st.image(encrypted_image, caption="Encrypted Image Preview", use_container_width=True)
                with open(result, "rb") as f:
                    st.download_button("Download Encrypted Image", f, file_name=result, mime="image/png")

# ----------------- Decryption Tab -----------------
with tab2:
    st.header("Decrypt a Message from an Encrypted Image")
    st.write("Select your encrypted image. You can either use the default or upload your own.")
    
    # Let the user choose between using a default encrypted image or uploading one.
    option = st.radio("Select Image Source:", options=["Use Default Encrypted Image", "Upload Encrypted Image"])
    encrypted_image_path = None
    encryption_id = ""
    
    if option == "Upload Encrypted Image":
        uploaded_file = st.file_uploader("Upload the encrypted image (PNG)", type=["png"])
        if uploaded_file is not None:
            encrypted_image_path = "uploaded_encrypted.png"
            with open(encrypted_image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        # Let the user type the encryption ID manually
        encryption_id = st.text_input("Enter the Encryption ID associated with the image")
    else:
        st.write("Using default encrypted image.")
        # Find a file that starts with "encrypted_"
        default_encrypted = None
        for file in os.listdir():
            if file.startswith("encrypted_") and file.endswith(".png"):
                default_encrypted = file
                break
        if default_encrypted:
            encrypted_image_path = default_encrypted
            # Auto-extract the encryption ID from the file name:
            extracted_enc_id = default_encrypted[len("encrypted_"):-len(".png")]
            encryption_id = st.text_input("Encryption ID", value=extracted_enc_id, disabled=True)
            st.image(encrypted_image_path, caption="Default Encrypted Image", use_container_width=True)
        else:
            st.error("No default encrypted image found.")
    
    decryption_password = st.text_input("Enter the password for decryption", type="password", key="decrypt_password")
    
    if st.button("Decrypt Message"):
        if encrypted_image_path is None or not os.path.exists(encrypted_image_path):
            st.error("Error: Encrypted image not found. Please upload an image or check default image.")
        elif encryption_id == "":
            st.error("Please enter the Encryption ID.")
        elif decryption_password == "":
            st.error("Please enter the decryption password.")
        else:
            decrypted_message = stego_decryption.decrypt_message(encrypted_image_path, encryption_id, decryption_password)
            if decrypted_message.startswith("Error") or decrypted_message == "YOU ARE NOT AUTHORIZED":
                st.error(decrypted_message)
            else:
                st.success(f"Decrypted Message: {decrypted_message}")
streamlit run Stegnography_streamlit_app.py
