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

# 3. ESTILO CSS FUTURISTA (ACTUALIZADO PARA TEXTOS BLANCOS)
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    
    /* Forzar que todas las etiquetas (Usuario, Contraseña, etc.) sean blancas */
    label { 
        color: white !important; 
        font-weight: bold !important; 
        font-size: 1.1rem !important; 
    }
    
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; font-weight: bold; width: 100%; }
    .main-header { color: #D4AF37; font-size: 35px; font-weight: bold; margin: 0px; }
    .card { background-color: #002b56; padding: 12px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 5px; }
    .calc-card { background-color: #1a3a5a; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; }
    .gain { color: #00FF41; font-weight: bold; font-size: 18px; }
    .academy-tip { background-color: #1a3a5a; padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; font-style: italic; margin-bottom: 20px; }
    
    /* Estilo para los inputs para que se vean modernos */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #002b56;
        color: white;
        border: 1px solid #D4AF37;
    }
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

resenas = {
    "BNC": "Banco Universal con sólida presencia en el mercado nacional. Líder en depósitos del sector privado.",
    "RST": "Ron Santa Teresa: Empresa bicentenaria, referente del ron premium venezolano en el mundo.",
    "TPG": "Telefónica Venezolana: Innovación constante en servicios de conectividad y entretenimiento.",
    "BVL": "Banco de Venezuela: Principal red bancaria del país, clave en el sistema de pagos nacional.",
    "ABC.A": "Aceros Boada: Tradición y calidad en la industria metalúrgica del país."
}

# --- 5. LÓGICA DE LOGIN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.columns(3)[1].markdown(f'<img src="data:image/png;base64,{logo_b64}" width="200">' if logo_b64 else "", unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;" class="main-header">Acceso a Terminal FintWay</p>', unsafe_allow_html=True)
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("ACCEDER A LA RED"):
        if u == "admin" and p == "fintway2026": 
            st.session_state.logged_in = True
            st.rerun()
else:
    # --- SIDEBAR ---
    st.sidebar.title("Menú Principal")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy"])
    st.sidebar.divider()
    if st.sidebar.button("Cerrar Sesión"): 
        st.session_state.logged_in = False
        st.rerun()

    # --- PÁGINA 1: DASHBOARD ---
    if opcion == "📊 Dashboard de Mercado":
        c_logo, c_title = st.columns([1, 4])
        with c_logo:
             if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="80">', unsafe_allow_html=True)
        with c_title:
            st.markdown('<p class="main-header">Terminal de Inversión 🛰️</p>', unsafe_allow_html=True)
        
        st.divider()

        col_tabla, col_calc = st.columns(2)

        with col_tabla:
            st.subheader("📊 Acciones BVC")
            st.dataframe(df[['Ticker', 'Nombre de Acción', 'Último Precio']], use_container_width=True, hide_index=True)
            
            st.write("---")
            ticker_sel = st.selectbox("🔍 Ver Ficha Técnica de:", df['Ticker'])
            resena_text = resenas.get(ticker_sel, "Información en proceso de carga por la Casa de Bolsa.")
            st.markdown(f'<div class="card"><b>{ticker_sel}</b>: {resena_text}</div>', unsafe_allow_html=True)

        with col_calc:
            st.subheader("🧮 Calculadora de Inversión")
            monto = st.number_input("Presupuesto de inversión (VES)", min_value=1.0, value=5000.0)
            accion_calc = st.selectbox("Acción a simular compra:", df['Ticker'])
            
            precio_accion = df[df['Ticker'] == accion_calc]['Último Precio'].values[0]
            cantidad = int(monto // precio_accion)
            comision = (monto * 0.01)
            
            st.markdown(f"""
                <div class="calc-card">
                    <p>Con un capital de <b>{monto:,.2f} VES</b> obtendrías:</p>
                    <h2 style="color:#00FF41; margin:0;">{cantidad} Acciones</h2>
                    <p style="margin-top:10px;">Precio Ref: {precio_accion:,.2f} VES</p>
                    <p>Comisión Est. (1%): {comision:,.2f} VES</p>
                    <hr>
                    <p style="font-size:12px; color:#D4AF37;">Cifras calculadas según el último precio registrado.</p>
                </div>
            """, unsafe_allow_html=True)

    # --- PÁGINA 2: ACADEMIA ---
    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="academy-tip">💡 Tip: {random.choice(["El IBC es el promedio del mercado.", "Diversificar reduce el riesgo."])}</div>', unsafe_allow_html=True)
        
        st.write("### 📖 Glosario del Inversionista")
        with st.expander("🔸 IBC"): st.write("Índice Bursátil Caracas.")
        with st.expander("🔸 Renta Variable"): st.write("Instrumentos donde el retorno no está garantizado (Acciones).")
