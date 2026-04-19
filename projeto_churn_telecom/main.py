"""
Script Principal - Pipeline de Análise de Churn
================================================
Executa o pipeline completo: limpeza, EDA e visualização.
"""

import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from src.data.data_cleaning import DataCleaner
from src.analysis.eda_analysis import EDAAnalyzer


def main():
    """Executa o pipeline completo de análise de churn."""
    
    print("="*80)
    print("PIPELINE DE ANÁLISE DE CHURN - TELECOM")
    print("="*80)
    
    BASE_PATH = Path('.')
    
    print("\n[1/4] Carregando e limpando dados...")
    cleaner = DataCleaner(BASE_PATH / 'data/raw/telco_churn.csv')
    df = cleaner.get_cleaned_data()
    cleaner.save_cleaned_data(BASE_PATH / 'data/processed/telco_churn_cleaned.csv')
    print(f"    -> Dados limpos salvos: {len(df)} registros")
    
    print("\n[2/4] Executando Análise Exploratória (EDA)...")
    analyzer = EDAAnalyzer(df, output_dir=BASE_PATH / 'reports')
    results = analyzer.run_full_eda()
    print(f"    -> Analise concluida")
    
    print("\n[3/4] Gerando relatório de insights...")
    print(results['report'])
    
    print("\n[4/4] Resumo do Pipeline")
    print("-"*40)
    print(f"Total de clientes analisados: {results['stats']['total_customers']:,}")
    print(f"Taxa de churn: {results['stats']['churn_rate']:.2f}%")
    print(f"Gráficos salvos em: reports/figures/")
    
    print("\n" + "="*80)
    print("PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*80)
    
    return df, results


if __name__ == "__main__":
    df, results = main()