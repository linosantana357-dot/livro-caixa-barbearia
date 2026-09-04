import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Livro Caixa - Barbearia", layout="wide")

st.title("💈 Livro Caixa Inteligente & Painel de Gestão")
st.markdown("---")

# Base de Dados na Sessão
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "Data", "Tipo", "Categoria", "Descricao", "Valor", "Meio", "Clientes", "Comissao_Pct"
    ])

# --- MENU LATERAL: NOVO LANÇAMENTO ---
st.sidebar.header("➕ Novo Lançamento")
tipo = st.sidebar.selectbox("Tipo de Movimentação", ["Entrada", "Saída"])

if tipo == "Entrada":
    categoria = st.sidebar.selectbox("Categoria", ["Serviços", "Produtos", "Outros"])
    comissao_pct = st.sidebar.number_input("Comissão do Colaborador (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
else:
    categoria = st.sidebar.selectbox("Categoria", ["Comissões", "Insumos", "Estrutura", "Manutenção", "Dízimo", "DAS-MEI", "Outros"])
    comissao_pct = 0.0

descricao = st.sidebar.text_input("Descrição (ex: Corte Social / Pomada)")
valor = st.sidebar.number_input("Valor R$", min_value=0.0, value=0.0, step=5.0)
meio = st.sidebar.selectbox("Meio de Pagamento", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
clientes = st.sidebar.number_input("Atendimentos (se houver)", min_value=0, value=1 if tipo == "Entrada" else 0)
data = st.sidebar.date_input("Data", datetime.today())

if st.sidebar.button("Salvar Registro"):
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
    st.sidebar.success("Lançamento adicionado com sucesso!")

# --- CONFIGURAÇÕES DE METAS & PROVISÕES NO MENU ---
st.sidebar.markdown("---")
st.sidebar.header("🎯 Metas & Gestão")
meta_mensal = st.sidebar.number_input("Meta de Faturamento Mensal (R$)", min_value=1000.0, value=5000.0, step=500.0)

df = st.session_state.df.copy()

if not df.empty:
    df["Data"] = pd.to_datetime(df["Data"])
    
    # --- FILTRO POR MÊS/ANO ---
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtro de Período")
    df["Ano_Mes"] = df["Data"].dt.strftime("%Y-%m")
    meses_disponiveis = df["Ano_Mes"].unique().tolist()
    mes_selecionado = st.sidebar.selectbox("Selecione o Mês", meses_disponiveis, index=len(meses_disponiveis)-1)
    
    df_filtrado = df[df["Ano_Mes"] == mes_selecionado].copy()
    
    # Cálculos Principais
    entradas = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Valor"].sum()
    saidas = df_filtrado[df_filtrado["Tipo"] == "Saída"]["Valor"].sum()
    
    # Provisões Automáticas
    dizimo = entradas * 0.10
    reserva_emergencia = entradas * 0.05
    manutencao_depreciacao = entradas * 0.05
    das_mei = 75.00  # Estimativa DAS-MEI
    
    # Cálculo de Comissões a Pagar aos Colaboradores
    df_filtrado["Valor_Comissao"] = (df_filtrado["Valor"] * df_filtrado["Comissao_Pct"]) / 100.0
    total_comissoes = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Valor_Comissao"].sum()
    
    lucro_liquido = entradas - saidas
    margem_lucro = (lucro_liquido / entradas * 100) if entradas > 0 else 0.0
    total_clientes = df_filtrado[df_filtrado["Tipo"] == "Entrada"]["Clientes"].sum()
    ticket_medio = (entradas / total_clientes) if total_clientes > 0 else 0.0

else:
    entradas = saidas = dizimo = reserva_emergencia = manutencao_depreciacao = total_comissoes = lucro_liquido = margem_lucro = ticket_medio = 0.0
    das_mei = 75.00
    total_clientes = 0
    df_filtrado = pd.DataFrame()

# --- PAINEL DE MÉTRICAS PRINCIPAIS ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Faturamento Bruto", f"R$ {entradas:,.2f}")
col2.metric("Total Despesas", f"R$ {saidas:,.2f}")
col3.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}", delta=f"{margem_lucro:.1f}% Margem")
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
col5.metric("Atendimentos", f"{total_clientes} clientes")

st.markdown("---")

# --- MÓDULO DE PROVISÕES E MENSALIDADES ---
st.subheader("🛡️ Provisões Financeiras & Reservas Automáticas")
p1, p2, p3, p4, p5 = st.columns(5)
p1.metric("Dízimo (10%)", f"R$ {dizimo:,.2f}")
p2.metric("Reserva Emergência (5%)", f"R$ {reserva_emergencia:,.2f}")
p3.metric("Manutenção/Lâminas (5%)", f"R$ {manutencao_depreciacao:,.2f}")
p4.metric("Repasse Colaboradores", f"R$ {total_comissoes:,.2f}")
p5.metric("Provisão DAS-MEI", f"R$ {das_mei:,.2f}")

st.markdown("---")

# --- BARRA DE PROGRESSO DE METAS ---
st.subheader("🎯 Progresso da Meta Mensal")
progresso = min(float(entradas / meta_mensal), 1.0) if meta_mensal > 0 else 0.0
st.progress(progresso)
st.caption(f"Alcançado: **R$ {entradas:,.2f}** de **R$ {meta_mensal:,.2f}** ({progresso * 100:.1f}%)")

st.markdown("---")

# --- GRÁFICOS & TABELA ---
if not df_filtrado.empty:
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("📈 Evolução Financeira Diária")
        df_graf = df_filtrado.copy()
        df_graf["Data_Dia"] = df_graf["Data"].dt.strftime("%Y-%m-%d")
        df_diario = df_graf.groupby(["Data_Dia", "Tipo"])["Valor"].sum().reset_index()
        fig_linha = px.line(
            df_diario, 
            x="Data_Dia", 
            y="Valor", 
            color="Tipo", 
            markers=True,
            color_discrete_map={"Entrada": "#00CC96", "Saída": "#EF553B"}
        )
        st.plotly_chart(fig_linha, use_container_width=True)

    with col_graf2:
        st.subheader("📊 Distribuição por Categoria")
        fig_pizza = px.pie(df_filtrado, values="Valor", names="Categoria", hole=0.4)
        st.plotly_chart(fig_pizza, use_container_width=True)

    st.subheader("📄 Histórico de Lançamentos")
    st.dataframe(df_filtrado.sort_values(by="Data", ascending=False), use_container_width=True)

    # --- BOTÃO DE EXPORTAÇÃO (BACKUP) ---
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Relatório (CSV/Excel)",
        data=csv,
        file_name=f"livro_caixa_{datetime.today().strftime('%Y_%m_%d')}.csv",
        mime="text/csv",
    )
else:
    st.info("Nenhum lançamento cadastrado para este período!")
