# Aplikasi Pencatat Sesi Pemesanan Shuttle Kampus

**CIK3101 · Web Application Development · Sains Data · Semester 3 · Universitas Cakrawala**

Aplikasi web untuk mencatat dan mengelola sesi pemesanan shuttle di area kampus (lihat, cari, tambah, dan hapus sesi).
Backend **FastAPI**, frontend **Vue 3 + Vite**, data disimpan in-memory.

- **Pengembang:** M. Maulana Khaerul Anam
- **NIM:** 25120500032
- **Program Studi:** S1 Sains Data
- **Domain:** Transportasi Kampus (pemesanan shuttle)

## 1. Prasyarat

| Alat | Versi | Cek |
|---|---|---|
| Git | apa saja | `git --version` |
| Node.js | 20 LTS atau lebih baru | `node -v` |
| Python | 3.11 atau lebih baru | `python --version` |

> Windows: saat install Python dari python.org, **centang "Add Python to PATH"**.
> Kalau `python` tidak dikenali, coba `py`.

Tidak ada basis data yang perlu di-install. Dataset berada di memori backend.

## 2. Layanan

| Layanan | Port lokal | Catatan |
|---|---|---|
| Frontend (Vite + Vue 3) | `5173` | folder `frontend/` |
| Backend (FastAPI + Uvicorn) | `8000` | folder `backend/`; dokumentasi Swagger di `/docs` |
| Basis data | - | tidak ada; in-memory di `backend/app/data.py` (12 baris sintetis), kembali ke awal saat server restart |

Endpoint backend:

| Method | Endpoint | Fungsi | Status sukses |
|---|---|---|---|
| GET | `/health` | cek server hidup | 200 |
| GET | `/sessions` | daftar sesi (query: `page`, `limit`, `search`) | 200 |
| GET | `/sessions/{id}` | detail satu sesi | 200 / 404 |
| POST | `/sessions` | buat sesi baru | 201 |
| DELETE | `/sessions/{id}` | hapus sesi | 204 |

## 3. Cara menjalankan

Backend dan frontend harus jalan **bersamaan**, jadi buka **2 terminal**.

```bash
# --- backend (terminal 1) ---
cd backend
python -m venv venv          # sekali saja, jika venv belum ada
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# --- frontend (terminal 2) ---
cd frontend
npm install
npm run dev
```

Jika berhasil:

- Backend: http://localhost:8000 (Swagger: http://localhost:8000/docs)
- Frontend: http://localhost:5173

## 4. Cara memverifikasi

### Otomatis

Kedua server harus sedang berjalan. Di terminal ketiga pada root project:

```bash
python verify.py --sesi 2
```

### Manual, per requirement

| # | Requirement | Cara verifikasi | Hasil yang diharapkan | Lolos |
|---|---|---|---|---|
| 1 | Server hidup | `curl -i http://localhost:8000/health` | `200` dengan `{"status":"ok"}` | [ ] |
| 2 | In-memory dataset | buka `backend/app/data.py`, atau `GET /sessions?limit=100` | minimal 12 baris data sintetis | [ ] |
| 3 | `GET /sessions` (pagination + search) | `curl "http://localhost:8000/sessions?page=1&limit=5"` lalu `curl "http://localhost:8000/sessions?search=<kata>"` | jumlah data sesuai `limit`; hasil search hanya yang cocok nama/rute | [ ] |
| 4 | `GET /sessions/{id}` + 404 | `curl -i http://localhost:8000/sessions/1` lalu `curl -i http://localhost:8000/sessions/99999` | ID valid: `200` + detail; ID tidak ada: `404` | [ ] |
| 5 | `POST /sessions` (Pydantic + 201) | Swagger `/docs` -> POST /sessions -> *Try it out*, sekali data valid, sekali data tidak lengkap | data valid: `201 Created`; data tidak valid: `422` | [ ] |
| 6 | `DELETE /sessions/{id}` + 204 | `curl -i -X DELETE http://localhost:8000/sessions/1`, lalu `GET` ID yang sama | delete: `204 No Content`; GET setelahnya: `404` | [ ] |
| 7 | CORS middleware | `curl -i -H "Origin: http://localhost:5173" http://localhost:8000/sessions` | header respons memuat `access-control-allow-origin` | [ ] |
| 8 | Frontend 4 state + Retry | buka `http://localhost:5173`: amati Loading lalu Success. Matikan backend, refresh halaman | muncul Error + tombol **Retry**; nyalakan backend, klik Retry, data tampil | [ ] |
| 9 | Validasi form + konfirmasi delete | submit form create dalam keadaan kosong; klik hapus pada satu data | form menolak input kosong; dialog konfirmasi muncul sebelum data terhapus | [ ] |

> Centang kolom **Lolos** hanya setelah requirement benar-benar terverifikasi.
> Tes delete bersifat destruktif: restart backend untuk mengembalikan data awal.

## 5. Masalah yang sering muncul

| Gejala | Sebab biasanya | Tindakan |
|---|---|---|
| `python` tidak dikenali (Windows) | PATH tidak dicentang saat install | pakai `py`, atau install ulang dan centang "Add Python to PATH" |
| `uvicorn` tidak dikenali | virtual environment belum aktif | jalankan `venv\Scripts\activate` dulu |
| `/health` atau `/docs` 404 | `uvicorn` dijalankan dari folder yang salah, atau `/health` belum didefinisikan | jalankan dari dalam `backend/`; cek `app/main.py` |
| Frontend error "Network Error" / CORS | backend mati atau CORS belum aktif | pastikan backend jalan di port 8000 |
| `npm run dev` jalan tapi halaman kosong | `index.html` tidak menunjuk `src/main.js` | cek `<script type="module" src="/src/main.js">` |
| `venv/` ikut ter-commit | `.gitignore` diubah | kembalikan `.gitignore` bawaan repo |
| Data kembali seperti awal | data in-memory, hilang saat server restart | perilaku normal, bukan bug |

