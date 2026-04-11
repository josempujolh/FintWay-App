import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay Terminal", layout="wide")

# LÓGICA DE LOGO
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.png")
def get_base64_logo(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None
logo_b64 = get_base64_logo(logo_path)

# ESTILO CSS
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 5px; font-weight: bold; width: 100%; }
    .main-header { color: #D4AF37; font-size: 35px; font-weight: bold; margin: 0px; }
    .card { background-color: #002b56; padding: 12px; border-radius: 10px; border-left: 4px solid #D4AF37; margin-bottom: 5px; }
    .gain { color: #00FF41; font-weight: bold; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS CORREGIDOS SPRINT 2 ---
data_market = {
    'Ticker': ['TPG', 'BNC', 'MVZ.A', 'MVZ.B', 'BVL', 'RST', 'FVI.B', 'ABC.A', 'IVC', 'CANTV', 'BPV', 'G_DOM', 'CRM.A'],
    'Nombre': ['Telefónica', 'Bco Nac de Crédito', 'Mercantil A', 'Mercantil B', 'Bco de Venezuela', 'Ron Santa Teresa', 'Fondo de Valores', 'Aceros Boada', 'Inm. Valcro', 'CANTV', 'Bco Provincial', 'Domínguez & Cía', 'Corimon'],
    'Ultimo': [8.50, 2.15, 110.50, 108.20, 15.30, 9.45, 12.30, 45.00, 5.40, 3.20, 22.10, 7.80, 4.10],
    'Cierre_Ant': [7.76, 2.14, 110.00, 108.00, 14.80, 9.10, 12.10, 45.00, 5.35, 3.20, 21.50, 7.90, 4.05],
    'VNeg': [12500, 45000, 8900, 7200, 31000, 15600, 12000, 500, 2100, 18000, 9500, 4300, 6700], # Datos corregidos
    'Compra': [8.45, 2.14, 110.10, 108.10, 15.20, 9.40, 12.25, 44.50, 5.30, 3.15, 22.00, 7.70, 4.00],
    'Venta': [8.55, 2.16, 110.90, 108.90, 15.40, 9.50, 12.35, 45.50, 5.45, 3.25, 22.20, 7.90, 4.20]
}
df = pd.DataFrame(data_market)
df['Var%'] = ((df['Ultimo'] - df['Cierre_Ant']) / df['Cierre_Ant'] * 100).round(2)

lista_casas = sorted([
    "Mercantil Merinvest", "BNCI", "Ratio Sociedad de Corretaje", "Rendivalores", "Fivenca",
    "Provivienda", "BNC Casa de Bolsa", "Banctrust", "Interbursa", "Kastillo", "Maximum",
    "Valores Vencred", "Activalores", "Albus", "Andalucía", "Arbi", "Caracas", "Citibank", 
    "Deustche Bank", "Eurobursa", "Finagentes", "GNB", "Global Service", "Invercapital", 
    "Multinvest", "Oriental", "Puma", "Statera"
])

# --- DASHBOARD ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="200">', unsafe_allow_html=True)
    u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
    if st.button("ACCEDER"):
        if u == "admin" and p == "fintway2026": st.session_state.logged_in = True; st.rerun()
else:
    c1, c2 = st.columns([1, 4])
    with c1: 
        if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="90">', unsafe_allow_html=True)
    with c2: st.markdown('<p class="main-header">FintWay Terminal 🛰️</p>', unsafe_allow_html=True)
    
    st.divider()

    # 1. TOP GAINERS EXPANDIDO (4 tarjetas)
    st.subheader("🚀 Top Gainers (BVC)")
    top_4 = df.sort_values(by='Var%', ascending=False).head(4)
    cols_gain = st.columns(4)
    for i, (idx, row) in enumerate(top_4.iterrows()):
        with cols_gain[i]:
            st.markdown(f'<div class="card"><h4 style="margin:0;">{row["Ticker"]}</h4><p class="gain">+{row["Var%"]}%</p><p style="margin:0; font-size:14px;">{row["Ultimo"]} VES</p></div>', unsafe_allow_html=True)

    # 2. IBC E INFO
    col_chart, col_info = st.columns([2, 1])
    with col_chart:
        df_ibc = pd.DataFrame({'Fecha': ['06/04', '07/04', '08/04', '09/04', '10/04'], 'Puntos': [5120, 5340, 5280, 5410, 5246.47]})
        fig = px.line(df_ibc, x='Fecha', y='Puntos', title="Desempeño IBC")
        fig.update_traces(line_color='#00FF41'); fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=200)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        st.info("💡 Tip: Revisa el volumen (VNeg) para asegurar liquidez en tus operaciones.")

    # 3. TABLA
    st.subheader("📊 Mercado por Volumen de Negociación")
    st.dataframe(df.sort_values(by='VNeg', ascending=False), use_container_width=True, hide_index=True)

    # 4. SIDEBAR
    st.sidebar.title("Operaciones")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    casa_sel = st.sidebar.selectbox("Casa de Bolsa:", lista_casas)
    st.sidebar.button("GENERAR ORDEN DE COMPRA")
    if st.sidebar.button("Cerrar Sesión"): st.session_state.logged_in = False; st.rerun()