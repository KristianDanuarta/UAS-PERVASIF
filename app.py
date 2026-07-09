import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit.components.v1 as components
import pandas as pd

# --- KONFIGURASI GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Log_Ujian").sheet1 

# --- DATABASE PESERTA DARI EXCEL ---
try:
    df_mhs = pd.read_excel("mahasiswa.xlsx", engine="openpyxl", dtype=str)
    df_mhs.columns = df_mhs.columns.str.strip().str.upper() 
    DAFTAR_MAHASISWA = dict(zip(df_mhs['NIM'], df_mhs['NAMA']))
except Exception as e:
    st.error(f"❌ Gagal memuat file mahasiswa.xlsx: {e}")
    DAFTAR_MAHASISWA = {}

st.set_page_config(page_title="Smart Exam", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

# --- CSS BASE UTAMA ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 50%, #bcccdc 100%); background-attachment: fixed; }
    .main-card { background-color: rgba(255, 255, 255, 0.85); padding: 30px; border-radius: 15px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15); backdrop-filter: blur(4px); border: 1px solid rgba(255, 255, 255, 0.18); margin-bottom: 20px; }
    .main-title { color: #102a43; text-align: center; font-family: 'Segoe UI', sans-serif; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 1. HANDLE JIKA TERJADI PELANGGARAN ---
if "violation" in st.query_params:
    alasan_blokir = st.query_params["violation"]
    nama_blokir = st.query_params.get("nama", "Tidak Dikenal")
    nim_blokir = st.query_params.get("nim", "Tidak Dikenal")
    
    if "tercatat" not in st.session_state:
        sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nama_blokir, nim_blokir, f"0 (Pelanggaran: {alasan_blokir})"])
        st.session_state.tercatat = True
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%); border: 2px solid #dc2626; padding: 40px; border-radius: 15px; text-align: center; font-family: sans-serif;'>
            <h1 style='color:#991b1b;'>Ujian Dihentikan!</h1>
            <h3 style='color:#7f1d1d;'>Sesi ujian ditutup otomatis dan dicatat ke spreadsheet.</h3>
            <p style='color:#450a0a; font-weight: bold; font-size:18px;'>Alasan: {alasan_blokir}</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Kembali ke Login", use_container_width=True):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- 2. HANDLE JIKA UJIAN SELESAI NORMAL / WAKTU HABIS ---
if "score" in st.query_params:
    skor_akhir = st.query_params["score"]
    nama_mhs = st.query_params.get("nama", "Tidak Dikenal")
    nim_mhs = st.query_params.get("nim", "Tidak Dikenal")
    
    if "tercatat" not in st.session_state:
        sheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nama_mhs, nim_mhs, skor_akhir])
        st.session_state.tercatat = True
        
    st.markdown(f"""
        <div class='main-card' style='text-align:center; font-family: sans-serif;'>
            <h1 style='color:#102a43;'>🎉 Ujian Selesai!</h1>
            <h3>Terima kasih telah mengerjakan ujian dengan jujur.</h3>
            <h2 style='color:#102a43;'>Skor Anda: {skor_akhir}</h2>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚪 Keluar Sesi", use_container_width=True):
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- 3. ALUR LOGIN DAN EXAM ELEMENT ---
st.markdown("<h1 class='main-title'>🧠 Smart Exam Pervasive</h1><br>", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.container():
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        with st.form("form_login"):
            nama_input = st.text_input("Nama Lengkap")
            nim_input = st.text_input("NIM")
            submit_login = st.form_submit_button("🚀 Mulai Ujian", use_container_width=True)
            if submit_login:
                if nama_input and nim_input:
                    if nim_input in DAFTAR_MAHASISWA and DAFTAR_MAHASISWA[nim_input].lower() == nama_input.lower():
                        st.session_state.nama = nama_input
                        st.session_state.nim = nim_input
                        st.session_state.logged_in = True
                        st.rerun()
                    else: st.error("❌ Nama atau NIM tidak terdaftar!")
                else: st.warning("Isi Nama dan NIM!")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- APLIKASI UJIAN INTEGRATED HTML & JAVASCRIPT ---
    exam_html = f"""
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #102a43; background: transparent; margin:0; padding:0; }}
        .exam-card {{ background-color: rgba(255, 255, 255, 0.9); padding: 25px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .timer-box {{ position: fixed; top: 10px; left: 50%; transform: translateX(-50%); background: #fee2e2; padding: 8px 20px; border-radius: 8px; font-weight: bold; color: #991b1b; border: 2px solid #fca5a5; z-index: 999; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
        .soal-block {{ margin-bottom: 20px; background: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }}
        .btn-submit {{ background: #102a43; color: white; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 15px; }}
        .btn-submit:hover {{ background: #244a73; }}
        input[type='radio'] {{ margin-right: 8px; transform: scale(1.1); }}
        label {{ font-size: 15px; display: inline-block; margin-bottom: 6px; cursor: pointer; }}
    </style>

    <div id="examContainer">
        <div class="timer-box" id="timerDisplay">⏱️ Waktu Ujian: 03:00</div>

        <div class="exam-card">
            <form id="formUjian">
                <div class="soal-block">
                    <p><strong>1. Format ekstensi file untuk bahasa pemrograman Python adalah...</strong></p>
                    <label><input type="radio" name="q1" value=".py"> .py</label><br>
                    <label><input type="radio" name="q1" value=".html"> .html</label><br>
                    <label><input type="radio" name="q1" value=".js"> .js</label>
                </div>

                <div class="soal-block">
                    <p><strong>2. Protokol yang digunakan untuk mengamankan pengiriman data di web adalah...</strong></p>
                    <label><input type="radio" name="q2" value="HTTPS"> HTTPS</label><br>
                    <label><input type="radio" name="q2" value="FTP"> FTP</label><br>
                    <label><input type="radio" name="q2" value="SMTP"> SMTP</label>
                </div>

                <div class="soal-block">
                    <p><strong>3. Library Python yang digunakan untuk manipulasi dan analisis data adalah...</strong></p>
                    <label><input type="radio" name="q3" value="Pandas"> Pandas</label><br>
                    <label><input type="radio" name="q3" value="Django"> Django</label><br>
                    <label><input type="radio" name="q3" value="Flask"> Flask</label>
                </div>

                <div class="soal-block">
                    <p><strong>4. Komponen komputer yang berfungsi sebagai otak utama untuk memproses data adalah...</strong></p>
                    <label><input type="radio" name="q4" value="CPU"> CPU</label><br>
                    <label><input type="radio" name="q4" value="RAM"> RAM</label><br>
                    <label><input type="radio" name="q4" value="SSD"> SSD</label>
                </div>

                <div class="soal-block">
                    <p><strong>5. Jenis database yang menggunakan struktur tabel relasional disebut...</strong></p>
                    <label><input type="radio" name="q5" value="SQL"> SQL</label><br>
                    <label><input type="radio" name="q5" value="NoSQL"> NoSQL</label><br>
                    <label><input type="radio" name="q5" value="GraphDB"> GraphDB</label>
                </div>

                <button type="submit" class="btn-submit">✅ Selesai & Kumpulkan Ujian</button>
            </form>
        </div>
    </div>

    <script>
        let totalSeconds = 180; 
        let idleTime = 0;
        let afkWarnings = 0;
        let isSelesai = false; 
        const nama = "{st.session_state.nama}";
        const nim = "{st.session_state.nim}";

        function hitungSkorSekarang() {{
            let q1 = document.querySelector('input[name="q1"]:checked');
            let q2 = document.querySelector('input[name="q2"]:checked');
            let q3 = document.querySelector('input[name="q3"]:checked');
            let q4 = document.querySelector('input[name="q4"]:checked');
            let q5 = document.querySelector('input[name="q5"]:checked');

            let skor = 0;
            if(q1 && q1.value === ".py") skor += 20;
            if(q2 && q2.value === "HTTPS") skor += 20;
            if(q3 && q3.value === "Pandas") skor += 20;
            if(q4 && q4.value === "CPU") skor += 20;
            if(q5 && q5.value === "SQL") skor += 20;
            return skor;
        }}

        function kunciDanTampilkanBlokir(tipe, detail) {{
            if (isSelesai) return;
            clearInterval(examTimer);
            isSelesai = true;

            let pesanHtml = "";
            let warnaBg = "linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%)";
            let warnaTombol = "#dc2626";

            if (tipe === "pelanggaran") {{
                pesanHtml = `
                    <h1 style="color:#991b1b; margin-top:0;">🚨 Ujian Dihentikan!</h1>
                    <h3 style="color:#7f1d1d;">Terdeteksi tindakan tidak jujur.</h3>
                    <p style="color:#450a0a; font-weight:bold; font-size:16px;">Alasan: ${{detail}}</p>
                    <p style="color:#450a0a;">Sesi ujian Anda telah dikunci otomatis.</p>
                `;
            }} else if (tipe === "waktu_habis") {{
                pesanHtml = `
                    <h1 style="color:#92400e; margin-top:0;">⏱️ Waktu Ujian Habis!</h1>
                    <h3 style="color:#78350f;">Waktu pengerjaan Anda telah selesai.</h3>
                    <p style="color:#451a03;">Sesi ujian Anda telah berakhir.</p>
                `;
                warnaBg = "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)";
                warnaTombol = "#d97706";
            }}

            document.getElementById("examContainer").innerHTML = `
                <div style="background: ${{warnaBg}}; border: 2px solid ${{warnaTombol}}; padding: 40px; border-radius: 15px; text-align: center; font-family: sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    ${{pesanHtml}}
                </div>
            `;
        }}

        // 1. Deteksi Pindah Tab Browser
        document.addEventListener("visibilitychange", () => {{
            if (document.hidden && !isSelesai) {{
                kunciDanTampilkanBlokir("pelanggaran", "Berpindah tab browser");
            }}
        }});

        // 2. Deteksi Keluar Jendela Browser / Buka Aplikasi Lain
        window.addEventListener("blur", () => {{
            setTimeout(() => {{
                if (!document.hasFocus() && !isSelesai) {{
                    kunciDanTampilkanBlokir("pelanggaran", "Meninggalkan halaman ujian / Membuka aplikasi lain");
                }}
            }}, 300);
        }});

        function resetIdle() {{ idleTime = 0; }}
        document.addEventListener("mousemove", resetIdle);
        document.addEventListener("keypress", resetIdle);
        document.addEventListener("click", resetIdle);

        // Loop Timer & AFK Tracker
        let examTimer = setInterval(() => {{
            if (isSelesai) return;

            if(totalSeconds > 0) {{
                totalSeconds--;
                let m = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
                let s = (totalSeconds % 60).toString().padStart(2, '0');
                document.getElementById("timerDisplay").innerHTML = "⏱️ Waktu Ujian: " + m + ":" + s;
            }} else {{
                kunciDanTampilkanBlokir("waktu_habis", "Waktu ujian habis");
                return;
            }}

            idleTime++;
            if (idleTime >= 25 && !document.hidden && totalSeconds > 0) {{ 
                afkWarnings++;
                idleTime = 0; 
                
                if (afkWarnings >= 3) {{
                    kunciDanTampilkanBlokir("pelanggaran", "AFK sebanyak 3 kali");
                }} else {{
                    alert("⚠️ PERINGATAN AFK! Jangan tinggalkan halaman ujian. (Peringatan " + afkWarnings + " dari 3)");
                }}
            }}
        }}, 1000);

        // Submit Normal Form Jawaban
        document.getElementById("formUjian").addEventListener("submit", (e) => {{
            e.preventDefault();
            if (isSelesai) return;

            let q1 = document.querySelector('input[name="q1"]:checked');
            let q2 = document.querySelector('input[name="q2"]:checked');
            let q3 = document.querySelector('input[name="q3"]:checked');
            let q4 = document.querySelector('input[name="q4"]:checked');
            let q5 = document.querySelector('input[name="q5"]:checked');

            if(!q1 || !q2 || !q3 || !q4 || !q5) {{
                alert("Mohon jawab semua pertanyaan terlebih dahulu!");
                return;
            }}

            isSelesai = true;
            clearInterval(examTimer);
            let skor = hitungSkorSekarang();
            
            let baseUrl = document.referrer ? document.referrer.split('?')[0] : window.location.origin;
            let targetUrl = baseUrl + "?score=" + skor + "&nama=" + encodeURIComponent(nama) + "&nim=" + encodeURIComponent(nim);
            window.open(targetUrl, '_blank');
        }});
    </script>
    """
    components.html(exam_html, height=750, scrolling=True)