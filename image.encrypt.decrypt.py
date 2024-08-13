import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox as mbox, simpledialog
from PIL import ImageTk, Image
import cv2
import numpy as np
import hashlib
import winsound

# Create the main window
window = Tk()
window.geometry("1000x700")
window.title("Image Encryption & Decryption")
window.configure(bg="#e6f7ff")  # Mild attrac addtive background color

# Define variables
global count, eimg, encryption_password_hash
frp = []
tname = []
con = 1
bright = 0
panelB = None
panelA = None
encryption_password_hash = None

# Utility functions
def getpath(path):
    a = path.split('/')
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

def getfilename(path):
    a = path.split('/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

def openfilename():
    filename = filedialog.askopenfilename(title="Open")
    return filename

def open_img():
    global x, panelA, panelB
    global count, eimg, location, filename
    count = 0
    x = openfilename()
    img = Image.open(x)
    eimg = img
    img = ImageTk.PhotoImage(img)
    temp = x
    location = getpath(temp)
    filename = getfilename(temp)
    
    panelA.config(image=img)
    panelA.image = img
    panelB.config(image=img)
    panelB.image = img

def en_fun():
    global x, image_encrypted, key, encryption_password_hash

    # Ask for password
    password = simpledialog.askstring("Password", "Enter password for encryption:", show='*')
    if not password:
        mbox.showerror("Error", "Encryption password cannot be empty.")
        return

    # Hash the password for storing
    encryption_password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Encrypt the image
    image_input = cv2.imread(x, 0)
    (x1, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0

    mu, sigma = 0, 0.1
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    image_encrypted = image_input / key
    cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)

    imge = Image.open('image_encrypted.jpg')
    imge = ImageTk.PhotoImage(imge)
    panelB.config(image=imge)
    panelB.image = imge
    mbox.showinfo("Encrypt Status", "Image Encrypted successfully.")

def de_fun():
    global image_encrypted, key, encryption_password_hash

    # Ask for decryption password
    password = simpledialog.askstring("Password", "Enter password for decryption:", show='*')
    if not password:
        mbox.showerror("Error", "Decryption password cannot be empty.")
        return

    # Check if the entered password matches the encryption password
    if hashlib.sha256(password.encode()).hexdigest() != encryption_password_hash:
        mbox.showerror("Error", "Incorrect password. Decryption failed.")
        
        # Play warning sound for 2 seconds
        winsound.Beep(1000, 2000)  # Beep at 1000 Hz for 2000 ms (2 seconds)
        
        return

    # Decrypt the image
    image_output = image_encrypted * key
    image_output *= 255.0
    cv2.imwrite('image_output.jpg', image_output)

    imgd = Image.open('image_output.jpg')
    imgd = ImageTk.PhotoImage(imgd)
    panelB.config(image=imgd)
    panelB.image = imgd
    mbox.showinfo("Decrypt Status", "Image decrypted successfully.")

def reset():
    image = cv2.imread(x)[:, :, ::-1]
    global count, eimg
    count = 6
    global o6
    o6 = image
    image = Image.fromarray(o6)
    eimg = image
    image = ImageTk.PhotoImage(image)
    panelB.config(image=image)
    panelB.image = image
    mbox.showinfo("Success", "Image reset to original format!")

def save_img():
    global location, filename, eimg
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    eimg.save(filename)
    mbox.showinfo("Success", "Encrypted Image Saved Successfully!")

def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Frames for layout
frame_buttons_top = Frame(window, bg="#e6f7ff")
frame_buttons_top.pack(side=TOP, fill=X, padx=10, pady=10)

frame_image = Frame(window, bg="#e6f7ff")
frame_image.pack(expand=True, fill=BOTH, padx=10, pady=10)

frame_buttons_bottom = Frame(window, bg="#e6f7ff")
frame_buttons_bottom.pack(side=BOTTOM, fill=X, padx=10, pady=10)

# Centered title text
title_label = Label(frame_image, text="Image Encryption & Decryption", font=("Arial", 30), bg="#e6f7ff", fg="dark blue")
title_label.pack(side=TOP, pady=20)

# Image panels
panelA = Label(frame_image, bg="#e6f7ff")
panelA.pack(side=LEFT, padx=20, pady=20)

panelB = Label(frame_image, bg="#e6f7ff")
panelB.pack(side=RIGHT, padx=20, pady=20)

# Top buttons (Left: Choose, Save; Right: Exit)
chooseb = Button(frame_buttons_top, text="Choose", command=open_img, font=("Arial", 14), bg="#8fbc8f", fg="white", borderwidth=0)
chooseb.pack(side=LEFT, padx=5, pady=5)

saveb = Button(frame_buttons_top, text="Save", command=save_img, font=("Arial", 14), bg="#8fbc8f", fg="white", borderwidth=0)
saveb.pack(side=LEFT, padx=5, pady=5)

exitb = Button(frame_buttons_top, text="EXIT", command=exit_win, font=("Arial", 14), bg="#ff6347", fg="white", borderwidth=0)
exitb.pack(side=RIGHT, padx=5, pady=5)

# Bottom buttons (Encrypt, Decrypt, Reset)
enb = Button(frame_buttons_bottom, text="Encrypt", command=en_fun, font=("Arial", 18), bg="#4682b4", fg="white", borderwidth=0)
enb.pack(side=LEFT, expand=True, padx=20, pady=10)

deb = Button(frame_buttons_bottom, text="Decrypt", command=de_fun, font=("Arial", 18), bg="#32cd32", fg="white", borderwidth=0)
deb.pack(side=LEFT, expand=True, padx=20, pady=10)

resetb = Button(frame_buttons_bottom, text="Reset", command=reset, font=("Arial", 18), bg="#ffd700", fg="white", borderwidth=0)
resetb.pack(side=LEFT, expand=True, padx=20, pady=10)

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()
