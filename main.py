# Perintah '%%writefile' akan menyimpan semua kode di bawah ini
# ke dalam sebuah file bernama main.py

import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO  # Ini mengimpor dari kode yolov13 yang sudah kita instal
import io
from PIL import Image
import os
import json

# --- IMPOR BARU UNTUK CORS ---
from fastapi.middleware.cors import CORSMiddleware

# --- 1. Konfigurasi Awal ---
# Pastikan path ini benar (model ada di dalam folder /content/yolov13/)
MODEL_PATH = '/content/yolov13/contekvnano.pt'
model = YOLO(MODEL_PATH)
print(f"Model {MODEL_PATH} berhasil dimuat.")

# --- 2. Inisialisasi FastAPI ---
app = FastAPI(title="YOLOv13 Anti-Cheating API")

# --- TAMBAHKAN BLOK INI UNTUK MENGIZINKAN KONEKSI DARI BROWSER ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan SEMUA domain (termasuk browser Anda)
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan SEMUA metode (GET, POST, dll)
    allow_headers=["*"],  # Mengizinkan SEMUA header
)
# --- AKHIR BLOK BARU ---


# --- 3. Definisikan Endpoint API ---
@app.get('/')
def read_root():
  return {"message": "Server YOLOv13 Anti-Cheating berjalan."}

@app.post("/detect/")
async def detect_cheating(file: UploadFile = File(...)):
  """
  Endpoint untuk mendeteksi kecurangan dari file gambar.
  """
  try:
    # Baca file gambar yang di-upload
    contents = await file.read()

    # Ubah bytes menjadi gambar
    img = Image.open(io.BytesIO(contents))

    # Lakukan deteksi dengan model YOLOv13
    results = model(img)

    # Ekstrak hasil deteksi
    detections_json = results[0].tojson()
    print("Deteksi berhasil, mengirim hasil...")

    # Kembalikan hasil sebagai JSON
    return JSONResponse(content=json.loads(detections_json))

  except Exception as e:
    print(f"Error saat deteksi: {e}")
    return JSONResponse(content={"error": str(e)}, status_code=500)
