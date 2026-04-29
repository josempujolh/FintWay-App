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

# 3. ESTILO CSS FUTURISTA
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    label { color: white !important; font-weight: bold !important; }
    .main-header { color: #D4AF37; font-size: 42px; font-weight: bold; text-align: center; margin-top: 10px; }
    .welcome-text { color: #D4AF37; font-size: 28px; text-align: center; margin-bottom: 30px; font-weight: bold; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; border: none; font-weight: bold; width: 100%; height: 45px; }
    .intro-card { 
        background-color: #002b56; padding: 0px; border-radius: 15px; border: 1px solid #D4AF37; 
        text-align: center; min-height: 320px; overflow: hidden; display: flex; flex-direction: column;
        transition: transform 0.3s, box-shadow 0.3s; margin: 0 auto; max-width: 280px; 
    }
    .intro-card:hover { transform: translateY(-10px); box-shadow: 0px 10px 20px rgba(212, 175, 55, 0.4); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #001529; color: #D4AF37; text-align: center; padding: 10px; font-size: 14px; border-top: 1px solid #D4AF37; z-index: 100; }
    .card { background-color: #002b56; padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 10px; }
    .calc-card { background-color: #1a3a5a; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; }
    .gain { color: #00FF41; font-weight: bold; }
    .term-title { color: #D4AF37; font-weight: bold; }
    .web-button { display: inline-block; padding: 10px 20px; background-color: #D4AF37; color: black !important; text-decoration: none !important; border-radius: 5px; font-weight: bold; margin-top: 10px; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #002b56; color: white; border: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. GESTIÓN DE ESTADOS Y DATOS ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'perfil_completado' not in st.session_state: st.session_state.perfil_completado = False
if 'tipo_inversionista' not in st.session_state: st.session_state.tipo_inversionista = None

data_market = {
    'Ticker': ['ABC.A', 'BNC', 'BPV', 'BYCC', 'BVL', 'CCP.B', 'DOM', 'ENY', 'MVZ.B', 'RST', 'RST.B', 'SVS', 'TPG', 'IBC'],
    'Nombre de Acción': ['Aceros Boada', 'Bco Nac. de Crédito', 'Bco Provincial', 'Bolsa de Caracas', 'Bco de Venezuela', 'Corp. Capriles B', 'Domínguez & Cía', 'Envases Venezolanos', 'Mercantil B', 'Ron Santa Teresa', 'Ron Santa Teresa B', 'Sivensa', 'Telefónica', 'Índice IBC'],
    'Último Precio': [1610.00, 1500.00, 126.40, 670.00, 1729.00, 503.00, 690.00, 710.00, 6800.00, 545.46, 400.00, 1160.00, 19.00, 5835.16],
    'Cierre Anterior': [1610.00, 1455.00, 127.01, 679.00, 1729.00, 503.00, 696.00, 705.00, 7092.92, 545.46, 399.71, 1150.00, 20.00, 5246.47]
}
df = pd.DataFrame(data_market)
df['Var%'] = ((df['Último Precio'] - df['Cierre Anterior']) / df['Cierre Anterior'] * 100).round(2)

# --- 5. LÓGICA DE FLUJO ---

# CASO A: LANDING PAGE
if not st.session_state.logged_in:
    if logo_b64: st.markdown(f'<div style="display: flex; justify-content: center; margin-top: 20px;"><img src="data:image/png;base64,{logo_b64}" width="220"></div>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-text">Tu camino financiero más sencillo</p>', unsafe_allow_html=True)
    col_ah, col_ap, col_in = st.columns(3)
    with col_ah:
        if img_ahorra: st.markdown(f'<div class="intro-card"><img src="data:image/png;base64,{img_ahorra}" width="100%"><div style="padding:10px;"><h3>Ahorra</h3><p>Protege tu capital hoy</p></div></div>', unsafe_allow_html=True)
    with col_ap:
        if img_aprende: st.markdown(f'<div class="intro-card"><img src="data:image/png;base64,{img_aprende}" width="100%"><div style="padding:10px;"><h3>Aprende</h3><p>Domina términos básicos</p></div></div>', unsafe_allow_html=True)
    with col_in:
        if img_invierte: st.markdown(f'<div class="intro-card"><img src="data:image/png;base64,{img_invierte}" width="100%"><div style="padding:10px;"><h3>AInvierte</h3><p>Multiplica tus ahorros con IA</p></div></div>', unsafe_allow_html=True)
    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f2:
        u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER"):
            if u == "admin" and p == "fintway2026": st.session_state.logged_in = True; st.rerun()
    st.markdown('<div class="footer">🛡️ Seguridad Garantizada | FintWay Terminal 2026</div>', unsafe_allow_html=True)

# CASO B: TEST DE PERFIL (Solo tras Login)
elif st.session_state.logged_in and not st.session_state.perfil_completado:
    st.markdown('<p class="main-header">Descubre tu Perfil Inversionista 🛰️</p>', unsafe_allow_html=True)
    with st.form("test_perfil"):
        p1 = st.radio("1. Experiencia previa:", ["Ninguna", "Alguna", "Frecuente"])
        p2 = st.radio("2. Objetivo:", ["Protección", "Equilibrio", "Crecimiento"])
        p3 = st.radio("3. Reacción a caída del 10%:", ["Vender", "Esperar", "Comprar más"])
        p4 = st.radio("4. ¿Sigue el IBC?", ["No", "A veces", "Diario"])
        p5 = st.radio("5. Capital a invertir:", ["<10%", "10-30%", ">50%"])
        p6 = st.radio("6. Plazo:", ["Corto", "Medio", "Largo"])
        p7 = st.radio("7. Diferencia Renta Fija/Variable:", ["No", "Un poco", "Si"])
        p8 = st.radio("8. ¿Tiene Casa de Bolsa?", ["No", "En proceso", "Si"])
        p9 = st.radio("9. Información financiera:", ["No", "Redes", "Estados Financieros"])
        p10 = st.radio("10. Rendimiento esperado:", ["Bajo", "Medio", "Alto"])
        if st.form_submit_button("CALCULAR PERFIL"):
            st.session_state.tipo_inversionista = random.choice(["Novato", "Intermedio", "Avanzado"]) # Lógica simplificada
            st.session_state.perfil_completado = True; st.rerun()

# CASO C: ACCESO TOTAL A LA TERMINAL (Desbloqueado)
else:
    st.sidebar.title(f"Perfil: {st.session_state.tipo_inversionista}")
    if logo_b64: st.sidebar.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="120"></div>', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard", "🎓 Academy", "🏢 Directorio"])
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False; st.session_state.perfil_completado = False; st.rerun()

    if opcion == "📊 Dashboard":
        st.markdown(f'<p class="main-header">Terminal {st.session_state.tipo_inversionista} 🛰️</p>', unsafe_allow_html=True)
        # Top Gainers
        tg = df.sort_values(by='Var%', ascending=False).head(4)
        cols_tg = st.columns(4)
        for i, (_, r) in enumerate(tg.iterrows()):
            cols_tg[i].markdown(f'<div class="card"><h4>{r["Ticker"]}</h4><p class="gain">+{r["Var%"]}%</p></div>', unsafe_allow_html=True)
        # Tabla y Calculadora
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Bolsa de Caracas")
            st.dataframe(df[['Ticker', 'Nombre de Acción', 'Último Precio']], use_container_width=True, hide_index=True)
        with c2:
            st.subheader("Calculadora")
            m = st.number_input("Monto (VES)", min_value=1.0, value=1000.0)
            a = st.selectbox("Acción:", df['Ticker'])
            p = float(df[df['Ticker']==a]['Último Precio'].values)
            st.markdown(f'<div class="calc-card">Obtendrías: <h2 style="color:#00FF41;">{int(m//p)} Acciones</h2></div>', unsafe_allow_html=True)

    elif opcion == "🎓 Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        def term(t, e): st.markdown(f'<p><span class="term-title">{t}:</span> {e}</p>', unsafe_allow_html=True)
        with st.expander("🏛️ Términos Fundamentales"):
            term("Bolsa de Valores de Caracas (BVC)", "Institución donde se negocian títulos valores.")
            term("Casa de Bolsa", "Intermediario financiero necesario para operar.")
            term("Caja Venezolana de Valores (CVV)", "Lugar donde se custodian tus acciones.")

    elif opcion == "🏢 Directorio":
        st.markdown('<p class="main-header">Directorio 🏢</p>', unsafe_allow_html=True)
        # (Aquí irían tus 12 casas de bolsa con formato dorado/blanco)
        st.info("Directorio de Casas de Bolsa desbloqueado.")
