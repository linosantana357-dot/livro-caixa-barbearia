import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Renove Barbearia - Gestão", page_icon="💈", layout="wide")

# Estilo CSS Personalizado (Dark Premium / Gold & Charcoal)
st.markdown("""
<style>
    .main {
        background-color: #121212;
        color: #E0E0E0;
    }
    [data-testid="stMetric"] {
        background-color: #1E1E1E;
        border: 1px solid #333333;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #A0A0A0 !important;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #D4AF37 !important;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        border-radius: 8px;
        color: #A0A0A0;
        padding: 10px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #D4AF37 !important;
        color: #121212 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# TOPO COM LOGO E TÍTULO
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    try:
        st.image("logo.png", width=120)
    except:
        st.write("💈")

with col_titulo:
    st.title("Renove Barbearia — Gestão & Caixa")

st.markdown("---")

# Base de Dados na Sessão
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Data", "Tipo", "Categoria", "Descricao", "Valor", "Meio", "Clientes", "Comissao_Pct"
    ])

# MENU LATERAL
try:
    st.sidebar.image("logo.png", use_container_width=True)
except:
    pass

st.sidebar.header("➕ Novo Lançamento")
tipo = st.sidebar.selectbox("Tipo de Movimentação", ["Entrada", "Saída"])

if tipo == "Entrada":
    categoria = st.sidebar.selectbox("Categoria", ["Serviços", "Produtos", "Outros"])
    comissao_pct = st.sidebar.number_input("Comissão Colaborador (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
else:
    categoria = st.sidebar.selectbox("Categoria", ["Comissões", "Insumos", "Estrutura", "Manutenção", "Dízimo", "DAS-MEI", "Outros"])
    comissao_pct = 0.0

descricao = st.sidebar.text_input("Descrição (ex: Corte Social)")
valor = st.sidebar.number_input("Valor (R$)", min_value=0.0, value=0.0, step=5.0)
meio = st.sidebar.selectbox("Meio de Pagamento", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
clientes = st.sidebar.number_input("Atendimentos", min_value=0, value=1 if tipo == "Entrada" else 0)
data = st.sidebar.date_input("Data", datetime.today())

if st.sidebar.button("💾 Salvar Registro"):
    novo_dado = pd.DataFrame([{
        "Data": str(data),
        "Tipo": tipo,
        "Categoria": categoria,
        "Descricao": descricao,
        "Valor": valor,
        "Meio": meio,
        "Clientes": clientes,
        "Comissao_Pct": comissao_pct
    }])
    st.session_state.df = pd.concat([st.session_state.df, novo_dado], ignore_index=True)
    st.sidebar.success("Lançamento salvo!")

st.sidebar.markdown("---")
meta_mensal = st.sidebar.number_input("Target Meta Mensal (R$)", min_value=1000.0, value=5000.0, step=500.0)

df = st.session_state.df.copy()

if not df.empty:
    df["Data"] = pd.to_datetime(df["Data"])
    df["Ano_Mes"] = df["Data"].dt.strftime("%Y-%m")
    meses_disponiveis = df["Ano_Mes"].unique().tolist()
    mes_selecionado = st.sidebar.selectbox("Mês de Referência", meses_disponiveis, index=len(meses_disponiveis)-1)
    
    df_filtrado = df[df["Ano_Mes"] == mes_selecionado].copy()
    
    entradas = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Valor"].sum()
    saidas = df_filtrado[df_filtrado["Tipo"] == "Saída"]["Valor"].sum()
    
    dizimo = entradas * 0.10
    reserva_emergencia = entradas * 0.05
    manutencao = entradas * 0.05
    das_mei = 75.00
    
    df_filtrado["Valor_Comissao"] = (df_filtrado["Valor"] * df_filtrado["Comissao_Pct"]) / 100.0
    total_comissoes = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Valor_Comissao"].sum()
    
    lucro_liquido = entradas - saidas
    margem_lucro = (lucro_liquido / entradas * 100) if entradas > 0 else 0.0
    total_clientes = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Clientes"].sum()
    ticket_medio = (entradas / total_clientes) if total_clientes > 0 else 0.0

else:
    entradas = saidas = dizimo = reserva_emergencia = manutencao = total_comissoes = lucro_liquido = margem_lucro = ticket_medio = 0.0
    das_mei = 75.00
    total_clientes = 0
    df_filtrado = pd.DataFrame()

# NAVEGAÇÃO EM ABAS
aba1, aba2, aba3 = st.tabs(["📊 Visão Geral", "🛡️ Provisões & Metas", "📄 Lançamentos"])

with aba1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento Bruto", f"R$ {entradas:,.2f}")
    c2.metric("Total Despesas", f"R$ {saidas:,.2f}")
    c3.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}", delta=f"{margem_lucro:.1f}% Margem")
    
    c4, c5 = st.columns(2)
    c4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    c5.metric("Atendimentos", f"{total_clientes} clientes")
    
    st.markdown("---")
    
    if not df_filtrado.empty:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("📈 Fluxo Diário")
            df_graf = df_filtrado.copy()
            df_graf["Data_Dia"] = df_graf["Data"].dt.strftime("%Y-%m-%d")
            df_diario = df_graf.groupby(["Data_Dia", "Tipo"])["Valor"].sum().reset_index()
            fig_linha = px.line(df_diario, x="Data_Dia", y="Valor", color="Tipo", template="plotly_dark",
                                color_discrete_map={"Entrada": "#D4AF37", "Saída": "#EF553B"})
            st.plotly_chart(fig_linha, use_container_width=True)
        
        with col_g2:
            st.subheader("📊 Categorias")
            fig_pizza = px.pie(df_filtrado, values="Valor", names="Categoria", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig_pizza, use_container_width=True)

with aba2:
    st.subheader("🎯 Progresso da Meta")
    progresso = min(float(entradas / meta_mensal), 1.0) if meta_mensal > 0 else 0.0
    st.progress(progresso)
    st.caption(f"Alcançado: **R$ {entradas:,.2f}** de **R$ {meta_mensal:,.2f}** ({progresso * 100:.1f}%)")
    
    st.markdown("---")
    st.subheader("🛡️ Reservas Automáticas")
    p1, p2 = st.columns(2)
    p1.metric("Dízimo (10%)", f"R$ {dizimo:,.2f}")
    p2.metric("Reserva Emergência (5%)", f"R$ {reserva_emergencia:,.2f}")
    
    p3, p4, p5 = st.columns(3)
    p3.metric("Manutenção/Lâminas (5%)", f"R$ {manutencao:,.2f}")
    p4.metric("Repasse Colaboradores", f"R$ {total_comissoes:,.2f}")
    p5.metric("Provisão DAS-MEI", f"R$ {das_mei:,.2f}")

with aba3:
    st.subheader("📄 Histórico de Lançamentos")
    if not df_filtrado.empty:
        st.dataframe(df_filtrado.sort_values(by="Data", ascending=False), use_container_width=True)
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Relatório (CSV)", data=csv, file_name="caixa_barbearia.csv", mime="text/csv")
    else:
        st.info("Nenhum lançamento no período.")
