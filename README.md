Image Encryption and Decryption
This Python script provides functionalities to encrypt and decrypt images using the Python Imaging Library (PIL). Encryption involves adding a key to each RGB value of the pixels, and decryption reverses this process.

Requirements
Python 3.x
Pillow (Python Imaging Library)

Installation
Clone or download the repository to your local machine.
Install the required dependencies using pip:
pip install pillow
Usage
Place the image file you want to encrypt in the project directory.

Open the Python script (image_encrypt_decrypt.py) and modify the image_path variable to specify the path to your image file.

Choose a key (an integer value) for encryption and decryption. Modify the key variable accordingly.

Run the script:

python image_encrypt_decrypt.py
The script will encrypt the image and save the encrypted version as encrypted_image.png. It will then decrypt the encrypted image and save the decrypted version as decrypted_image.png.

Example
# Example usage
image_path = "C:/Users/Admin/Downloads/text.jpg"
key = 250000  # Change this key as needed
encrypt_image(image_path, key)
decrypt_image("encrypted_image.png", key)

Ensure that the image file exists at the specified path and that you have write permissions to the directory for saving the encrypted and decrypted images.

The encryption and decryption process can take some time, depending on the size of the image.
