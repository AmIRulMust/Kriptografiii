import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np


#GUI 
class CipherApp:
    def __init__(self, root):
        self.root = root
        root.title("GUI")

        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.grid(row=0, column=0, columnspan=2)

        self.key_label = tk.Label(root, text="Key (min 12 chars):")
        self.key_label.grid(row=1, column=0)
        
        self.key_entry = tk.Entry(root)
        self.key_entry.grid(row=1, column=1)

        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt)
        self.encrypt_button.grid(row=2, column=0)

        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt)
        self.decrypt_button.grid(row=2, column=1)

        self.cipher_var = tk.StringVar()
        self.cipher_var.set("Vigenere")
        
        # pilihan
        self.cipher_menu = tk.OptionMenu(root, self.cipher_var, "Vigenere", "Playfair", "Hill")
        self.cipher_menu.grid(row=3, column=0, columnspan=2)

        # up
        self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=4, column=0, columnspan=2)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def encrypt(self):
        text = self.text_area.get(1.0, tk.END).strip()
        key = self.key_entry.get().strip()

        if len(key) < 12:
            messagebox.showerror("Error", "Key must be at least 12 characters.")
            return

        cipher_type = self.cipher_var.get()
        if cipher_type == "Vigenere":
            encrypted_text = vigenere_encrypt(text, key)
        elif cipher_type == "Playfair":
            encrypted_text = playfair_encrypt(text, key)
        elif cipher_type == "Hill":
            encrypted_text = hill_encrypt(text, key)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, encrypted_text)

    def decrypt(self):
        text = self.text_area.get(1.0, tk.END).strip()
        key = self.key_entry.get().strip()

        if len(key) < 12:
            messagebox.showerror("Error", "Key must be at least 12 characters.")
            return

        cipher_type = self.cipher_var.get()
        if cipher_type == "Vigenere":
            decrypted_text = vigenere_decrypt(text, key)
        elif cipher_type == "Playfair":
            decrypted_text = playfair_decrypt(text, key)
        elif cipher_type == "Hill":
            decrypted_text = hill_decrypt(text, key)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, decrypted_text)

def vigenere_encrypt(text, key):
    encrypted = []
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_int = [ord(i) for i in text.upper() if i.isalpha()]
    
    for i in range(len(text_int)):
        value = (text_int[i] + key_as_int[i % key_length]) % 26
        encrypted.append(chr(value + 65))
    
    return ''.join(encrypted)

def vigenere_decrypt(ciphertext, key):
    decrypted = []
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext.upper() if i.isalpha()]
    
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        decrypted.append(chr(value + 65))
    
    return ''.join(decrypted)



def playfair_generate_key_matrix(key):
    matrix = []
    key = ''.join(sorted(set(key), key=key.index)).replace('J', 'I').upper()
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    
    for char in key:
        if char not in matrix:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair_prepare_text(text):
    text = text.upper().replace('J', 'I')
    prepared_text = ''
    
    i = 0
    while i < len(text):
        char1 = text[i]
        char2 = text[i+1] if i+1 < len(text) else 'X'
        if char1 == char2:
            prepared_text += char1 + 'X'
            i += 1
        else:
            prepared_text += char1 + char2
            i += 2
            
    if len(prepared_text) % 2 != 0:
        prepared_text += 'X'
    return prepared_text

def playfair_find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None

def playfair_encrypt(text, key):
    matrix = playfair_generate_key_matrix(key)
    text = playfair_prepare_text(text)
    encrypted = ''
    
    for i in range(0, len(text), 2):
        row1, col1 = playfair_find_position(matrix, text[i])
        row2, col2 = playfair_find_position(matrix, text[i+1])
        
        if row1 == row2:
            encrypted += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            encrypted += matrix[row1][col2] + matrix[row2][col1]
    
    return encrypted

def playfair_decrypt(ciphertext, key):
    matrix = playfair_generate_key_matrix(key)
    decrypted = ''
    
    for i in range(0, len(ciphertext), 2):
        row1, col1 = playfair_find_position(matrix, ciphertext[i])
        row2, col2 = playfair_find_position(matrix, ciphertext[i+1])
        
        if row1 == row2:
            decrypted += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            decrypted += matrix[row1][col2] + matrix[row2][col1]
    
    return decrypted




import numpy as np

def validate_key(key):
    if len(key) < 12:
        raise ValueError("The key must be at least 12 characters long.")

def process_key(key):
    key = key.upper().replace(" ", "")  
    key_numeric = [ord(c) - 65 for c in key if c.isalpha()]  
    
    if len(key_numeric) < 9:
        raise ValueError("Not enough characters to form a 3x3 matrix from the key.")
    return np.array(key_numeric[:9]).reshape(3, 3)  # Use the first 9 characters

def mod_inverse(a, m):
    a = a % m
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def hill_encrypt(text, key):
    validate_key(key)  
    key_matrix = process_key(key)  # Use the first 9 letters for a 3x3 matrix
    
    text = text.upper().replace(" ", "")
    text_vector = [ord(c) - 65 for c in text]

    while len(text_vector) % 3 != 0:
        text_vector.append(23)  

    encrypted = []
    for i in range(0, len(text_vector), 3):
        vector = np.array(text_vector[i:i+3])
        result = np.dot(key_matrix, vector) % 26
        encrypted.extend(result)

    return ''.join(chr(c + 65) for c in encrypted)


def hill_decrypt(ciphertext, key):
    validate_key(key)
    key_matrix = process_key(key)  

    determinant = int(np.round(np.linalg.det(key_matrix))) % 26
    determinant_inv = mod_inverse(determinant, 26)
    
    if determinant_inv is None:
        raise ValueError("The key matrix is not invertible in modulo 26. Please use a different key.")
    
    adjugate_matrix = np.array([[key_matrix[1, 1] * key_matrix[2, 2] - key_matrix[1, 2] * key_matrix[2, 1],
                                 key_matrix[0, 2] * key_matrix[2, 1] - key_matrix[0, 1] * key_matrix[2, 2],
                                 key_matrix[0, 1] * key_matrix[1, 2] - key_matrix[0, 2] * key_matrix[1, 1]],
                                [key_matrix[1, 2] * key_matrix[2, 0] - key_matrix[1, 0] * key_matrix[2, 2],
                                 key_matrix[0, 0] * key_matrix[2, 2] - key_matrix[0, 2] * key_matrix[2, 0],
                                 key_matrix[0, 2] * key_matrix[1, 0] - key_matrix[0, 0] * key_matrix[1, 2]],
                                [key_matrix[1, 0] * key_matrix[2, 1] - key_matrix[1, 1] * key_matrix[2, 0],
                                 key_matrix[0, 1] * key_matrix[2, 0] - key_matrix[0, 0] * key_matrix[2, 1],
                                 key_matrix[0, 0] * key_matrix[1, 1] - key_matrix[0, 1] * key_matrix[1, 0]]])

    key_inv = (determinant_inv * adjugate_matrix) % 26
    key_inv = key_inv.astype(int)

    ciphertext_vector = [ord(c) - 65 for c in ciphertext]
    decrypted = []

    for i in range(0, len(ciphertext_vector), 3):
        vector = np.array(ciphertext_vector[i:i+3])
        result = np.dot(key_inv, vector) % 26
        decrypted.extend(result)

    return ''.join(chr(c + 65) for c in decrypted)



#Run
root = tk.Tk()
app = CipherApp(root)
root.mainloop()
