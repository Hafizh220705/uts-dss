import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

# =====================================================================================
# --- KONFIGURASI APLIKASI & INISIALISASI ---
# =====================================================================================
st.set_page_config(page_title="Dashboard SPK Modern", page_icon="✨", layout="wide")

# Custom CSS yang sudah disempurnakan untuk tampilan lebih rapi
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
    }
    
    /* 1. Menambah jarak antar tombol tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; /* Jarak diperlebar dari 2px menjadi 8px */
    }

    /* 2. Style untuk tab yang TIDAK dipilih */
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: var(--secondary-background-color);
        border-radius: 4px 4px 0px 0px;
        /* 3. Menambah border halus dan padding horizontal */
        border: 1px solid var(--gray-300);
        padding: 10px 25px; /* Padding horizontal diperbesar */
        transition: background-color 0.3s ease;
    }

    /* 4. Style untuk tab yang SEDANG dipilih */
    .stTabs [aria-selected="true"] {
        background-color: var(--background-color);
        /* Menghilangkan border bawah agar terlihat menyatu dengan konten */
        border-bottom: 1px solid var(--background-color); 
    }
</style>""", unsafe_allow_html=True)


# Inisialisasi session state (jika belum ada)
def init_session_state():
    # State untuk mode Direct Input
    if 'criteria_list' not in st.session_state:
        st.session_state.criteria_list = []
    if 'alternatives_list' not in st.session_state:
        st.session_state.alternatives_list = []
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None

    # State untuk mode AHP
    if 'ahp_criteria_list' not in st.session_state:
        st.session_state.ahp_criteria_list = []
    if 'ahp_matrix_df' not in st.session_state:
        st.session_state.ahp_matrix_df = None
    if 'ahp_weights_results' not in st.session_state:
        st.session_state.ahp_weights_results = None
    if 'ahp_alternatives_list' not in st.session_state:
        st.session_state.ahp_alternatives_list = []
    if 'ahp_results_df' not in st.session_state:
        st.session_state.ahp_results_df = None

init_session_state()

# Alamat API Backend
API_URL_CALCULATE = "[http://127.0.0.1:8000/calculate](http://127.0.0.1:8000/calculate)"
API_URL_AHP = "[http://127.0.0.1:8000/calculate-ahp-weights](http://127.0.0.1:8000/calculate-ahp-weights)"


# =====================================================================================
# --- TAMPILAN UTAMA ---
# =====================================================================================
st.title("✨ Dashboard Sistem Pendukung Keputusan")
st.write("Sebuah antarmuka yang modern dan intuitif untuk membantu Anda mengambil keputusan dengan berbagai metode SPK.")

# Pemilihan Mode Input
input_mode = st.radio(
    "Pilih Metode Input Bobot Kriteria:",
    ("Input Bobot Langsung (SAW, WP, TOPSIS)", "Perbandingan Berpasangan (AHP)"),
    horizontal=True
)
st.markdown("---")

# =====================================================================================
# --- MODE 1: INPUT BOBOT LANGSUNG (SAW, WP, TOPSIS) ---
# =====================================================================================
if input_mode == "Input Bobot Langsung (SAW, WP, TOPSIS)":
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "① Kriteria & Bobot", 
        "② Alternatif", 
        "③ Penilaian", 
        "④ Hasil Perangkingan"
    ])

    # --- TAB 1: KRITERIA & BOBOT ---
    with tab1:
        st.header("⚖️ Pengaturan Kriteria & Bobot", divider="rainbow")
        st.info("Tambahkan kriteria yang akan digunakan untuk penilaian. Pastikan total bobot dari semua kriteria adalah **1.0**.")
        
        with st.form("criteria_form"):
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                criteria_name = st.text_input("Nama Kriteria", placeholder="Contoh: Kualitas Kamera")
            with col2:
                criteria_weight = st.number_input("Bobot", min_value=0.0, max_value=1.0, step=0.05, format="%.2f")
            with col3:
                criteria_type = st.selectbox("Tipe", ["Benefit", "Cost"])
            
            submitted = st.form_submit_button("➕ Tambah Kriteria")
            if submitted and criteria_name:
                st.session_state.criteria_list.append({
                    "Kriteria": criteria_name, "Bobot": criteria_weight, "Tipe": criteria_type
                })

        st.markdown("---")
        
        # Tampilkan daftar kriteria yang sudah ditambahkan
        if st.session_state.criteria_list:
            st.subheader("Daftar Kriteria Saat Ini")
            criteria_df = pd.DataFrame(st.session_state.criteria_list)
            st.dataframe(criteria_df, use_container_width=True)
            
            total_weight = criteria_df['Bobot'].sum()
            st.metric(label="Total Bobot", value=f"{total_weight:.2f}", delta="Harus Tepat 1.0" if not np.isclose(total_weight, 1.0) else "✅ Sesuai")
            
            if st.button("🗑️ Hapus Kriteria Terakhir"):
                st.session_state.criteria_list.pop()
                st.rerun()

    # --- TAB 2: ALTERNATIF ---
    with tab2:
        st.header("🎯 Pengaturan Alternatif", divider="rainbow")
        st.info("Masukkan semua alternatif yang akan dinilai. Pisahkan setiap alternatif dengan baris baru.")
        
        alternatives_input = st.text_area("Daftar Alternatif:", "Laptop A\nLaptop B\nLaptop C", height=150)
        st.session_state.alternatives_list = [name.strip() for name in alternatives_input.split('\n') if name.strip()]
        
        if st.session_state.alternatives_list:
            st.success(f"{len(st.session_state.alternatives_list)} alternatif berhasil ditambahkan.")
            st.write(st.session_state.alternatives_list)

    # --- TAB 3: PENILAIAN ---
    with tab3:
        st.header("📝 Matriks Penilaian", divider="rainbow")
        
        if not st.session_state.criteria_list or not st.session_state.alternatives_list:
            st.warning("Harap lengkapi Kriteria pada Tab ① dan Alternatif pada Tab ② terlebih dahulu.")
        else:
            st.info("Silakan isi nilai untuk setiap alternatif berdasarkan kriteria yang ada.")
            criteria_df = pd.DataFrame(st.session_state.criteria_list)
            criteria_names = criteria_df['Kriteria'].tolist()
            
            values_df = pd.DataFrame(1.0, columns=criteria_names, index=st.session_state.alternatives_list)
            edited_values_df = st.data_editor(values_df, use_container_width=True)
            
            st.markdown("---")
            col_meth, col_btn = st.columns([3,1])
            with col_meth:
                method = st.selectbox("Pilih Metode Perangkingan:", ("SAW", "WP", "TOPSIS"))
            with col_btn:
                st.write("") # Spacer
                st.write("") # Spacer
                calculate_button = st.button("🚀 Hitung Peringkat", type="primary")

            if calculate_button:
                total_weight = criteria_df['Bobot'].sum()
                if not np.isclose(total_weight, 1.0):
                    st.error("Total Bobot Kriteria harus 1.0. Silakan perbaiki di Tab ①.")
                else:
                    with st.spinner("Mengirim data dan menghitung..."):
                        payload = {
                            "method": method.lower(),
                            "criteria": st.session_state.criteria_list,
                            "alternatives": edited_values_df.reset_index().rename(columns={'index': 'alternatif'}).to_dict(orient='records')
                        }
                        try:
                            response = requests.post(API_URL_CALCULATE, data=json.dumps(payload))
                            if response.status_code == 200:
                                st.session_state.results_df = pd.DataFrame(response.json().get("result", []))
                                st.success("Perhitungan berhasil! Hasil dapat dilihat di Tab ④.")
                            else:
                                st.error(f"Error dari backend: {response.text}")
                        except requests.exceptions.ConnectionError as e:
                            st.error(f"Gagal terhubung ke backend. Pastikan backend sudah berjalan. Detail: {e}")

    # --- TAB 4: HASIL ---
    with tab4:
        st.header("🏆 Hasil Akhir Perangkingan", divider="rainbow")
        if st.session_state.results_df is not None:
            st.dataframe(st.session_state.results_df, use_container_width=True)
        else:
            st.info("Hasil akan ditampilkan di sini setelah proses perhitungan pada Tab ③ selesai.")

# =====================================================================================
# --- MODE 2: INPUT AHP ---
# =====================================================================================
elif input_mode == "Perbandingan Berpasangan (AHP)":
    
    tab_ahp1, tab_ahp2, tab_ahp3, tab_ahp4 = st.tabs([
        "① Kriteria AHP", 
        "② Matriks Perbandingan", 
        "③ Alternatif & Penilaian", 
        "④ Hasil Perangkingan AHP"
    ])

    with tab_ahp1:
        st.header("⚖️ Pengaturan Kriteria (AHP)", divider="rainbow")
        st.info("Masukkan kriteria yang akan dibandingkan satu sama lain.")
        criteria_input_ahp = st.text_area("Daftar Kriteria:", "Harga\nRAM\nStorage\nBaterai", height=150)
        st.session_state.ahp_criteria_list = [c.strip() for c in criteria_input_ahp.split('\n') if c.strip()]
        
        if st.session_state.ahp_criteria_list:
            st.success(f"{len(st.session_state.ahp_criteria_list)} kriteria berhasil ditambahkan.")

    with tab_ahp2:
        st.header("🔢 Matriks Perbandingan Kriteria", divider="rainbow")
        if len(st.session_state.ahp_criteria_list) < 2:
            st.warning("Harap masukkan minimal 2 kriteria pada Tab ①.")
        else:
            st.info("""
            Isi matriks sesuai tingkat kepentingan relatif antar kriteria.
            - **1**: Sama penting
            - **3**: Sedikit lebih penting
            - **5**: Jelas lebih penting
            - **7**: Sangat jelas lebih penting
            - **9**: Mutlak lebih penting
            Gunakan nilai kebalikan (contoh: 1/3, 1/5) untuk perbandingan sebaliknya.
            """)
            
            matrix_df = pd.DataFrame(
                np.identity(len(st.session_state.ahp_criteria_list)),
                index=st.session_state.ahp_criteria_list,
                columns=st.session_state.ahp_criteria_list
            )
            st.session_state.ahp_matrix_df = st.data_editor(matrix_df, use_container_width=True)

            if st.button("⚖️ Hitung Bobot & Konsistensi", type="primary"):
                with st.spinner("Menghitung..."):
                    try:
                        payload = {"comparison_matrix": st.session_state.ahp_matrix_df.values.tolist()}
                        response = requests.post(API_URL_AHP, json=payload)
                        if response.status_code == 200:
                            st.session_state.ahp_weights_results = response.json()
                        else:
                            st.error(f"Error dari backend: {response.text}")
                    except requests.exceptions.ConnectionError as e:
                        st.error(f"Gagal terhubung ke backend. Detail: {e}")

        if st.session_state.ahp_weights_results:
            st.markdown("---")
            st.subheader("📊 Hasil Perhitungan Bobot")
            results = st.session_state.ahp_weights_results
            
            col_w, col_cr = st.columns(2)
            with col_w:
                weights_df = pd.DataFrame({
                    'Kriteria': st.session_state.ahp_criteria_list,
                    'Bobot': results.get("weights")
                })
                st.dataframe(weights_df.style.format({'Bobot': "{:.4f}"}))
            
            with col_cr:
                cr_value = results.get("consistency_ratio")
                status = results.get("consistency_status")
                st.metric("Consistency Ratio (CR)", f"{cr_value:.4f}")
                if status == "Konsisten":
                    st.success(f"**Status: {status}** (CR <= 0.1)")
                else:
                    st.error(f"**Status: {status}** (CR > 0.1). Penilaian tidak konsisten, harap perbaiki matriks.")
    
    with tab_ahp3:
        st.header("📝 Penilaian Alternatif (AHP)", divider="rainbow")
        results = st.session_state.ahp_weights_results
        if not results or results.get("consistency_status") != "Konsisten":
            st.warning("Harap hitung bobot kriteria yang konsisten pada Tab ② terlebih dahulu.")
        else:
            st.info("Bobot kriteria yang konsisten telah didapat. Sekarang, masukkan alternatif dan nilainya.")
            ahp_alternatives_input = st.text_area("Daftar Alternatif:", "Alternatif X\nAlternatif Y\nAlternatif Z", height=150)
            st.session_state.ahp_alternatives_list = [name.strip() for name in ahp_alternatives_input.split('\n') if name.strip()]

            if st.session_state.ahp_alternatives_list:
                ahp_values_df = pd.DataFrame(1.0, columns=st.session_state.ahp_criteria_list, index=st.session_state.ahp_alternatives_list)
                edited_ahp_values_df = st.data_editor(ahp_values_df, use_container_width=True)

                if st.button("🚀 Hitung Peringkat AHP", type="primary"):
                    with st.spinner("Mengirim data dan menghitung..."):
                        ahp_criteria_final_df = pd.DataFrame({
                            'Kriteria': st.session_state.ahp_criteria_list,
                            'Bobot': results.get("weights"),
                            'Tipe': 'Benefit' 
                        })
                        payload = {
                            "method": "ahp",
                            "criteria": ahp_criteria_final_df.to_dict(orient='records'),
                            "alternatives": edited_ahp_values_df.reset_index().rename(columns={'index': 'alternatif'}).to_dict(orient='records')
                        }
                        try:
                            response = requests.post(API_URL_CALCULATE, data=json.dumps(payload))
                            if response.status_code == 200:
                                st.session_state.ahp_results_df = pd.DataFrame(response.json().get("result", []))
                                st.success("Perhitungan berhasil! Hasil dapat dilihat di Tab ④.")
                            else:
                                st.error(f"Error dari backend: {response.text}")
                        except requests.exceptions.ConnectionError as e:
                            st.error(f"Gagal terhubung ke backend. Detail: {e}")
    
    with tab_ahp4:
        st.header("🏆 Hasil Akhir Perangkingan (AHP)", divider="rainbow")
        if st.session_state.ahp_results_df is not None:
            st.dataframe(st.session_state.ahp_results_df, use_container_width=True)
        else:
            st.info("Hasil akan ditampilkan di sini setelah proses perhitungan pada Tab ③ selesai.")