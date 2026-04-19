"""
Dashboard Streamlit - Análise de Churn em Tempo Real
======================================================
Dashboard interativo para monitoramento de KPIs de churn.
Execute: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


@st.cache_data
def load_data():
    """Carrega os dados processados."""
    df = pd.read_csv('data/processed/telco_churn_cleaned.csv')
    return df


def main():
    """Dashboard principal."""
    
    st.set_page_config(
        page_title="📊 Telecom Churn Analytics",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    df = load_data()
    
    st.title("📊 Dashboard de Análise de Churn")
    st.markdown("---")
    
    # SIDEBAR - Filtros
    st.sidebar.header("🔍 Filtros")
    
    contract_filter = st.sidebar.multiselect(
        "Tipo de Contrato",
        options=df['Contract'].unique(),
        default=df['Contract'].unique()
    )
    
    internet_filter = st.sidebar.multiselect(
        "Tipo de Internet",
        options=df['InternetService'].unique(),
        default=df['InternetService'].unique()
    )
    
    df_filtered = df[
        (df['Contract'].isin(contract_filter)) & 
        (df['InternetService'].isin(internet_filter))
    ]
    
    # KPIs PRINCIPAIS
    st.header("📈 Métricas Chave")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = len(df_filtered)
    churn_rate = df_filtered['Churn'].mean() * 100
    avg_tenure = df_filtered['tenure'].mean()
    avg_revenue = df_filtered['MonthlyCharges'].mean()
    
    col1.metric("Total de Clientes", f"{total_customers:,}")
    col2.metric("Taxa de Churn", f"{churn_rate:.1f}%", delta_color="inverse")
    col3.metric("Tempo Médio (meses)", f"{avg_tenure:.1f}")
    col4.metric("Receita Média Mensal", f"${avg_revenue:.2f}")
    
    st.markdown("---")
    
    # GRÁFICOS
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📋 Churn por Tipo de Contrato")
        contract_churn = df_filtered.groupby('Contract')['Churn'].agg(['sum', 'count'])
        contract_churn['rate'] = contract_churn['sum'] / contract_churn['count'] * 100
        fig_contract = px.bar(
            contract_churn, 
            x=contract_churn.index, 
            y='rate',
            color='rate',
            color_continuous_scale='RdYlGn_r',
            title="Taxa de Churn por Contrato"
        )
        st.plotly_chart(fig_contract, use_container_width=True)
    
    with col_right:
        st.subheader("🌐 Churn por Tipo de Internet")
        internet_churn = df_filtered.groupby('InternetService')['Churn'].mean() * 100
        fig_internet = px.pie(
            values=internet_churn.values,
            names=internet_churn.index,
            title="Distribuição de Churn"
        )
        st.plotly_chart(fig_internet, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💳 Churn por Método de Pagamento")
        payment_churn = df_filtered.groupby('PaymentMethod')['Churn'].mean() * 100
        fig_payment = px.bar(
            x=payment_churn.index,
            y=payment_churn.values,
            color=payment_churn.values,
            color_continuous_scale='RdYlGn_r',
            title="Taxa de Churn por Pagamento"
        )
        st.plotly_chart(fig_payment, use_container_width=True)
    
    with col2:
        st.subheader("⏱️ Distribuição de Tenure")
        fig_tenure = px.histogram(
            df_filtered, 
            x="tenure", 
            color="Churn",
            barmode="overlay",
            title="Distribuição de Tempo de Cliente"
        )
        st.plotly_chart(fig_tenure, use_container_width=True)
    
    # TABELA DE DADOS
    st.markdown("---")
    st.subheader("📊 Dados dos Clientes")
    
    st.dataframe(
        df_filtered.head(100),
        use_container_width=True
    )
    
    # DOWNLOAD
    st.download_button(
        label="📥 Download Dados Filtrados",
        data=df_filtered.to_csv(index=False),
        file_name="churn_filtered.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    main()