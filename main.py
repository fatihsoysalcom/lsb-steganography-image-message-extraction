from PIL import Image
import io
import os

def hide_message(image_path, message, output_path="stego_image.png"):
    """Hides a message in the least significant bits of an image's pixel data."""
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert message to binary string
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Add a unique delimiter to mark the end of the message (e.g., two null bytes in binary)
    binary_message += '0000000000000000'

    # Check if the message is too long for the image
    if len(binary_message) > width * height * 3: # Each pixel has 3 color channels (R,G,B)
        raise ValueError("Message too long to hide in the image.")

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3): # Iterate through R, G, B channels (Red, Green, Blue)
                if data_index < len(binary_message):
                    # Modify the least significant bit (LSB) of the pixel channel
                    # pixel[i] & ~1 clears the LSB
                    # int(binary_message[data_index]) sets the LSB to 0 or 1
                    pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index]) # This is where LSB steganography happens
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                break # All message bits have been hidden
        if data_index >= len(binary_message):
            break

    img.save(output_path)
    return img # Return the modified image object for in-memory extraction demo

def extract_message(img_object):
    """Extracts a hidden message from the least significant bits of an image."""
    binary_message = ""
    width, height = img_object.size

    for y in range(height):
        for x in range(width):
            pixel = list(img_object.getpixel((x, y)))
            for i in range(3): # Iterate through R, G, B channels
                # Extract the least significant bit (LSB)
                binary_message += str(pixel[i] & 1) # Extracting the LSB
                # Check for the delimiter
                if binary_message.endswith('0000000000000000'): # Delimiter found
                    try:
                        # Convert binary string to characters, excluding the delimiter
                        message = ""
                        binary_message = binary_message[:-16] # Remove the delimiter
                        for j in range(0, len(binary_message), 8):
                            byte = binary_message[j:j+8]
                            message += chr(int(byte, 2))
                        return message
                    except ValueError:
                        return "Error: Could not decode message."
    return "No hidden message found or message corrupted."

if __name__ == "__main__":
    # 1. Create a dummy image for demonstration
    # This ensures the example is self-contained without needing an external image file.
    dummy_image = Image.new('RGB', (100, 100), color = 'white')
    dummy_image_path = "original_image.png"
    dummy_image.save(dummy_image_path)
    print(f"Created a dummy image: {dummy_image_path}")

    # The secret message (flag) to hide
    secret_message = "CTF{Unblur_Me_LSB_Success_123}"
    print(f"Secret message to hide: '{secret_message}'")

    # 2. Hide the message in the dummy image
    stego_image_path = "stego_image.png"
    modified_image_obj = hide_message(dummy_image_path, secret_message, stego_image_path)
    print(f"Message hidden in {stego_image_path}")

    # 3. Extract the message from the steganographic image
    # Simulate loading the steganographic image from a file for extraction
    loaded_stego_image = Image.open(stego_image_path)
    extracted_message = extract_message(loaded_stego_image)
    print(f"Extracted message: '{extracted_message}'")

    if extracted_message == secret_message:
        print("LSB Steganography successful: The hidden message was correctly extracted!")
    else:
        print("LSB Steganography failed or message mismatch.")

    # Clean up dummy files
    os.remove(dummy_image_path)
    os.remove(stego_image_path)
    print("Cleaned up dummy image files.")
