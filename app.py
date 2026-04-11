import streamlit as st
import pandas as pd
import os
import base64
import plotly.express as px # Nueva librería para gráficos futuristas

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="FintWay - Terminal Financiera", layout="wide")

# LÓGICA DE RUTA PARA EL LOGO
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "logo.png")

def get_base64_logo(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64_logo(logo_path)

# CSS VIBE FUTURISTA
st.markdown("""
    <style>
    .stApp { background-color: #001f3f; color: #ffffff; }
    .stButton>button { 
        background-color: #D4AF37; color: black; 
        border-radius: 5px; border: none; font-weight: bold; width: 100%;
    }
    .main-header { color: #D4AF37; font-size: 38px; font-weight: bold; margin: 0px; }
    .card { 
        background-color: #002b56; padding: 15px; 
        border-radius: 10px; border-left: 5px solid #D4AF37;
        margin-bottom: 10px;
    }
    .gain { color: #00FF41; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS DE MERCADO ---
data_market = {
    'Ticker': ['TPG', 'BNC', 'ABC.A', 'MVZ.A', 'FVI.B', 'IVC', 'PGR', 'CANTV'],
    'Nombre': ['Telefónica', 'Banco Nac. de Crédito', 'Aceros Boada', 'Mercantil', 'Fondo de Val.', 'Inm. Valcro', 'Progreso', 'CANTV'],
    'Ultimo': [8.50, 2.15, 45.00, 110.50, 12.30, 5.40, 0.85, 3.20],
    'Cierre_Ant': [7.76, 2.14, 45.00, 110.00, 12.10, 5.35, 0.98, 3.20],
    'VNeg': [15200, 45800, 1200, 3400, 8900, 5400, 2100, 15000],
    'Compra': [8.45, 2.14, 44.50, 110.10, 12.25, 5.30, 0.80, 3.15],
    'Venta': [8.55, 2.16, 45.50, 110.90, 12.35, 5.45, 0.90, 3.25]
}
df = pd.DataFrame(data_market)
df['Var%'] = ((df['Ultimo'] - df['Cierre_Ant']) / df['Cierre_Ant'] * 100).round(2)

# DATOS HISTÓRICOS IBC (Simulados para el gráfico)
df_ibc = pd.DataFrame({
    'Fecha': ['06/04', '07/04', '08/04', '09/04', '10/04'],
    'Puntos': [5120, 5340, 5280, 5410, 5246.47]
})

# --- LÓGICA DE LOGIN ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="200">', unsafe_allow_html=True)
    u = st.text_input("Usuario"); p = st.text_input("Contraseña", type="password")
    if st.button("ACCEDER"):
        if u == "admin" and p == "fintway2026":
            st.session_state.logged_in = True
            st.rerun()
else:
    # --- DASHBOARD ---
    c1, c2 = st.columns([1, 4])
    with c1:
        if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="100">', unsafe_allow_html=True)
    with c2:
        st.markdown('<p class="main-header">FintWay Terminal 🛰️</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # 1. TOP GAINERS e IBC
    col_g, col_chart = st.columns([2, 1])
    
    with col_g:
        st.subheader("🚀 Top Gainers (BVC)")
        tg = df.sort_values(by='Var%', ascending=False).head(2)
        for _, row in tg.iterrows():
            st.markdown(f'<div class="card"><h3 style="margin:0;">{row["Ticker"]}</h3><p class="gain">+{row["Var%"]}%</p></div>', unsafe_allow_html=True)

    with col_chart:
        st.subheader("📈 Índice IBC")
        fig = px.line(df_ibc, x='Fecha', y='Puntos', markers=True)
        fig.update_traces(line_color='#00FF41', marker=dict(size=8, color='#D4AF37'))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color="white", margin=dict(l=0, r=0, t=30, b=0), height=180,
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 2. TABLA PRINCIPAL
    st.subheader("📊 Mercado por Volumen (VNeg)")
    st.dataframe(df.sort_values(by='VNeg', ascending=False), use_container_width=True, hide_index=True)

    # 3. SIDEBAR
    st.sidebar.title("Operaciones")
    if logo_b64: st.sidebar.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="150">', unsafe_allow_html=True)
    casa = st.sidebar.selectbox("Casa de Bolsa:", ["Mercantil Merinvest", "BNCI", "Ratio", "Fivenca"])
    if st.sidebar.button("GENERAR ORDEN DE COMPRA"):
        st.sidebar.success(f"Orden lista para {casa}")