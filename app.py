import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# 2. LÓGICA DE RUTA PARA EL LOGO
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.png")

def get_base64_logo(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64_logo(logo_path)

# 3. ESTILO CSS FUTURISTA
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    label { color: white !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; border: none; font-weight: bold; width: 100%; }
    .main-header { color: #D4AF37; font-size: 35px; font-weight: bold; margin: 0px; }
    .card { background-color: #002b56; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 10px; }
    .calc-card { background-color: #1a3a5a; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; }
    .gain { color: #00FF41; font-weight: bold; font-size: 18px; }
    .term-title { color: #D4AF37; font-weight: bold; }
    .web-button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #D4AF37;
        color: black !important;
        text-decoration: none !important;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 10px;
    }
    .web-button:hover { background-color: #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATOS DE MERCADO ---
data_market = {
    'Ticker': ['ABC.A', 'BNC', 'BPV', 'BYCC', 'BVL', 'CCP.B', 'DOM', 'ENY', 'MVZ.B', 'RST', 'RST.B', 'SVS', 'TPG'],
    'Nombre de Acción': ['Aceros Boada', 'Bco Nac. de Crédito', 'Bco Provincial', 'Bolsa de Caracas', 'Bco de Venezuela', 'Corp. Capriles B', 'Domínguez & Cía', 'Envases Venezolanos', 'Mercantil B', 'Ron Santa Teresa', 'Ron Santa Teresa B', 'Sivensa', 'Telefónica'],
    'Último Precio': [1610.00, 1500.00, 126.40, 670.00, 1729.00, 503.00, 690.00, 710.00, 6800.00, 545.46, 400.00, 1160.00, 19.00],
    'Cierre Anterior': [1610.00, 1455.00, 127.01, 679.00, 1729.00, 503.00, 696.00, 705.00, 7092.92, 545.46, 399.71, 1150.00, 20.00]
}
df = pd.DataFrame(data_market)

# --- 5. DIRECTORIO CASAS DE BOLSA ---
directorio_casas = {
    "Mercantil Merinvest": {
        "desc": "Líder en el mercado de valores venezolano, ofreciendo servicios de corretaje y asesoría financiera con el respaldo del Grupo Mercantil.",
        "web": "https://mercantilmerinvest.com"
    },
    "BNCI Casa de Bolsa": {
        "desc": "Especialistas en intermediación de títulos valores y gestión de portafolios para clientes naturales y jurídicos.",
        "web": "https://bnci.com.ve"
    },
    "Ratio Casa de Bolsa": {
        "desc": "Enfocados en brindar soluciones de inversión estratégicas en el mercado de capitales venezolano.",
        "web": "https://ratiocasadobolsa.com"
    },
    "Rendivalores": {
        "desc": "Casa de Bolsa con amplia trayectoria, destacada por su plataforma tecnológica y análisis de mercado.",
        "web": "https://rendivalores.com"
    },
    "Fivenca": {
        "desc": "Institución financiera dedicada a la gestión de activos y asesoría en el mercado bursátil nacional e internacional.",
        "web": "https://fivenca.com"
    },
    "BNC Casa de Bolsa": {
        "desc": "Filial del Banco Nacional de Crédito, enfocada en la democratización del acceso al mercado de valores.",
        "web": "https://bncenlinea.com"
    },
    "Banctrust": {
        "desc": "Especialistas en banca de inversión y mercados emergentes con fuerte presencia en la región.",
        "web": "https://banctrust.com"
    },
    "Interbursa": {
        "desc": "Corretaje de títulos valores con enfoque en atención personalizada y transparencia operativa.",
        "web": "https://interbursa.com.ve"
    },
    "Valores Vencred": {
        "desc": "Casa de bolsa con sólida ética profesional, ofreciendo custodia y negociación de activos financieros.",
        "web": "https://valoresvencred.com"
    },
    "Activalores": {
        "desc": "Expertos en estructuración de emisiones y corretaje de acciones en la Bolsa de Valores de Caracas.",
        "web": "https://activalores.com"
    }
}

# --- 6. LÓGICA DE LOGIN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    c_log1, c_log2, c_log3 = st.columns(3)
    with c_log2:
        if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="200">', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;" class="main-header">Acceso a Terminal FintWay</p>', unsafe_allow_html=True)
    u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
    if st.button("ACCEDER A LA RED"):
        if u == "admin" and p == "fintway2026": 
            st.session_state.logged_in = True
            st.rerun()
else:
    # --- SIDEBAR ---
    st.sidebar.title("Menú Principal")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy", "🏢 Directorio Casas de Bolsa"])
    st.sidebar.divider()
    if st.sidebar.button("Cerrar Sesión"): 
        st.session_state.logged_in = False
        st.rerun()

    # --- PÁGINA 1: DASHBOARD ---
    if opcion == "📊 Dashboard de Mercado":
        st.markdown('<p class="main-header">Terminal de Inversión 🛰️</p>', unsafe_allow_html=True)
        st.divider()
        col_tabla, col_calc = st.columns(2)
        with col_tabla:
            st.subheader("📊 Acciones BVC")
            st.dataframe(df[['Ticker', 'Nombre de Acción', 'Último Precio']], use_container_width=True, hide_index=True)
        with col_calc:
            st.subheader("🧮 Calculadora")
            monto = st.number_input("Presupuesto (VES)", min_value=1.0, value=5000.0)
            accion = st.selectbox("Acción:", df['Ticker'])
            precio = df[df['Ticker'] == accion]['Último Precio'].values
            st.markdown(f'<div class="calc-card">Comprarías: <h2 style="color:#00FF41;">{int(monto//precio)} Acciones</h2></div>', unsafe_allow_html=True)

    # --- PÁGINA 2: ACADEMIA ---
    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        with st.expander("🏛️ Términos Fundamentales"):
            st.markdown('<p><span class="term-title">Bolsa de Valores de Caracas (BVC):</span> Institución donde se negocian títulos valores.</p>', unsafe_allow_html=True)

    # --- PÁGINA 3: DIRECTORIO ---
    elif opcion == "🏢 Directorio Casas de Bolsa":
        st.markdown('<p class="main-header">Directorio de Casas de Bolsa 🏢</p>', unsafe_allow_html=True)
        st.write("Selecciona una institución para ver detalles y acceder a su portal oficial.")
        
        casa_sel = st.selectbox("Buscar Casa de Bolsa:", list(directorio_casas.keys()))
        info = directorio_casas[casa_sel]
        
        st.markdown(f"""
            <div class="card">
                <h3 style="color:#D4AF37; margin-bottom:10px;">{casa_sel}</h3>
                <p style="color:white; font-size:1.1rem; line-height:1.5;">{info['desc']}</p>
                <br>
                <a href="{info['web']}" target="_blank" class="web-button">
                    🌐 Visitar Página Web Oficial
                </a>
            </div>
        """, unsafe_allow_html=True)
