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
    .card { background-color: #002b56; padding: 12px; border-radius: 10px; border-left: 5px solid #D4AF37; margin-bottom: 5px; }
    .calc-card { background-color: #1a3a5a; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37; }
    .gain { color: #00FF41; font-weight: bold; font-size: 18px; }
    .academy-tip { background-color: #1a3a5a; padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; font-style: italic; margin-bottom: 20px; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { background-color: #002b56; color: white; border: 1px solid #D4AF37; }
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
df['Var%'] = ((df['Último Precio'] - df['Cierre Anterior']) / df['Cierre Anterior'] * 100).round(2)

resenas = {
    "BNC": "Banco Universal enfocado en banca comercial. Líder en depósitos del sector privado.",
    "RST": "Ron Santa Teresa: Empresa bicentenaria, referente del ron premium venezolano.",
    "TPG": "Telefónica Venezolana (Movistar). Líder en servicios de telecomunicaciones.",
    "BVL": "Banco de Venezuela: La institución financiera más grande del país.",
    "ABC.A": "Aceros Boada: Tradición y calidad en la industria metalúrgica."
}

# --- 5. LÓGICA DE LOGIN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    c_log1, c_log2, c_log3 = st.columns(3)
    with c_log2:
        if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="200">', unsafe_allow_html=True)
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
        c_logo, c_title = st.columns(2)
        with c_logo:
             if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="80">', unsafe_allow_html=True)
        with c_title:
            st.markdown('<p class="main-header">FintWay Terminal 🛰️</p>', unsafe_allow_html=True)
        
        st.divider()

        # TOP GAINERS
        st.subheader("🚀 Top Gainers (BVC)")
        top_4 = df.sort_values(by='Var%', ascending=False).head(4)
        cols_gain = st.columns(4)
        for i, (idx, row) in enumerate(top_4.iterrows()):
            with cols_gain[i]:
                st.markdown(f'<div class="card"><h4 style="margin:0;">{row["Ticker"]}</h4><p class="gain">+{row["Var%"]}%</p><p style="margin:0; font-size:14px;">{row["Último Precio"]} VES</p></div>', unsafe_allow_html=True)

        st.write("---")

        col_tabla, col_calc = st.columns(2)

        with col_tabla:
            st.subheader("📊 Acciones BVC")
            st.dataframe(df[['Ticker', 'Nombre de Acción', 'Último Precio', 'Cierre Anterior']], use_container_width=True, hide_index=True)
            
            st.write("---")
            ticker_sel = st.selectbox("🔍 Ver Ficha Técnica de:", df['Ticker'])
            resena_text = resenas.get(ticker_sel, "Información técnica en proceso de actualización.")
            st.markdown(f'<div class="card"><b>{ticker_sel}</b>: {resena_text}</div>', unsafe_allow_html=True)

        with col_calc:
            st.subheader("🧮 Calculadora de Inversión")
            monto = st.number_input("Presupuesto de inversión (VES)", min_value=1.0, value=5000.0)
            accion_calc = st.selectbox("Acción a simular compra:", df['Ticker'], key="calc_tab")
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
        st.write("### 📖 Glosario del Inversionista (BVC)")
        
        # CATEGORÍA 1: MERCADO
        with st.expander("🏛️ Términos Fundamentales del Mercado"):
            st.write("**Bolsa de Valores de Caracas (BVC):** Institución privada donde se realizan las negociaciones de títulos valores (acciones, bonos, papeles comerciales) en Venezuela, operando principalmente a través del Sistema Integrado Bursátil Electrónico (SIBE).")
            st.write("**Casa de Bolsa:** Intermediario financiero autorizado (corredor de bolsa) necesario para comprar o vender acciones. Son los únicos autorizados para operar en la BVC.")
            st.write("**Caja Venezolana de Valores (CVV):** Depósito central de los títulos valores. Es el lugar donde se registran, custodian y traspasan las acciones que compras, garantizando la seguridad de tu propiedad.")
            st.write("**Acciones (Renta Variable):** Partes alícuotas del capital de una empresa. Al comprar acciones, te haces socio (accionista) participando en sus ganancias o pérdidas.")
            st.write("**IBC (Índice Bursátil Caracas):** Principal indicador de la BVC. Mide el comportamiento promedio del precio de las acciones más negociadas.")
            st.write("**Mercado Primario:** Cuando una empresa emite acciones o bonos por primera vez para financiarse.")
            st.write("**Mercado Secundario:** Donde se compran y venden acciones ya emitidas entre inversionistas.")

        # CATEGORÍA 2: VALORACIÓN
        with st.expander("💰 Términos de Valoración y Retorno"):
            st.write("**Dividendos:** Distribución de parte de las utilidades de una empresa entre sus accionistas, pagados en dinero o en más acciones.")
            st.write("**Ganancia de Capital:** La diferencia positiva entre el precio de venta de una acción y su precio de compra original.")
            st.write("**Papeles Comerciales (Renta Fija):** Instrumentos de deuda a corto plazo emitidos por empresas para obtener liquidez con una tasa de interés conocida.")
            st.write("**Rendimiento:** La ganancia o pérdida porcentual obtenida en una inversión en un periodo de tiempo.")

        # CATEGORÍA 3: GESTIÓN DE RIESGO
        with st.expander("🛡️ Conceptos para la Gestión de Riesgo"):
            st.write("**Bursatilidad:** Medida de qué tan fácil es comprar o vender una acción sin alterar significativamente su precio.")
            st.write("**Diversificación:** Estrategia de no poner todo el dinero en una sola empresa o sector. 'No poner todos los huevos en la misma canasta'.")
            st.write("**Volatilidad:** La frecuencia e intensidad de los cambios de precio de una acción.")
            st.write("**Inflación/Cobertura:** Uso de activos bursátiles para proteger el poder adquisitivo del dinero frente al aumento de precios.")

        st.info("💡 Consejo: Dominar estos términos te permitirá tomar decisiones más acertadas en la Terminal.")
