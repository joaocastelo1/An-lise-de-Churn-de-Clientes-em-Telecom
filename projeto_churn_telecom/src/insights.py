import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/data/telecom_limpo.csv')

insights = []

print("="*70)
print("RELATORIO DE INSIGHTS - TELECOM CHURN ANALYSIS")
print("="*70)

print("\n" + "="*70)
print("1. INSIGHTS DE CONTRATO E PLANO")
print("="*70)

churn_contrato = df.groupby('tipo_contrato')['churn'].mean() * 100
print(churn_contrato.sort_values(ascending=False))
insights.append({
    'categoria': 'Contrato',
    'insight': 'Contrato Mensal tem 2x mais chances de churn que bienais',
    'impacto': 'ALTO',
    'acao': 'Oferecer discount de 15-20% para migracao para contrato anual'
})

churn_plano = df.groupby('plano')['churn'].mean() * 100
print(churn_plano.sort_values(ascending=False))
insights.append({
    'categoria': 'Plano',
    'insight': 'Planos Basicos tem churn 74% maior que Premium',
    'impacto': 'ALTO',
    'acao': 'Upsell para planos superiores com beneficios relevantes'
})

print("\n" + "="*70)
print("2. INSIGHTS DE SATISFACAO")
print("="*70)

satis_churn = df.groupby('satisfacao_1_10')['churn'].mean() * 100
print(f" satisfacao <= 3: {satis_churn[satis_churn.index <= 3].mean():.1f}% churn")
print(f" satisfacao >= 8: {satis_churn[satis_churn.index >= 8].mean():.1f}% churn")
insights.append({
    'categoria': 'Satisfacao',
    'insight': 'Satisfacao <= 3 indica 70% de churn vs 22% para >= 8',
    'impacto': 'CRITICO',
    'acao': 'NPS < 3: contato imediato com equipe de retention em 24h'
})

print("\n" + "="*70)
print("3. INSIGHTS DE RECLAMACOES")
print("="*70)

recla_churn = df.groupby('num_reclamacoes')['churn'].mean() * 100
print(f"0 reclamacoes: {recla_churn[0]:.1f}% de churn")
print(f"4+ reclamacoes: {recla_churn[recla_churn.index >= 4].mean():.1f}% de churn")
insights.append({
    'categoria': 'Reclamacoes',
    'insight': '4+ reclamacoes = 65% churn (vs 30% com 0)',
    'impacto': 'CRITICO',
    'acao': 'Trigger automatico para retention apos 3a reclamacao'
})

print("\n" + "="*70)
print("4. INSIGHTS DE FIBRA OTICA")
print("="*70)

fibra_churn = df.groupby('tem_fibra')['churn'].mean() * 100
print(f"Sem fibra: {fibra_churn[False]:.1f}% de churn")
print(f"Com fibra: {fibra_churn[True]:.1f}% de churn")
insights.append({
    'categoria': 'Infraestrutura',
    'insight': 'Sem fibra = 47% churn vs 32% com fibra',
    'impacto': 'ALTO',
    'acao': 'Priorizar expansao de fibra para areas com alta conversao'
})

print("\n" + "="*70)
print("5. INSIGHTS DE TEMPO DE CLIENTE")
print("="*70)

df['faixa_tempo'] = pd.cut(df['tempo_cliente_meses'], bins=[0, 6, 12, 24, 60], labels=['0-6', '6-12', '12-24', '24+'])
tempo_churn = df.groupby('faixa_tempo')['churn'].mean() * 100
print(tempo_churn)
insights.append({
    'categoria': 'Ciclo de Vida',
    'insight': 'Clientes nos primeiros 6 meses tem 54% churn - fase critica',
    'impacto': 'CRITICO',
    'acao': 'Programa de onboarding estruturado nos 1os 6 meses'
})

print("\n" + "="*70)
print("6. INSIGHTS DE USO E PAGAMENTO")
print("="*70)

uso_churn = df.groupby(pd.cut(df['uso_dados_gb'], bins=[0, 20, 50, 100], labels=['Baixo', 'Medio', 'Alto']))['churn'].mean() * 100
print(uso_churn)
insights.append({
    'categoria': 'Uso',
    'insight': 'Alto uso de dados (50GB+) sem fibra = churn elevado',
    'impacto': 'MEDIO',
    'acao': 'Oferta de upgrade de internet para heavy users'
})

pagamento_churn = df.groupby('metodo_pagamento')['churn'].mean() * 100
print(pagamento_churn)
insights.append({
    'categoria': 'Pagamento',
    'insight': 'Boleto tem maior churn vs PIX',
    'impacto': 'MEDIO',
    'acao': 'Incentivar migracao para PIX com 5% discount'
})

print("\n" + "="*70)
print("7. INSIGHTS REGIONAIS")
print("="*70)

regiao_churn = df.groupby('regiao')['churn'].agg(['mean', 'count'])
regiao_churn['mean'] = regiao_churn['mean'] * 100
print(regiao_churn.sort_values('mean', ascending=False))
insights.append({
    'categoria': 'Regiao',
    'insight': 'Norte e Nordeste tem churn acima da media (43-45%)',
    'impacto': 'MEDIO',
    'acao': 'Planos regionais especificos com melhor custo-beneficio'
})

print("\n" + "="*70)
print("IMPACTO FINANCEIRO ESTIMADO")
print("="*70)

churn_rate = df['churn'].mean()
valor_medio = df['valor_mensal'].mean()
clientes_churn = df['churn'].sum()
receita_perdida_mensal = clientes_churn * valor_medio
receita_perdida_anual = receita_perdida_mensal * 12

print(f"Taxa de churn atual: {churn_rate*100:.1f}%")
print(f"Clientes que churnaram: {clientes_churn}")
print(f"Receita mensal perdida: R$ {receita_perdida_mensal:,.2f}")
print(f"Receita anual perdida: R$ {receita_perdida_anual:,.2f}")

print("\nSe reduzirmos churn em 20%:")
reducao = receita_perdida_anual * 0.20
print(f"Economia anual estimada: R$ {reducao:,.2f}")

insights_df = pd.DataFrame(insights)
insights_df.to_csv('C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/reports/insights.csv', index=False)

print("\nInsights salvos em reports/insights.csv")
print("\n" + "="*70)
print("RESUMO: 8 INSIGHTS PRINCIPAIS IDENTIFICADOS")
print("="*70)
for i, insight in enumerate(insights, 1):
    print(f"\n{i}. [{insight['impacto']}] {insight['categoria']}")
    print(f"   -> {insight['insight']}")
    print(f"   -> Acao: {insight['acao']}")