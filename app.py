import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# 2. LÓGICA DE CARGA DE IMÁGENES (LOGO Y TARJETAS)
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_base64(file_name):
    path = os.path.join(current_dir, file_name)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64("logo.png")
img_ahorra = get_base64("ahorra.png")
img_aprende = get_base64("aprende.png")
img_invierte = get_base64("invierte.png")

# 3. ESTILO CSS FUTURISTA COMPLETO
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    label { color: white !important; font-weight: bold !important; font-size: 1.1rem !important; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; border: none; font-weight: bold; width: 100%; }
    .main-header { color: #D4AF37; font-size: 40px; font-weight: bold; margin: 0px; text-align: center; }
    .welcome-text { color: white; font-size: 22px; text-align: center; margin-bottom: 30px; font-style: italic; }
    
    .intro-card { 
        background-color: #002b56; padding: 0px; border-radius: 15px; 
        border: 1px solid #D4AF37; text-align: center; min-height: 420px;
        overflow: hidden; display: flex; flex-direction: column;
    }
    .card-text-container { padding: 15px; }
    .intro-card h3 { color: #D4AF37; margin-top: 10px; margin-bottom: 5px; }
    .intro-card p { color: white; font-size: 14px; }
    
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

# --- 4. DATOS DE MERCADO ---
data_market = {
    'Ticker': ['ABC.A', 'BNC', 'BPV', 'BYCC', 'BVL', 'CCP.B', 'DOM', 'ENY', 'MVZ.B', 'RST', 'RST.B', 'SVS', 'TPG', 'IBC'],
    'Nombre de Acción': ['Aceros Boada', 'Bco Nac. de Crédito', 'Bco Provincial', 'Bolsa de Caracas', 'Bco de Venezuela', 'Corp. Capriles B', 'Domínguez & Cía', 'Envases Venezolanos', 'Mercantil B', 'Ron Santa Teresa', 'Ron Santa Teresa B', 'Sivensa', 'Telefónica', 'Índice IBC'],
    'Último Precio': [1610.00, 1500.00, 126.40, 670.00, 1729.00, 503.00, 690.00, 710.00, 6800.00, 545.46, 400.00, 1160.00, 19.00, 5835.16],
    'Cierre Anterior': [1610.00, 1455.00, 127.01, 679.00, 1729.00, 503.00, 696.00, 705.00, 7092.92, 545.46, 399.71, 1150.00, 20.00, 5246.47]
}
df = pd.DataFrame(data_market)
df['Var%'] = ((df['Último Precio'] - df['Cierre Anterior']) / df['Cierre Anterior'] * 100).round(2)

resenas = {
    "BNC": "Banco Universal enfocado en banca comercial. Líder en depósitos del sector privado.",
    "RST": "Ron Santa Teresa: Empresa bicentenaria, referente del ron premium venezolano.",
    "TPG": "Telefónica Venezolana (Movistar). Líder en servicios de telecomunicaciones.",
    "BVL": "Banco de Venezuela: La institución financiera más grande del país.",
    "ABC.A": "Aceros Boada: Tradición y calidad en la industria metalúrgica."
}

# --- 5. DIRECTORIO CASAS DE BOLSA ---
directorio_casas = {
    "Solfin Casa de Bolsa, C.A": {"rif": "J-31049062-7", "desc": "Excelencia y búsqueda de rentabilidad.", "dir": "Torre Oriental, El Rosal.", "tel": "+58 212 953 8177", "mail": "info@solfin.com.ve", "web": "https://solfin.com.ve"},
    "Acciona Casa de Bolsa, C.A.": {"rif": "J-50037354-6", "desc": "Innovadora propuesta de valor digital.", "dir": "C.C. San Ignacio, La Castellana.", "tel": "+58 02122617196", "mail": "info@accionavalores.com", "web": "https://accionavalores.com"},
    "BNCI Casa de Bolsa, C.A.": {"rif": "J-50028351-2", "desc": "Intermediación de títulos valores en renta fija y variable.", "dir": "Torre BNC La Castellana.", "tel": "+58 2129547830", "mail": "info@bnci-casadebolsa.com", "web": "https://bnci-casadebolsa.com"},
    "Fivenca Casa de Bolsa, C.A.": {"rif": "J-08501464-0", "desc": "Estrategias personalizadas nacionales e internacionales.", "dir": "CC Lido, El Rosal.", "tel": "+58 212-3075799", "mail": "atencionalcliente@grupofivenca.com", "web": "https://fivenca.com"},
    "Mercantil Merinvest": {"rif": "J-00300384-0", "desc": "Especializada en intermediación y gestión de inversiones.", "dir": "Banco Mercantil, San Bernardino.", "tel": "+58 0212 5032066", "mail": "ccdeinversion@mercantilmerinvest.com", "web": "https://mercantilmerinvest.com"},
    "Rendivalores Casa de Bolsa": {"rif": "J-30292237-2", "desc": "Más de 29 años de trayectoria exitosa en el mercado.", "dir": "La Castellana, Caracas.", "tel": "+58 2122679909", "mail": "info@rendivalores.com", "web": "https://rendivalores.com"}
}

# --- 6. LÓGICA DE NAVEGACIÓN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    # LOGO CENTRADO ABSOLUTO
    if logo_b64:
        st.markdown(f'<div style="display: flex; justify-content: center; margin-top: 20px;"><img src="data:image/png;base64,{logo_b64}" width="280"></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="main-header">FintWay</p>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-text">Bienvenido a tu camino financiero más sencillo</p>', unsafe_allow_html=True)

    # TARJETAS DE INICIO
    col_ah, col_ap, col_in = st.columns(3)
    with col_ah:
        if img_ahorra: st.image(f"data:image/png;base64,{img_ahorra}", use_container_width=True)
        st.markdown('<div class="intro-card" style="border-top:none; border-radius:0 0 15px 15px; min-height:auto;"><div class="card-text-container"><h3>Ahorra</h3><p>Protege tu capital hoy</p></div></div>', unsafe_allow_html=True)
    with col_ap:
        if img_aprende: st.image(f"data:image/png;base64,{img_aprende}", use_container_width=True)
        st.markdown('<div class="intro-card" style="border-top:none; border-radius:0 0 15px 15px; min-height:auto;"><div class="card-text-container"><h3>Aprende</h3><p>Domina el mercado bursátil</p></div></div>', unsafe_allow_html=True)
    with col_in:
        if img_invierte: st.image(f"data:image/png;base64,{img_invierte}", use_container_width=True)
        st.markdown('<div class="intro-card" style="border-top:none; border-radius:0 0 15px 15px; min-height:auto;"><div class="card-text-container"><h3>Invierte</h3><p>Multiplica tus ahorros</p></div></div>', unsafe_allow_html=True)

    st.markdown('<p style="text-align:center; font-weight:bold; color:#D4AF37; font-size:24px; margin-top:30px;">Multiplica tu Dinero de forma rápida y sencilla</p>', unsafe_allow_html=True)
    
    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f2:
        u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER A LA TERMINAL"):
            if u == "admin" and p == "fintway2026": st.session_state.logged_in = True; st.rerun()
else:
    # --- TERMINAL OPERATIVA ---
    st.sidebar.title("Menú Principal")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy", "🏢 Directorio Casas de Bolsa"])
    st.sidebar.divider()
    if st.sidebar.button("Cerrar Sesión"): st.session_state.logged_in = False; st.rerun()

    if opcion == "📊 Dashboard de Mercado":
        st.markdown('<p class="main-header" style="text-align:left;">FintWay Terminal 🛰️</p>', unsafe_allow_html=True)
        st.divider()
        # Top Gainers
        top_4 = df.sort_values(by='Var%', ascending=False).head(4)
        cols_g = st.columns(4)
        for i, (idx, row) in enumerate(top_4.iterrows()):
            with cols_g[i]: st.markdown(f'<div class="card"><h4>{row["Ticker"]}</h4><p class="gain">+{row["Var%"]}%</p></div>', unsafe_allow_html=True)
        
        # Tabla y Calculadora
        c_tab, c_calc = st.columns(2)
        with c_tab:
            st.subheader("📊 Acciones BVC")
            st.dataframe(df[['Ticker', 'Nombre de Acción', 'Último Precio', 'Cierre Anterior']], use_container_width=True, hide_index=True)
            st.write("---")
            ticker_sel = st.selectbox("🔍 Ver Ficha Técnica de:", df['Ticker'])
            resena_text = resenas.get(ticker_sel, "Información en proceso de carga.")
            st.markdown(f'<div class="card"><b>{ticker_sel}</b>: {resena_text}</div>', unsafe_allow_html=True)
        with c_calc:
            st.subheader("🧮 Calculadora de Inversión")
            monto = st.number_input("Presupuesto (VES)", min_value=1.0, value=5000.0)
            acc_c = st.selectbox("Acción a simular:", df['Ticker'], key="calc_acc")
            pr = float(df[df['Ticker'] == acc_c]['Último Precio'].values)
            st.markdown(f'<div class="calc-card">Podrías comprar: <h2 style="color:#00FF41;">{int(monto//pr)} Acciones</h2><p>Comisión Est. (1%): {(monto*0.01):,.2f} VES</p></div>', unsafe_allow_html=True)

    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        st.write("### 📖 Glosario del Inversionista (BVC)")
        def term(t, e): st.markdown(f'<p><span class="term-title">{t}:</span> {e}</p>', unsafe_allow_html=True)
        with st.expander("🏛️ Términos Fundamentales"):
            term("Bolsa de Valores de Caracas (BVC)", "Institución donde se negocian títulos valores.")
            term("Casa de Bolsa", "Intermediario financiero necesario para operar.")
            term("Caja Venezolana de Valores (CVV)", "Depósito central donde se custodian tus acciones.")
            term("Acciones (Renta Variable)", "Partes del capital de una empresa.")
            term("IBC (Índice Bursátil Caracas)", "Principal indicador del mercado venezolano.")

    elif opcion == "🏢 Directorio Casas de Bolsa":
        st.markdown('<p class="main-header">Directorio 🏢</p>', unsafe_allow_html=True)
        c_sel = st.selectbox("Buscar Casa:", list(directorio_casas.keys()))
        inf = directorio_casas[c_sel]
        st.markdown(f'<div class="card"><p><span class="term-title">Nombre:</span> {c_sel}</p><p><span class="term-title">Rif:</span> {inf["rif"]}</p><p><span class="term-title">Descripción:</span> {inf["desc"]}</p><br><a href="{inf["web"]}" target="_blank" class="web-button">🌐 Visitar Web Oficial</a></div>', unsafe_allow_html=True)
