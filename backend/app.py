from flask import Flask, request, send_file
import os
import tempfile
import heapq
import pickle
from flask import Flask, request, send_file
from flask_cors import CORS  # ✅ Add this

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes


# ---------------- Huffman Compression Logic ----------------

class Node:
    def __init__(self, char=None, freq=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(data):
    freq = {}
    for ch in data:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

def build_huffman_tree(freq):
    heap = [Node(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(freq=n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)
    return heap[0]

def build_codes(node, prefix='', codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def huffman_compress(data):
    freq = build_frequency_dict(data)
    root = build_huffman_tree(freq)
    codes = build_codes(root)
    encoded = ''.join([codes[ch] for ch in data])
    # Pad to make divisible by 8
    extra_padding = 8 - len(encoded) % 8
    encoded += '0' * extra_padding
    b = bytearray()
    for i in range(0, len(encoded), 8):
        byte = encoded[i:i+8]
        b.append(int(byte, 2))
    return b, codes

# ---------------- Flask Route ----------------

@app.route("/compress", methods=["POST"])
def compress_file():
    if 'file' not in request.files:
        return "No file uploaded", 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return "No selected file", 400

    raw_data = uploaded_file.read().decode('utf-8', errors='ignore')
    compressed_data, codebook = huffman_compress(raw_data)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".huff")
    with open(temp.name, "wb") as f:
        f.write(pickle.dumps({'data': compressed_data, 'codebook': codebook}))

    return send_file(temp.name, as_attachment=True, download_name="compressed.huff")

# ---------------- Main ----------------

if __name__ == "__main__":
    app.run(debug=True)
