import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/data/telecom_clientes.csv')

print("="*60)
print("RELATORIO DE QUALIDADE DE DADOS")
print("="*60)

print(f"\nDIMENSOES: {df.shape[0]} linhas x {df.shape[1]} colunas")

print("\nTIPOS DE DADOS:")
print(df.dtypes)

print("\nVALORES NULOS:")
nulos = df.isnull().sum()
print(nulos[nulos > 0] if nulos.sum() > 0 else "Sem valores nulos")

print("\nESTATISTICAS DESCRITIVAS:")
print(df.describe())

print("\nVERIFICACAO DE DUPLICADOS:")
print(f"Duplicados: {df.duplicated().sum()}")

print("\nLIMPEZA DE DADOS:")

df_limpo = df.copy()

df_limpo['valor_mensal'] = df_limpo['valor_mensal'].replace(0, df_limpo['valor_mensal'].median())

df_limpo['tempo_cliente_meses'] = df_limpo['tempo_cliente_meses'].clip(lower=1)

df_limpo.loc[df_limpo['satisfacao_1_10'] < 1, 'satisfacao_1_10'] = 1
df_limpo.loc[df_limpo['satisfacao_1_10'] > 10, 'satisfacao_1_10'] = 10

df_limpo['uso_dados_gb'] = df_limpo['uso_dados_gb'].abs()

print("Limpezas aplicadas:")
print("   - Valores zerados no plano substitudos pela mediana")
print("   - Tempo de cliente normalizado (minimo 1 mes)")
print("   - Satisfacao boundada entre 1-10")
print("   - Uso de dados transformado para valores positivos")

df_limpo.to_csv('C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/data/telecom_limpo.csv', index=False)
print("\nDataset limpo salvo em: data/telecom_limpo.csv")

print("\n" + "="*60)
print("ANALISE EXPLORATORIA (EDA)")
print("="*60)

print("\nDISTRIBUICAO DE CHURN:")
churn_dist = df_limpo['churn'].value_counts()
print(f"Nao churnou: {churn_dist[0]} ({churn_dist[0]/len(df_limpo)*100:.1f}%)")
print(f"Churnou: {churn_dist[1]} ({churn_dist[1]/len(df_limpo)*100:.1f}%)")

print("\nTAXA DE CHURN POR PLANO:")
churn_plano = df_limpo.groupby('plano')['churn'].mean() * 100
print(churn_plano.sort_values(ascending=False))

print("\nTAXA DE CHURN POR REGIAO:")
churn_regiao = df_limpo.groupby('regiao')['churn'].mean() * 100
print(churn_regiao.sort_values(ascending=False))

print("\nTAXA DE CHURN POR CONTRATO:")
churn_contrato = df_limpo.groupby('tipo_contrato')['churn'].mean() * 100
print(churn_contrato.sort_values(ascending=False))

print("\nCORRELACOES COM CHURN:")
numeric_cols = df_limpo.select_dtypes(include=[np.number]).columns
corr_churn = df_limpo[numeric_cols].corr()['churn'].sort_values(ascending=False)
print(corr_churn.head(10))

print("\nEDA concluida!")