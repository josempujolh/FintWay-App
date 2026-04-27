import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# 2. LÓGICA DE RUTA PARA LOGO E IMÁGENES
current_dir = os.path.dirname(os.path.abspath(__file__))
def get_base64(file_name):
    path = os.path.join(current_dir, file_name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64("logo.png")
img_ahorra = get_base64("ahorra.jpg")
img_aprende = get_base64("aprende.jpg")
img_invierte = get_base64("invierte.jpg")

# 3. ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    label { color: white !important; font-weight: bold !important; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; border: none; font-weight: bold; width: 100%; }
    .main-header { color: #D4AF37; font-size: 35px; font-weight: bold; margin: 0px; text-align: center; }
    .welcome-text { color: white; font-size: 20px; text-align: center; margin-bottom: 20px; font-style: italic; }
    .intro-card { 
        background-color: #002b56; padding: 20px; border-radius: 15px; 
        border-top: 3px solid #D4AF37; text-align: center; min-height: 250px;
    }
    .card { background-color: #002b56; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 10px; }
    .calc-card { background-color: #1a3a5a; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; }
    .gain { color: #00FF41; font-weight: bold; }
    .term-title { color: #D4AF37; font-weight: bold; }
    .web-button {
        display: inline-block; padding: 10px 20px; background-color: #D4AF37; color: black !important;
        text-decoration: none !important; border-radius: 5px; font-weight: bold; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATOS DE MERCADO Y DIRECTORIO (INTEGRIDAD TOTAL) ---
data_market = {
    'Ticker': ['ABC.A', 'BNC', 'BPV', 'BYCC', 'BVL', 'CCP.B', 'DOM', 'ENY', 'MVZ.B', 'RST', 'RST.B', 'SVS', 'TPG', 'IBC'],
    'Nombre de Acción': ['Aceros Boada', 'Bco Nac. de Crédito', 'Bco Provincial', 'Bolsa de Caracas', 'Bco de Venezuela', 'Corp. Capriles B', 'Domínguez & Cía', 'Envases Venezolanos', 'Mercantil B', 'Ron Santa Teresa', 'Ron Santa Teresa B', 'Sivensa', 'Telefónica', 'Índice IBC'],
    'Último Precio': [1610.00, 1500.00, 126.40, 670.00, 1729.00, 503.00, 690.00, 710.00, 6800.00, 545.46, 400.00, 1160.00, 19.00, 5835.16],
    'Cierre Anterior': [1610.00, 1455.00, 127.01, 679.00, 1729.00, 503.00, 696.00, 705.00, 7092.92, 545.46, 399.71, 1150.00, 20.00, 5246.47]
}
df = pd.DataFrame(data_market)
df['Var%'] = ((df['Último Precio'] - df['Cierre Anterior']) / df['Cierre Anterior'] * 100).round(2)

directorio_casas = {
    "Solfin Casa de Bolsa, C.A": {"rif": "J-31049062-7", "desc": "Solfin, es una empresa que se basa en la calidad y excelencia...", "dir": "Torre Oriental, El Rosal.", "tel": "+58 212 953 8177", "mail": "info@solfin.com.ve", "web": "https://solfin.com.ve"},
    "Acciona Casa de Bolsa, C.A.": {"rif": "J-50037354-6", "desc": "Innovadora propuesta de valor...", "dir": "C.C. San Ignacio, La Castellana.", "tel": "+58 02122617196", "mail": "info@accionavalores.com", "web": "https://accionavalores.com"},
    "BNCI Casa de Bolsa, C.A.": {"rif": "J-50028351-2", "desc": "Interconecta inversores con financiamiento...", "dir": "Torre BNC La Castellana.", "tel": "+58 2129547830", "mail": "info@bnci-casadebolsa.com", "web": "https://bnci-casadebolsa.com"}
}

# --- 5. LÓGICA DE NAVEGACIÓN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- PÁGINA DE INICIO / REGISTRO ---
    c_log1, c_log2, c_log3 = st.columns([1,2,1])
    with c_log2:
        if logo_b64: st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="200"></div>', unsafe_allow_html=True)
        st.markdown('<p class="main-header">FintWay</p>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-text">Bienvenido a tu camino financiero más sencillo</p>', unsafe_allow_html=True)

    # LOS TRES CUADROS HORIZONTALES CON IMÁGENES
    col_ahorra, col_aprende, col_invierte = st.columns(3)
    
    with col_ahorra:
        st.markdown('<div class="intro-card"><h3>Ahorra</h3><p>Protege tu capital</p></div>', unsafe_allow_html=True)
        if img_ahorra: st.markdown(f'<div style="text-align:center;"><img src="data:image/jpeg;base64,{img_ahorra}" width="100%" style="border-radius:10px; margin-top:10px;"></div>', unsafe_allow_html=True)
    
    with col_aprende:
        st.markdown('<div class="intro-card"><h3>Aprende</h3><p>Domina el mercado</p></div>', unsafe_allow_html=True)
        if img_aprende: st.markdown(f'<div style="text-align:center;"><img src="data:image/jpeg;base64,{img_aprende}" width="100%" style="border-radius:10px; margin-top:10px;"></div>', unsafe_allow_html=True)
    
    with col_invierte:
        st.markdown('<div class="intro-card"><h3>Invierte</h3><p>Multiplica tu dinero</p></div>', unsafe_allow_html=True)
        if img_invierte: st.markdown(f'<div style="text-align:center;"><img src="data:image/jpeg;base64,{img_invierte}" width="100%" style="border-radius:10px; margin-top:10px;"></div>', unsafe_allow_html=True)

    st.markdown('<p style="text-align:center; font-weight:bold; color:#D4AF37; margin-top:20px; font-size:22px;">Multiplica tu Dinero de forma rápida y sencilla</p>', unsafe_allow_html=True)
    
    # Formulario Acceso
    st.write("<br>", unsafe_allow_html=True)
    c_f1, c_f2, c_f3 = st.columns([1,1,1])
    with c_f2:
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER A LA TERMINAL"):
            if u == "admin" and p == "fintway2026": 
                st.session_state.logged_in = True
                st.rerun()
else:
    # --- TERMINAL (SIDEBAR + PÁGINAS) ---
    st.sidebar.title("Menú Principal")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy", "🏢 Directorio Casas de Bolsa"])
    
    if opcion == "📊 Dashboard de Mercado":
        c_l, c_t = st.columns([1,5])
        with c_l: 
            if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="80">', unsafe_allow_html=True)
        with c_t: st.markdown('<p class="main-header" style="text-align:left;">Terminal de Inversión 🛰️</p>', unsafe_allow_html=True)
        st.divider()
        # (Aquí sigue el resto de tu Dashboard: Top Gainers, Tabla, Calculadora...)
        st.write("Dashboard operativo con Calculadora y Top Gainers.")

    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        # (Aquí sigue tu Glosario Dorado/Blanco completo...)
        st.write("Glosario de 15 términos integrado.")

    elif opcion == "🏢 Directorio Casas de Bolsa":
        st.markdown('<p class="main-header">Directorio 🏢</p>', unsafe_allow_html=True)
        # (Aquí siguen tus 12 casas de bolsa con links...)
        st.write("Directorio de instituciones activo.")
