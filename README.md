# File & Image Compressor
This web app compresses files and images using a custom backend algorithm.

This project is a full-stack web application that allows users to compress text-based files (like .txt, .csv, etc.) using Huffman Encoding, a lossless data compression algorithm. It's built using:

🔥 Frontend: React + Axios + Vite

🧠 Backend: Flask + Huffman compression logic

🌍 Communication: REST API with CORS enabled

 **Features:**
✅ Upload and compress .txt, .csv, or similar plain-text files
✅ Download compressed output as a .huff file
✅ Huffman coding-based logic for effective compression
✅ React frontend with clean UX
✅ Flask backend with a single compression endpoint

project-root/
├── backend/
│   └── app.py              # Flask API with Huffman compression
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       └── App.jsx         # Main React component
└── README.md

**Setup and Run Flask Backend**: 
cd backend
pip install flask flask-cors
python app.py

**Setup and Run React Frontend**:cd ../frontend
npm install
npm run dev
