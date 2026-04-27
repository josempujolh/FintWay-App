import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# 2. LÓGICA DE CARGA DE IMÁGENES (OPTIMIZADA PARA PNG)
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_base64(file_name):
    # Forzamos la búsqueda de tus archivos PNG
    path = os.path.join(current_dir, file_name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Cargamos tus archivos PNG
logo_b64 = get_base64("logo.png")
img_ahorra = get_base64("ahorra.png")
img_aprende = get_base64("aprende.png")
img_invierte = get_base64("invierte.png")

# 3. ESTILO CSS FUTURISTA
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    label { color: white !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; border: none; font-weight: bold; width: 100%; }
    .main-header { color: #D4AF37; font-size: 35px; font-weight: bold; margin: 0px; text-align: center; }
    .welcome-text { color: white; font-size: 22px; text-align: center; margin-bottom: 20px; font-style: italic; }
    .intro-card { 
        background-color: #002b56; padding: 20px; border-radius: 15px; 
        border: 1px solid #D4AF37; text-align: center; min-height: 380px;
    }
    .card { background-color: #002b56; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 10px; }
    .calc-card { background-color: #1a3a5a; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; }
    .gain { color: #00FF41; font-weight: bold; font-size: 18px; }
    .term-title { color: #D4AF37; font-weight: bold; }
    .web-button {
        display: inline-block; padding: 10px 20px; background-color: #D4AF37; color: black !important;
        text-decoration: none !important; border-radius: 5px; font-weight: bold; margin-top: 10px;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #002b56; color: white; border: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATOS INTEGRADOS (DASHBOARD / DIRECTORIO / ACADEMIA) ---
data_market = {
    'Ticker': ['ABC.A', 'BNC', 'BPV', 'BYCC', 'BVL', 'CCP.B', 'DOM', 'ENY', 'MVZ.B', 'RST', 'RST.B', 'SVS', 'TPG', 'IBC'],
    'Nombre de Acción': ['Aceros Boada', 'Bco Nac. de Crédito', 'Bco Provincial', 'Bolsa de Caracas', 'Bco de Venezuela', 'Corp. Capriles B', 'Domínguez & Cía', 'Envases Venezolanos', 'Mercantil B', 'Ron Santa Teresa', 'Ron Santa Teresa B', 'Sivensa', 'Telefónica', 'Índice IBC'],
    'Último Precio': [1610.00, 1500.00, 126.40, 670.00, 1729.00, 503.00, 690.00, 710.00, 6800.00, 545.46, 400.00, 1160.00, 19.00, 5835.16],
    'Cierre Anterior': [1610.00, 1455.00, 127.01, 679.00, 1729.00, 503.00, 696.00, 705.00, 7092.92, 545.46, 399.71, 1150.00, 20.00, 5246.47]
}
df = pd.DataFrame(data_market)
df['Var%'] = ((df['Último Precio'] - df['Cierre Anterior']) / df['Cierre Anterior'] * 100).round(2)

directorio_casas = {
    "Solfin Casa de Bolsa, C.A": {"rif": "J-31049062-7", "desc": "Excelencia y búsqueda de rentabilidad.", "dir": "El Rosal, Caracas.", "tel": "+58 212 953 8177", "mail": "info@solfin.com.ve", "web": "https://solfin.com.ve"},
    "BNCI Casa de Bolsa, C.A.": {"rif": "J-50028351-2", "desc": "Intermediación de títulos valores.", "dir": "Torre BNC La Castellana.", "tel": "+58 2129547830", "mail": "info@bnci-casadebolsa.com", "web": "https://bnci-casadebolsa.com"},
    "Mercantil Merinvest": {"rif": "J-00300384-0", "desc": "Intermediación y gestión de inversiones.", "dir": "San Bernardino, Caracas.", "tel": "+58 0212 5032066", "mail": "ccdeinversion@mercantilmerinvest.com", "web": "https://mercantilmerinvest.com"}
}

# --- 5. LÓGICA DE NAVEGACIÓN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- PÁGINA DE INICIO ---
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if logo_b64: st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="200"></div>', unsafe_allow_html=True)
        st.markdown('<p class="main-header">FintWay</p>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-text">Bienvenido a tu camino financiero más sencillo</p>', unsafe_allow_html=True)

    # LOS TRES CUADROS HORIZONTALES (PNG OK)
    col_ah, col_ap, col_in = st.columns(3)
    
    with col_ah:
        st.markdown('<div class="intro-card"><h3>Ahorra</h3><p>Protege tu capital hoy</p>', unsafe_allow_html=True)
        if img_ahorra: st.markdown(f'<img src="data:image/png;base64,{img_ahorra}" width="100%" style="border-radius:10px; margin-top:10px;">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_ap:
        st.markdown('<div class="intro-card"><h3>Aprende</h3><p>Domina el mercado bursátil</p>', unsafe_allow_html=True)
        if img_aprende: st.markdown(f'<img src="data:image/png;base64,{img_aprende}" width="100%" style="border-radius:10px; margin-top:10px;">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_in:
        st.markdown('<div class="intro-card"><h3>Invierte</h3><p>Multiplica tus ahorros</p>', unsafe_allow_html=True)
        if img_invierte: st.markdown(f'<img src="data:image/png;base64,{img_invierte}" width="100%" style="border-radius:10px; margin-top:10px;">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p style="text-align:center; font-weight:bold; color:#D4AF37; font-size:24px; margin-top:30px;">Multiplica tu Dinero de forma rápida y sencilla</p>', unsafe_allow_html=True)
    
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
    # --- TERMINAL (SIDEBAR + CONTENIDO) ---
    st.sidebar.title("Menú Principal")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy", "🏢 Directorio Casas de Bolsa"])
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()

    if opcion == "📊 Dashboard de Mercado":
        st.markdown('<p class="main-header" style="text-align:left;">FintWay Terminal 🛰️</p>', unsafe_allow_html=True)
        st.divider()
        # Top Gainers
        top_4 = df.sort_values(by='Var%', ascending=False).head(4)
        cols_g = st.columns(4)
        for i, (idx, row) in enumerate(top_4.iterrows()):
            with cols_g[i]:
                st.markdown(f'<div class="card"><h4>{row["Ticker"]}</h4><p class="gain">+{row["Var%"]}%</p></div>', unsafe_allow_html=True)
        
        # Tabla y Calculadora
        c_tab, c_calc = st.columns(2)
        with c_tab:
            st.subheader("📊 Acciones BVC")
            st.dataframe(df[['Ticker', 'Nombre de Acción', 'Último Precio']], use_container_width=True, hide_index=True)
        with c_calc:
            st.subheader("🧮 Calculadora")
            monto = st.number_input("Presupuesto (VES)", min_value=1.0, value=5000.0)
            acc_c = st.selectbox("Acción:", df['Ticker'])
            pr = float(df[df['Ticker'] == acc_c]['Último Precio'].values)
            st.markdown(f'<div class="calc-card">Comprarías: <h2 style="color:#00FF41;">{int(monto//pr)} Acciones</h2></div>', unsafe_allow_html=True)

    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        def term(t, e): st.markdown(f'<p><span class="term-title">{t}:</span> {e}</p>', unsafe_allow_html=True)
        with st.expander("🏛️ Fundamentos"):
            term("Bolsa de Valores de Caracas (BVC)", "Institución donde se negocian títulos valores.")
            # ... (Aquí el resto de tus 15 términos con formato Dorado/Blanco)

    elif opcion == "🏢 Directorio Casas de Bolsa":
        st.markdown('<p class="main-header">Directorio 🏢</p>', unsafe_allow_html=True)
        c_sel = st.selectbox("Selecciona:", list(directorio_casas.keys()))
        inf = directorio_casas[c_sel]
        st.markdown(f'<div class="card"><h3 style="color:#D4AF37;">{c_sel}</h3><p>{inf["desc"]}</p><br><a href="{inf["web"]}" target="_blank" class="web-button">🌐 Visitar Web</a></div>', unsafe_allow_html=True)
