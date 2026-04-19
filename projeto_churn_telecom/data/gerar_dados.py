import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

n_clientes = 5000

tipos_plano = ['Premium', 'Básico', 'Padrão', 'Familia']
regioes = ['Sudeste', 'Nordeste', 'Sul', 'Centro-Oeste', 'Norte']
metodos_pagamento = ['Cartão de Crédito', 'Boleto', 'Débito Automático', 'PIX']
tipos_contrato = ['Mensal', 'Anual', 'Bienal']

def gerar_dados():
    ids = [f'CL{i:06d}' for i in range(1, n_clientes + 1)]
    
    data_inicio = datetime(2022, 1, 1)
    datas = [data_inicio + timedelta(days=random.randint(0, 730)) for _ in range(n_clientes)]
    
    dados = {
        'cliente_id': ids,
        'nome': [f'Cliente_{i}' for i in range(1, n_clientes + 1)],
        'idade': np.random.randint(18, 75, n_clientes),
        'genero': np.random.choice(['M', 'F', 'Outro'], n_clientes, p=[0.48, 0.48, 0.04]),
        'regiao': np.random.choice(regioes, n_clientes, p=[0.35, 0.20, 0.20, 0.15, 0.10]),
        'tipo_contrato': np.random.choice(tipos_contrato, n_clientes, p=[0.50, 0.35, 0.15]),
        'plano': np.random.choice(tipos_plano, n_clientes, p=[0.25, 0.35, 0.25, 0.15]),
        'valor_mensal': np.round(np.random.uniform(50, 300, n_clientes), 2),
        'tempo_cliente_meses': np.random.randint(1, 61, n_clientes),
        'data_contratacao': [d.strftime('%Y-%m-%d') for d in datas],
        'chamadas_por_mes': np.random.randint(50, 500, n_clientes),
        'minutos_usados': np.random.randint(100, 2000, n_clientes),
        'sms_enviados': np.random.randint(0, 500, n_clientes),
        'uso_dados_gb': np.round(np.random.uniform(1, 100, n_clientes), 1),
        'num_reclamacoes': np.random.randint(0, 8, n_clientes),
        'satisfacao_1_10': np.random.randint(1, 11, n_clientes),
        'ultimo_login_dias': np.random.randint(0, 60, n_clientes),
        'metodo_pagamento': np.random.choice(metodos_pagamento, n_clientes, p=[0.40, 0.25, 0.20, 0.15]),
        'tem_fibra': np.random.choice([True, False], n_clientes, p=[0.45, 0.55]),
        'tem_celular_empresarial': np.random.choice([True, False], n_clientes, p=[0.30, 0.70]),
        'promocoes_ativas': np.random.randint(0, 4, n_clientes),
        'desconto_percentual': np.random.choice([0, 5, 10, 15, 20, 25], n_clientes, p=[0.40, 0.20, 0.15, 0.15, 0.07, 0.03]),
    }
    
    df = pd.DataFrame(dados)
    
    df = aplicar_churn_logic(df)
    
    return df

def aplicar_churn_logic(df):
    churn_prob = np.zeros(n_clientes)
    
    churn_prob += (df['num_reclamacoes'] >= 4).astype(int) * 0.25
    churn_prob += (df['satisfacao_1_10'] <= 3).astype(int) * 0.30
    churn_prob += (df['ultimo_login_dias'] > 30).astype(int) * 0.15
    churn_prob += (df['tempo_cliente_meses'] <= 6).astype(int) * 0.20
    churn_prob += ((df['plano'] == 'Básico') & (df['valor_mensal'] > 150)).astype(int) * 0.15
    churn_prob += (df['promocoes_ativas'] == 0).astype(int) * 0.10
    churn_prob += ((df['tem_fibra'] == False) & (df['uso_dados_gb'] > 50)).astype(int) * 0.10
    
    churn_prob = np.clip(churn_prob, 0, 1)
    
    df['churn'] = (np.random.random(n_clientes) < churn_prob).astype(int)
    
    return df

df = gerar_dados()

df.to_csv('C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/data/telecom_clientes.csv', index=False)

print(f"Dataset criado com {len(df)} registros")
print(f"Taxa de churn: {df['churn'].mean()*100:.2f}%")