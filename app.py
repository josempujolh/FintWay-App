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

# --- 5. DATOS DIRECTORIO CASAS DE BOLSA (EXACTAMENTE COMO EL PDF) ---
directorio_casas = {
    "Solfin Casa de Bolsa, C.A": {
        "rif": "J-31049062-7",
        "desc": "Solfin, es una empresa que se basa en la calidad y excelencia, pensando siempre en la búsqueda de la rentabilidad apropiada, de acuerdo al perfil de cada uno de nuestros clientes. Somos una institución financiera de calidad institucional, soportada por inquebrantables valores éticos.",
        "dir": "Distrito Capital / Torre Oriental de Seguros, piso 1, Av. Venezuela, El Rosal Caracas.",
        "tel": "+58 212 953 8177",
        "mail": "info@solfin.com.ve",
        "web": "https://www.solfin.com.ve/"
    },
    "Acciona Casa de Bolsa, C.A.": {
        "rif": "J-50037354-6",
        "desc": "Nuestra innovadora propuesta de valor soportada en economías productivas y oportunidades globales digitales, nos posiciona como lideres en servicios bursátiles integrales.",
        "dir": "Distrito Capital / C.C. San Ignacio. Torre Copernico, La Castellana Caracas 1060.",
        "tel": "+58 02122617196",
        "mail": "info@accionavalores.com",
        "web": "https://accionavalores.com"
    },
    "Caja Caracas Casa de Bolsa, C.A.": {
        "rif": "J-30318305-0",
        "desc": "Proporcionamos soluciones globales en el área de servicios financieros a inversionistas y empresas en búsqueda de desarrollo estratégico.",
        "dir": "Distrito Capital / Av. Francisco de Miranda, Edif. Parque Cristal, Torre Este, Piso 2, Los Palos Grandes.",
        "tel": "+58 2122191818",
        "mail": "contactenos@cajacaracas.com",
        "web": "https://cajacaracas.com/"
    },
    "Per Capital Sociedad de Corretaje": {
        "rif": "J-500299516",
        "desc": "Empresa miembro de la Bolsa de Valores de Caracas, ofrece servicios de corretaje, gestión de inversiones y estructuración financiera con aplicación móvil.",
        "dir": "Distrito Capital / Av. Tamanaco, Torre Atlantic, Piso 5, El Rosal, Caracas.",
        "tel": "+58 4242824480",
        "mail": "info@per-capital.com",
        "web": "https://per-capital.com/"
    },
    "BNCI Casa de Bolsa, C.A.": {
        "rif": "J-50028351-2",
        "desc": "Institución que interconecta inversores con oportunidades de financiamiento en renta fija y variable, especialista en papeles comerciales.",
        "dir": "Miranda / Av. Blandin con San Felipe, Torre BNC La Castellana, Piso 1.",
        "tel": "+58 2129547830",
        "mail": "info@bnci-casadebolsa.com",
        "web": "https://bnci.com.ve"
    },
    "Fivenca Casa de Bolsa, C.A.": {
        "rif": "J-08501464-0",
        "desc": "Grupo financiero enfocado en desarrollar estrategias personalizadas con amplia experiencia en el mercado venezolano e internacional.",
        "dir": "Distrito Capital / Av. F. de Miranda, CC Lido, Torre C, Piso 5, El Rosal.",
        "tel": "+58 212-3075799",
        "mail": "atencionalcliente@grupofivenca.com",
        "web": "https://fivenca.com/"
    },
    "Mercosur Casa de Bolsa, C.A.": {
        "rif": "J-08501466-0",
        "desc": "Institución financiera joven y dinámica con el firme propósito de contribuir activamente en el desarrollo económico.",
        "dir": "Distrito Capital / Avenida Venezuela con Calle Mohedano, Torre JWM, Piso 6, El Rosal.",
        "tel": "+58 212 952 4165",
        "mail": "negocios@mercosur.com.ve",
        "web": "https://mercosur.com.ve/home/"
    },
    "Kaizen Casa de Bolsa, C.A": {
        "rif": "J-500199163",
        "desc": "Institución conformada por profesionales con gran trayectoria en el sector financiero y de consultoría.",
        "dir": "Distrito Capital / Av. Segunda, Edif. Torre Credival, Piso 4, Campo Alegre.",
        "tel": "+58 212 8148994",
        "mail": "info@kaizencasadebolsa.com",
        "web": "https://www.kaizencasadebolsa.com/"
    },
    "Mercantil Merinvest Casa de Bolsa": {
        "rif": "J-00300384-0",
        "desc": "Especializada en intermediación y gestión de inversiones desde 1987. Forma parte del holding Mercantil Servicios Financieros.",
        "dir": "Distrito Capital / Edf. Banco Mercantil, Piso 31, Urb. San Bernardino, Caracas.",
        "tel": "+58 0212 5032066",
        "mail": "ccdeinversion@mercantilmerinvest.com",
        "web": "https://www.mercantilmerinvest.com/"
    },
    "Rendivalores Casa de Bolsa, C.A.": {
        "rif": "J-30292237-2",
        "desc": "Más de 29 años de trayectoria exitosa ofreciendo una gama diversificada de productos y servicios financieros.",
        "dir": "Miranda / Av. San Felipe con 2da Transversal, Edif. Bancarias, Piso 9, La Castellana.",
        "tel": "+58 2122679909",
        "mail": "info@rendivalores.com",
        "web": "https://rendivalores.com/"
    },
    "Invercapital Casa de Bolsa, C.A.": {
        "rif": "J-31688953-0",
        "desc": "Ayuda a transformar ahorros en inversión, guiando en las distintas áreas del mercado y acompañando todo el proceso.",
        "dir": "Distrito Capital / Av. Francisco de Miranda, Torre Parque Cristal, Piso 5, Los Palos Grandes.",
        "tel": "+58 (212) 740.01.50",
        "mail": "comunicaciones@invercapital.com",
        "web": "https://invercapital.com/"
    },
    "World Trading Casa de Bolsa, C.A.": {
        "rif": "J-41253655-9",
        "desc": "Sociedad debidamente autorizada por la SUNAVAL, constituida para operar bajo las leyes de Venezuela.",
        "dir": "Edo. Miranda / Calle California Con Mucuchies, Residencias California, Piso 3, Las Mercedes.",
        "tel": "+02129940178",
        "mail": "worldtradingadmon@gmail.com",
        "web": "https://wtcasadebolsa.com/"
    }
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
    # --- SIDEBAR ---
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
        with col_calc:
            st.subheader("🧮 Calculadora de Inversión")
            monto = st.number_input("Presupuesto (VES)", min_value=1.0, value=5000.0)
            accion_c = st.selectbox("Acción a simular:", df['Ticker'], key="calc")
            precio = df[df['Ticker'] == accion_c]['Último Precio'].values
            st.markdown(f'<div class="calc-card">Podrías comprar: <h2 style="color:#00FF41;">{int(monto//precio)} Acciones</h2><p>Comisión Est. (1%): {(monto*0.01):,.2f} VES</p></div>', unsafe_allow_html=True)

    # --- PÁGINA 2: ACADEMIA ---
    elif opcion == "🎓 FintWay Academy":
        st.markdown('<p class="main-header">FintWay Academy 📚</p>', unsafe_allow_html=True)
        st.write("### 📖 Glosario del Inversionista (BVC)")
        def term(t, e): st.markdown(f'<p><span class="term-title">{t}:</span> {e}</p>', unsafe_allow_html=True)

        with st.expander("🏛️ Términos Fundamentales del Mercado"):
            term("Bolsa de Valores de Caracas (BVC)", "Institución privada donde se realizan las negociaciones.")
            term("Casa de Bolsa", "Intermediario financiero autorizado necesario para operar.")
            term("Caja Venezolana de Valores (CVV)", "Depósito central donde se custodian tus acciones.")
            term("Acciones (Renta Variable)", "Partes del capital de una empresa.")
            term("IBC (Índice Bursátil Caracas)", "Principal indicador del mercado.")
            term("Mercado Primario", "Emisión de acciones por primera vez.")
            term("Mercado Secundario", "Negociación entre inversionistas.")

        with st.expander("💰 Términos de Valoración"):
            term("Dividendos", "Distribución de utilidades.")
            term("Ganancia de Capital", "Diferencia entre precio de venta y compra.")
            term("Papeles Comerciales", "Deuda a corto plazo.")
            term("Rendimiento", "Ganancia o pérdida porcentual.")

    # --- PÁGINA 3: DIRECTORIO (ORDENADO Y DORADO) ---
    elif opcion == "🏢 Directorio Casas de Bolsa":
        st.markdown('<p class="main-header">Directorio de Casas de Bolsa 🏢</p>', unsafe_allow_html=True)
        
        # Mantenemos el orden original del PDF
        casa_sel = st.selectbox("Buscar Casa de Bolsa:", list(directorio_casas.keys()))
        info = directorio_casas[casa_sel]
        
        st.markdown(f"""
            <div class="card">
                <p><span class="term-title">Nombre de Casa de Bolsa:</span> {casa_sel}</p>
                <p><span class="term-title">Rif:</span> {info['rif']}</p>
                <p><span class="term-title">Descripción:</span> {info['desc']}</p>
                <p><span class="term-title">Dirección:</span> {info['dir']}</p>
                <p><span class="term-title">Contacto:</span> {info['tel']}</p>
                <p><span class="term-title">Email:</span> {info['mail']}</p>
                <br>
                <a href="{info['web']}" target="_blank" class="web-button">🌐 Visitar Página Web Oficial</a>
            </div>
        """, unsafe_allow_html=True)
