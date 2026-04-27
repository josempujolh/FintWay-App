import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# 2. LÓGICA DE RUTA PARA LOGO E IMÁGENES (MEJORADA)
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_base64(file_name):
    # Intentamos buscar el archivo con varias extensiones comunes
    posibles_extensiones = [file_name, file_name.replace('.jpg', '.png'), file_name.replace('.jpg', '.jpeg')]
    for ext in posibles_extensiones:
        path = os.path.join(current_dir, ext)
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
    .welcome-text { color: white; font-size: 22px; text-align: center; margin-bottom: 20px; font-style: italic; }
    .intro-card { 
        background-color: #002b56; padding: 20px; border-radius: 15px; 
        border: 1px solid #D4AF37; text-align: center; min-height: 350px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .img-container {
        border-radius: 10px; overflow: hidden; margin-top: 15px; border: 1px solid #1a3a5a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LÓGICA DE NAVEGACIÓN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Header
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if logo_b64: st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="180"></div>', unsafe_allow_html=True)
        st.markdown('<p class="main-header">FintWay</p>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-text">Bienvenido a tu camino financiero más sencillo</p>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    # LOS TRES CUADROS CON IMÁGENES
    col_ah, col_ap, col_in = st.columns(3)
    
    with col_ah:
        st.markdown('<div class="intro-card"><h3>Ahorra</h3><p>Protege tu capital hoy</p>', unsafe_allow_html=True)
        if img_ahorra: st.markdown(f'<div class="img-container"><img src="data:image/jpeg;base64,{img_ahorra}" width="100%"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_ap:
        st.markdown('<div class="intro-card"><h3>Aprende</h3><p>Domina el mercado bursátil</p>', unsafe_allow_html=True)
        if img_aprende: st.markdown(f'<div class="img-container"><img src="data:image/jpeg;base64,{img_aprende}" width="100%"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_in:
        st.markdown('<div class="intro-card"><h3>Invierte</h3><p>Multiplica tus ahorros</p>', unsafe_allow_html=True)
        if img_invierte: st.markdown(f'<div class="img-container"><img src="data:image/jpeg;base64,{img_invierte}" width="100%"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-weight:bold; color:#D4AF37; font-size:24px;">Multiplica tu Dinero de forma rápida y sencilla</p>', unsafe_allow_html=True)
    
    # Formulario Acceso
    c_f1, c_f2, c_f3 = st.columns([1,1,1])
    with c_f2:
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER A LA TERMINAL"):
            if u == "admin" and p == "fintway2026": 
                st.session_state.logged_in = True
                st.rerun()
            else: st.error("Credenciales incorrectas")

else:
    # (AQUÍ SIGUE EL CÓDIGO DE TU DASHBOARD, ACADEMIA Y DIRECTORIO IGUAL QUE ANTES)
    st.sidebar.title("Menú Principal")
    if st.sidebar.button("Cerrar Sesión"): 
        st.session_state.logged_in = False
        st.rerun()
    st.write("Bienvenido a la Terminal Operativa")
