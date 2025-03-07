import cv2
import hashlib

def xor_decrypt(encrypted_message, key):
    return ''.join(chr(ord(ch) ^ ord(key[i % len(key)])) for i, ch in enumerate(encrypted_message))

def decrypt_message(image_path, enc_id, password):
    # Load the encrypted image
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Encrypted image not found."
    
    # Open the corresponding metadata file using the provided encryption ID
    metadata_filename = f"metadata_{enc_id}.txt"
    try:
        with open(metadata_filename, "r") as f:
            lines = f.readlines()
            stored_hashed_password = lines[0].strip()
            message_length = int(lines[1].strip())
    except Exception:
        return f"Error: Metadata for encryption ID {enc_id} not found."
    
    # Verify the provided password
    input_hashed = hashlib.sha256(password.encode()).hexdigest()
    if input_hashed != stored_hashed_password:
        return "YOU ARE NOT AUTHORIZED"
    
    # Flatten the image and extract the encrypted message from the first message_length pixels
    flat_img = img.flatten()
    if message_length > len(flat_img):
        return "Error: Message length exceeds image data."
    
    encrypted_chars = [chr(flat_img[i]) for i in range(message_length)]
    encrypted_message = ''.join(encrypted_chars)
    
    # Decrypt the message using XOR decryption
    decrypted_message = xor_decrypt(encrypted_message, password)
    return decrypted_message
