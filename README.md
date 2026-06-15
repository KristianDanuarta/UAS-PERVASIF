# Context-Aware Smart Exam 🎓

Proyek ini adalah Simulasi E-Ujian (Mini Online Exam Platform) berbasis web yang dilengkapi dengan fitur **Pervasive Computing (Smart Detector)**. Aplikasi ini sadar konteks (context-aware) dan mampu mendeteksi keberadaan (*presence*) serta perhatian (*attention*) pengguna secara *real-time*.

Dibuat untuk memenuhi Tugas UAS Mata Kuliah Komputasi Pervasif.

## 🌟 Fitur Utama (Pervasive Logic)

1. **Tab Visibility Monitor (Anti-Cheating)**
   Sistem memanfaatkan `Page Visibility API` (`document.hidden`). Jika pengguna mencoba berpindah tab atau membuka aplikasi lain (misal untuk mencari jawaban), sistem akan memunculkan peringatan (alert) dan mencatat log pelanggaran secara otomatis.

2. **User Inactivity / Idle Detector (Presence Tracker)**
   Sistem memantau event DOM (`mousemove`, `keypress`, `scroll`) di latar belakang. Jika pengguna meninggalkan laptop (tidak ada input selama **15 detik**), layar peringatan "User is Away From Keyboard" akan muncul, dan timer ujian akan **dijeda (pause)** secara otomatis.

## 🛠️ Tech Stack
- **Frontend:** Vanilla HTML5
- **Styling:** CSS3 & Tailwind CSS (via CDN)
- **Logika & Pervasive Engine:** Vanilla JavaScript

## 🚀 Cara Menjalankan Aplikasi
Karena aplikasi ini dibuat menggunakan murni HTML, CSS, dan JavaScript tanpa *backend* eksternal:
1. Unduh atau *clone* repository ini.
2. Buka folder proyek.
3. Klik dua kali pada file `index.html` untuk membukanya di browser apa saja (Chrome, Firefox, Safari).
4. Masukkan Nama/NIM dan uji coba simulasi dengan berpindah tab atau membiarkan laptop tanpa interaksi selama 15 detik.

## 🎥 Demo Video
Tautan Video Demo (Max 3 Menit): `[MASUKKAN LINK YOUTUBE/DRIVE DEMO ANDA DI SINI]`

---
*"Teknologi yang baik adalah teknologi yang menyatu dengan aktivitas kita, ia tahu kapan kita hadir dan kapan kita berpaling."*