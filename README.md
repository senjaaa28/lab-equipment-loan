# Lab Equipment Loan System (Flask + SQLite)

## Prasyarat
- Python 3.10+

## Instalasi
1. Buat dan aktifkan virtual environment:
   - Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
   - Linux/MacOS: `python -m venv .venv; source .venv/bin/activate`
2. Install dependency: `pip install -r requirements.txt`

## Menjalankan Aplikasi
1. Inisialisasi database: `flask --app run init-db`
2. Jalankan aplikasi: `python run.py` (http://127.0.0.1:5000)

## Testing
- `pytest -q`
