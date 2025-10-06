import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

# =====================================================================================
# KONFIGURASI APLIKASI
# =====================================================================================
st.set_page_config(
    page_title="Decision Support System", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================================
# CUSTOM CSS - PREMIUM DESIGN
# =====================================================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px;
    }
    
    /* Header Styling */
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
    }
    
    h2 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
    }
    
    /* Hero Section */
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.25rem;
        font-weight: 400;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Card Design */
    .css-1r6slb0, .css-12oz5g7 {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Radio Buttons - Modern Toggle Style */
    .stRadio > div {
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .stRadio > div > label {
        background: transparent !important;
        padding: 0.875rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
    }

    /* Ini adalah bagian kunci yang diperbaiki */
    .stRadio > div > label > div p {
        color: #1e293b !important; 
    }

    .stRadio > div > label:hover {
        background: #f8fafc !important;
    }

    .stRadio > div > label:hover p {
        color: #667eea !important;
    }

    .stRadio > div > label[data-baseweb="radio"] > div:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Radio button text visibility fix */
    .stRadio label span {
        color: #1e293b !important;
    }
    
    /* Tabs - Premium Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        padding: 0;
    }

    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 1rem 1.75rem;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 12px;
        border: 2px solid transparent;
        font-weight: 600;
        color: #64748b;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.9);
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Info/Warning/Success Boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 1.25rem;
        font-weight: 500;
    }
    
    .stAlert > div {
        padding-left: 1rem;
    }
    
    /* DataFrames */
    .dataframe {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
    }
    
    .dataframe tbody tr:hover {
        background: #f8fafc !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Data Editor */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 12px;
        font-weight: 600;
        color: #334155;
    }
    
    /* Custom Card Component */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
        transform: translateY(-4px);
    }
    
    /* Step Indicator */
    .step-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50%;
        font-weight: 700;
        font-size: 1.1rem;
        margin-right: 12px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5568d3;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================================
# INISIALISASI SESSION STATE
# =====================================================================================
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

# API Configuration
API_URL_CALCULATE = "http://127.0.0.1:8000/calculate"
API_URL_AHP = "http://127.0.0.1:8000/calculate-ahp-weights"

# =====================================================================================
# HEADER SECTION
# =====================================================================================
st.title("Decision Support System")
st.markdown('<p class="hero-subtitle">Platform untuk analisis keputusan multi-kriteria dengan metode SAW, WP, TOPSIS, dan AHP</p>', unsafe_allow_html=True)

# Mode Selection
st.markdown("### 🎛️ Pilih Metode Analisis")
input_mode = st.radio(
    "",
    ("Input Bobot Langsung (SAW, WP, TOPSIS)", "Perbandingan Berpasangan (AHP)"),
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<hr>", unsafe_allow_html=True)

# =====================================================================================
# MODE 1: INPUT BOBOT LANGSUNG
# =====================================================================================
if input_mode == "Input Bobot Langsung (SAW, WP, TOPSIS)":
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Kriteria & Bobot", 
        "🎯 Alternatif", 
        "📝 Penilaian", 
        "🏆 Hasil"
    ])

    # TAB 1: KRITERIA & BOBOT
    with tab1:
        st.markdown("## ⚖️ Pengaturan Kriteria & Bobot")
        
        # Info Card
        st.info("💡 **Tips:** Tambahkan kriteria yang akan digunakan untuk penilaian. Pastikan total bobot adalah **1.0** untuk hasil yang akurat.")
        
        # Form Input
        with st.form("criteria_form", clear_on_submit=True):
            st.markdown("#### ➕ Tambah Kriteria Baru")
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                criteria_name = st.text_input("Nama Kriteria", placeholder="Contoh: Kualitas Produk")
            with col2:
                criteria_weight = st.number_input("Bobot", min_value=0.0, max_value=1.0, step=0.05, value=0.25, format="%.2f")
            with col3:
                criteria_type = st.selectbox("Tipe", ["Benefit", "Cost"])
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("✚ Tambah", use_container_width=True)
            
            if submitted and criteria_name:
                st.session_state.criteria_list.append({
                    "Kriteria": criteria_name, 
                    "Bobot": criteria_weight, 
                    "Tipe": criteria_type
                })
                st.success(f"✅ Kriteria '{criteria_name}' berhasil ditambahkan!")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Criteria List
        if st.session_state.criteria_list:
            st.markdown("#### 📋 Daftar Kriteria Aktif")
            criteria_df = pd.DataFrame(st.session_state.criteria_list)
            
            # Styling DataFrame
            styled_df = criteria_df.style.format({'Bobot': '{:.2f}'})
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Weight Summary
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            total_weight = criteria_df['Bobot'].sum()
            
            with col_metric1:
                st.metric("📊 Total Bobot", f"{total_weight:.2f}")
            with col_metric2:
                st.metric("📈 Jumlah Kriteria", len(criteria_df))
            with col_metric3:
                if np.isclose(total_weight, 1.0):
                    st.metric("✅ Status", "Valid")
                else:
                    st.metric("⚠️ Status", "Perlu Penyesuaian")
            
            # Actions
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🗑️ Hapus Kriteria Terakhir", use_container_width=True):
                    st.session_state.criteria_list.pop()
                    st.rerun()
            with col_btn2:
                if st.button("🔄 Reset Semua Kriteria", use_container_width=True):
                    st.session_state.criteria_list = []
                    st.rerun()
        else:
            st.info("🔍 Belum ada kriteria yang ditambahkan. Mulai dengan menambahkan kriteria pertama Anda!")

    # TAB 2: ALTERNATIF
    with tab2:
        st.markdown("## 🎯 Pengaturan Alternatif")
        
        st.info("💡 **Tips:** Masukkan semua opsi yang akan dibandingkan. Pisahkan setiap alternatif dengan baris baru.")
        
        col_input, col_preview = st.columns([2, 1])
        
        with col_input:
            st.markdown("#### ✏️ Input Alternatif")
            alternatives_input = st.text_area(
                "Daftar Alternatif:",
                "Laptop A\nLaptop B\nLaptop C\nLaptop D", 
                height=250,
                help="Masukkan satu alternatif per baris"
            )
            st.session_state.alternatives_list = [name.strip() for name in alternatives_input.split('\n') if name.strip()]
        
        with col_preview:
            st.markdown("#### 👁️ Preview")
            if st.session_state.alternatives_list:
                st.success(f"✅ {len(st.session_state.alternatives_list)} alternatif terdeteksi")
                for idx, alt in enumerate(st.session_state.alternatives_list, 1):
                    st.markdown(f"`{idx}.` {alt}")
            else:
                st.warning("Belum ada alternatif")

    # TAB 3: PENILAIAN
    with tab3:
        st.markdown("## 📝 Matriks Penilaian")
        
        if not st.session_state.criteria_list or not st.session_state.alternatives_list:
            st.warning("⚠️ Harap lengkapi **Kriteria** (Tab 1) dan **Alternatif** (Tab 2) terlebih dahulu.")
        else:
            st.success(f"✅ Siap menilai **{len(st.session_state.alternatives_list)} alternatif** berdasarkan **{len(st.session_state.criteria_list)} kriteria**")
            
            criteria_df = pd.DataFrame(st.session_state.criteria_list)
            criteria_names = criteria_df['Kriteria'].tolist()
            
            st.markdown("#### 📊 Input Nilai Penilaian")
            st.caption("Sesuaikan nilai untuk setiap kombinasi alternatif dan kriteria")
            
            values_df = pd.DataFrame(
                1.0, 
                columns=criteria_names, 
                index=st.session_state.alternatives_list
            )
            edited_values_df = st.data_editor(
                values_df, 
                use_container_width=True,
                num_rows="fixed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Method Selection & Calculate
            col_method, col_spacer, col_button = st.columns([2, 1, 1])
            
            with col_method:
                st.markdown("#### 🎲 Pilih Metode")
                method = st.selectbox(
                    "",
                    ("SAW", "WP", "TOPSIS"),
                    label_visibility="collapsed"
                )
            
            with col_button:
                st.markdown("#### 🚀 Eksekusi")
                calculate_button = st.button("🎯 Hitung Peringkat", type="primary", use_container_width=True)

            if calculate_button:
                total_weight = criteria_df['Bobot'].sum()
                if not np.isclose(total_weight, 1.0):
                    st.error(f"❌ Total bobot kriteria adalah {total_weight:.2f}. Harus tepat **1.0**. Silakan perbaiki di Tab 1.")
                else:
                    with st.spinner("⚙️ Memproses data dan menghitung ranking..."):
                        payload = {
                            "method": method.lower(),
                            "criteria": st.session_state.criteria_list,
                            "alternatives": edited_values_df.reset_index().rename(columns={'index': 'alternatif'}).to_dict(orient='records')
                        }
                        try:
                            response = requests.post(API_URL_CALCULATE, data=json.dumps(payload))
                            if response.status_code == 200:
                                st.session_state.results_df = pd.DataFrame(response.json().get("result", []))
                                st.success(f"✅ Perhitungan dengan metode **{method}** berhasil! Lihat hasil di Tab 4.")
                                st.balloons()
                            else:
                                st.error(f"❌ Error dari backend: {response.text}")
                        except requests.exceptions.ConnectionError as e:
                            st.error(f"❌ Gagal terhubung ke backend. Pastikan server sudah berjalan.\n\n**Detail:** {e}")

    # TAB 4: HASIL
    with tab4:
        st.markdown("## 🏆 Hasil Akhir Perangkingan")
        
        if st.session_state.results_df is not None:
            st.success("✅ Perhitungan selesai! Berikut adalah hasil perangkingan:")
            
            # Display Results
            result_styled = st.session_state.results_df.style.background_gradient(
                subset=['Score'] if 'Score' in st.session_state.results_df.columns else None,
                cmap='RdYlGn'
            )
            st.dataframe(result_styled, use_container_width=True, hide_index=True)
            
            # Winner Highlight
            if not st.session_state.results_df.empty:
                winner = st.session_state.results_df.iloc[0]
                st.markdown("### 🥇 Pemenang")
                st.success(f"**{winner.get('Alternatif', 'N/A')}** dengan skor **{winner.get('Skor', 'N/A')}**")
            
            # Download Button
            csv = st.session_state.results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Hasil (CSV)",
                data=csv,
                file_name="hasil_ranking.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("📊 Hasil perhitungan akan ditampilkan di sini setelah Anda menyelesaikan proses di Tab 3.")
            st.image("https://via.placeholder.com/800x400/667eea/ffffff?text=Menunggu+Hasil+Perhitungan", use_container_width=True)

# =====================================================================================
# MODE 2: AHP
# =====================================================================================
elif input_mode == "Perbandingan Berpasangan (AHP)":
    
    tab_ahp1, tab_ahp2, tab_ahp3, tab_ahp4 = st.tabs([
        "📊 Kriteria", 
        "🔢 Matriks AHP", 
        "📝 Alternatif", 
        "🏆 Hasil"
    ])

    # TAB AHP 1: KRITERIA
    with tab_ahp1:
        st.markdown("## ⚖️ Pengaturan Kriteria (AHP)")
        
        st.info("💡 **Tips:** Masukkan semua kriteria yang akan dibandingkan menggunakan metode AHP.")
        
        col_input, col_preview = st.columns([2, 1])
        
        with col_input:
            st.markdown("#### ✏️ Input Kriteria")
            criteria_input_ahp = st.text_area(
                "Daftar Kriteria:",
                "Harga\nPerforma\nDesain\nDaya Tahan", 
                height=200,
                help="Masukkan satu kriteria per baris"
            )
            st.session_state.ahp_criteria_list = [c.strip() for c in criteria_input_ahp.split('\n') if c.strip()]
        
        with col_preview:
            st.markdown("#### 👁️ Preview")
            if st.session_state.ahp_criteria_list:
                st.success(f"✅ {len(st.session_state.ahp_criteria_list)} kriteria")
                for idx, crit in enumerate(st.session_state.ahp_criteria_list, 1):
                    st.markdown(f"`{idx}.` {crit}")
            else:
                st.warning("Belum ada kriteria")

    # TAB AHP 2: MATRIKS
    with tab_ahp2:
        st.markdown("## 🔢 Matriks Perbandingan Berpasangan")
        
        if len(st.session_state.ahp_criteria_list) < 2:
            st.warning("⚠️ Harap masukkan minimal **2 kriteria** pada Tab 1.")
        else:
            with st.expander("📖 Panduan Skala Perbandingan AHP", expanded=False):
                guide_df = pd.DataFrame({
                    'Intensitas': [1, 3, 5, 7, 9, '2, 4, 6, 8', '1/3, 1/5, dst'],
                    'Definisi': [
                        'Sama penting',
                        'Sedikit lebih penting',
                        'Jelas lebih penting',
                        'Sangat jelas lebih penting',
                        'Mutlak lebih penting',
                        'Nilai antara',
                        'Kebalikan perbandingan'
                    ]
                })
                st.table(guide_df)
            
            st.markdown("#### 📊 Input Matriks Perbandingan")
            
            matrix_df = pd.DataFrame(
                np.identity(len(st.session_state.ahp_criteria_list)),
                index=st.session_state.ahp_criteria_list,
                columns=st.session_state.ahp_criteria_list
            )
            st.session_state.ahp_matrix_df = st.data_editor(
                matrix_df, 
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("⚖️ Hitung Bobot & Konsistensi", type="primary", use_container_width=True):
                with st.spinner("⚙️ Menghitung eigenvalue dan consistency ratio..."):
                    try:
                        payload = {"comparison_matrix": st.session_state.ahp_matrix_df.values.tolist()}
                        response = requests.post(API_URL_AHP, json=payload)
                        if response.status_code == 200:
                            st.session_state.ahp_weights_results = response.json()
                            st.success("✅ Perhitungan berhasil!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except requests.exceptions.ConnectionError as e:
                        st.error(f"❌ Gagal terhubung ke backend. Detail: {e}")

        # Display Results
        if st.session_state.ahp_weights_results:
            st.markdown("---")
            st.markdown("### 📊 Hasil Perhitungan Bobot AHP")
            
            results = st.session_state.ahp_weights_results
            
            col_weights, col_consistency = st.columns(2)
            
            with col_weights:
                st.markdown("#### 📈 Bobot Kriteria")
                weights_df = pd.DataFrame({
                    'Kriteria': st.session_state.ahp_criteria_list,
                    'Bobot': results.get("weights")
                })
                st.dataframe(
                    weights_df.style.format({'Bobot': "{:.4f}"}).background_gradient(subset=['Bobot'], cmap='Blues'),
                    use_container_width=True,
                    hide_index=True
                )
            
            with col_consistency:
                st.markdown("#### ✅ Uji Konsistensi")
                cr_value = results.get("consistency_ratio")
                status = results.get("consistency_status")
                
                st.metric("Consistency Ratio (CR)", f"{cr_value:.4f}")
                
                if status == "Konsisten":
                    st.success(f"✅ **{status}** (CR ≤ 0.1)")
                    st.caption("Matriks perbandingan valid dan dapat digunakan.")
                else:
                    st.error(f"❌ **{status}** (CR > 0.1)")
                    st.caption("Penilaian tidak konsisten. Harap revisi matriks perbandingan.")

    # TAB AHP 3: ALTERNATIF
    with tab_ahp3:
        st.markdown("## 📝 Penilaian Alternatif (AHP)")
        
        results = st.session_state.ahp_weights_results
        if not results or results.get("consistency_status") != "Konsisten":
            st.warning("⚠️ Harap hitung bobot kriteria yang **konsisten** pada Tab 2 terlebih dahulu.")
            st.info("Setelah matriks perbandingan konsisten, Anda dapat melanjutkan ke tahap penilaian alternatif.")
        else:
            st.success("✅ Bobot kriteria valid! Sekarang masukkan alternatif dan nilai penilaiannya.")
            
            # Display Current Weights
            with st.expander("📊 Lihat Bobot Kriteria yang Digunakan", expanded=False):
                weights_df = pd.DataFrame({
                    'Kriteria': st.session_state.ahp_criteria_list,
                    'Bobot': results.get("weights")
                })
                st.dataframe(
                    weights_df.style.format({'Bobot': "{:.4f}"}),
                    use_container_width=True,
                    hide_index=True
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_input, col_preview = st.columns([2, 1])
            
            with col_input:
                st.markdown("#### ✏️ Input Alternatif")
                ahp_alternatives_input = st.text_area(
                    "Daftar Alternatif:",
                    "Alternatif A\nAlternatif B\nAlternatif C", 
                    height=200,
                    help="Masukkan satu alternatif per baris"
                )
                st.session_state.ahp_alternatives_list = [name.strip() for name in ahp_alternatives_input.split('\n') if name.strip()]
            
            with col_preview:
                st.markdown("#### 👁️ Preview")
                if st.session_state.ahp_alternatives_list:
                    st.success(f"✅ {len(st.session_state.ahp_alternatives_list)} alternatif")
                    for idx, alt in enumerate(st.session_state.ahp_alternatives_list, 1):
                        st.markdown(f"`{idx}.` {alt}")
                else:
                    st.warning("Belum ada alternatif")

            if st.session_state.ahp_alternatives_list:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 📊 Matriks Penilaian Alternatif")
                
                ahp_values_df = pd.DataFrame(
                    1.0, 
                    columns=st.session_state.ahp_criteria_list, 
                    index=st.session_state.ahp_alternatives_list
                )
                edited_ahp_values_df = st.data_editor(
                    ahp_values_df, 
                    use_container_width=True,
                    num_rows="fixed"
                )

                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("🚀 Hitung Peringkat AHP", type="primary", use_container_width=True):
                    with st.spinner("⚙️ Memproses data dengan metode AHP..."):
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
                                st.success("✅ Perhitungan AHP berhasil! Lihat hasil di Tab 4.")
                                st.balloons()
                            else:
                                st.error(f"❌ Error dari backend: {response.text}")
                        except requests.exceptions.ConnectionError as e:
                            st.error(f"❌ Gagal terhubung ke backend.\n\n**Detail:** {e}")
    
    # TAB AHP 4: HASIL
    with tab_ahp4:
        st.markdown("## 🏆 Hasil Akhir Perangkingan (AHP)")
        
        if st.session_state.ahp_results_df is not None:
            st.success("✅ Perhitungan AHP selesai! Berikut adalah hasil perangkingan:")
            
            # Display Results with styling
            result_styled = st.session_state.ahp_results_df.style.background_gradient(
                subset=['Score'] if 'Score' in st.session_state.ahp_results_df.columns else None,
                cmap='RdYlGn'
            )
            st.dataframe(result_styled, use_container_width=True, hide_index=True)
            
            # Winner Highlight
            if not st.session_state.ahp_results_df.empty:
                winner = st.session_state.ahp_results_df.iloc[0]
                st.markdown("### 🥇 Alternatif Terbaik")
                st.success(f"**{winner.get('alternatif', 'N/A')}** dengan skor **{winner.get('Score', winner.get('score', 'N/A'))}**")
            
            # Summary Statistics
            if 'Score' in st.session_state.ahp_results_df.columns or 'score' in st.session_state.ahp_results_df.columns:
                score_col = 'Score' if 'Score' in st.session_state.ahp_results_df.columns else 'score'
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    st.metric("📈 Skor Tertinggi", f"{st.session_state.ahp_results_df[score_col].max():.4f}")
                with col_stat2:
                    st.metric("📉 Skor Terendah", f"{st.session_state.ahp_results_df[score_col].min():.4f}")
                with col_stat3:
                    st.metric("📊 Rata-rata", f"{st.session_state.ahp_results_df[score_col].mean():.4f}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Download Button
            csv = st.session_state.ahp_results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Hasil (CSV)",
                data=csv,
                file_name="hasil_ranking_ahp.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("📊 Hasil perhitungan AHP akan ditampilkan di sini setelah Anda menyelesaikan proses di Tab 3.")
            st.image("https://via.placeholder.com/800x400/667eea/ffffff?text=Menunggu+Hasil+Perhitungan+AHP", use_container_width=True)

# =====================================================================================
# FOOTER
# =====================================================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: white; padding: 2rem;'>
        <p style='font-size: 0.9rem; opacity: 0.8;'>
            Decision Support System Dashboard v2.0 | Powered by Streamlit & FastAPI
        </p>
        <p style='font-size: 0.8rem; opacity: 0.6;'>
            © 2025 All Rights Reserved
        </p>
    </div>
    """,
    unsafe_allow_html=True
)