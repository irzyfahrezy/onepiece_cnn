import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- 1. DATABASE KARAKTER ---
class_names = ['Ace', 'Akainu', 'Brook', 'Chopper', 'Crocodile', 'Franky', 
               'Jinbei', 'Kurohige', 'Law', 'Luffy', 'Mihawk', 'Nami', 
               'Rayleigh', 'Robin', 'Sanji', 'Shanks', 'Usopp', 'Zoro']

character_info = {
    "Ace": {
        "Nama": "Portgas D. Ace",
        "Role": "Komandan Divisi 2",
        "Afiliasi": "Whitebeard Pirates",
        "Status": "Deceased",
        "Umur": "20",
        "Tinggi": "185 cm",
        "Ras": "Manusia",
        "Asal": "East Blue",
        "Devil Fruit": "Mera Mera no Mi",
        "Haki": "Haoshoku, Busoshoku",
        "Fighting Style": "Fire-based combat",
        "Bounty": "550,000,000",
        "First Appearance": "Episode 91",
        "Deskripsi": "Ace adalah anak biologis Gol D. Roger yang menyembunyikan identitasnya dan memilih hidup sebagai bajak laut di bawah Whitebeard. Ia menjadi komandan divisi kedua, menunjukkan kekuatan dan kepemimpinan tinggi. Dengan Mera Mera no Mi, ia mengontrol api secara destruktif. Secara psikologis, Ace berjuang dengan eksistensi dirinya—apakah ia pantas hidup sebagai anak Raja Bajak Laut. Loyalitasnya terhadap Whitebeard dan saudara-saudaranya menjadi inti karakternya, hingga akhirnya ia mati demi melindungi Luffy."
    },
    "Akainu": {
        "Nama": "Sakazuki",
        "Role": "Fleet Admiral",
        "Afiliasi": "Marines",
        "Status": "Alive",
        "Umur": "55",
        "Tinggi": "306 cm",
        "Ras": "Manusia",
        "Asal": "North Blue",
        "Devil Fruit": "Magu Magu no Mi",
        "Haki": "Busoshoku, Kenbunshoku",
        "Fighting Style": "Magma-based combat",
        "Bounty": "-",
        "First Appearance": "Episode 278",
        "Deskripsi": "Akainu adalah simbol “Absolute Justice” dalam Angkatan Laut. Ia percaya bahwa kejahatan harus dihancurkan tanpa kompromi, bahkan jika itu berarti pengorbanan besar. Dengan kekuatan magma dari Magu Magu no Mi, ia memiliki daya hancur ekstrem. Ia bukan sekadar kuat, tapi juga ideologis—keputusan-keputusannya sering brutal namun konsisten. Ia adalah antagonis sistemik, bukan pribadi."
    },
    "Brook": {
        "Nama": "Brook",
        "Role": "Musician",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "90",
        "Tinggi": "277 cm",
        "Ras": "Manusia (Revived)",
        "Asal": "West Blue",
        "Devil Fruit": "Yomi Yomi no Mi",
        "Haki": "None",
        "Fighting Style": "Soul-based swordsmanship",
        "Bounty": "383,000,000",
        "First Appearance": "Episode 337",
        "Deskripsi": "Brook adalah mantan anggota Rumbar Pirates yang hidup kembali berkat Yomi Yomi no Mi. Sebagai skeleton, ia menguasai kekuatan jiwa, termasuk membekukan lawan dengan “cold soul”. Ia membawa trauma kehilangan seluruh krunya, tapi memilih hidup dengan humor dan musik. Perannya di kru bukan hanya musisi, tapi juga penghubung emosional."
    },
    "Chopper": {
        "Nama": "Tony Tony Chopper",
        "Role": "Doctor",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "17",
        "Tinggi": "90 cm",
        "Ras": "Rusa",
        "Asal": "Drum Island",
        "Devil Fruit": "Hito Hito no Mi",
        "Haki": "None",
        "Fighting Style": "Zoan transformation",
        "Bounty": "1,000",
        "First Appearance": "Episode 81",
        "Deskripsi": "Chopper adalah rusa yang memperoleh kecerdasan manusia melalui Hito Hito no Mi. Ia berkembang dari makhluk yang ditolak menjadi dokter andalan kru. Ia memiliki berbagai transformasi (Monster Point, dll) yang membuatnya fleksibel dalam pertempuran. Karakternya menonjol karena empati tinggi dan konflik antara identitas “monster” vs “manusia”."
    },
    "Crocodile": {
        "Nama": "Sir Crocodile",
        "Role": "Former Shichibukai",
        "Afiliasi": "Cross Guild",
        "Status": "Alive",
        "Umur": "46",
        "Tinggi": "253 cm",
        "Ras": "Manusia",
        "Asal": "Grand Line",
        "Devil Fruit": "Suna Suna no Mi",
        "Haki": "Unknown",
        "Fighting Style": "Sand manipulation",
        "Bounty": "1,965,000,000",
        "First Appearance": "Episode 76",
        "Deskripsi": "Crocodile adalah mantan Shichibukai dengan pola pikir strategis dan manipulatif. Ia tidak mengandalkan kekuatan saja, tapi juga kontrol politik dan organisasi (Baroque Works). Dengan Suna Suna no Mi, ia bisa mengontrol pasir dan lingkungan. Ia mencerminkan tipe villain yang rasional dan oportunistik, bukan emosional."
    },
    "Franky": {
        "Nama": "Franky",
        "Role": "Shipwright",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "36",
        "Tinggi": "240 cm",
        "Ras": "Cyborg",
        "Asal": "South Blue",
        "Devil Fruit": "None",
        "Haki": "None",
        "Fighting Style": "Cyborg weapons",
        "Bounty": "394,000,000",
        "First Appearance": "Episode 233",
        "Deskripsi": "Franky adalah cyborg yang membangun dirinya sendiri setelah kecelakaan. Ia adalah shipwright jenius yang menciptakan Thousand Sunny. Dalam pertarungan, ia mengandalkan teknologi dan senjata berat. Karakternya mencerminkan kreativitas, kebebasan berekspresi, dan tanggung jawab terhadap ciptaannya."
    },
    "Jinbei": {
        "Nama": "Jinbei",
        "Role": "Helmsman",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "46",
        "Tinggi": "301 cm",
        "Ras": "Fish-Man",
        "Asal": "Fish-Man Island",
        "Devil Fruit": "None",
        "Haki": "Busoshoku, Kenbunshoku",
        "Fighting Style": "Fish-Man Karate",
        "Bounty": "1,100,000,000",
        "First Appearance": "Episode 430",
        "Deskripsi": "Jinbei adalah Fish-Man yang menguasai Fish-Man Karate dan memiliki pengalaman luas sebagai mantan Shichibukai. Ia membawa tema diskriminasi ras dan perjuangan kesetaraan. Secara mental, ia sangat stabil dan bijaksana, sering menjadi penyeimbang dalam kru. Loyalitas dan kehormatan adalah nilai utamanya."
    },
    "Kurohige": {
        "Nama": "Marshall D. Teach",
        "Role": "Yonko",
        "Afiliasi": "Blackbeard Pirates",
        "Status": "Alive",
        "Umur": "40",
        "Tinggi": "344 cm",
        "Ras": "Manusia",
        "Asal": "Grand Line",
        "Devil Fruit": "Yami Yami no Mi, Gura Gura no Mi",
        "Haki": "Busoshoku, Kenbunshoku",
        "Fighting Style": "Darkness + quake",
        "Bounty": "3,996,000,000",
        "First Appearance": "Episode 146",
        "Deskripsi": "Teach adalah karakter yang mewakili ambisi tanpa batas. Ia sabar, manipulatif, dan oportunistik—menunggu momen yang tepat untuk bergerak. Dengan dua Devil Fruit (Yami dan Gura), ia menjadi ancaman unik. Ia bukan hanya kuat, tapi juga simbol chaos dalam dunia One Piece."
    },
    "Law": {
        "Nama": "Trafalgar D. Water Law",
        "Role": "Captain",
        "Afiliasi": "Heart Pirates",
        "Status": "Alive",
        "Umur": "26",
        "Tinggi": "191 cm",
        "Ras": "Manusia",
        "Asal": "North Blue",
        "Devil Fruit": "Ope Ope no Mi",
        "Haki": "Busoshoku, Kenbunshoku",
        "Fighting Style": "Surgical combat",
        "Bounty": "3,000,000,000",
        "First Appearance": "Episode 392",
        "Deskripsi": "Law adalah dokter sekaligus kapten yang sangat rasional. Ope Ope no Mi memberinya kemampuan manipulasi ruang seperti ruang operasi. Ia memiliki masa lalu tragis dan motivasi balas dendam terhadap Doflamingo. Ia berkembang dari individu dingin menjadi sekutu strategis Luffy."
    },
    "Luffy": {
        "Nama": "Monkey D. Luffy",
        "Role": "Captain",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "19",
        "Tinggi": "174 cm",
        "Ras": "Manusia",
        "Asal": "East Blue",
        "Devil Fruit": "Hito Hito no Mi, Model: Nika",
        "Haki": "Haoshoku, Busoshoku, Kenbunshoku",
        "Fighting Style": "Rubber-based combat",
        "Bounty": "3,000,000,000",
        "First Appearance": "Episode 1",
        "Deskripsi": "Luffy adalah pusat narasi One Piece. Ia memiliki sifat bebas, tidak konvensional, dan sangat percaya pada instingnya. Dengan kekuatan Nika (Gear 5), ia menjadi simbol kebebasan. Kekuatan terbesarnya bukan hanya fisik, tapi kemampuan menginspirasi dan menyatukan orang lain."
    },
    "Mihawk": {
        "Nama": "Dracule Mihawk",
        "Role": "Swordsman",
        "Afiliasi": "Cross Guild",
        "Status": "Alive",
        "Umur": "43",
        "Tinggi": "198 cm",
        "Ras": "Manusia",
        "Asal": "Grand Line",
        "Devil Fruit": "None",
        "Haki": "Busoshoku, Kenbunshoku",
        "Fighting Style": "Swordsmanship",
        "Bounty": "3,590,000,000",
        "First Appearance": "Episode 23",
        "Deskripsi": "Mihawk adalah pendekar pedang terkuat di dunia. Ia hidup dengan standar tinggi terhadap kekuatan dan teknik. Tidak banyak bicara, tapi setiap tindakannya presisi. Ia menjadi benchmark utama bagi Zoro dan representasi puncak swordsmanship."
    },
    "Nami": {
        "Nama": "Nami",
        "Role": "Navigator",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "20",
        "Tinggi": "170 cm",
        "Ras": "Manusia",
        "Asal": "East Blue",
        "Devil Fruit": "None",
        "Haki": "None",
        "Fighting Style": "Weather manipulation",
        "Bounty": "366,000,000",
        "First Appearance": "Episode 1",
        "Deskripsi": "Nami adalah navigator dengan kecerdasan tinggi dalam membaca cuaca dan navigasi laut. Masa lalunya di bawah Arlong membentuk obsesinya terhadap uang dan kebebasan. Ia bukan petarung utama, tapi kontribusinya vital untuk kelangsungan kru."
    },
    "Rayleigh": {
        "Nama": "Silvers Rayleigh",
        "Role": "Former First Mate",
        "Afiliasi": "Roger Pirates",
        "Status": "Alive",
        "Umur": "78",
        "Tinggi": "188 cm",
        "Ras": "Manusia",
        "Asal": "Grand Line",
        "Devil Fruit": "None",
        "Haki": "Haoshoku, Busoshoku, Kenbunshoku",
        "Fighting Style": "Advanced Haki combat",
        "Bounty": "Unknown",
        "First Appearance": "Episode 8",
        "Deskripsi": "Rayleigh adalah mantan tangan kanan Gol D. Roger. Ia menguasai semua jenis Haki dan menjadi mentor Luffy. Ia merepresentasikan generasi lama yang memahami rahasia dunia. Meskipun pensiun, kekuatannya tetap di level atas."
    },
    "Robin": {
        "Nama": "Nico Robin",
        "Role": "Archaeologist",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "30",
        "Tinggi": "188 cm",
        "Ras": "Manusia",
        "Asal": "Ohara",
        "Devil Fruit": "Hana Hana no Mi",
        "Haki": "None",
        "Fighting Style": "Limb replication",
        "Bounty": "930,000,000",
        "First Appearance": "Episode 67",
        "Deskripsi": "Robin adalah arkeolog yang mampu membaca Poneglyph, menjadikannya target Pemerintah Dunia. Ia memiliki masa lalu penuh pengkhianatan dan kesepian. Kemampuan Hana Hana no Mi membuatnya fleksibel dalam pertarungan. Ia adalah kunci sejarah dunia."
    },
    "Sanji": {
        "Nama": "Vinsmoke Sanji",
        "Role": "Cook",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "21",
        "Tinggi": "180 cm",
        "Ras": "Manusia (Modified)",
        "Asal": "North Blue",
        "Devil Fruit": "None",
        "Haki": "Busoshoku, Kenbunshoku",
        "Fighting Style": "Kick-based combat",
        "Bounty": "1,032,000,000",
        "First Appearance": "Episode 20",
        "Deskripsi": "Sanji adalah koki kru dengan prinsip kuat, terutama soal menghormati wanita. Ia bertarung menggunakan kaki, menjaga tangannya untuk memasak. Setelah arc Whole Cake Island, terungkap bahwa ia adalah hasil eksperimen genetik, meningkatkan kekuatan fisiknya."
    },
    "Shanks": {
        "Nama": "Red-Haired Shanks",
        "Role": "Yonko",
        "Afiliasi": "Red Hair Pirates",
        "Status": "Alive",
        "Umur": "39",
        "Tinggi": "199 cm",
        "Ras": "Manusia",
        "Asal": "West Blue",
        "Devil Fruit": "None",
        "Haki": "Haoshoku, Busoshoku, Kenbunshoku",
        "Fighting Style": "Haki mastery",
        "Bounty": "4,048,900,000",
        "First Appearance": "Episode 4",
        "Deskripsi": "Shanks adalah Yonko dengan pengaruh besar. Ia tidak memiliki Devil Fruit, tapi Haki-nya luar biasa. Ia adalah figur mentor bagi Luffy dan penjaga keseimbangan dunia. Pendekatannya lebih diplomatis dibanding Yonko lain."
    },
    "Usopp": {
        "Nama": "Usopp",
        "Role": "Sniper",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "19",
        "Tinggi": "176 cm",
        "Ras": "Manusia",
        "Asal": "East Blue",
        "Devil Fruit": "None",
        "Haki": "Kenbunshoku",
        "Fighting Style": "Sniping",
        "Bounty": "500,000,000",
        "First Appearance": "Episode 9",
        "Deskripsi": "Usopp adalah sniper yang berkembang dari pengecut menjadi pejuang. Ia mengandalkan kreativitas, strategi, dan alat tempur. Ia juga memiliki kemampuan observasi (Kenbunshoku Haki). Karakternya realistis—takut, tapi tetap bertindak."
    },
    "Zoro": {
        "Nama": "Roronoa Zoro",
        "Role": "Swordsman",
        "Afiliasi": "Straw Hat Pirates",
        "Status": "Alive",
        "Umur": "21",
        "Tinggi": "181 cm",
        "Ras": "Manusia",
        "Asal": "East Blue",
        "Devil Fruit": "None",
        "Haki": "Haoshoku, Busoshoku, Kenbunshoku",
        "Fighting Style": "Three-sword style",
        "Bounty": "1,111,000,000",
        "First Appearance": "Episode 2",
        "Deskripsi": "Zoro adalah pendekar pedang dengan gaya tiga pedang. Ia memiliki disiplin tinggi dan dedikasi ekstrem untuk menjadi yang terkuat. Loyalitasnya terhadap Luffy tidak tergoyahkan. Ia juga memiliki Haoshoku Haki, menandakan potensi besar sebagai pemimpin."
    }
}

# --- 2. KONFIGURASI TAMPILAN WEB & SIDEBAR ---
st.set_page_config(page_title="One Piece AI", page_icon="🏴‍☠️")
st.title("One Piece Character Classifier 🏴‍☠️")
st.write("Upload foto karakter One Piece untuk diidentifikasi oleh AI!")

with st.sidebar:
    st.header("Daftar Karakter")
    st.write("Model ini hanya dapat mengenali 18 karakter berikut:")
    st.write(", ".join(class_names))
    st.markdown("---")
    st.info("Sistem dilengkapi fitur *Confidence Threshold* untuk menyaring karakter di luar dataset.")

# --- 3. LOAD MODEL AI ---
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('model_onepiece.keras')

model = load_my_model()

# --- 4. UPLOAD & PREPROCESSING GAMBAR ---
file_terunggah = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png"])

if file_terunggah is not None:
    image = Image.open(file_terunggah)
    st.image(image, caption='Gambar yang diunggah', use_container_width=True)
    
    img = image.resize((224, 224))
    img_array = np.array(img.convert('RGB'))
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    # --- 5. LOGIKA PREDIKSI ---
    if st.button("Identifikasi Karakter"):
        prediksi = model.predict(img_array)
        confidence_scores = prediksi[0]
        
        idx_tertinggi = np.argmax(confidence_scores)
        hasil = class_names[idx_tertinggi]
        persentase = confidence_scores[idx_tertinggi] * 100
        
        threshold = 60.0 # Ambang batas keamanan
        
        if persentase < threshold:
            # Jika skor di bawah 60%
            st.warning("⚠️ **Gambar tidak dikenali dengan pasti.**")
            st.toast("Model ragu dengan hasilnya", icon="⚠️")
            top_2_indices = confidence_scores.argsort()[-2:][::-1]
            saran1 = class_names[top_2_indices[0]]
            saran2 = class_names[top_2_indices[1]]
            
            st.write(f"**Did You Mean?** **{saran1}** or **{saran2}**?")
            
        else:
            # Jika skor di atas 60%
            st.balloons()
            
            st.toast(f"{hasil} terdeteksi!", icon="🏴‍☠️")
            st.success(f"### Hasil Klasifikasi: {hasil}")
            st.write(f"**Tingkat Kepercayaan:** {persentase:.2f}%")
            
            st.divider()

            # Ambil data karakter
            info = character_info.get(hasil, {})
            
            # Baris 1: Informasi Dasar
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"👤 **Nama:** {info.get('Nama', hasil)}")
                st.write(f"🎭 **Role:** {info.get('Role', '-')}")
                st.write(f"🏴‍☠️ **Afiliasi:** {info.get('Afiliasi', '-')}")
            with col2:
                st.write(f"📊 **Status:** {info.get('Status', '-')}")
                st.write(f"💰 **Bounty:** {info.get('Bounty', '-')}")
            
            st.divider()

            # BARIS 2: PROFIL DASAR
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📅 **Umur:** {info.get('Umur', '-')}")
                st.write(f"📏 **Tinggi:** {info.get('Tinggi', '-')}")
            with col2:
                st.write(f"🧬 **Ras:** {info.get('Ras', '-')}")
                st.write(f"🌍 **Asal:** {info.get('Asal', '-')}")
            
            st.divider()

            # BARIS 3: KEKUATAN
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"🍇 **Devil Fruit:** {info.get('Devil Fruit', '-')}")
                st.write(f"⚔️ **Haki:** {info.get('Haki', '-')}")
            with col2:
                st.write(f"🥊 **Fighting Style:** {info.get('Fighting Style', '-')}")
            
            st.divider()

            # BARIS 4: NARATIF
            st.write(f"📺 **First Appearance:** {info.get('First Appearance', '-')}")
            
            st.markdown("---")

            # DESKRIPSI
            st.write("### 📜 Deskripsi Karakter")
            st.info(info.get('Deskripsi', 'Deskripsi tidak tersedia.'))