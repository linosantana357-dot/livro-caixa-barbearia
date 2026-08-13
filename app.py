import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Livro Caixa Inteligente - Barbearia", layout="wide")

st.title("💈 Livro Caixa Inteligente & Painel de Crescimento")
st.markdown("---")

# Inicialização da base de dados em memória
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame([
        {"Data": "2026-08-01", "Tipo": "Entrada", "Categoria": "Serviços", "Descricao": "Cortes e Barbas", "Valor": 450.0, "Meio": "Pix", "Clientes": 10},
        {"Data": "2026-08-01", "Tipo": "Saída", "Categoria": "Comissões", "Descricao": "Repasse equipe", "Valor": 225.0, "Meio": "Pix", "Clientes": 0},
        {"Data": "2026-08-02", "Tipo": "Entrada", "Categoria": "Serviços", "Descricao": "Combos + Pigmentação", "Valor": 680.0, "Meio": "Cartão", "Clientes": 12},
        {"Data": "2026-08-02", "Tipo": "Entrada", "Categoria": "Produtos", "Descricao": "Pomadas e Óleos", "Valor": 140.0, "Meio": "Dinheiro", "Clientes": 4},
        {"Data": "2026-08-03", "Tipo": "Saída", "Categoria": "Estrutura", "Descricao": "Conta de Energia", "Valor": 320.0, "Meio": "Pix", "Clientes": 0},
        {"Data": "2026-08-04", "Tipo": "Entrada", "Categoria": "Serviços", "Descricao": "Atendimentos do dia", "Valor": 820.0, "Meio": "Pix", "Clientes": 18},
        {"Data": "2026-08-04", "Tipo": "Saída", "Categoria": "Insumos", "Descricao": "Lâminas e cremes", "Valor": 90.0, "Meio": "Cartão", "Clientes": 0},
    ])

# --- BARRA LATERAL: NOVO LANÇAMENTO ---
st.sidebar.header("➕ Novo Lançamento")
tipo = st.sidebar.selectbox("Tipo de Movimentação", ["Entrada", "Saída"])

if tipo == "Entrada":
    categoria = st.sidebar.selectbox("Categoria", ["Serviços", "Produtos", "Outros"])
else:
    categoria = st.sidebar.selectbox("Categoria", ["Comissões", "Insumos", "Estrutura", "Manutenção", "Outros"])

descricao = st.sidebar.text_input("Descrição (ex: 5 Cortes social)")
valor = st.sidebar.number_input("Valor R$", min_value=0.0, value=50.0, step=5.0)
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
        "Clientes": clientes
    }])
    st.session_state.df = pd.concat([st.session_state.df, novo_dado], ignore_index=True)
    st.sidebar.success("Lançamento adicionado com sucesso!")

# --- CÁLCULOS E KPIS ---
df = st.session_state.df
df["Data"] = pd.to_datetime(df["Data"])

entradas = df[df["Tipo"] == "Entrada"]["Valor"].sum()
saidas = df[df["Tipo"] == "Saída"]["Valor"].sum()
lucro_liquido = entradas - saidas
margem_lucro = (lucro_liquido / entradas * 100) if entradas > 0 else 0.0

total_clientes = df[df["Tipo"] == "Entrada"]["Clientes"].sum()
ticket_medio = (entradas / total_clientes) if total_clientes > 0 else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Faturamento Bruto", f"R$ {entradas:,.2f}")
col2.metric("Total Despesas", f"R$ {saidas:,.2f}")
col3.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}", delta=f"{margem_lucro:.1f}% Margem")
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
col5.metric("Atendimentos", f"{total_clientes} clientes")

st.markdown("---")

# --- GRÁFICOS DE DESEMPENHO E CRESCIMENTO ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("📈 Evolução Financeira Diária (Entradas vs Saídas)")
    df_diario = df.groupby(["Data", "Tipo"])["Valor"].sum().reset_index()
    fig_linha = px.line(
        df_diario, 
        x="Data", 
        y="Valor", 
        color="Tipo", 
        markers=True,
        color_discrete_map={"Entrada": "#00CC96", "Saída": "#EF553B"}
    )
    st.plotly_chart(fig_linha, use_container_width=True)

with col_graf2:
    st.subheader("📊 Distribuição de Receitas e Despesas por Categoria")
    fig_pizza = px.pie(df, values="Valor", names="Categoria", hole=0.4, title="Participação por Categoria")
    st.plotly_chart(fig_pizza, use_container_width=True)

# --- TABELA DE HISTÓRICO ---
st.subheader("📄 Histórico de Lançamentos")
st.dataframe(df.sort_values(by="Data", ascending=False), use_container_width=True)
