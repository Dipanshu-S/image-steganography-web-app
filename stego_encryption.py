import cv2
import os
import hashlib
import uuid

def xor_encrypt(message, key):
    return ''.join(chr(ord(ch) ^ ord(key[i % len(key)])) for i, ch in enumerate(message))

def encrypt_message(image_path, message, password):
    # Load the source image
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Source image not found.", None
    
    # Hash the password so it isn’t stored in plain text
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Encrypt the message using XOR encryption
    encrypted_msg = xor_encrypt(message, password)
    message_length = len(encrypted_msg)
    
    # Flatten the image to embed the data sequentially
    flat_img = img.flatten()
    if message_length > len(flat_img):
        return "Error: Image is too small to hold the message.", None
    
    # Embed the encrypted message into the flattened image
    for i, ch in enumerate(encrypted_msg):
        flat_img[i] = ord(ch)
    
    # Reshape the image back to its original dimensions
    img = flat_img.reshape(img.shape)
    
    # Generate a unique encryption ID (hex string)
    enc_id = uuid.uuid4().hex
    output_image_path = f"encrypted_{enc_id}.png"
    
    # Save the encrypted image
    cv2.imwrite(output_image_path, img)
    
    # Save metadata (hashed password and message length) in a separate file
    metadata_filename = f"metadata_{enc_id}.txt"
    with open(metadata_filename, "w") as f:
        f.write(hashed_password + "\n")
        f.write(str(message_length))
    
    # Return the encryption ID and the output image path
    return enc_id, output_image_path
