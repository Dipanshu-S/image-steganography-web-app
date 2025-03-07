import cv2
import os
import hashlib
import random

def xor_encrypt(message, key):
    return ''.join(chr(ord(ch) ^ ord(key[i % len(key)])) for i, ch in enumerate(message))

def encrypt_message(image_path, message, password):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Source image not found."
    
    # Generate a unique 8-character encryption ID (hexadecimal)
    encryption_id = "{:08x}".format(random.getrandbits(32))
    
    # Create a verification token: first 8 characters of SHA-256 hash of the password
    verification_token = hashlib.sha256(password.encode()).hexdigest()[:8]
    
    # Encrypt the message using XOR encryption
    encrypted_msg = xor_encrypt(message, password)
    
    # Create header:
    # "STEG" (4 chars) + encryption_id (8 chars) + message length (8-digit zero-padded) + verification token (8 chars)
    msg_length = str(len(encrypted_msg)).zfill(8)
    header = "STEG" + encryption_id + msg_length + verification_token  # Total header length = 28
    
    total_data = header + encrypted_msg
    
    # Flatten the image array to embed data sequentially
    flat_img = img.flatten()
    
    if len(total_data) > len(flat_img):
        return "Error: Image is too small to hold the message."
    
    # Embed the header and encrypted message into the image pixels
    for i, ch in enumerate(total_data):
        flat_img[i] = ord(ch)
    
    # Reshape back to original image shape and save the output image
    img = flat_img.reshape(img.shape)
    output_image_path = "encryptedImage.png"
    cv2.imwrite(output_image_path, img)
    
    # Store the encryption ID and the hashed password in a separate file (append mode)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    db_entry = encryption_id + "," + hashed_password + "\n"
    with open("encryption_db.txt", "a") as db_file:
        db_file.write(db_entry)
    
    # Return both the encryption ID and the output image path
    return encryption_id, output_image_path
