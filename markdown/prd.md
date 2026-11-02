# Product Requirement Document (PRD)

## Lab Equipment Loan System

### 1. Ringkasan Produk
Lab Equipment Loan System adalah API berbasis Flask untuk mengelola peminjaman peralatan laboratorium. Sistem memastikan stok peralatan selalu akurat, menolak peminjaman yang melebihi stok tersedia, serta mencatat pengembalian secara konsisten.

### 2. Tujuan
- Menyediakan pencatatan peminjaman dan pengembalian peralatan laboratorium yang sederhana dan dapat diandalkan.
- Menjaga konsistensi stok peralatan setelah setiap transaksi.
- Menyediakan riwayat peminjaman per mahasiswa.

### 3. Aturan Bisnis (Business Rules)

| Kode | Aturan |
|---|---|
| BR-01 | Stok berkurang saat peminjaman berhasil dilakukan. Nilai `available_stock` dikurangi sebesar `quantity`. |
| BR-02 | Peminjaman ditolak jika stok akan menjadi kurang dari 0, yaitu ketika `quantity > available_stock`. |
| BR-03 | Peminjaman ditolak jika `item_id` tidak ditemukan. |
| BR-04 | Pengembalian yang berhasil memulihkan stok: `available_stock` bertambah sebesar `quantity` dan status berubah menjadi `RETURNED`. |
| BR-05 | Transaksi yang sudah berstatus `RETURNED` tidak boleh dikembalikan lagi. |
| BR-06 | `available_stock` tidak boleh bernilai negatif dalam kondisi apa pun. |
| BR-07 | `available_stock` tidak boleh melebihi `total_stock` saat pengembalian. |

### 4. User Stories

#### US-01 Melihat Daftar Peralatan
**Sebagai** asisten laboratorium,
**saya ingin** melihat daftar seluruh peralatan beserta stok terbarunya,
**agar** saya dapat mengetahui ketersediaan alat sebelum melayani peminjaman.

**Acceptance Criteria:**
- Endpoint `GET /items` mengembalikan daftar seluruh item.
- Setiap item menampilkan `id`, `name`, `total_stock`, dan `available_stock`.
- Data `available_stock` yang ditampilkan adalah stok terbaru setelah transaksi.

#### US-02 Mencatat Peminjaman
**Sebagai** asisten laboratorium,
**saya ingin** mencatat peminjaman alat oleh mahasiswa,
**agar** penggunaan alat dapat terlacak dan stok berkurang secara otomatis.

**Acceptance Criteria:**
- Endpoint `POST /loans` menerima `student_id`, `item_id`, dan `quantity`.
- Mengembalikan `201 Created` jika peminjaman valid.
- Mengembalikan `400 Bad Request` jika `quantity > available_stock`.
- Mengembalikan `404 Not Found` jika `item_id` tidak ditemukan.
- Stok tersedia berkurang sesuai `quantity` setelah peminjaman berhasil.

#### US-03 Mengembalikan Alat
**Sebagai** asisten laboratorium,
**saya ingin** mencatat pengembalian alat dari mahasiswa,
**agar** stok kembali tersedia dan status peminjaman menjadi `RETURNED`.

**Acceptance Criteria:**
- Endpoint `PUT /loans/{id}/return` mengubah status loan menjadi `RETURNED`.
- Mengembalikan `200 OK` jika pengembalian berhasil.
- Mengembalikan `400 Bad Request` jika loan sudah berstatus `RETURNED`.
- Mengembalikan `404 Not Found` jika loan tidak ditemukan.
- Stok tersedia bertambah sesuai `quantity` setelah pengembalian berhasil.

#### US-04 Melihat Riwayat Peminjaman Mahasiswa
**Sebagai** asisten laboratorium,
**saya ingin** melihat riwayat peminjaman berdasarkan ID mahasiswa,
**agar** saya dapat menelusuri tanggung jawab dan status peminjaman mahasiswa tersebut.

**Acceptance Criteria:**
- Endpoint `GET /loans/student/{student_id}` mengembalikan daftar loan milik mahasiswa.
- Setiap loan menampilkan `id`, `student_id`, `item_id`, `quantity`, `status`, dan `created_at`.
- Jika tidak ada transaksi, sistem mengembalikan daftar kosong.

### 5. Acceptance Criteria Rinci (API)

#### 5.1 POST `/loans`
| Kondisi | Status | Keterangan |
|---|---|---|
| `quantity > available_stock` | `400 Bad Request` | Peminjaman melebihi stok |
| `item_id` tidak ditemukan | `404 Not Found` | Item tidak ada |
| Permintaan valid | `201 Created` | Loan dibuat, stok berkurang |

#### 5.2 PUT `/loans/{id}/return`
| Kondisi | Status | Keterangan |
|---|---|---|
| Loan sudah `RETURNED` | `400 Bad Request` | Tidak boleh dikembalikan ulang |
| Pengembalian berhasil | `200 OK` | Status jadi `RETURNED`, stok pulih |
| Loan tidak ditemukan | `404 Not Found` | Loan tidak ada |

#### 5.3 GET `/items`
| Kondisi | Status | Keterangan |
|---|---|---|
| Permintaan valid | `200 OK` | Menampilkan stok terbaru |

### 6. Alur Utama

1. Asisten menambahkan item melalui `POST /items`.
2. Mahasiswa mengajukan peminjaman; asisten mencatat melalui `POST /loans`.
3. Sistem memvalidasi ketersediaan stok dan item.
4. Jika valid, stok berkurang dan loan berstatus `BORROWED`.
5. Saat alat dikembalikan, asisten memanggil `PUT /loans/{id}/return`.
6. Status berubah menjadi `RETURNED` dan stok pulih.
7. Asisten dapat memeriksa riwayat melalui `GET /loans/student/{student_id}`.

### 7. Di Luar Ruang Lingkup
- Autentikasi dan otorisasi pengguna.
- Antarmuka pengguna berbasis web.
- Notifikasi, denda, dan batas waktu peminjaman.
- Pembatalan peminjaman melalui endpoint khusus.

### 8. Metrik Keberhasilan
- Seluruh acceptance criteria API terpenuhi.
- Tidak ada kasus stok negatif pada pengujian.
- Data stok konsisten antara `GET /items` dan riwayat transaksi.
