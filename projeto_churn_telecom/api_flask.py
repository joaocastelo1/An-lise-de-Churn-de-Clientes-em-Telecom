from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv('C:/Users/joao castelo/Desktop/Cusro_Python_Pandas/projeto_churn_telecom/data/telecom_limpo.csv')

def calcular_risco_churn(dados):
    score = 0
    
    if dados.get('satisfacao_1_10', 5) <= 3:
        score += 30
    elif dados.get('satisfacao_1_10', 5) <= 6:
        score += 15
    
    score += dados.get('num_reclamacoes', 0) * 8
    
    if dados.get('tempo_cliente_meses', 12) <= 6:
        score += 20
    elif dados.get('tempo_cliente_meses', 12) <= 12:
        score += 10
    
    if dados.get('tipo_contrato') == 'Mensal':
        score += 15
    elif dados.get('tipo_contrato') == 'Anual':
        score += 5
    
    if not dados.get('tem_fibra', False):
        score += 10
    
    if dados.get('ultimo_login_dias', 0) > 30:
        score += 10
    
    risco = "Baixo" if score < 20 else "Medio" if score < 40 else "Alto"
    probabilidade = min(score / 100, 0.95)
    
    return {
        "risco": risco,
        "probabilidade_churn": round(probabilidade * 100, 1),
        "score_risco": score,
        "recomendacoes": gerar_recomendacoes(dados, risco)
    }

def gerar_recomendacoes(dados, risco):
    recs = []
    
    if dados.get('satisfacao_1_10', 5) <= 3:
        recs.append("Contato imediato com equipe de retention")
    if dados.get('num_reclamacoes', 0) >= 3:
        recs.append("Trigger automatico de suporte prioritario")
    if dados.get('tempo_cliente_meses', 12) <= 6:
        recs.append("Programa de onboarding estruturado")
    if dados.get('tipo_contrato') == 'Mensal':
        recs.append("Oferecer desconto para contrato anual")
    if not dados.get('tem_fibra', False) and dados.get('uso_dados_gb', 0) > 30:
        recs.append("Oferta de upgrade para fibra otica")
    
    if not recs:
        recs.append("Manter monitoramento regular")
    
    return recs

@app.route('/')
def home():
    return jsonify({
        "api": "Telecom Churn Prediction API",
        "versao": "1.0",
        "endpoints": {
            "/predict": "POST - Predizer risco de churn",
            "/health": "GET - Verificar status da API",
            "/stats": "GET - Estatisticas do dataset"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "online", "clientes": len(df)})

@app.route('/stats')
def stats():
    return jsonify({
        "total_clientes": len(df),
        "taxa_churn": round(df['churn'].mean() * 100, 1),
        "churnados": int(df['churn'].sum()),
        "media_valor": round(df['valor_mensal'].mean(), 2)
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        dados = request.json
        
        resultado = calcular_risco_churn(dados)
        
        return jsonify({
            "sucesso": True,
            "resultado": resultado
        })
    
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 400

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    try:
        clientes = request.json.get('clientes', [])
        resultados = []
        
        for cliente in clientes:
            resultados.append(calcular_risco_churn(cliente))
        
        return jsonify({
            "sucesso": True,
            "resultados": resultados
        })
    
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "erro": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)