# Análise de Churn de Clientes - Telecom

[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat&logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-1.8K+)](https://pandas.pydata.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.56+-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Sobre o Projeto

Projeto completo de análise de churn (cancelamento) de clientes para o setor de telecomunicações. Demonstra competências em Python, análise exploratória de dados (EDA), visualização e construção de dashboards interativos.

## KPIs Identificados

| Métrica | Valor |
|--------|-------|
| Taxa de Churn | 35.94% |
| Total de Clientes | 64 |
| Clientes Perdidos | 23 |
| Ticket Médio Mensal | R$ 64.49 |

## Principais Insights

- **Contrato Month-to-Month**: 65.7% de churn (alto risco)
- **Internet Fiber**: 40% de churn
- **Electronic Check**: 73.7% de churn (forma de pagamento de maior risco)
- **Contratos Two Year**: 0% de churn (clientes fieis)

## Tecnologias e Competências

### Python & Dados
- Manipulação de dados com **Pandas** e **NumPy**
- Limpeza e transformação de dados
- Feature Engineering
- Análise estatística

### Visualização
- **Matplotlib** e **Seaborn**
- Gráficos interativos
- Matrizes de correlação

### Dashboard & API
- **Streamlit** - Dashboard interativo
- **Flask** - API REST
- Deploy local

### Metodologias
- EDA (Análise Exploratória de Dados)
- Análise de cohortes
- Análise de correlação

## Como Executar

```bash
# Clone o repositório
git clone https://github.com/joaocastelo1/Analise-de-Churn-de-Clientes-em-Telecom.git

# Instale as dependências
pip install -r projeto_churn_telecom/requirements.txt

# Execute o pipeline de análise
cd projeto_churn_telecom
python main.py

# Execute o dashboard
streamlit run dashboard_streamlit.py
```

## Estrutura do Projeto

```
projeto_churn_telecom/
├── data/
│   ├── raw/                 # Dados brutos
│   ├── processed/           # Dados processados
│   └── telecom_limpo.csv    # Dados limpos
├── src/
│   ├── analysis/            # Análise EDA
│   └── data/               # Limpeza de dados
├── reports/
│   └── figures/            # Gráficos gerados
├── dashboard_streamlit.py  # Dashboard interativo
├── api_flask.py           # API REST
└── main.py                # Pipeline principal
```

## Contato

<a href="mailto:jcrocap2@gmail.com">
  <img src="https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=gmail&logoColor=white" alt="Gmail"/>
</a>

<a href="https://linkedin.com/in/joaocastelo1">
  <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn"/>
</a>

---

*Projeto desenvolvido para demostrar competências em análise de dados e Python para oportunidades profissionais.*