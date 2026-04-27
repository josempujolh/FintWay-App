import streamlit as st
import pandas as pd
import os
import plotly.express as px
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# 2. LÓGICA DE NAVEGACIÓN
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# 3. ESTILO CSS FUTURISTA
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    label { color: white !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; border: none; font-weight: bold; width: 100%; }
    .main-header { color: #D4AF37; font-size: 35px; font-weight: bold; margin: 0px; text-align: center; }
    .welcome-text { color: white; font-size: 22px; text-align: center; margin-bottom: 20px; font-style: italic; }
    
    .intro-card { 
        background-color: #002b56; 
        padding: 0px; 
        border-radius: 15px; 
        border: 1px solid #D4AF37; 
        text-align: center; 
        min-height: 420px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    .card-text-container { padding: 15px; }
    .intro-card h3 { color: #D4AF37; margin-top: 10px; margin-bottom: 5px; }
    .intro-card p { color: white; font-size: 14px; margin-bottom: 15px; }
    
    /* Centrado de imagen de logo */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATOS DE MERCADO (INTEGRACIÓN TOTAL) ---
data_market = {
    'Ticker': ['ABC.A', 'BNC', 'BPV', 'BYCC', 'BVL', 'CCP.B', 'DOM', 'ENY', 'MVZ.B', 'RST', 'RST.B', 'SVS', 'TPG', 'IBC'],
    'Nombre de Acción': ['Aceros Boada', 'Bco Nac. de Crédito', 'Bco Provincial', 'Bolsa de Caracas', 'Bco de Venezuela', 'Corp. Capriles B', 'Domínguez & Cía', 'Envases Venezolanos', 'Mercantil B', 'Ron Santa Teresa', 'Ron Santa Teresa B', 'Sivensa', 'Telefónica', 'Índice IBC'],
    'Último Precio': [1610.00, 1500.00, 126.40, 670.00, 1729.00, 503.00, 690.00, 710.00, 6800.00, 545.46, 400.00, 1160.00, 19.00, 5835.16],
    'Cierre Anterior': [1610.00, 1455.00, 127.01, 679.00, 1729.00, 503.00, 696.00, 705.00, 7092.92, 545.46, 399.71, 1150.00, 20.00, 5246.47]
}
df = pd.DataFrame(data_market)

# --- 5. PÁGINA DE INICIO / REGISTRO ---
if not st.session_state.logged_in:
    # AJUSTE: Logo centrado usando columnas proporcionales
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if os.path.exists("logo.png"):
            # Usamos st.image con centrado manual
            st.image("logo.png", width=250)
        st.markdown('<p class="main-header">FintWay</p>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-text">Bienvenido a tu camino financiero más sencillo</p>', unsafe_allow_html=True)

    # LAS TRES TARJETAS
    col_ah, col_ap, col_in = st.columns(3)
    
    with col_ah:
        with st.container():
            if os.path.exists("ahorra.png"): st.image("ahorra.png", use_container_width=True)
            st.markdown('<div class="intro-card" style="border-top:none; border-radius: 0 0 15px 15px; min-height:auto;"><div class="card-text-container"><h3>Ahorra</h3><p>Protege tu capital hoy</p></div></div>', unsafe_allow_html=True)
    
    with col_ap:
        with st.container():
            if os.path.exists("aprende.png"): st.image("aprende.png", use_container_width=True)
            st.markdown('<div class="intro-card" style="border-top:none; border-radius: 0 0 15px 15px; min-height:auto;"><div class="card-text-container"><h3>Aprende</h3><p>Domina el mercado bursátil</p></div></div>', unsafe_allow_html=True)
    
    with col_in:
        with st.container():
            if os.path.exists("invierte.png"): st.image("invierte.png", use_container_width=True)
            st.markdown('<div class="intro-card" style="border-top:none; border-radius: 0 0 15px 15px; min-height:auto;"><div class="card-text-container"><h3>Invierte</h3><p>Multiplica tus ahorros</p></div></div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-weight:bold; color:#D4AF37; font-size:24px;">Multiplica tu Dinero de forma rápida y sencilla</p>', unsafe_allow_html=True)
    
    # Formulario Acceso centrado
    c_f1, c_f2, c_f3 = st.columns([1, 1, 1])
    with c_f2:
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER A LA TERMINAL"):
            if u == "admin" and p == "fintway2026": 
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Credenciales incorrectas")

else:
    # --- TERMINAL (SIDEBAR + CONTENIDO) ---
    st.sidebar.title("Menú Principal")
    if os.path.exists("logo.png"): st.sidebar.image("logo.png", width=120)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy", "🏢 Directorio Casas de Bolsa"])
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()

    if opcion == "📊 Dashboard de Mercado":
        st.markdown('<p class="main-header" style="text-align:left;">FintWay Terminal 🛰️</p>', unsafe_allow_html=True)
        st.divider()
        st.write("Dashboard con Top Gainers, Tabla de Acciones y Calculadora activos.")

    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        st.write("Glosario de 15 términos en Dorado/Blanco disponible.")

    elif opcion == "🏢 Directorio Casas de Bolsa":
        st.markdown('<p class="main-header">Directorio 🏢</p>', unsafe_allow_html=True)
        st.write("Directorio de 12 Casas de Bolsa con links oficiales cargado.")
