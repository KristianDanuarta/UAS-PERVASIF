# 🎓 Smart Exam Pervasive

Aplikasi ujian online berbasis **Streamlit** yang dilengkapi dengan fitur anti-kecurangan (proctoring) menggunakan JavaScript terintegrasi dan pencatatan log otomatis ke **Google Sheets**.

---

## 🚀 Fitur Utama
* **Sistem Login Validasi**: Memverifikasi NIM dan Nama mahasiswa berdasarkan data dari file Excel (`mahasiswa.xlsx`).
* **Anti-Cheat Jendela & Tab Browser**: Mengunci ujian otomatis jika mahasiswa berpindah tab atau membuka aplikasi lain.
* **Deteksi AFK (Away From Keyboard)**: Memberikan peringatan jika tidak ada aktivitas selama 25 detik (maksimal 3 kali sebelum dikunci).
* **Timer Otomatis**: Batas waktu pengerjaan selama 3 menit (180 detik).
* **Integrasi Google Sheets**: Menyimpan hasil skor akhir atau alasan pelanggaran secara real-time.

---

## 📦 Prasyarat Instalasi

Pastikan Anda sudah menginstal Python (versi 3.8 atau yang lebih baru). Instal semua library yang dibutuhkan dengan perintah berikut:

```bash
pip install streamlit gspread oauth2client pandas openpyxl
🛠️ Persiapan File & Konfigurasi
Sebelum menjalankan aplikasi, pastikan file-file berikut berada dalam satu direktori yang sama dengan app.py:

credentials.json: File akun layanan (Service Account) dari Google Cloud Console untuk akses Google Sheets API. Ensure Google Sheet Anda sudah di-share ke email yang ada di dalam file json ini.

mahasiswa.xlsx: File database mahasiswa peserta ujian. Harus memiliki kolom NIM dan NAMA.

Google Sheet (Log_Ujian): Buat spreadsheet di Google Drive dengan nama Log_Ujian untuk menampung data log masuk/skor mahasiswa.

💻 Cara Menjalankan Aplikasi
Jalankan perintah berikut di terminal Anda:

Bash
streamlit run app.py