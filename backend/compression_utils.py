
import heapq
import os
from collections import defaultdict, Counter

from flask import Flask, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Define the upload folder path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency):
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(freq=node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    return heap[0]

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def compress_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    frequency = Counter(data)
    root = build_huffman_tree(frequency)
    codes = generate_codes(root)

    encoded_data = ''.join(codes[byte] for byte in data)
    padded_encoded_data = encoded_data + '0' * ((8 - len(encoded_data) % 8) % 8)
    byte_array = bytearray()

    for i in range(0, len(padded_encoded_data), 8):
        byte = padded_encoded_data[i:i+8]
        byte_array.append(int(byte, 2))

    output_path = file_path + '.huff'
    with open(output_path, 'wb') as out:
        out.write(bytes(byte_array))

@app.route('/decompress', methods=['POST'])
def decompress():
    uploaded_file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(file_path)
    freq_path = file_path.replace('.huff', '.freq')
    decompressed_path = decompress_file(file_path, freq_path)
    return send_file(decompressed_path, as_attachment=True)

def decompress_file(file_path, freq_path):
    # Placeholder implementation for decompression
    # Replace this with actual decompression logic
    # For now, just return the original file path for demonstration
    return file_path
