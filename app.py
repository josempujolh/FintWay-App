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

# 3. ESTILO CSS FUTURISTA (Dorado, Blanco, Azul)
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
    .academy-tip { background-color: #1a3a5a; padding: 15px; border-radius: 10px; border: 1px solid #D4AF37; font-style: italic; margin-bottom: 20px; }
    .web-button {
        display: inline-block; padding: 10px 20px; background-color: #D4AF37; color: black !important;
        text-decoration: none !important; border-radius: 5px; font-weight: bold; margin-top: 10px;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #002b56; color: white; border: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATOS DE MERCADO Y RESEÑAS ---
data_market = {
    'Ticker': ['ABC.A', 'BNC', 'BPV', 'BYCC', 'BVL', 'CCP.B', 'DOM', 'ENY', 'MVZ.B', 'RST', 'RST.B', 'SVS', 'TPG'],
    'Nombre de Acción': ['Aceros Boada', 'Bco Nac. de Crédito', 'Bco Provincial', 'Bolsa de Caracas', 'Bco de Venezuela', 'Corp. Capriles B', 'Domínguez & Cía', 'Envases Venezolanos', 'Mercantil B', 'Ron Santa Teresa', 'Ron Santa Teresa B', 'Sivensa', 'Telefónica'],
    'Último Precio': [1610.00, 1500.00, 126.40, 670.00, 1729.00, 503.00, 690.00, 710.00, 6800.00, 545.46, 400.00, 1160.00, 19.00],
    'Cierre Anterior': [1610.00, 1455.00, 127.01, 679.00, 1729.00, 503.00, 696.00, 705.00, 7092.92, 545.46, 399.71, 1150.00, 20.00]
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

# --- 5. DATOS DIRECTORIO CASAS DE BOLSA ---
directorio_casas = {
    "Mercantil Merinvest": {"desc": "Líder en el mercado de valores venezolano, ofreciendo servicios de corretaje y asesoría financiera.", "web": "https://mercantilmerinvest.com"},
    "BNCI Casa de Bolsa": {"desc": "Especialistas en intermediación de títulos valores y gestión de portafolios.", "web": "https://bnci.com.ve"},
    "Ratio Casa de Bolsa": {"desc": "Enfocados en brindar soluciones de inversión estratégicas en el mercado de capitales.", "web": "https://ratiocasadobolsa.com"},
    "Rendivalores": {"desc": "Casa de Bolsa destacada por su plataforma tecnológica y análisis de mercado.", "web": "https://rendivalores.com"},
    "Fivenca": {"desc": "Institución financiera dedicada a la gestión de activos y asesoría bursátil.", "web": "https://fivenca.com"},
    "BNC Casa de Bolsa": {"desc": "Filial del BNC, enfocada en la democratización del acceso al mercado de valores.", "web": "https://bncenlinea.com"},
    "Banctrust": {"desc": "Especialistas en banca de inversión y mercados emergentes.", "web": "https://banctrust.com"},
    "Interbursa": {"desc": "Corretaje de títulos valores con enfoque en atención personalizada.", "web": "https://interbursa.com.ve"},
    "Valores Vencred": {"desc": "Sólida ética profesional, ofreciendo custodia y negociación de activos.", "web": "https://valoresvencred.com"},
    "Activalores": {"desc": "Expertos en estructuración de emisiones y corretaje de acciones en la BVC.", "web": "https://activalores.com"}
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
    # --- SIDEBAR NAVEGACIÓN ---
    st.sidebar.title("Menú Principal")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    opcion = st.sidebar.radio("Navegación:", ["📊 Dashboard de Mercado", "🎓 FintWay Academy", "🏢 Directorio Casas de Bolsa"])
    st.sidebar.divider()
    if st.sidebar.button("Cerrar Sesión"): 
        st.session_state.logged_in = False
        st.rerun()

    # --- PÁGINA 1: DASHBOARD ---
    if opcion == "📊 Dashboard de Mercado":
        c_logo, c_title = st.columns(2)
        with c_logo:
             if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="80">', unsafe_allow_html=True)
        with c_title: st.markdown('<p class="main-header">FintWay Terminal 🛰️</p>', unsafe_allow_html=True)
        st.divider()

        st.subheader("🚀 Top Gainers (BVC)")
        top_4 = df.sort_values(by='Var%', ascending=False).head(4)
        cols_gain = st.columns(4)
        for i, (idx, row) in enumerate(top_4.iterrows()):
            with cols_gain[i]:
                st.markdown(f'<div class="card"><h4 style="margin:0;">{row["Ticker"]}</h4><p class="gain">+{row["Var%"]}%</p></div>', unsafe_allow_html=True)

        col_tabla, col_calc = st.columns(2)
        with col_tabla:
            st.subheader("📊 Acciones Bolsa de Valores de Caracas")
            st.dataframe(df[['Ticker', 'Nombre de Acción', 'Último Precio', 'Cierre Anterior']], use_container_width=True, hide_index=True)
            st.write("---")
            ticker_sel = st.selectbox("🔍 Ver Ficha Técnica de:", df['Ticker'])
            resena_text = resenas.get(ticker_sel, "Información técnica en proceso de actualización.")
            st.markdown(f'<div class="card"><b>{ticker_sel}</b>: {resena_text}</div>', unsafe_allow_html=True)
        with col_calc:
            st.subheader("🧮 Calculadora de Inversión")
            monto = st.number_input("Presupuesto (VES)", min_value=1.0, value=5000.0)
            accion_c = st.selectbox("Acción a simular:", df['Ticker'], key="calc")
            precio = df[df['Ticker'] == accion_c]['Último Precio'].values[0]
            st.markdown(f'<div class="calc-card">Podrías comprar: <h2 style="color:#00FF41;">{int(monto//precio)} Acciones</h2><p>Comisión Est. (1%): {(monto*0.01):,.2f} VES</p></div>', unsafe_allow_html=True)

    # --- PÁGINA 2: ACADEMIA (RECUPERADA) ---
    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        tips = ["El IBC mide las 15 mayores empresas.", "Diversificar reduce el riesgo."]
        st.markdown(f'<div class="academy-tip">💡 Tip: {random.choice(tips)}</div>', unsafe_allow_html=True)
        
        st.write("### 📖 Glosario del Inversionista (BVC)")
        def term(t, e): st.markdown(f'<p><span class="term-title">{t}:</span> {e}</p>', unsafe_allow_html=True)

        with st.expander("🏛️ Términos Fundamentales del Mercado"):
            term("Bolsa de Valores de Caracas (BVC)", "Institución donde se realizan las negociaciones de títulos valores.")
            term("Casa de Bolsa", "Intermediario financiero autorizado necesario para operar en la BVC.")
            term("Caja Venezolana de Valores (CVV)", "Depósito central donde se custodian y registran tus acciones.")
            term("Acciones (Renta Variable)", "Partes del capital de una empresa. Te haces socio de la misma.")
            term("IBC (Índice Bursátil Caracas)", "Principal indicador que mide el comportamiento promedio del mercado.")
            term("Mercado Primario", "Emisión de acciones por primera vez.")
            term("Mercado Secundario", "Negociación de acciones ya existentes entre inversionistas.")

        with st.expander("💰 Términos de Valoración y Retorno"):
            term("Dividendos", "Distribución de utilidades de la empresa entre sus accionistas.")
            term("Ganancia de Capital", "Diferencia positiva entre el precio de venta y el de compra.")
            term("Papeles Comerciales (Renta Fija)", "Deuda a corto plazo con tasa de interés conocida.")
            term("Rendimiento", "Ganancia o pérdida porcentual obtenida.")

        with st.expander("🛡️ Gestión de Riesgo"):
            term("Bursatilidad", "Facilidad para comprar o vender una acción sin afectar su precio.")
            term("Diversificación", "Estrategia de repartir el capital para reducir riesgos.")
            term("Volatilidad", "Intensidad de los cambios de precio de una acción.")
            term("Inflación/Cobertura", "Uso de activos para proteger el poder adquisitivo.")

    # --- PÁGINA 3: DIRECTORIO ---
    elif opcion == "🏢 Directorio Casas de Bolsa":
        st.markdown('<p class="main-header">Directorio de Casas de Bolsa 🏢</p>', unsafe_allow_html=True)
        casa_sel = st.selectbox("Buscar Casa de Bolsa:", list(directorio_casas.keys()))
        info = directorio_casas[casa_sel]
        st.markdown(f'<div class="card"><h3 style="color:#D4AF37;">{casa_sel}</h3><p>{info["desc"]}</p><br><a href="{info["web"]}" target="_blank" class="web-button">🌐 Visitar Página Web</a></div>', unsafe_allow_html=True)
