<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview - Renove Barbearia</title>
    <style>
        :root {
            --bg-color: #121212;
            --card-bg: #1E1E1E;
            --border-color: #333333;
            --gold: #D4AF37;
            --text-color: #E0E0E0;
            --text-muted: #A0A0A0;
            --red: #EF553B;
            --green: #00CC96;
        }

        * {
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            justify-content: center;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            width: 100%;
        }

        /* Topo / Header */
        .header {
            display: flex;
            align-items: center;
            gap: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
        }

        .header img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid var(--gold);
        }

        .header h1 {
            font-size: 1.5rem;
            color: #FFFFFF;
            font-weight: 700;
        }

        /* Abas */
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }

        .tab-button {
            background-color: var(--card-bg);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }

        .tab-button.active {
            background-color: var(--gold);
            color: #121212;
            border-color: var(--gold);
        }

        /* Conteúdo das Abas */
        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Grid de Cards */
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }

        .card-label {
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 8px;
        }

        .card-value {
            font-size: 1.6rem;
            color: var(--gold);
            font-weight: 700;
        }

        .card-delta {
            font-size: 0.8rem;
            color: var(--green);
            margin-top: 5px;
        }

        /* Barra de Progresso */
        .progress-bar-container {
            background-color: var(--border-color);
            border-radius: 10px;
            height: 12px;
            width: 100%;
            overflow: hidden;
            margin: 12px 0 8px 0;
        }

        .progress-bar-fill {
            background-color: var(--gold);
            height: 100%;
            width: 43%; /* Exemplo de progresso */
            border-radius: 10px;
        }

        /* Tabela Exemplo */
        .table-container {
            width: 100%;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background-color: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
        }

        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
            font-size: 0.9rem;
        }

        th {
            background-color: #252525;
            color: var(--gold);
        }

        tr:last-child td {
            border-bottom: none;
        }

        .tag-entrada {
            color: var(--green);
            font-weight: bold;
        }

        .tag-saida {
            color: var(--red);
            font-weight: bold;
        }

        @media (max-width: 600px) {
            .header {
                flex-direction: column;
                text-align: center;
            }
            .grid-3, .grid-2 {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Header com Logo -->
    <div class="header">
        <img src="https://lh3.googleusercontent.com/d/1000295311.png" alt="Renove Barbearia Logo" onerror="this.src='https://via.placeholder.com/80/1E1E1E/D4AF37?text=💈'">
        <div>
            <h1>Renove Barbearia — Gestão & Caixa</h1>
            <p style="color: var(--text-muted); font-size: 0.9rem;">Painel de Controle Financeiro</p>
        </div>
    </div>

    <!-- Navegação por Abas -->
    <div class="tabs">
        <button class="tab-button active" onclick="switchTab('visao-geral', this)">📊 Visão Geral</button>
        <button class="tab-button" onclick="switchTab('provisoes', this)">🛡️ Provisões & Metas</button>
        <button class="tab-button" onclick="switchTab('lancamentos', this)">📄 Lançamentos</button>
    </div>

    <!-- Aba 1: Visão Geral -->
    <div id="visao-geral" class="tab-content active">
        <div class="grid-3">
            <div class="card">
                <div class="card-label">Faturamento Bruto</div>
                <div class="card-value">R$ 2.150,00</div>
            </div>
            <div class="card">
                <div class="card-label">Total Despesas</div>
                <div class="card-value" style="color: var(--red);">R$ 420,00</div>
            </div>
            <div class="card">
                <div class="card-label">Lucro Líquido</div>
                <div class="card-value">R$ 1.730,00</div>
                <div class="card-delta">↑ 80.5% Margem</div>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <div class="card-label">Ticket Médio</div>
                <div class="card-value">R$ 43,00</div>
            </div>
            <div class="card">
                <div class="card-label">Atendimentos Realizados</div>
                <div class="card-value">50 clientes</div>
            </div>
        </div>
    </div>

    <!-- Aba 2: Provisões & Metas -->
    <div id="provisoes" class="tab-content">
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-label">🎯 Progresso da Meta Mensal</div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill"></div>
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">Alcançado: <strong style="color: #FFF;">R$ 2.150,00</strong> de <strong style="color: #FFF;">R$ 5.000,00</strong> (43.0%)</p>
        </div>

        <h3 style="color: var(--gold); margin-bottom: 15px; font-size: 1.1rem;">🛡️ Reservas Automáticas</h3>
        
        <div class="grid-2">
            <div class="card">
                <div class="card-label">Dízimo (10%)</div>
                <div class="card-value">R$ 215,00</div>
            </div>
            <div class="card">
                <div class="card-label">Reserva de Emergência (5%)</div>
                <div class="card-value">R$ 107,50</div>
            </div>
        </div>

        <div class="grid-3">
            <div class="card">
                <div class="card-label">Manutenção / Lâminas (5%)</div>
                <div class="card-value">R$ 107,50</div>
            </div>
            <div class="card">
                <div class="card-label">Repasse Colaboradores</div>
                <div class="card-value">R$ 350,00</div>
            </div>
            <div class="card">
                <div class="card-label">Provisão DAS-MEI</div>
                <div class="card-value">R$ 75,00</div>
            </div>
        </div>
    </div>

    <!-- Aba 3: Lançamentos -->
    <div id="lancamentos" class="tab-content">
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Tipo</th>
                        <th>Categoria</th>
                        <th>Descrição</th>
                        <th>Valor</th>
                        <th>Pagamento</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>2026-04-18</td>
                        <td><span class="tag-entrada">Entrada</span></td>
                        <td>Serviços</td>
                        <td>Corte Social + Barba</td>
                        <td>R$ 60,00</td>
                        <td>Pix</td>
                    </tr>
                    <tr>
                        <td>2026-04-18</td>
                        <td><span class="tag-entrada">Entrada</span></td>
                        <td>Serviços</td>
                        <td>Corte Degradê</td>
                        <td>R$ 40,00</td>
                        <td>Cartão de Débito</td>
                    </tr>
                    <tr>
                        <td>2026-04-17</td>
                        <td><span class="tag-saida">Saída</span></td>
                        <td>Insumos</td>
                        <td>Lâminas e Pomadas</td>
                        <td>R$ 120,00</td>
                        <td>Pix</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
    function switchTab(tabId, element) {
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelectorAll('.tab-button').forEach(button => {
            button.classList.remove('active');
        });
        
        document.getElementById(tabId).classList.add('active');
        element.classList.add('active');
    }
</script>

</body>
</html>
