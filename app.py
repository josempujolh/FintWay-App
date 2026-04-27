import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# 2. LÓGICA DE CARGA DE IMÁGENES
current_dir = os.path.dirname(os.path.abspath(__file__))
def get_base64(file_name):
    path = os.path.join(current_dir, file_name)
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64("logo.png")
img_ahorra = get_base64("ahorra.png")
img_aprende = get_base64("aprende.png")
img_invierte = get_base64("invierte.png")

# 3. ESTILO CSS FUTURISTA ACTUALIZADO
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    label { color: white !important; font-weight: bold !important; }
    
    /* Títulos y textos */
    .main-header { color: #D4AF37; font-size: 42px; font-weight: bold; text-align: center; margin-top: 10px; }
    .welcome-text { color: #D4AF37; font-size: 28px; text-align: center; margin-bottom: 30px; font-weight: bold; }
    
    /* Botones Dorados */
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; border: none; font-weight: bold; width: 100%; height: 45px; }
    .stButton>button:hover { background-color: #f1c40f; color: black; }

    /* Animación y tamaño de cuadros */
    .intro-card { 
        background-color: #002b56; padding: 0px; border-radius: 15px; 
        border: 1px solid #D4AF37; text-align: center; min-height: 320px;
        overflow: hidden; display: flex; flex-direction: column;
        transition: transform 0.3s, box-shadow 0.3s;
        margin: 0 auto; max-width: 280px; /* Reducción de tamaño */
    }
    .intro-card:hover {
        transform: translateY(-10px);
        box-shadow: 0px 10px 20px rgba(212, 175, 55, 0.4);
    }
    .card-text-container { padding: 10px; }
    .intro-card h3 { color: #D4AF37; margin-top: 5px; font-size: 20px; }
    .intro-card p { color: white; font-size: 13px; }
    
    /* Footer */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #001529; color: #D4AF37; text-align: center;
        padding: 10px; font-size: 14px; border-top: 1px solid #D4AF37;
    }

    .card { background-color: #002b56; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; }
    .gain { color: #00FF41; font-weight: bold; }
    .term-title { color: #D4AF37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LÓGICA DE NAVEGACIÓN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Logo Centrado (Sin palabra FintWay debajo)
    if logo_b64:
        st.markdown(f'<div style="display: flex; justify-content: center; margin-top: 20px;"><img src="data:image/png;base64,{logo_b64}" width="220"></div>', unsafe_allow_html=True)
    
    # Eslogan más grande y dorado
    st.markdown('<p class="welcome-text">Tu camino financiero más sencillo</p>', unsafe_allow_html=True)

    # LOS TRES CUADROS REDUCIDOS CON ANIMACIÓN
    col_ah, col_ap, col_in = st.columns(3)
    
    with col_ah:
        if img_ahorra: st.markdown(f'<div class="intro-card"><img src="data:image/png;base64,{img_ahorra}" width="100%"><div class="card-text-container"><h3>Ahorra</h3><p>Protege tu capital hoy</p></div></div>', unsafe_allow_html=True)
    
    with col_ap:
        if img_aprende: st.markdown(f'<div class="intro-card"><img src="data:image/png;base64,{img_aprende}" width="100%"><div class="card-text-container"><h3>Aprende</h3><p>Domina términos básicos</p></div></div>', unsafe_allow_html=True)
    
    with col_in:
        if img_invierte: st.markdown(f'<div class="intro-card"><img src="data:image/png;base64,{img_invierte}" width="100%"><div class="card-text-container"><h3>AInvierte</h3><p>Multiplica tus ahorros con IA</p></div></div>', unsafe_allow_html=True)

    st.write("<br><br>", unsafe_allow_html=True)
    
    # Formulario Acceso + Botón Registro
    c_f1, c_f2, c_f3 = st.columns([1, 2, 1])
    with c_f2:
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        
        # Botones en horizontal
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("ACCEDER"):
                if u == "admin" and p == "fintway2026": 
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("Credenciales incorrectas")
        with btn_col2:
            if st.button("CREAR CUENTA"):
                st.toast("Módulo de registro próximamente disponible", icon="🚀")

    # PIE DE PÁGINA
    st.markdown('<div class="footer">🛡️ Seguridad Garantizada | FintWay Terminal 2026 | @FintWayApp</div>', unsafe_allow_html=True)

else:
    # --- TERMINAL OPERATIVA (DASHBOARD, ACADEMIA, DIRECTORIO) ---
    st.sidebar.title("Menú Principal")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="120">', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy", "🏢 Directorio Casas de Bolsa"])
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
    
    # (El resto del código interno se mantiene intacto: Tablas, Glosario Dorado, Casas de Bolsa)
    st.write(f"Accediendo a: {opcion}")
