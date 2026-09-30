# Backend - API Pemesanan Shuttle Kampus

Layanan backend berbasis **FastAPI** dan **Uvicorn** untuk mengelola sesi pemesanan shuttle di area kampus. Data disimpan in-memory, sehingga kembali ke kondisi awal setiap server di-restart.

> Panduan menjalankan seluruh aplikasi (backend + frontend) dan verifikasi tiap requirement ada di [`README.md`](../README.md) pada root project.

## Struktur folder

```text
backend/
├── app/
│   ├── __init__.py
│   ├── data.py         # dataset sintetis in-memory (12 baris)
│   ├── main.py         # aplikasi FastAPI, middleware CORS, endpoint
│   └── schemas.py      # schema Pydantic untuk validasi request/response
└── requirements.txt    # dependensi Python
```

## Menjalankan server

Dari root project:

```bash
cd backend
python -m venv venv          # sekali saja, jika venv belum ada

# Windows CMD:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Server aktif di `http://localhost:8000`. Jalankan `uvicorn` dari dalam folder `backend/`, karena `app.main` dicari relatif terhadap folder tersebut.

## Endpoint

| Method | Endpoint | Fungsi | Status |
|---|---|---|---|
| GET | `/health` | cek server hidup | `200` |
| GET | `/sessions` | daftar sesi; query `page`, `limit`, `search` | `200` |
| GET | `/sessions/{id}` | detail sesi berdasarkan ID | `200` / `404` |
| POST | `/sessions` | tambah sesi baru (divalidasi Pydantic) | `201` / `422` |
| DELETE | `/sessions/{id}` | hapus sesi berdasarkan ID | `204` / `404` |

## Dokumentasi interaktif

Swagger UI di `http://localhost:8000/docs` dipakai untuk mencoba tiap endpoint langsung dari browser.

Cek cepat dari terminal:

```bash
curl -i http://localhost:8000/health
```
