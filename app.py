import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from supabase import create_client, Client


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Renove Barbearia - Gestão",
    page_icon="💈",
    layout="wide"
)


# ============================================================
# CONEXÃO COM SUPABASE
# ============================================================

@st.cache_resource
def conectar_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]

    return create_client(url, key)


try:
    supabase = conectar_supabase()
except Exception as e:
    st.error("❌ Não foi possível conectar ao banco de dados.")
    st.code(str(e))
    st.stop()


# ============================================================
# FUNÇÕES DO BANCO DE DADOS
# ============================================================

def carregar_lancamentos():

    resposta = (
        supabase
        .table("lancamentos")
        .select("*")
        .order("data", desc=True)
        .order("id", desc=True)
        .execute()
    )

    dados = resposta.data

    if not dados:
        return pd.DataFrame(columns=[
            "id",
            "data",
            "tipo",
            "categoria",
            "descricao",
            "valor",
            "meio",
            "clientes",
            "comissao_pct",
            "criado_em"
        ])

    df = pd.DataFrame(dados)

    return df


def salvar_lancamento(
    data,
    tipo,
    categoria,
    descricao,
    valor,
    meio,
    clientes,
    comissao_pct
):

    dados = {
        "data": str(data),
        "tipo": tipo,
        "categoria": categoria,
        "descricao": descricao,
        "valor": float(valor),
        "meio": meio,
        "clientes": int(clientes),
        "comissao_pct": float(comissao_pct)
    }

    resposta = (
        supabase
        .table("lancamentos")
        .insert(dados)
        .execute()
    )

    return resposta


def excluir_lancamento(id_lancamento):

    resposta = (
        supabase
        .table("lancamentos")
        .delete()
        .eq("id", id_lancamento)
        .execute()
    )

    return resposta


# ============================================================
# CSS
# ============================================================

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


# ============================================================
# TOPO
# ============================================================

col_logo, col_titulo = st.columns([1, 4])

with col_logo:

    try:
        st.image("logo.png", width=120)
    except:
        st.write("💈")


with col_titulo:

    st.title("Renove Barbearia — Gestão & Caixa")


st.markdown("---")


# ============================================================
# CARREGAR DADOS DO SUPABASE
# ============================================================

try:

    df = carregar_lancamentos()

except Exception as e:

    st.error("❌ Erro ao carregar os lançamentos.")

    st.code(str(e))

    st.stop()


# ============================================================
# MENU LATERAL
# ============================================================

try:

    st.sidebar.image(
        "logo.png",
        use_container_width=True
    )

except:
    pass


st.sidebar.header("➕ Novo Lançamento")


tipo = st.sidebar.selectbox(
    "Tipo de Movimentação",
    ["Entrada", "Saída"]
)


# ============================================================
# CATEGORIAS
# ============================================================

if tipo == "Entrada":

    categoria = st.sidebar.selectbox(
        "Categoria",
        [
            "Serviços",
            "Produtos",
            "Outros"
        ]
    )

    comissao_pct = st.sidebar.number_input(
        "Comissão Colaborador (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=5.0
    )

else:

    categoria = st.sidebar.selectbox(
        "Categoria",
        [
            "Comissões",
            "Insumos",
            "Estrutura",
            "Manutenção",
            "Dízimo",
            "DAS-MEI",
            "Outros"
        ]
    )

    comissao_pct = 0.0


# ============================================================
# CAMPOS
# ============================================================

descricao = st.sidebar.text_input(
    "Descrição (ex: Corte Social)"
)


valor = st.sidebar.number_input(
    "Valor (R$)",
    min_value=0.0,
    value=0.0,
    step=5.0
)


meio = st.sidebar.selectbox(
    "Meio de Pagamento",
    [
        "Pix",
        "Cartão de Crédito",
        "Cartão de Débito",
        "Dinheiro"
    ]
)


clientes = st.sidebar.number_input(
    "Atendimentos",
    min_value=0,
    value=1 if tipo == "Entrada" else 0,
    step=1
)


data = st.sidebar.date_input(
    "Data",
    datetime.today()
)


# ============================================================
# SALVAR LANÇAMENTO
# ============================================================

if st.sidebar.button(
    "💾 Salvar Registro",
    use_container_width=True
):

    if valor <= 0:

        st.sidebar.error(
            "Informe um valor maior que R$ 0,00."
        )

    elif descricao.strip() == "":

        st.sidebar.error(
            "Informe uma descrição."
        )

    else:

        try:

            salvar_lancamento(
                data=data,
                tipo=tipo,
                categoria=categoria,
                descricao=descricao,
                valor=valor,
                meio=meio,
                clientes=clientes,
                comissao_pct=comissao_pct
            )

            st.sidebar.success(
                "✅ Lançamento salvo permanentemente!"
            )

            st.rerun()

        except Exception as e:

            st.sidebar.error(
                "❌ Erro ao salvar lançamento."
            )

            st.sidebar.code(str(e))


# ============================================================
# META MENSAL
# ============================================================

meta_mensal = st.sidebar.number_input(
    "Target Meta Mensal (R$)",
    min_value=1000.0,
    value=5000.0,
    step=500.0
)


# ============================================================
# TRATAMENTO DOS DADOS
# ============================================================

if not df.empty:

    df["data"] = pd.to_datetime(df["data"])

    df["ano_mes"] = df["data"].dt.strftime("%Y-%m")

    meses_disponiveis = (
        df["ano_mes"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

else:

    meses_disponiveis = []


# ============================================================
# SELEÇÃO DO MÊS
# ============================================================

if meses_disponiveis:

    mes_selecionado = st.sidebar.selectbox(
        "Mês de Referência",
        meses_disponiveis,
        index=len(meses_disponiveis) - 1
    )

    df_filtrado = df[
        df["ano_mes"] == mes_selecionado
    ].copy()

else:

    df_filtrado = pd.DataFrame()


# ============================================================
# CÁLCULOS
# ============================================================

if not df_filtrado.empty:

    entradas = df_filtrado[
        df_filtrado["tipo"] == "Entrada"
    ]["valor"].sum()

    saidas = df_filtrado[
        df_filtrado["tipo"] == "Saída"
    ]["valor"].sum()

    dizimo = entradas * 0.10

    reserva_emergencia = entradas * 0.05

    manutencao = entradas * 0.05

    das_mei = 75.00

    df_filtrado["valor_comissao"] = (
        df_filtrado["valor"]
        * df_filtrado["comissao_pct"]
        / 100.0
    )

    total_comissoes = df_filtrado[
        df_filtrado["tipo"] == "Entrada"
    ]["valor_comissao"].sum()

    lucro_liquido = entradas - saidas

    margem_lucro = (
        lucro_liquido / entradas * 100
        if entradas > 0
        else 0.0
    )

    total_clientes = df_filtrado[
        df_filtrado["tipo"] == "Entrada"
    ]["clientes"].sum()

    ticket_medio = (
        entradas / total_clientes
        if total_clientes > 0
        else 0.0
    )

else:

    entradas = 0.0
    saidas = 0.0
    dizimo = 0.0
    reserva_emergencia = 0.0
    manutencao = 0.0
    total_comissoes = 0.0
    lucro_liquido = 0.0
    margem_lucro = 0.0
    ticket_medio = 0.0
    total_clientes = 0
    das_mei = 75.00


# ============================================================
# ABAS
# ============================================================

aba1, aba2, aba3 = st.tabs([
    "📊 Visão Geral",
    "🛡️ Provisões & Metas",
    "📄 Lançamentos"
])


# ============================================================
# ABA 1 — VISÃO GERAL
# ============================================================

with aba1:

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Faturamento Bruto",
        f"R$ {entradas:,.2f}"
    )

    c2.metric(
        "Total Despesas",
        f"R$ {saidas:,.2f}"
    )

    c3.metric(
        "Lucro Líquido",
        f"R$ {lucro_liquido:,.2f}",
        delta=f"{margem_lucro:.1f}% Margem"
    )


    c4, c5 = st.columns(2)

    c4.metric(
        "Ticket Médio",
        f"R$ {ticket_medio:,.2f}"
    )

    c5.metric(
        "Atendimentos",
        f"{total_clientes} clientes"
    )


    st.markdown("---")


    # ========================================================
    # GRÁFICOS
    # ========================================================

    if not df_filtrado.empty:

        col_g1, col_g2 = st.columns(2)


        # ----------------------------------------------------
        # FLUXO DIÁRIO
        # ----------------------------------------------------

        with col_g1:

            st.subheader("📈 Fluxo Diário")

            df_graf = df_filtrado.copy()

            df_graf["data_dia"] = (
                df_graf["data"]
                .dt.strftime("%Y-%m-%d")
            )

            df_diario = (
                df_graf
                .groupby(
                    ["data_dia", "tipo"]
                )["valor"]
                .sum()
                .reset_index()
            )

            fig_linha = px.line(
                df_diario,
                x="data_dia",
                y="valor",
                color="tipo",
                template="plotly_dark",
                color_discrete_map={
                    "Entrada": "#D4AF37",
                    "Saída": "#EF553B"
                }
            )

            st.plotly_chart(
                fig_linha,
                use_container_width=True
            )


        # ----------------------------------------------------
        # CATEGORIAS
        # ----------------------------------------------------

        with col_g2:

            st.subheader("📊 Categorias")

            fig_pizza = px.pie(
                df_filtrado,
                values="valor",
                names="categoria",
                hole=0.4,
                template="plotly_dark"
            )

            st.plotly_chart(
                fig_pizza,
                use_container_width=True
            )


# ============================================================
# ABA 2 — PROVISÕES E METAS
# ============================================================

with aba2:

    st.subheader("🎯 Progresso da Meta")


    progresso = (
        min(float(entradas / meta_mensal), 1.0)
        if meta_mensal > 0
        else 0.0
    )


    st.progress(progresso)


    st.caption(
        f"Alcançado: **R$ {entradas:,.2f}** "
        f"de **R$ {meta_mensal:,.2f}** "
        f"({progresso * 100:.1f}%)"
    )


    st.markdown("---")


    st.subheader("🛡️ Reservas Automáticas")


    p1, p2 = st.columns(2)


    p1.metric(
        "Dízimo (10%)",
        f"R$ {dizimo:,.2f}"
    )


    p2.metric(
        "Reserva Emergência (5%)",
        f"R$ {reserva_emergencia:,.2f}"
    )


    p3, p4, p5 = st.columns(3)


    p3.metric(
        "Manutenção/Lâminas (5%)",
        f"R$ {manutencao:,.2f}"
    )


    p4.metric(
        "Repasse Colaboradores",
        f"R$ {total_comissoes:,.2f}"
    )


    p5.metric(
        "Provisão DAS-MEI",
        f"R$ {das_mei:,.2f}"
    )


# ============================================================
# ABA 3 — LANÇAMENTOS
# ============================================================

with aba3:

    st.subheader("📄 Histórico de Lançamentos")


    if not df_filtrado.empty:

        # ----------------------------------------------------
        # TABELA VISUAL
        # ----------------------------------------------------

        tabela = df_filtrado.copy()


        tabela["data"] = (
            tabela["data"]
            .dt.strftime("%d/%m/%Y")
        )


        tabela = tabela.rename(
            columns={
                "id": "ID",
                "data": "Data",
                "tipo": "Tipo",
                "categoria": "Categoria",
                "descricao": "Descrição",
                "valor": "Valor",
                "meio": "Pagamento",
                "clientes": "Atendimentos",
                "comissao_pct": "Comissão %",
                "valor_comissao": "Comissão R$"
            }
        )


        colunas_mostrar = [
            "ID",
            "Data",
            "Tipo",
            "Categoria",
            "Descrição",
            "Valor",
            "Pagamento",
            "Atendimentos",
            "Comissão %",
            "Comissão R$"
        ]


        st.dataframe(
            tabela[colunas_mostrar],
            use_container_width=True,
            hide_index=True
        )


        # ----------------------------------------------------
        # DOWNLOAD CSV
        # ----------------------------------------------------

        csv = df_filtrado.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            "📥 Baixar Relatório (CSV)",
            data=csv,
            file_name="caixa_barbearia.csv",
            mime="text/csv",
            use_container_width=True
        )


        # ----------------------------------------------------
        # EXCLUIR LANÇAMENTO
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader("🗑️ Excluir lançamento")


        ids = df_filtrado["id"].tolist()


        id_excluir = st.selectbox(
            "Selecione o lançamento pelo ID",
            ids
        )


        if st.button(
            "🗑️ Excluir lançamento selecionado",
            type="secondary"
        ):

            try:

                excluir_lancamento(
                    id_excluir
                )

                st.success(
                    f"✅ Lançamento #{id_excluir} excluído."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    "❌ Erro ao excluir lançamento."
                )

                st.code(str(e))


    else:

        st.info(
            "Nenhum lançamento no período."
    )
