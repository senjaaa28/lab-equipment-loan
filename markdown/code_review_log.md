# Code Review Log

Berdasarkan `markdown/code_review.md`, berikut hasil review implementasi backend Lab Equipment Loan System.

## Informasi Review
- Tanggal review: 2026-11-02
- Reviewer: Automated Review
- Commit / Versi: Setelah reorganisasi repo
- File yang direview: app/, tests/, run.py, requirements.txt

## Hasil Review
### 1. Kesesuaian dengan Requirement
- [x] Endpoint pada requirement.md telah diimplementasikan (Items & Loans)
- [x] Model Item dan Loan sesuai spesifikasi
- [x] Status loan: BORROWED, RETURNED, CANCELLED
- [x] Format request/response JSON

### 2. Database
- [x] Skema items dan loans
- [x] Foreign key loans.item_id -> items.id
- [x] Parameter binding digunakan
- [x] Transaksi untuk peminjaman/pengembalian

### 3. Business Logic
- [x] Stok berkurang saat pinjam (BR-01)
- [x] Validasi stok cukup (BR-02)
- [x] Item tidak ditemukan -> 404 (BR-03)
- [x] Pengembalian kembalikan stok jadi RETURNED (BR-04)
- [x] Loan RETURNED tidak bisa dikembalikan ulang (BR-05)
- [x] Stok tidak negatif (BR-06)

### 4. API
- [x] GET /items 200
- [x] POST /items 201
- [x] POST /loans 201/400/404
- [x] PUT /loans/{id}/return 200/400/404
- [x] GET /loans/student/{student_id} 200

### 5. Kualitas Kode
- [x] Struktur terpisah (routes/services/repositories)
- [x] Penanganan error konsisten
- [x] Validasi terpusat

### 6. Keamanan
- [x] Parameterized queries
- [x] Validasi input
- [x] Tidak ada hardcoded secrets

### 7. Bukti Pengujian
- [x] Test items dan loans tersedia
- [x] Semua skenario Postman lulus (sesuai laporan)

## Ringkasan Review
- Jumlah temuan: 0 (Tinggi: 0, Sedang: 0, Rendah: 0)
- Kesesuaian terhadap requirement: 100%
- Status pengujian: Lulus
- Rekomendasi akhir: Approve
- Catatan: Struktur proyek sudah rapi. Siap untuk integrasi/submit.
