# Code Review Checklist

## Lab Equipment Loan System

Dokumen ini digunakan sebagai checklist review kode untuk proyek Lab Equipment Loan System (Python 3.x, Flask, SQLite, JSON).

**Informasi Review**
- Tanggal review: ____________________
- Reviewer: ____________________
- Commit / Versi: ____________________
- File yang direview: ____________________

### 1. Kesesuaian dengan Requirement
- [ ] Seluruh endpoint pada `requirement.md` telah diimplementasikan.
- [ ] Model data `Item` dan `Loan` sesuai spesifikasi (field, tipe, relasi).
- [ ] Status loan hanya menggunakan `BORROWED`, `RETURNED`, atau `CANCELLED`.
- [ ] Format request dan response menggunakan JSON.
- [ ] Tidak ada fitur di luar ruang lingkup yang ditambahkan tanpa persetujuan.

### 2. Database
- [ ] Skema tabel `items` dan `loans` sesuai model data.
- [ ] `loans.item_id` memiliki foreign key ke `items.id`.
- [ ] Primary key menggunakan auto-increment.
- [ ] Tipe data kolom sesuai (integer, string, datetime).
- [ ] Koneksi database ditutup dengan benar setelah digunakan.
- [ ] Query menggunakan parameter binding (tidak ada string concatenation).
- [ ] Perubahan stok dan pembuatan loan berada dalam satu transaksi/commit.

### 3. Business Logic
- [ ] Stok berkurang saat peminjaman berhasil (BR-01).
- [ ] Peminjaman ditolak jika `quantity > available_stock` (BR-02).
- [ ] Peminjaman ditolak jika `item_id` tidak ditemukan (BR-03).
- [ ] Pengembalian memulihkan stok dan mengubah status menjadi `RETURNED` (BR-04).
- [ ] Loan berstatus `RETURNED` tidak dapat dikembalikan ulang (BR-05).
- [ ] `available_stock` tidak pernah negatif (BR-06).
- [ ] `available_stock` tidak melebihi `total_stock` saat pengembalian (BR-07).
- [ ] Validasi input `quantity` positif dan bukan nol.

### 4. API
- [ ] `GET /items` mengembalikan `200 OK` dan stok terbaru.
- [ ] `POST /items` mengembalikan `201 Created` untuk data valid.
- [ ] `POST /loans` mengembalikan `201 Created` untuk data valid.
- [ ] `POST /loans` mengembalikan `400 Bad Request` jika stok tidak cukup.
- [ ] `POST /loans` mengembalikan `404 Not Found` jika item tidak ada.
- [ ] `PUT /loans/{id}/return` mengembalikan `200 OK` jika berhasil.
- [ ] `PUT /loans/{id}/return` mengembalikan `400 Bad Request` jika sudah `RETURNED`.
- [ ] `PUT /loans/{id}/return` mengembalikan `404 Not Found` jika loan tidak ada.
- [ ] `GET /loans/student/{student_id}` mengembalikan daftar loan yang sesuai.
- [ ] Kode status HTTP dan struktur respons konsisten.

### 5. Kualitas Kode
- [ ] Kode mengikuti konvensi PEP 8.
- [ ] Penamaan variabel dan fungsi jelas serta konsisten.
- [ ] Tidak ada kode duplikat yang dapat direfaktor.
- [ ] Fungsi memiliki tanggung jawab tunggal (single responsibility).
- [ ] Penanganan error terpusat dan konsisten.
- [ ] Tidak ada kode mati atau `print` debug yang tertinggal.
- [ ] Struktur proyek rapi (routing, model, logika terpisah).

### 6. Keamanan
- [ ] Query database menggunakan parameter binding untuk mencegah SQL injection.
- [ ] Input divalidasi sebelum diproses.
- [ ] Tidak ada kredensial, secret, atau path sensitif yang di-hardcode.
- [ ] Error tidak membocorkan detail internal (stack trace) ke klien.
- [ ] `debug=True` tidak digunakan pada konfigurasi produksi.

### 7. Bukti Pengujian
- [ ] Tersedia pengujian untuk `POST /loans` (skenario 201, 400, 404).
- [ ] Tersedia pengujian untuk `PUT /loans/{id}/return` (skenario 200, 400, 404).
- [ ] Tersedia pengujian untuk `GET /items` (stok terbaru).
- [ ] Tersedia pengujian untuk `GET /loans/student/{student_id}`.
- [ ] Seluruh pengujian lulus.
- [ ] Hasil pengujian dilampirkan (log/screenshot).

### 8. Tabel Temuan

| No | Kategori | Lokasi (file:baris) | Temuan | Tingkat | Rekomendasi | Status |
|---|---|---|---|---|---|---|
| 1 | | | | Tinggi/Sedang/Rendah | | Open/Fixed |
| 2 | | | | | | |
| 3 | | | | | | |

**Keterangan tingkat:**
- **Tinggi**: memblokir fungsi utama atau berpotensi merusak data.
- **Sedang**: memengaruhi sebagian fungsi atau kualitas.
- **Rendah**: perbaikan kosmetik atau peningkatan.

### 9. Ringkasan Review
- Jumlah temuan: ____ (Tinggi: ____, Sedang: ____, Rendah: ____)
- Kesesuaian terhadap requirement: ____ %
- Status pengujian: Lulus / Tidak Lulus
- Rekomendasi akhir: **Approve / Approve dengan catatan / Perlu perbaikan**
- Catatan tambahan:

  ____________________________________________________________

  ____________________________________________________________
