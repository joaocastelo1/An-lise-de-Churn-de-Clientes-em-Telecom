import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
sns.set_palette("husl")

df = pd.read_csv('C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/data/telecom_limpo.csv')

output_dir = 'C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/visualizations/'

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

churn_counts = df['churn'].value_counts()
axes[0, 0].pie([churn_counts[0], churn_counts[1]], 
               labels=['Mantido', 'Churn'], 
               autopct='%1.1f%%', 
               colors=['#2ecc71', '#e74c3c'],
               explode=(0, 0.05))
axes[0, 0].set_title('Taxa de Churn Total', fontsize=14, fontweight='bold')

churn_plano = df.groupby('plano')['churn'].mean() * 100
colors = sns.color_palette("husl", len(churn_plano))
bars = axes[0, 1].bar(churn_plano.index, churn_plano.values, color=colors)
axes[0, 1].set_title('Taxa de Churn por Plano', fontsize=14, fontweight='bold')
axes[0, 1].set_ylabel('Taxa de Churn (%)')
axes[0, 1].tick_params(axis='x', rotation=45)
for bar, val in zip(bars, churn_plano.values):
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{val:.1f}%', ha='center', fontsize=10)

churn_regiao = df.groupby('regiao')['churn'].mean() * 100
bars = axes[1, 0].barh(churn_regiao.index, churn_regiao.values, color=sns.color_palette("coolwarm", len(churn_regiao)))
axes[1, 0].set_title('Taxa de Churn por Região', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Taxa de Churn (%)')
for bar, val in zip(bars, churn_regiao.values):
    axes[1, 0].text(val + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}%', va='center', fontsize=10)

churn_contrato = df.groupby('tipo_contrato')['churn'].mean() * 100
colors = ['#3498db', '#9b59b6', '#e67e22']
bars = axes[1, 1].bar(churn_contrato.index, churn_contrato.values, color=colors)
axes[1, 1].set_title('Taxa de Churn por Tipo de Contrato', fontsize=14, fontweight='bold')
axes[1, 1].set_ylabel('Taxa de Churn (%)')
for bar, val in zip(bars, churn_contrato.values):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{val:.1f}%', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig(output_dir + 'churn_geral.png', dpi=150, bbox_inches='tight')
plt.close()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

sns.boxplot(data=df, x='churn', y='valor_mensal', ax=axes[0, 0], palette=['#2ecc71', '#e74c3c'])
axes[0, 0].set_title('Valor Mensal vs Churn', fontsize=14, fontweight='bold')
axes[0, 0].set_xticklabels(['Mantido', 'Churn'])

sns.boxplot(data=df, x='churn', y='num_reclamacoes', ax=axes[0, 1], palette=['#2ecc71', '#e74c3c'])
axes[0, 1].set_title('Reclamações vs Churn', fontsize=14, fontweight='bold')
axes[0, 1].set_xticklabels(['Mantido', 'Churn'])

sns.boxplot(data=df, x='churn', y='satisfacao_1_10', ax=axes[1, 0], palette=['#2ecc71', '#e74c3c'])
axes[1, 0].set_title('Satisfação vs Churn', fontsize=14, fontweight='bold')
axes[1, 0].set_xticklabels(['Mantido', 'Churn'])

sns.boxplot(data=df, x='churn', y='uso_dados_gb', ax=axes[1, 1], palette=['#2ecc71', '#e74c3c'])
axes[1, 1].set_title('Uso de Dados (GB) vs Churn', fontsize=14, fontweight='bold')
axes[1, 1].set_xticklabels(['Mantido', 'Churn'])

plt.tight_layout()
plt.savefig(output_dir + 'churn_numerico.png', dpi=150, bbox_inches='tight')
plt.close()

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

churn_fibra = df.groupby('tem_fibra')['churn'].mean() * 100
bars = axes[0].bar(['Sem Fibra', 'Com Fibra'], churn_fibra.values, color=['#e74c3c', '#2ecc71'])
axes[0].set_title('Churn vs Fibra Óptica', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Taxa de Churn (%)')
for bar, val in zip(bars, churn_fibra.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                  f'{val:.1f}%', ha='center', fontsize=12)

churn_pagamento = df.groupby('metodo_pagamento')['churn'].mean() * 100
bars = axes[1].barh(churn_pagamento.index, churn_pagamento.values, color=sns.color_palette("viridis", len(churn_pagamento)))
axes[1].set_title('Churn vs Método de Pagamento', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Taxa de Churn (%)')
for bar, val in zip(bars, churn_pagamento.values):
    axes[1].text(val + 0.5, bar.get_y() + bar.get_height()/2, 
                  f'{val:.1f}%', va='center', fontsize=10)

satis_bins = pd.cut(df['satisfacao_1_10'], bins=[0, 3, 6, 10], labels=['Baixa(1-3)', 'Média(4-6)', 'Alta(7-10)'])
churn_satis = df.groupby(satis_bins)['churn'].mean() * 100
bars = axes[2].bar(churn_satis.index, churn_satis.values, color=['#e74c3c', '#f39c12', '#2ecc71'])
axes[2].set_title('Churn por Nível de Satisfação', fontsize=14, fontweight='bold')
axes[2].set_ylabel('Taxa de Churn (%)')
for bar, val in zip(bars, churn_satis.values):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                  f'{val:.1f}%', ha='center', fontsize=12)

plt.tight_layout()
plt.savefig(output_dir + 'churn_fatores.png', dpi=150, bbox_inches='tight')
plt.close()

plt.figure(figsize=(12, 10))
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=0.5)
plt.title('Matriz de Correlação', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir + 'correlacao.png', dpi=150, bbox_inches='tight')
plt.close()

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='tempo_cliente_meses', hue='churn', kde=True, 
             palette=['#2ecc71', '#e74c3c'], bins=30)
plt.title('Tempo de Cliente vs Churn', fontsize=14, fontweight='bold')
plt.xlabel('Meses como Cliente')
plt.ylabel('Contagem')
plt.tight_layout()
plt.savefig(output_dir + 'tempo_cliente.png', dpi=150, bbox_inches='tight')
plt.close()

plt.figure(figsize=(10, 6))
reclamacao_churn = df.groupby('num_reclamacoes')['churn'].mean() * 100
plt.plot(reclamacao_churn.index, reclamacao_churn.values, 'o-', linewidth=2, markersize=8, color='#e74c3c')
plt.title('Taxa de Churn por Número de Reclamações', fontsize=14, fontweight='bold')
plt.xlabel('Número de Reclamações')
plt.ylabel('Taxa de Churn (%)')
plt.grid(True, alpha=0.3)
for i, v in enumerate(reclamacao_churn.values):
    plt.text(reclamacao_churn.index[i], v + 1, f'{v:.1f}%', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(output_dir + 'reclamacoes_churn.png', dpi=150, bbox_inches='tight')
plt.close()

print("Todos os graficos gerados e salvos na pasta 'visualizations/'")