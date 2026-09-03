import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Livro Caixa Inteligente - Barbearia", layout="wide")

st.title("💈 Livro Caixa Inteligente & Painel de Crescimento")
st.markdown("---")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
            "Data", "Tipo", "Categoria", "Descricao", "Valor", "Meio", "Clientes"
                ])

                st.sidebar.header("➕ Novo Lançamento")
                tipo = st.sidebar.selectbox("Tipo de Movimentação", ["Entrada", "Saída"])

                if tipo == "Entrada":
                    categoria = st.sidebar.selectbox("Categoria", ["Serviços", "Produtos", "Outros"])
                    else:
                        categoria = st.sidebar.selectbox("Categoria", ["Comissões", "Insumos", "Estrutura", "Manutenção", "Outros"])

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
                                                                                    "Clientes": clientes
                                                                                        }])
                                                                                            st.session_state.df = pd.concat([st.session_state.df, novo_dado], ignore_index=True)
                                                                                                st.sidebar.success("Lançamento adicionado com sucesso!")

                                                                                                df = st.session_state.df

                                                                                                if not df.empty:
                                                                                                    df["Data"] = pd.to_datetime(df["Data"])
                                                                                                        entradas = df[df["Tipo"] == "Entrada"]["Valor"].sum()
                                                                                                            saidas = df[df["Tipo"] == "Saída"]["Valor"].sum()
                                                                                                                lucro_liquido = entradas - saidas
                                                                                                                    margem_lucro = (lucro_liquido / entradas * 100) if entradas > 0 else 0.0
                                                                                                                        total_clientes = df[df["Tipo"] == "Entrada"]["Clientes"].sum()
                                                                                                                            ticket_medio = (entradas / total_clientes) if total_clientes > 0 else 0.0
                                                                                                                            else:
                                                                                                                                entradas = 0.0
                                                                                                                                    saidas = 0.0
                                                                                                                                        lucro_liquido = 0.0
                                                                                                                                            margem_lucro = 0.0
                                                                                                                                                total_clientes = 0
                                                                                                                                                    ticket_medio = 0.0

                                                                                                                                                    col1, col2, col3, col4, col5 = st.columns(5)
                                                                                                                                                    col1.metric("Faturamento Bruto", f"R$ {entradas:,.2f}")
                                                                                                                                                    col2.metric("Total Despesas", f"R$ {saidas:,.2f}")
                                                                                                                                                    col3.metric("Lucro Líquido", f"R$ {lucro_liquido:,.2f}", delta=f"{margem_lucro:.1f}% Margem")
                                                                                                                                                    col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
                                                                                                                                                    col5.metric("Atendimentos", f"{total_clientes} clientes")

                                                                                                                                                    st.markdown("---")

                                                                                                                                                    if not df.empty:
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

                                                                                                                                                                                                                                                                                                            st.subheader("📄 Histórico de Lançamentos")
                                                                                                                                                                                                                                                                                                                st.dataframe(df.sort_values(by="Data", ascending=False), use_container_width=True)
                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                    st.info("Nenhum lançamento cadastrado ainda. Utilize o menu lateral para adicionar a primeira movimentação!")
                                                                                                                                                                                                                                                                                                                    