import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk

def data2binary(data):
    if isinstance(data, str):
        return ''.join(format(ord(char), '08b') for char in data)
    elif isinstance(data, (bytes, np.ndarray)):
        return [format(byte, '08b') for byte in data]
    else:
        raise ValueError("Invalid data type")

def hidedata(img, data):
    data += "$$"  # '$$' is the secret key
    d_index = 0
    b_data = data2binary(data)
    len_data = len(b_data)

    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index], 2)
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-1] + b_data[d_index], 2)
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index], 2)
                d_index += 1
            if d_index >= len_data:
                break
    return img

def find_data(img):
    bin_data = ""
    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$$":
            break
    return readable_data[:-2]

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StegCraft- Image Steganography")
        self.image_path = None

        self.label = tk.Label(root, text="Select an image:")
        self.open_button = tk.Button(root, text="Open Image", command=self.open_image)
        self.label1 = tk.Label(root, text="Enter the message to hide:")
        self.text_entry = tk.Entry(root, width=70)
        self.hide_button = tk.Button(root, text="Hide Data", command=self.hide_data)
        self.show_button = tk.Button(root, text="Show Data", command=self.show_data)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_output)
        self.output_text = tk.Text(root,height=5, width=70)
        self.author_label = tk.Label(root, text="By Mehul Sarswat", font=("Helvetica",10))


        self.label.grid(row=0, column=0, columnspan=2)
        self.open_button.grid(row=1, column=0, columnspan=2)
        self.label1.grid(row=2, column=0, columnspan=2)
        self.text_entry.grid(row=3,column=0, columnspan=4)
        self.hide_button.grid(row=4, column=0, columnspan=2)
        self.show_button.grid(row=5, column=0, columnspan=2)
        self.clear_button.grid(row=6, column=0, columnspan=2)
        self.output_text.grid(row=7, column=0, columnspan=2)
        self.author_label.grid(row=8, column=0, columnspan=2)

    def open_image(self):
        self.image_path = filedialog.askopenfilename()

    def hide_data(self):
        if self.image_path:
            data = self.text_entry.get()
            if data:
                image = cv2.imread(self.image_path)
                encoded_image = hidedata(image, data)
                enc_img_path = "encoded_image.png"
                cv2.imwrite(enc_img_path, encoded_image)
                self.output_text.insert(tk.END, "Data hidden successfully!\nImage saved with the name of 'encoded_image.png'\n")
            else:
                self.output_text.insert(tk.END, "Please enter a message to hide.\n")
        else:
            self.output_text.insert(tk.END, "Please select an image first.\n")

    def show_data(self):
        if self.image_path:
            decoded_data = find_data(cv2.imread(self.image_path))
            self.output_text.insert(tk.END, f"Hidden message: {decoded_data}\n")
        else:
            self.output_text.insert(tk.END, "Please select an image first.\n")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
