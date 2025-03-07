import cv2
import hashlib
import os

def xor_decrypt(encrypted_message, key):
    return ''.join(chr(ord(ch) ^ ord(key[i % len(key)])) for i, ch in enumerate(encrypted_message))

def decrypt_message(image_path, password):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Encrypted image not found."
    
    # Flatten the image to extract the embedded data
    flat_img = img.flatten()
    
    # The header is 28 characters long
    if len(flat_img) < 28:
        return "Error: Image does not contain a valid header."
    
    header_chars = [chr(flat_img[i]) for i in range(28)]
    header = ''.join(header_chars)
    
    if not header.startswith("STEG"):
        return "Error: Not a valid stego image."
    
    # Parse the header:
    # - Encryption ID: characters 4 to 12
    # - Message length: characters 12 to 20
    # - Verification token: characters 20 to 28
    encryption_id = header[4:12]
    msg_length_str = header[12:20]
    token_in_image = header[20:28]
    
    try:
        msg_length = int(msg_length_str)
    except ValueError:
        return "Error: Invalid message length in header."
    
    # Lookup the encryption ID in the database file
    db_path = "encryption_db.txt"
    if not os.path.exists(db_path):
        return "Error: Encryption database not found."
    
    stored_hashed_password = None
    with open(db_path, "r") as db_file:
        for line in db_file:
            parts = line.strip().split(",")
            if len(parts) == 2 and parts[0] == encryption_id:
                stored_hashed_password = parts[1]
                break
    if stored_hashed_password is None:
        return "Error: Encryption ID not found in database."
    
    # Verify the provided password by comparing hashes
    input_hashed = hashlib.sha256(password.encode()).hexdigest()
    if stored_hashed_password != input_hashed:
        return "YOU ARE NOT AUTHORIZED"
    
    # Also verify the token stored in the header matches the password's hash token
    verification_token = hashlib.sha256(password.encode()).hexdigest()[:8]
    if token_in_image != verification_token:
        return "YOU ARE NOT AUTHORIZED"
    
    # Extract the encrypted message from the image (after the 28-character header)
    start_index = 28
    end_index = 28 + msg_length
    if end_index > len(flat_img):
        return "Error: Encrypted message exceeds image data."
    
    encrypted_chars = [chr(flat_img[i]) for i in range(start_index, end_index)]
    encrypted_message = ''.join(encrypted_chars)
    
    # Decrypt the message using XOR decryption
    decrypted_message = xor_decrypt(encrypted_message, password)
    return decrypted_message
