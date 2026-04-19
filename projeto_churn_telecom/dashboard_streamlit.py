import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Telecom Churn Dashboard", page_icon="chart:", layout="wide")

st.title("Telecom Customer Churn Analysis")
st.markdown("Dashboard interativo para analise de churn de clientes")

@st.cache_data
def load_data():
    return pd.read_csv('data/telecom_limpo.csv')

df = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["Geral", "Planos e Contratos", "Satisfacao", "Regional"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    churn_rate = df['churn'].mean() * 100
    col1.metric("Taxa de Churn", f"{churn_rate:.1f}%")
    col2.metric("Total Clientes", len(df))
    col3.metric("Churnados", df['churn'].sum())
    col4.metric("Receita Media", f"R$ {df['valor_mensal'].mean():.0f}")
    
    st.subheader("Distribuicao de Churn")
    fig, ax = plt.subplots(figsize=(8, 5))
    churn_counts = df['churn'].value_counts()
    ax.pie([churn_counts[0], churn_counts[1]], 
           labels=['Mantido', 'Churn'], 
           autopct='%1.1f%%',
           colors=['#2ecc71', '#e74c3c'])
    st.pyplot(fig)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Churn por Plano")
        churn_plano = df.groupby('plano')['churn'].mean() * 100
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(churn_plano.index, churn_plano.values, color=sns.color_palette("husl", len(churn_plano)))
        ax.set_ylabel('Taxa de Churn (%)')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Churn por Contrato")
        churn_contrato = df.groupby('tipo_contrato')['churn'].mean() * 100
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(churn_contrato.index, churn_contrato.values, color=['#3498db', '#9b59b6', '#e67e22'])
        ax.set_ylabel('Taxa de Churn (%)')
        st.pyplot(fig)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Churn por Satisfacao")
        satis_bins = pd.cut(df['satisfacao_1_10'], bins=[0, 3, 6, 10], labels=['Baixa(1-3)', 'Media(4-6)', 'Alta(7-10)'])
        churn_satis = df.groupby(satis_bins)['churn'].mean() * 100
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(churn_satis.index, churn_satis.values, color=['#e74c3c', '#f39c12', '#2ecc71'])
        ax.set_ylabel('Taxa de Churn (%)')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Churn por Reclamacoes")
        recla_churn = df.groupby('num_reclamacoes')['churn'].mean() * 100
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(recla_churn.index, recla_churn.values, 'o-', linewidth=2, color='#e74c3c')
        ax.set_xlabel('Numero de Reclamacoes')
        ax.set_ylabel('Taxa de Churn (%)')
        st.pyplot(fig)

with tab4:
    st.subheader("Churn por Regiao")
    churn_regiao = df.groupby('regiao')['churn'].mean() * 100
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(churn_regiao.index, churn_regiao.values, color=sns.color_palette("coolwarm", len(churn_regiao)))
    ax.set_xlabel('Taxa de Churn (%)')
    st.pyplot(fig)

st.sidebar.header("Filtros")
regiao_filter = st.sidebar.multiselect("Regiao", df['regiao'].unique(), default=df['regiao'].unique())
plano_filter = st.sidebar.multiselect("Plano", df['plano'].unique(), default=df['plano'].unique())

df_filtered = df[(df['regiao'].isin(regiao_filter)) & (df['plano'].isin(plano_filter))]
st.sidebar.metric("Clientes Filtrados", len(df_filtered))
st.sidebar.metric("Churn Filtrado", f"{df_filtered['churn'].mean()*100:.1f}%")