"""
API REST para Predição de Churn (Flask)
=======================================
API simples para predição de churn por cliente.
Execute: python api.py
Endpoints disponíveis:
- GET / - Health check
- POST /predict - Predição de churn
- GET /stats - Estatísticas do dataset
"""

from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from pathlib import Path


app = Flask(__name__)


def load_model_data():
    """Carrega dados para predição simulada."""
    df = pd.read_csv('data/processed/telco_churn_cleaned.csv')
    return df


@app.route('/')
def health_check():
    """Endpoint de verificação de saúde."""
    return jsonify({
        'status': 'healthy',
        'service': 'Churn Prediction API',
        'version': '1.0.0'
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para predição de churn."""
    
    try:
        data = request.get_json()
        
        required_fields = ['tenure', 'MonthlyCharges', 'Contract', 'InternetService']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} obrigatório'}), 400
        
        contract_scores = {
            'Month-to-month': 0.42,
            'One year': 0.15,
            'Two year': 0.03
        }
        
        internet_scores = {
            'Fiber optic': 0.42,
            'DSL': 0.19,
            'No': 0.07
        }
        
        tenure = data.get('tenure', 0)
        if tenure < 12:
            tenure_factor = 0.40
        elif tenure < 24:
            tenure_factor = 0.22
        elif tenure < 48:
            tenure_factor = 0.15
        else:
            tenure_factor = 0.10
        
        base_score = (
            contract_scores.get(data['Contract'], 0.26) * 0.35 +
            internet_scores.get(data['InternetService'], 0.26) * 0.25 +
            tenure_factor * 0.30 +
            0.10
        )
        
        monthly = data.get('MonthlyCharges', 70)
        if monthly > 80:
            base_score *= 1.15
        
        churn_probability = min(base_score, 1.0)
        
        risk_level = 'high' if churn_probability > 0.35 else 'medium' if churn_probability > 0.20 else 'low'
        
        return jsonify({
            'churn_probability': round(churn_probability * 100, 2),
            'risk_level': risk_level,
            'recommendations': get_recommendations(data, churn_probability)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_recommendations(data, probability):
    """Gera recomendações baseadas nos dados."""
    recommendations = []
    
    if data.get('Contract') == 'Month-to-month':
        recommendations.append('Oferecer discount para contrato anual')
    
    if data.get('InternetService') == 'Fiber optic':
        recommendations.append('Verificar satisfação com serviço de fibra')
    
    if data.get('tenure', 0) < 12:
        recommendations.append('Intensificar onboarding e suporte')
    
    if probability > 0.35:
        recommendations.append('Contato proativo para retenção')
    
    return recommendations


@app.route('/stats', methods=['GET'])
def stats():
    """Endpoint para estatísticas do dataset."""
    
    df = load_model_data()
    
    return jsonify({
        'total_customers': int(len(df)),
        'churn_rate': round(df['Churn'].mean() * 100, 2),
        'avg_tenure': round(df['tenure'].mean(), 1),
        'avg_monthly_charges': round(df['MonthlyCharges'].mean(), 2),
        'churn_by_contract': {
            row['Contract']: round(row['Churn'] * 100, 2)
            for _, row in df.groupby('Contract')['Churn'].mean().reset_index().iterrows()
        }
    })


@app.route('/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Endpoint para buscar dados de um cliente específico."""
    
    try:
        df = load_model_data()
        return jsonify({'message': 'Implementar busca por ID'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 API de Churn - Servidor iniciado")
    print("   URL: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)