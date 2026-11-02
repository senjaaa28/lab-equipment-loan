# Software Requirement Specification (SRS)

## Lab Equipment Loan System

### 1. Pendahuluan

#### 1.1 Tujuan
Dokumen ini mendefinisikan kebutuhan perangkat lunak untuk **Lab Equipment Loan System**, yaitu aplikasi sederhana untuk mengelola peminjaman dan pengembalian peralatan laboratorium oleh mahasiswa.

#### 1.2 Ruang Lingkup
Sistem menyediakan API untuk:
- Menampilkan dan menambah data peralatan laboratorium.
- Mencatat peminjaman peralatan oleh mahasiswa.
- Mencatat pengembalian peralatan.
- Menampilkan riwayat peminjaman berdasarkan mahasiswa.

Sistem **tidak** mencakup autentikasi pengguna, antarmuka web, dan manajemen pengguna pada versi ini.

#### 1.3 Definisi dan Singkatan
| Istilah | Deskripsi |
|---|---|
| SRS | Software Requirement Specification |
| API | Application Programming Interface |
| JSON | JavaScript Object Notation |
| FK | Foreign Key |
| CRUD | Create, Read, Update, Delete |
| Stok tersedia | Jumlah unit barang yang belum dipinjam |

### 2. Tech Stack

| Komponen | Teknologi |
|---|---|
| Bahasa Pemrograman | Python 3.x |
| Framework Web | Flask |
| Database | SQLite |
| Format Data | JSON |

### 3. Model Data

#### 3.1 Item
Merepresentasikan peralatan laboratorium.

| Field | Tipe | Keterangan |
|---|---|---|
| `id` | Integer (PK, auto-increment) | ID unik item |
| `name` | String | Nama item |
| `total_stock` | Integer | Total stok awal |
| `available_stock` | Integer | Stok yang tersedia untuk dipinjam |

#### 3.2 Loan
Merepresentasikan transaksi peminjaman.

| Field | Tipe | Keterangan |
|---|---|---|
| `id` | Integer (PK, auto-increment) | ID unik peminjaman |
| `student_id` | String | ID mahasiswa peminjam |
| `item_id` | Integer (FK ke `Item.id`) | Item yang dipinjam |
| `quantity` | Integer | Jumlah unit yang dipinjam |
| `status` | Enum | `BORROWED`, `RETURNED`, `CANCELLED` |
| `created_at` | Datetime/String | Waktu transaksi dibuat |

#### 3.3 Relasi
- Satu `Item` dapat dimiliki oleh banyak `Loan` (relasi satu-ke-banyak).
- `Loan.item_id` wajib merujuk pada `Item.id` yang valid.

### 4. Functional Requirements

#### FR-01 Melihat Daftar Item
Sistem harus menyediakan endpoint untuk menampilkan seluruh item beserta stok terbarunya.

#### FR-02 Menambah Item
Sistem harus menyediakan endpoint untuk menambahkan item baru dengan nama, total stok, dan stok tersedia.

#### FR-03 Membuat Peminjaman
Sistem harus menyediakan endpoint untuk membuat transaksi peminjaman. Saat peminjaman berhasil, stok tersedia item harus berkurang sesuai `quantity` dan status loan menjadi `BORROWED`.

#### FR-04 Mengembalikan Item
Sistem harus menyediakan endpoint untuk menandai peminjaman sebagai `RETURNED` dan memulihkan stok tersedia item.

#### FR-05 Melihat Riwayat Peminjaman Mahasiswa
Sistem harus menyediakan endpoint untuk menampilkan seluruh transaksi peminjaman berdasarkan `student_id`.

### 5. API Specification

#### 5.1 GET `/items`
Menampilkan seluruh item.

- **Method:** `GET`
- **Response sukses:** `200 OK`
- **Body:** array JSON berisi objek item.

Contoh respons:
```json
[
  {
    "id": 1,
    "name": "Mikroskop",
    "total_stock": 10,
    "available_stock": 8
  }
]
```

#### 5.2 POST `/items`
Menambahkan item baru.

- **Method:** `POST`
- **Request body:**
```json
{
  "name": "Mikroskop",
  "total_stock": 10,
  "available_stock": 10
}
```
- **Response sukses:** `201 Created`
- **Response gagal:** `400 Bad Request` jika payload tidak valid.

#### 5.3 POST `/loans`
Membuat transaksi peminjaman baru.

- **Method:** `POST`
- **Request body:**
```json
{
  "student_id": "MHS001",
  "item_id": 1,
  "quantity": 2
}
```
- **Response sukses:** `201 Created`
- **Response gagal:**
  - `400 Bad Request` jika `quantity` melebihi `available_stock`.
  - `404 Not Found` jika `item_id` tidak ditemukan.

#### 5.4 PUT `/loans/{id}/return`
Mengembalikan item dari transaksi peminjaman.

- **Method:** `PUT`
- **Path parameter:** `id` (ID loan)
- **Response sukses:** `200 OK`
- **Response gagal:**
  - `400 Bad Request` jika transaksi sudah berstatus `RETURNED`.
  - `404 Not Found` jika loan tidak ditemukan.

#### 5.5 GET `/loans/student/{student_id}`
Menampilkan seluruh transaksi peminjaman milik mahasiswa tertentu.

- **Method:** `GET`
- **Path parameter:** `student_id`
- **Response sukses:** `200 OK`
- **Body:** array JSON berisi objek loan.

### 6. Non-Functional Requirements

| Kode | Kebutuhan |
|---|---|
| NFR-01 | Aplikasi berjalan menggunakan Python 3.x dan Flask. |
| NFR-02 | Data disimpan secara persisten pada database SQLite. |
| NFR-03 | Seluruh komunikasi API menggunakan format JSON. |
| NFR-04 | Operasi yang mengubah stok harus atomik untuk menghindari stok negatif. |
| NFR-05 | Kode harus terstruktur dan mudah dipelihara. |
| NFR-06 | Kesalahan input harus menghasilkan kode status HTTP yang sesuai. |

### 7. Asumsi dan Batasan
- Tidak ada autentikasi dan otorisasi pada versi ini.
- `student_id` dianggap valid selama berbentuk string tidak kosong.
- Tidak ada fitur pembatalan pinjaman (`CANCELLED`) melalui endpoint khusus; status disediakan pada model data.
- Satu transaksi hanya memuat satu item.

### 8. Kriteria Penerimaan
- `POST /loans` mengembalikan `400` jika `quantity` lebih besar dari `available_stock`.
- `POST /loans` mengembalikan `404` jika `item_id` tidak ada.
- `POST /loans` mengembalikan `201` jika data valid.
- `PUT /loans/{id}/return` mengembalikan `400` jika loan sudah `RETURNED`.
- `PUT /loans/{id}/return` mengembalikan `200` jika pengembalian berhasil.
- `GET /items` selalu menampilkan stok terbaru.
