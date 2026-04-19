"""
Módulo de Limpeza e Processamento de Dados de Churn
====================================================
Script para tratamento de dados brutos de clientes de telecomunicações.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataCleaner:
    """Classe para limpeza e processamento de dados de churn."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = None
        self.raw_df = None
        
    def load_data(self) -> pd.DataFrame:
        """Carrega dados do arquivo CSV."""
        logger.info(f"Carregando dados de: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.raw_df = self.df.copy()
        logger.info(f"Dados carregados: {len(self.df)} registros, {len(self.df.columns)} colunas")
        return self.df
    
    def basic_info(self) -> dict:
        """Retorna informações básicas do dataset."""
        info = {
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.to_dict(),
            'missing': self.df.isnull().sum().to_dict(),
            'duplicates': self.df.duplicated().sum()
        }
        return info
    
    def clean_total_charges(self) -> pd.DataFrame:
        """Converte coluna TotalCharges para numérico e trata valores inválidos."""
        logger.info("Processando coluna TotalCharges...")
        
        self.df['TotalCharges'] = pd.to_numeric(self.df['TotalCharges'], errors='coerce')
        
        missing_before = self.df['TotalCharges'].isnull().sum()
        logger.info(f"Valores ausentes em TotalCharges: {missing_before}")
        
        self.df.loc[self.df['TotalCharges'].isnull(), 'TotalCharges'] = 0
        
        return self.df
    
    def remove_unnecessary_columns(self) -> pd.DataFrame:
        """Remove colunas desnecessárias."""
        if 'customerID' in self.df.columns:
            logger.info("Removendo coluna customerID (identificador)")
            self.df = self.df.drop(columns=['customerID'])
        return self.df
    
    def standardize_categorical(self) -> pd.DataFrame:
        """Padroniza valores categóricos."""
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            if col != 'customerID':
                self.df[col] = self.df[col].str.strip().str.title()
        
        return self.df
    
    def handle_missing_values(self) -> pd.DataFrame:
        """Trata valores ausentes remanescentes."""
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if self.df[col].dtype in ['float64', 'int64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                else:
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
                    
        logger.info(f"Valores ausentes após tratamento: {self.df.isnull().sum().sum()}")
        return self.df
    
    def create_features(self) -> pd.DataFrame:
        """Cria novas features para análise."""
        
        self.df['HasPartner'] = (self.df['Partner'] == 'Yes').astype(int)
        self.df['HasDependents'] = (self.df['Dependents'] == 'Yes').astype(int)
        self.df['IsSenior'] = (self.df['SeniorCitizen'] == 1).astype(int)
        
        self.df['TenureGroup'] = pd.cut(
            self.df['tenure'], 
            bins=[0, 12, 24, 48, 72], 
            labels=['0-12', '12-24', '24-48', '48-72']
        )
        
        services = ['PhoneService', 'MultipleLines', 'OnlineSecurity', 
                    'OnlineBackup', 'DeviceProtection', 'TechSupport', 
                    'StreamingTV', 'StreamingMovies']
        
        self.df['TotalServices'] = sum(
            (self.df[col] == 'Yes').astype(int) for col in services if col in self.df.columns
        )
        
        self.df['HasInternet'] = (self.df['InternetService'] != 'No').astype(int)
        self.df['HasStreaming'] = (
            (self.df['StreamingTV'] == 'Yes') | (self.df['StreamingMovies'] == 'Yes')
        ).astype(int)
        
        self.df['ChargePerMonth'] = np.where(
            self.df['tenure'] > 0,
            self.df['TotalCharges'] / self.df['tenure'],
            self.df['MonthlyCharges']
        )
        
        logger.info("Features criadas com sucesso")
        return self.df
    
    def encode_target(self) -> pd.DataFrame:
        """Converte variável target para numérico."""
        self.df['Churn'] = self.df['Churn'].map({'Yes': 1, 'No': 0})
        return self.df
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Executa pipeline completo de limpeza."""
        self.load_data()
        self.clean_total_charges()
        self.remove_unnecessary_columns()
        self.standardize_categorical()
        self.handle_missing_values()
        self.create_features()
        self.encode_target()
        
        logger.info("Pipeline de limpeza concluído")
        return self.df
    
    def save_cleaned_data(self, output_path: str) -> None:
        """Salva dados limpos em arquivo CSV."""
        self.df.to_csv(output_path, index=False)
        logger.info(f"Dados limpos salvos em: {output_path}")


def main():
    """Função principal para execução do script."""
    
    DATA_PATH = 'data/raw/telco_churn.csv'
    OUTPUT_PATH = 'data/processed/telco_churn_cleaned.csv'
    
    cleaner = DataCleaner(DATA_PATH)
    df_cleaned = cleaner.get_cleaned_data()
    
    cleaner.save_cleaned_data(OUTPUT_PATH)
    
    print("\n" + "="*60)
    print("RESUMO DA LIMPEZA DE DADOS")
    print("="*60)
    print(f"Registros originais: {len(cleaner.raw_df)}")
    print(f"Registros finais: {len(df_cleaned)}")
    print(f"Colunas removidas: 1 (customerID)")
    print(f"Novas features criadas: 9")
    print(f"Total de features: {len(df_cleaned.columns)}")
    print("="*60)
    
    return df_cleaned


if __name__ == "__main__":
    df = main()