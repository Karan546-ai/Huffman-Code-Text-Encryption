import heapq
from collections import Counter
import tkinter as tk
from tkinter import messagebox, font

# Huffman Coding Section
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    
    return heap[0]

def build_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    
    return codebook

def huffman_encoding(text):
    huffman_tree = build_huffman_tree(text)
    codebook = build_codes(huffman_tree)
    encoded_text = ''.join([codebook[char] for char in text])
    return encoded_text, huffman_tree

def huffman_decoding(encoded_text, huffman_tree):
    decoded_text = []
    node = huffman_tree
    for bit in encoded_text:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.char is not None:
            decoded_text.append(node.char)
            node = huffman_tree
    return ''.join(decoded_text)

# Tkinter GUI Section with Enhanced Formatting
class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Code Encryption & Decryption")
        self.root.geometry("600x450")
        self.root.config(bg="#2F3E46")  # Dark background color
        
        # Font styling
        self.header_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.label_font = font.Font(family="Arial", size=12)
        self.output_font = font.Font(family="Courier", size=10)
        
        # Header with enhanced background and font color
        self.header_label = tk.Label(root, text="Huffman Code Text Encryption", font=self.header_font, bg="#4E6C74", fg="#E1E1E1", pady=10)
        self.header_label.grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="nsew")
        
        # Input Message Field
        self.label = tk.Label(root, text="Enter Message:", font=self.label_font, bg="#2F3E46", fg="#D9D9D9")
        self.label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.message_entry = tk.Entry(root, width=50, font=self.label_font, bg="#F0F0F0", relief="flat")
        self.message_entry.grid(row=1, column=1, padx=20, pady=10, ipady=5)
        
        # Encrypt Button with hover effect
        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt_message, bg="#00A676", fg="white", font=self.label_font, relief="flat", padx=20, pady=5)
        self.encrypt_button.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.encrypt_button.bind("<Enter>", self.on_hover_encrypt)
        self.encrypt_button.bind("<Leave>", self.on_leave_encrypt)
        
        # Decrypt Button with hover effect
        self.decrypt_button = tk.Button(root, text="Decrypt", command=self.decrypt_message, bg="#FF715B", fg="white", font=self.label_font, relief="flat", padx=20, pady=5)
        self.decrypt_button.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        self.decrypt_button.bind("<Enter>", self.on_hover_decrypt)
        self.decrypt_button.bind("<Leave>", self.on_leave_decrypt)
        
        # Display Output
        self.output_label = tk.Label(root, text="Output:", font=self.label_font, bg="#2F3E46", fg="#D9D9D9")
        self.output_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        
        self.output_text = tk.Text(root, height=7, width=50, font=self.output_font, wrap="word", bg="#D9D9D9", relief="flat")
        self.output_text.grid(row=4, column=0, columnspan=2, padx=20, pady=5)
        self.output_text.config(state="disabled")
        
        self.huffman_tree = None
        self.encoded_message = ""
    
    def encrypt_message(self):
        text = self.message_entry.get()
        if not text:
            messagebox.showerror("Input Error", "Please enter a message to encrypt")
            return
        
        encoded_message, self.huffman_tree = huffman_encoding(text)
        self.encoded_message = encoded_message
        self.update_output(f"Encrypted Message: {encoded_message}")
    
    def decrypt_message(self):
        if not self.huffman_tree or not self.encoded_message:
            messagebox.showerror("Decryption Error", "No message to decrypt. Encrypt a message first.")
            return
        
        decoded_message = huffman_decoding(self.encoded_message, self.huffman_tree)
        self.update_output(f"Decrypted Message: {decoded_message}")
    
    def update_output(self, message):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        self.output_text.config(state="disabled")
    
    def on_hover_encrypt(self, event):
        self.encrypt_button.config(bg="#007B5B")

    def on_leave_encrypt(self, event):
        self.encrypt_button.config(bg="#00A676")
    
    def on_hover_decrypt(self, event):
        self.decrypt_button.config(bg="#CC5A48")
    
    def on_leave_decrypt(self, event):
        self.decrypt_button.config(bg="#FF715B")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
